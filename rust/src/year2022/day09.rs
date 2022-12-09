use genawaiter::rc::gen;
use genawaiter::yield_;
use itertools::Itertools;

type Coordinate =
    crate::utils::grid::Coordinate<{ isize::MIN }, { isize::MIN }, { isize::MAX }, { isize::MAX }>;

fn move_tail(tail: &mut Coordinate, head: Coordinate, direction: (isize, isize)) -> (isize, isize) {
    if head.neighbours_all().contains(tail) || head == *tail {
        return (0, 0);
    }

    let old_tail = *tail;

    if head.x != tail.x && head.y != tail.y {
        if direction.0 != 0 && direction.1 != 0 {
            tail.x += direction.0;
            tail.y += direction.1;
        } else if direction.0 != 0 {
            tail.x += direction.0;
            tail.y = head.y;
        } else if direction.1 != 0 {
            tail.x = head.x;
            tail.y += direction.1;
        }
    } else {
        if head.y == tail.y {
            tail.x += direction.0;
        } else if head.x == tail.x {
            tail.y += direction.1;
        } else {
            tail.x += direction.0;
            tail.y += direction.1;
        }
    }

    (tail.x - old_tail.x, tail.y - old_tail.y)
}

fn simulate_rope<const TAIL_COUNT: usize>(
    instructions: &str,
) -> impl Iterator<Item = (Coordinate, [Coordinate; TAIL_COUNT])> + '_ {
    let parsed_instructions = instructions.lines().map(|line| {
        let (direction, steps) = line.split_once(' ').expect("line contains space");
        let direction = match direction {
            "U" => (0, 1),
            "D" => (0, -1),
            "R" => (1, 0),
            "L" => (-1, 0),
            _ => panic!("invalid direction"),
        };
        (direction, steps.parse().expect("a valid number"))
    });

    gen!({
        let mut head = Coordinate::new(0, 0).unwrap();
        let mut tails = [Coordinate::new(0, 0).unwrap(); TAIL_COUNT];

        for (direction, steps) in parsed_instructions {
            for _ in 0..steps {
                head.x += direction.0;
                head.y += direction.1;

                let mut direction = move_tail(&mut tails[0], head, direction);
                for i in 1..TAIL_COUNT {
                    let head = tails[i - 1];
                    direction = move_tail(&mut tails[i], head, direction);
                }

                yield_!((head, tails));
            }
        }
    })
    .into_iter()
}

pub fn solve_part1(input: &str) -> usize {
    simulate_rope::<1>(input)
        .map(|(_, tails)| tails[0])
        .unique()
        .count()
}

pub fn solve_part2(input: &str) -> usize {
    simulate_rope::<9>(input)
        .map(|(_, tails)| tails[8])
        .unique()
        .count()
}

#[cfg(test)]
mod tests {
    use super::*;

    static TEST_INPUT: &str = r#"R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"#;

    #[test]
    fn test_part1() {
        assert_eq!(solve_part1(TEST_INPUT), 13);
    }

    #[test]
    fn test_part2() {
        assert_eq!(solve_part2(TEST_INPUT), 1);
        let larger_input = r#"R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"#;
        assert_eq!(solve_part2(larger_input), 36);
    }

    crate::create_solver_test!(part1);
    crate::create_solver_test!(part2);
}
