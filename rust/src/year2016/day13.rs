use crate::utils::graph::{
    breadth_first_search, depth_first_search, shortest_path, VisitorAction, VisitorFactory,
};
use num::Integer;

#[derive(Debug, Copy, Clone, Eq, PartialEq, Hash)]
struct Coordinate {
    x: usize,
    y: usize,
}

impl Coordinate {
    pub fn new(x: usize, y: usize) -> Self {
        Coordinate { x, y }
    }

    pub fn neighbours(&self) -> impl Iterator<Item = Self> + '_ {
        [(0, -1), (1, 0), (0, 1), (-1, 0)]
            .iter()
            .filter_map(move |(x_off, y_off)| {
                let x = self.x as isize + x_off;
                let y = self.y as isize + y_off;
                if x < 0 || y < 0 {
                    None
                } else {
                    Some(Coordinate {
                        x: x as usize,
                        y: y as usize,
                    })
                }
            })
    }
}

fn is_wall(c: &Coordinate, magic_number: usize) -> bool {
    let (x, y) = (c.x, c.y);
    let mut sum = x * x + 3 * x + 2 * x * y + y + y * y;
    sum += magic_number;
    sum.count_ones().is_odd()
}

fn _solve_part1(magic_number: usize, target: Coordinate) -> usize {
    let start = Coordinate::new(1, 1);
    assert!(!is_wall(&start, magic_number));

    let path = shortest_path(
        start,
        target,
        |c: &Coordinate| {
            c.neighbours()
                .filter(|neighbour| !is_wall(neighbour, magic_number))
                .collect::<Vec<_>>() // FIXME: don't collect
        },
        |_: &Coordinate| 0,
    );
    path.expect("found a path").len() - 1
}

pub fn solve_part1(input: &str) -> usize {
    let magic_number = input.parse().expect("a number");
    _solve_part1(magic_number, Coordinate::new(31, 39))
}

fn _solve_part2(magic_number: usize, max_steps: usize) -> usize {
    let mut total_locations = 0;
    breadth_first_search(
        Coordinate::new(1, 1),
        |c: &Coordinate| {
            c.neighbours()
                .filter(|neighbour| !is_wall(neighbour, magic_number))
                .collect::<Vec<_>>() // FIXME: don't collect
        },
        VisitorFactory::with_visit(|_: &Coordinate, path_length: &usize| {
            total_locations += 1;
            if *path_length >= max_steps {
                VisitorAction::Stop
            } else {
                VisitorAction::Continue(*path_length + 1)
            }
        }),
    );

    total_locations
}

pub fn solve_part2(input: &str) -> usize {
    let magic_number = input.parse().expect("a number");
    _solve_part2(magic_number, 50)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(_solve_part1(10, Coordinate::new(7, 4)), 11);
    }

    #[test]
    fn test_part2() {
        assert_eq!(_solve_part2(10, 0), 1);
        assert_eq!(_solve_part2(10, 1), 3);
        assert_eq!(_solve_part2(10, 2), 5);
        assert_eq!(_solve_part2(10, 3), 6);
        assert_eq!(_solve_part2(10, 4), 9);
        assert_eq!(_solve_part2(10, 5), 11);
    }

    crate::create_solver_test!(year2016, day13, part1, verify_answer = true);
    crate::create_solver_test!(year2016, day13, part2, verify_answer = true);
}
