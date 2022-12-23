use itertools::Itertools;
use std::collections::HashSet;

type Coordinate = (isize, isize);

fn parse_elves(text: &str) -> HashSet<Coordinate> {
    text.lines()
        .enumerate()
        .flat_map(|(y, line)| {
            line.char_indices().filter_map(move |(x, c)| match c {
                '.' => None,
                '#' => Some((x as isize, y as isize)),
                _ => panic!("invalid char"),
            })
        })
        .collect()
}

const NEIGHBOURS: &[(isize, isize); 8] = &[
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
    (-1, -1),
    (1, -1),
    (1, 1),
    (-1, 1),
];

const DIRECTIONS: &[(&[(isize, isize); 3], (isize, isize)); 4] = &[
    // N, NE, NW -> N
    (&[(0, -1), (1, -1), (-1, -1)], (0, -1)),
    // S, SE, SW -> S
    (&[(0, 1), (1, 1), (-1, 1)], (0, 1)),
    // W, NW, SW -> W
    (&[(-1, 0), (-1, -1), (-1, 1)], (-1, 0)),
    // E, NE, SE -> E
    (&[(1, 0), (1, -1), (1, 1)], (1, 0)),
];

fn perform_rounds(
    mut elves: HashSet<Coordinate>,
    max_round: Option<usize>,
) -> (usize, HashSet<Coordinate>) {
    let mut direction_idx = 0;
    let mut round = 1;
    loop {
        match max_round {
            Some(max_round) if round == max_round + 1 => break,
            _ => {}
        };

        let moves = elves
            .iter()
            .filter_map(|(x, y)| {
                if NEIGHBOURS
                    .iter()
                    .filter(|(dx, dy)| elves.contains(&(x + dx, y + dy)))
                    .count()
                    == 0
                {
                    return None;
                }

                for i in 0..4 {
                    let (adjacent_positions, (dx, dy)) = DIRECTIONS[(i + direction_idx) % 4];
                    if adjacent_positions
                        .iter()
                        .filter(|(dx, dy)| elves.contains(&(x + dx, y + dy)))
                        .count()
                        == 0
                    {
                        return Some(((*x, *y), (x + dx, y + dy)));
                    }
                }

                None
            })
            .sorted_by_key(|(_, new_elf)| *new_elf)
            .group_by(|(_, new_elf)| *new_elf)
            .into_iter()
            .filter_map(|(_, group)| {
                let group = group.collect_vec();
                if group.len() == 1 {
                    Some(group[0])
                } else {
                    None
                }
            })
            .collect_vec();

        if moves.is_empty() {
            break;
        }

        // execute moves
        for (old_elf, _) in moves.iter() {
            elves.remove(old_elf);
        }
        for (_, new_elf) in moves.into_iter() {
            elves.insert(new_elf);
        }

        direction_idx = (direction_idx + 1) % 4;
        round += 1;
    }
    (round, elves)
}

pub fn solve_part1(input: &str) -> usize {
    let mut elves = parse_elves(input);
    (_, elves) = perform_rounds(elves, Some(10));

    let (min_x, max_x) = elves
        .iter()
        .map(|elf| elf.0)
        .minmax()
        .into_option()
        .unwrap();
    let (min_y, max_y) = elves
        .iter()
        .map(|elf| elf.1)
        .minmax()
        .into_option()
        .unwrap();
    ((max_y - min_y + 1) * (max_x - min_x + 1)) as usize - elves.len()
}

pub fn solve_part2(input: &str) -> usize {
    let elves = parse_elves(input);
    let (final_round, _) = perform_rounds(elves, None);
    final_round
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_perform_rounds() {
        const INPUT: &str = r".....
..##.
..#..
.....
..##.
.....";
        const EXPECTED: &[&str; 3] = &[
            r"..##.
.....
..#..
...#.
..#..
.....",
            r".....
..##.
.#...
....#
.....
..#..",
            r"..#..
....#
#....
....#
.....
..#..",
        ];

        let elves = parse_elves(INPUT);
        for round in 1..=3 {
            assert_eq!(
                perform_rounds(elves.clone(), Some(round)).1,
                parse_elves(EXPECTED[round - 1]),
                "round {round} failed",
            );
        }
    }

    static TEST_INPUT: &str = r#"....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."#;

    #[test]
    fn test_part1() {
        assert_eq!(solve_part1(TEST_INPUT), 110);
    }

    #[test]
    fn test_part2() {
        assert_eq!(solve_part2(TEST_INPUT), 20);
    }

    crate::create_solver_test!(part1);
    crate::create_solver_test!(part2);
}
