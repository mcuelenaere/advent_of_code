use crate::utils::graph::{depth_first_search, VisitorAction, VisitorFactory};
use itertools::Itertools;
use std::collections::HashMap;

type Coordinate = crate::utils::grid::Coordinate<0, 0, { isize::MAX }, { isize::MAX }>;

#[derive(Debug, Clone)]
struct HeightMap {
    start: Coordinate,
    target: Coordinate,
    heights: HashMap<Coordinate, usize>,
}

fn parse_heightmap(text: &str) -> HeightMap {
    let mut map = HeightMap {
        start: Coordinate::new(0, 0).unwrap(),
        target: Coordinate::new(0, 0).unwrap(),
        heights: HashMap::new(),
    };
    for (y, line) in text.lines().enumerate() {
        for (x, char) in line.char_indices() {
            let pos = Coordinate::new(x as isize, y as isize).unwrap();
            match char {
                'S' => {
                    map.start = pos;
                    map.heights.insert(pos, 0);
                }
                'E' => {
                    map.target = pos;
                    map.heights.insert(pos, 25);
                }
                'a'..='z' => {
                    map.heights.insert(pos, char as usize - 'a' as usize);
                }
                _ => panic!("invalid character"),
            }
        }
    }

    map
}

fn find_shortest_path_length(
    start: Coordinate,
    target: Coordinate,
    heights: HashMap<Coordinate, usize>,
) -> Option<usize> {
    let mut total_steps = None;
    depth_first_search(
        start,
        |pos| {
            pos.neighbours_cross()
                .filter(|neighbour| {
                    let current_height = *heights.get(pos).unwrap();
                    matches!(heights.get(neighbour), Some(neighbour_height) if *neighbour_height <= current_height + 1)
                })
                .collect_vec()
        },
        VisitorFactory::stateful_visitor::<_, usize, _>(|node, steps| {
            if *node == target {
                match total_steps {
                    None => {
                        total_steps = Some(*steps);
                    }
                    Some(_total_steps) if *steps < _total_steps => {
                        total_steps = Some(*steps);
                    }
                    _ => {}
                }
                VisitorAction::Stop
            } else {
                VisitorAction::Continue(steps + 1)
            }
        }),
    );
    total_steps
}

pub fn solve_part1(input: &str) -> usize {
    let map = parse_heightmap(input);
    find_shortest_path_length(map.start, map.target, map.heights).unwrap()
}

pub fn solve_part2(input: &str) -> usize {
    let map = parse_heightmap(input);
    map.heights
        .clone()
        .into_iter()
        .filter(|(_, height)| *height == 0)
        .filter_map(|(pos, _)| find_shortest_path_length(pos, map.target, map.heights.clone()))
        .min()
        .unwrap()
}

#[cfg(test)]
mod tests {
    use super::*;

    static TEST_INPUT: &str = r#"Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"#;

    #[test]
    fn test_part1() {
        assert_eq!(solve_part1(TEST_INPUT), 31);
    }

    #[test]
    fn test_part2() {
        assert_eq!(solve_part2(TEST_INPUT), 29);
    }

    crate::create_solver_test!(part1);
    crate::create_solver_test!(part2);
}
