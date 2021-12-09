use crate::utils::graph::{breadth_first_search, shortest_path, VisitorAction, VisitorFactory};
use itertools::Itertools;
use md5::{Digest, Md5};
use std::fmt::{Display, Write};

type Coordinate = crate::utils::grid::Coordinate<0, 0, 3, 3>;

#[derive(Debug, Eq, PartialEq)]
enum Direction {
    Up,
    Right,
    Down,
    Left,
}

impl Direction {
    pub fn try_move(&self, coordinate: Coordinate) -> Option<Coordinate> {
        let Coordinate { mut x, mut y } = coordinate;
        match self {
            Direction::Up => y -= 1,
            Direction::Down => y += 1,
            Direction::Right => x += 1,
            Direction::Left => x -= 1,
        }
        Coordinate::new(x, y)
    }
}

impl Display for Direction {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Up => f.write_char('U'),
            Self::Right => f.write_char('R'),
            Self::Down => f.write_char('D'),
            Self::Left => f.write_char('L'),
        }
    }
}

fn calculate_open_doors(passcode: &str) -> Vec<Direction> {
    let mut hasher = Md5::new();
    hasher.update(passcode);
    let hash = format!("{:x}", hasher.finalize());

    let mut open_doors = Vec::new();
    hash[0..4]
        .chars()
        .zip_eq([
            Direction::Up,
            Direction::Down,
            Direction::Left,
            Direction::Right,
        ])
        .for_each(|(char, direction)| {
            if !char.is_digit(10) && char != 'a' {
                // open door
                open_doors.push(direction);
            }
        });

    open_doors
}

fn get_neighbours((coordinate, passcode): &(Coordinate, String)) -> Vec<(Coordinate, String)> {
    calculate_open_doors(passcode)
        .into_iter()
        .filter_map(|direction| {
            direction
                .try_move(*coordinate)
                .map(|new_coordinate| (new_coordinate, format!("{}{:}", passcode, direction)))
        })
        .collect::<Vec<_>>()
}

pub fn solve_part1(input: &str) -> String {
    let target = Coordinate::new(3, 3).unwrap();
    let path = shortest_path(
        (Coordinate::new(0, 0).unwrap(), input.to_string()),
        |(coordinate, _): &(Coordinate, String)| *coordinate == target,
        get_neighbours,
        |(coordinate, _): &(Coordinate, String)| target.manhattan_distance(coordinate),
    )
    .expect("a valid path");

    path.last()
        .unwrap()
        .1
        .strip_prefix(input)
        .unwrap()
        .to_string()
}

pub fn solve_part2(input: &str) -> usize {
    let target = Coordinate::new(3, 3).unwrap();
    let mut max_path_length = 0;
    breadth_first_search(
        (Coordinate::new(0, 0).unwrap(), input.to_string()),
        get_neighbours,
        VisitorFactory::custom_visitor(
            |_: &(Coordinate, String), _: &usize| true,
            |(coordinate, _): &(Coordinate, String), path_len: &usize| {
                if *coordinate == target {
                    if *path_len > max_path_length {
                        max_path_length = *path_len;
                    }
                    VisitorAction::Stop
                } else {
                    VisitorAction::Continue(path_len + 1)
                }
            },
        ),
    );

    max_path_length
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_calculate_open_doors() {
        assert_eq!(
            calculate_open_doors("hijkl"),
            vec![Direction::Up, Direction::Down, Direction::Left]
        );
        assert_eq!(
            calculate_open_doors("hijklD"),
            vec![Direction::Up, Direction::Left, Direction::Right]
        );
        assert_eq!(calculate_open_doors("hijklDR"), vec![]);
        assert_eq!(calculate_open_doors("hijklDU"), vec![Direction::Right]);
        assert_eq!(calculate_open_doors("hijklDUR"), vec![]);
    }

    #[test]
    fn test_part1() {
        assert_eq!(solve_part1("ihgpwlah"), "DDRRRD");
        assert_eq!(solve_part1("kglvqrro"), "DDUDRLRRUDRD");
        assert_eq!(solve_part1("ulqzkmiv"), "DRURDRUDDLLDLUURRDULRLDUUDDDRR");
    }

    #[test]
    fn test_part2() {
        assert_eq!(solve_part2("ihgpwlah"), 370);
        assert_eq!(solve_part2("kglvqrro"), 492);
        assert_eq!(solve_part2("ulqzkmiv"), 830);
    }

    crate::create_solver_test!(year2016, day17, part1, verify_answer = true);
    crate::create_solver_test!(year2016, day17, part2, verify_answer = true);
}
