use crate::utils::grid::plot_line;
use itertools::Itertools;
use std::collections::HashSet;

type Coordinate = crate::utils::grid::Coordinate<0, 0, { isize::MAX }, { isize::MAX }>;
type Cave = HashSet<Coordinate>;

fn parse_cave(text: &str) -> Cave {
    let mut cave = Cave::new();
    for line in text.lines() {
        line.split(" -> ")
            .map(|points| {
                let (x, y) = points.split_once(',').expect("valid point");
                Coordinate::new(
                    x.parse().expect("valid number"),
                    y.parse().expect("valid number"),
                )
                .expect("valid coordinate")
            })
            .tuple_windows()
            .for_each(|(start, stop)| {
                for coordinate in plot_line(start, stop) {
                    cave.insert(coordinate);
                }
            })
    }
    cave
}

fn solve(cave: Cave) -> usize {
    let sand_origin = Coordinate::new(500, 0).unwrap();
    let lowest_y = cave.iter().map(|coordinate| coordinate.y).max().unwrap();
    let mut stuck_sand = HashSet::new();

    'outer: loop {
        let mut sand_grain = sand_origin;
        'inner: loop {
            if sand_grain.y > lowest_y {
                // we're flowing into the abyss
                break 'outer;
            }

            // try moving down
            sand_grain.y += 1;
            if !cave.contains(&sand_grain) && !stuck_sand.contains(&sand_grain) {
                continue;
            }

            // try moving down-left
            sand_grain.x -= 1;
            if !cave.contains(&sand_grain) && !stuck_sand.contains(&sand_grain) {
                continue;
            }

            // try moving down-right
            sand_grain.x += 2;
            if !cave.contains(&sand_grain) && !stuck_sand.contains(&sand_grain) {
                continue;
            }

            // we're stuck here, exit loop
            sand_grain.y -= 1;
            sand_grain.x -= 1;
            break 'inner;
        }
        stuck_sand.insert(sand_grain);
        if sand_grain == sand_origin {
            // we're blocked at the source
            break;
        }
    }

    stuck_sand.len()
}

pub fn solve_part1(input: &str) -> usize {
    let cave = parse_cave(input);
    solve(cave)
}

pub fn solve_part2(input: &str) -> usize {
    let mut cave = parse_cave(input);
    let floor_y = cave.iter().map(|coordinate| coordinate.y).max().unwrap() + 2;
    for x in 0..=1000 {
        // add floor
        cave.insert(Coordinate::new(x, floor_y).unwrap());
    }
    solve(cave)
}

#[cfg(test)]
mod tests {
    use super::*;

    static TEST_INPUT: &str = r#"498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"#;

    #[test]
    fn test_part1() {
        assert_eq!(solve_part1(TEST_INPUT), 24);
    }

    #[test]
    fn test_part2() {
        assert_eq!(solve_part2(TEST_INPUT), 93);
    }

    crate::create_solver_test!(part1);
    crate::create_solver_test!(part2);
}
