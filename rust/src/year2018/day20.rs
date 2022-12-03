use crate::utils::graph::{depth_first_search, VisitorAction, VisitorFactory};
use itertools::Itertools;
use std::collections::HashSet;

type Coordinate =
    crate::utils::grid::Coordinate<{ isize::MIN }, { isize::MIN }, { isize::MAX }, { isize::MAX }>;
type Map = HashSet<(Coordinate, Coordinate)>;

fn parse_map(input: &str) -> Map {
    assert!(input.starts_with('^') && input.ends_with('$'));

    let mut map = Map::new();
    let mut stack = Vec::new();
    let mut position = Coordinate::new(0, 0).unwrap();
    for letter in input.chars() {
        match letter {
            '^' => {
                // do nothing
            }
            '$' => {
                assert!(stack.is_empty());
                return map;
            }
            '(' => {
                stack.push(position);
            }
            '|' => {
                position = *stack.last().unwrap();
            }
            ')' => {
                position = stack.pop().unwrap();
            }
            c => {
                let old_position = position;
                match c {
                    'N' => position.y -= 1,
                    'E' => position.x += 1,
                    'S' => position.y += 1,
                    'W' => position.x -= 1,
                    _ => panic!("unsupported direction: {}", c),
                }
                map.insert((old_position, position));
            }
        }
    }

    panic!("unexpected end of regex");
}

pub fn solve_part1(input: &str) -> usize {
    let map = parse_map(input);

    let mut furthest_room = 0;
    depth_first_search(
        Coordinate::new(0, 0).unwrap(),
        |coordinate| {
            coordinate
                .neighbours_cross()
                .filter(|new_coordinate| map.contains(&(*coordinate, *new_coordinate)))
                .collect_vec() // FIXME: should not collect
        },
        VisitorFactory::stateful_visitor(|_: &Coordinate, path_length: &usize| {
            let path_length = *path_length + 1;
            if path_length > furthest_room {
                furthest_room = path_length;
            }
            VisitorAction::Continue(path_length)
        }),
    );

    furthest_room - 1
}

pub fn solve_part2(input: &str) -> usize {
    let map = parse_map(input);

    let mut room_count = 0;
    depth_first_search(
        Coordinate::new(0, 0).unwrap(),
        |coordinate| {
            coordinate
                .neighbours_cross()
                .filter(|new_coordinate| map.contains(&(*coordinate, *new_coordinate)))
                .collect_vec() // FIXME: should not collect
        },
        VisitorFactory::stateful_visitor(|_: &Coordinate, path_length: &usize| {
            let path_length = *path_length + 1;
            if path_length - 1 >= 1000 {
                room_count += 1;
            }
            VisitorAction::Continue(path_length)
        }),
    );

    room_count
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_map() {
        assert_eq!(
            parse_map("^ENWWW(NEEE|SSE(EE|N))$"),
            Map::from(
                [
                    ((0, 0), (1, 0)),     // E
                    ((1, 0), (1, -1)),    // N
                    ((1, -1), (0, -1)),   // W
                    ((0, -1), (-1, -1)),  // W
                    ((-1, -1), (-2, -1)), // W
                    ((-2, -1), (-2, -2)), // N
                    ((-2, -2), (-1, -2)), // E
                    ((-1, -2), (0, -2)),  // E
                    ((0, -2), (1, -2)),   // E
                    ((-2, -1), (-2, 0)),  // S
                    ((-2, 0), (-2, 1)),   // S
                    ((-2, 1), (-1, 1)),   // E
                    ((-1, 1), (0, 1)),    // E
                    ((0, 1), (1, 1)),     // E
                    ((-1, 1), (-1, 0)),   // N
                ]
                .map(|(a, b)| (
                    Coordinate::new(a.0, a.1).unwrap(),
                    Coordinate::new(b.0, b.1).unwrap()
                ))
            )
        );
    }

    #[test]
    fn test_part1() {
        assert_eq!(solve_part1("^WNE$"), 3);
        assert_eq!(solve_part1("^ENWWW(NEEE|SSE(EE|N))$"), 10);
        assert_eq!(solve_part1("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"), 18);
        assert_eq!(
            solve_part1("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$"),
            23
        );
        assert_eq!(
            solve_part1("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$"),
            31
        );
    }

    crate::create_solver_test!(year2018, day20, part1);
    crate::create_solver_test!(year2018, day20, part2);
}
