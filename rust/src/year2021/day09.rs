use crate::utils::graph::{breadth_first_search, VisitorAction, VisitorFactory};
use itertools::Itertools;
use std::collections::HashMap;

type Location = crate::utils::grid::Coordinate<0, 0, { isize::MAX }, { isize::MAX }>;

fn parse_locations(input: &str) -> impl Iterator<Item = (Location, usize)> + '_ {
    input.lines().enumerate().flat_map(|(y, line)| {
        line.char_indices().map(move |(x, c)| {
            let location = Location::new(x as isize, y as isize).expect("valid location");
            let height = c.to_digit(10).expect("valid height") as usize;
            (location, height)
        })
    })
}

fn find_low_points(
    locations: &HashMap<Location, usize>,
) -> impl Iterator<Item = (&Location, usize)> + '_ {
    locations
        .iter()
        .filter(|(location, height)| {
            location
                .neighbours_cross()
                .filter_map(|neighbour| locations.get(&neighbour))
                .all(|neighbour_height| **height < *neighbour_height)
        })
        .map(|(location, height)| (location, *height))
}

pub fn solve_part1(input: &str) -> usize {
    let locations: HashMap<_, _> = parse_locations(input).collect();

    find_low_points(&locations)
        .map(|(_, height)| height + 1)
        .sum()
}

pub fn solve_part2(input: &str) -> usize {
    let locations: HashMap<_, _> = parse_locations(input).collect();

    find_low_points(&locations)
        .map(|(low_point, _)| {
            let mut basin_size = 0usize;
            breadth_first_search(
                *low_point,
                |location: &Location| {
                    let location_height = locations[location];
                    location
                        .neighbours_cross()
                        .filter(|neighbour| match locations.get(neighbour) {
                            Some(neighbour_height) => {
                                *neighbour_height != 9 && *neighbour_height > location_height
                            }
                            None => false,
                        })
                        .collect_vec() // FIXME: should not collect
                },
                VisitorFactory::with_visit(|location: &Location, state: &()| {
                    basin_size += 1;
                    VisitorAction::Continue(())
                }),
            );

            basin_size
        })
        .sorted()
        .rev()
        .take(3)
        .reduce(|a, b| a * b)
        .unwrap()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let input = r#"2199943210
3987894921
9856789892
8767896789
9899965678"#;
        assert_eq!(solve_part1(input), 15);
    }

    #[test]
    fn test_part2() {
        let input = r#"2199943210
3987894921
9856789892
8767896789
9899965678"#;
        assert_eq!(solve_part2(input), 1134);
    }

    crate::create_solver_test!(year2021, day09, part1, verify_answer = true);
    crate::create_solver_test!(year2021, day09, part2, verify_answer = true);
}
