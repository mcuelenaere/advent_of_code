from ..day05.shared import parse_instructions, streaming_evaluate


JOYSTICK_LEFT = -1
JOYSTICK_RIGHT = 1
JOYSTICK_NEUTRAL = 0

TILE_EMPTY = 0
TILE_WALL = 1
TILE_BLOCK = 2
TILE_HORIZONTAL_PADDLE = 3
TILE_BALL = 4

TILE_MAPPING = {
    TILE_EMPTY: " ",
    TILE_WALL: "\u2588",
    TILE_BLOCK: "\u2591",
    TILE_HORIZONTAL_PADDLE: "\u2501",
    TILE_BALL: "\u26AB",
}


class Program(object):
    def __init__(self, text: str):
        self.tiles = {}
        self.score = 0
        instructions = parse_instructions(text)
        instructions[0] = 2
        self.cpu = streaming_evaluate(instructions)
        self.next_input = None

    def run(self):
        while True:
            try:
                _ = next(self.cpu)
                if _ is None:
                    # request input from caller
                    yield
                    x = self.cpu.send(self.next_input)
                    self.next_input = None
                else:
                    x = _
                y = next(self.cpu)
                tile_id = next(self.cpu)
                if (x, y) == (-1, 0):
                    self.score = tile_id
                else:
                    self.tiles[(x, y)] = tile_id
            except StopIteration:
                break

    def dump_to_stdout(self):
        max_x = max(x for x, y in self.tiles.keys())
        max_y = max(y for x, y in self.tiles.keys())
        for y in range(max_y + 1):
            print("".join(TILE_MAPPING[self.tiles[(x, y)]] for x in range(max_x + 1)))


def predict_ball_x_position(prev, cur, paddle):
    if prev is None:
        prev = (cur[0] - 1, cur[1] - 1)

    if prev[0] == cur[0]:
        # ball is moving down vertically
        return prev[0]
    elif prev[0] == cur[0] - 1:
        return cur[0] + (paddle[1] - cur[1])
    elif prev[0] == cur[0] + 1:
        return cur[0] - (paddle[1] - cur[1])
    else:
        raise RuntimeError("edgecase, I do not know how to handle this")


def calculate(text: str) -> int:
    program = Program(text)
    prev_ball_pos = None
    for _ in program.run():
        # find X offset of paddle and ball
        paddle_pos = next(pos for pos, type in program.tiles.items() if type == TILE_HORIZONTAL_PADDLE)
        ball_pos = next(pos for pos, type in program.tiles.items() if type == TILE_BALL)

        # predict final X position of ball when it'll hit the paddle
        predicted_ball_x_pos = predict_ball_x_position(prev_ball_pos, ball_pos, paddle_pos)

        # move paddle to where the ball is predicted to land
        if predicted_ball_x_pos < paddle_pos[0]:
            program.next_input = JOYSTICK_LEFT
        elif predicted_ball_x_pos > paddle_pos[0]:
            program.next_input = JOYSTICK_RIGHT
        else:
            program.next_input = JOYSTICK_NEUTRAL

        if ball_pos[1] == paddle_pos[1] - 1 and program.next_input == JOYSTICK_NEUTRAL:
            # we're about to hit the ball with the paddle, give it a spin
            program.next_input = JOYSTICK_LEFT

        # keep track of previous ball position
        prev_ball_pos = ball_pos

        # enable this for a visual representation of the in-game state
        # program.dump_to_stdout()

    return program.score
