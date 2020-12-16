import re
from typing import Tuple, Any, Optional

RE_ASSIGNMENT = re.compile(r'^(\d+) players; last marble is worth (\d+) points$')


def parse_assignment(text: str) -> Tuple[int, int]:
    m = RE_ASSIGNMENT.match(text)
    if m:
        return int(m.group(1)), int(m.group(2))


class Marble(object):
    next: Optional['Marble']
    prev: Optional['Marble']
    val: Any

    def __init__(self, prev: Optional['Marble'], next: Optional['Marble'], val: Any):
        self.prev = prev
        self.next = next
        self.val = val

    def __repr__(self):
        prev_val = self.prev.val if self.prev else None
        next_val = self.next.val if self.next else None
        return f'Marble(prev={prev_val}, next={next_val}, val={self.val})'


def list_marbles(first: Marble):
    marbles = [first.val]
    current = first.next
    while current is not first:
        marbles.append(current.val)
        current = current.next
    return marbles


def calculate_winning_score(player_count: int, last_marble_worth: int) -> int:
    player_scores = [0 for _ in range(player_count)]
    current_player = 0
    first_marble = Marble(None, None, 0)  # marbles are in an infinitely repeating linked list
    first_marble.next = first_marble
    first_marble.prev = first_marble
    current_marble = first_marble
    for marble in range(1, last_marble_worth + 1):
        if marble % 23 == 0:
            # add the new marble to the score of the player
            player_scores[current_player] += marble

            # find the marble 7 marbles CCW from the current marble and indicate the one CW of that as current
            other_marble = current_marble
            for _ in range(7):
                other_marble = other_marble.prev
            current_marble = other_marble.next

            # remove the CCW marble and add it to the player's score
            player_scores[current_player] += other_marble.val
            other_marble.prev.next = other_marble.next
            other_marble.next.prev = other_marble.prev
        else:
            # place the marble between the CW and CW-CW marble in the circle
            next_marble = current_marble.next
            next2_marble = next_marble.next
            current_marble = Marble(prev=next_marble, next=next2_marble, val=marble)
            next_marble.next = current_marble
            next2_marble.prev = current_marble

        # pick the next player
        current_player += 1
        current_player %= player_count

    return max(player_scores)
