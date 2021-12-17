use lazy_static::lazy_static;
use regex::Regex;
use std::ops::RangeInclusive;

#[derive(Debug)]
struct Area {
    x: RangeInclusive<isize>,
    y: RangeInclusive<isize>,
}

impl Area {
    pub fn contains(&self, coordinate: &Coordinate) -> bool {
        self.x.contains(&coordinate.x) && self.y.contains(&coordinate.y)
    }

    pub fn bottom_right(&self) -> Coordinate {
        Coordinate::new(*self.x.end(), *self.y.end()).unwrap()
    }
}

lazy_static! {
    static ref RE_TARGET_AREA: Regex =
        Regex::new(r"^target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)$").unwrap();
}

fn parse_target_area(input: &str) -> Area {
    let captures = RE_TARGET_AREA.captures(input).expect("valid target area");

    let x1 = captures[1].parse::<isize>().expect("a number");
    let x2 = captures[2].parse::<isize>().expect("a number");
    let y1 = captures[3].parse::<isize>().expect("a number");
    let y2 = captures[4].parse::<isize>().expect("a number");

    Area {
        x: x1..=x2,
        y: y1..=y2,
    }
}

type Coordinate =
    crate::utils::grid::Coordinate<{ isize::MIN }, { isize::MIN }, { isize::MAX }, { isize::MAX }>;

fn plot_path(
    start: &Coordinate,
    velocity: (isize, isize),
    target_area: &Area,
) -> Option<Vec<Coordinate>> {
    let area_bottom = target_area.bottom_right().y;

    let (mut v_x, mut v_y) = velocity;
    let mut current = *start;
    let mut path = Vec::new();
    path.push(current);

    loop {
        current.x += v_x;
        current.y += v_y;
        path.push(current);

        if v_x > 0 {
            v_x -= 1;
        } else if v_x < 0 {
            v_x += 1;
        }
        v_y -= 1;

        if target_area.contains(&current) {
            // we made it within the area!
            return Some(path);
        } else if current.y < area_bottom - 1 {
            // we are below the target and can never go up again, so abort
            return None;
        }
    }
}

pub fn solve_part1(input: &str) -> usize {
    let area = parse_target_area(input);
    let start = Coordinate::new(0, 0).unwrap();

    // this is just a bruteforce approach, constants were determined empirically
    let mut best_y = 0;
    for v_x in 1..=15 {
        for v_y in 0..=300 {
            if let Some(path) = plot_path(&start, (v_x, v_y), &area) {
                let max_y = path
                    .into_iter()
                    .map(|c| c.y)
                    .filter(|y| *y > 0)
                    .max()
                    .unwrap_or(0) as usize;
                best_y = best_y.max(max_y);
            }
        }
    }

    best_y
}

pub fn solve_part2(input: &str) -> usize {
    let area = parse_target_area(input);
    let start = Coordinate::new(0, 0).unwrap();

    let max_x = *area.x.end();
    let min_y = *area.y.start();

    // this is just a bruteforce approach, constants were determined empirically
    let mut counter = 0;
    for v_x in 1..=max_x {
        for v_y in min_y..=250 {
            if plot_path(&start, (v_x, v_y), &area).is_some() {
                counter += 1;
            }
        }
    }

    counter
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_plot_path() {
        let area = parse_target_area("target area: x=20..30, y=-10..-5");
        let start = Coordinate::new(0, 0).unwrap();

        let plot_path = |velocity: (isize, isize)| {
            plot_path(&start, velocity, &area)
                .map(|path| (path.len(), path.last().unwrap().to_tuple()))
        };

        assert_eq!(plot_path((7, 2)), Some((8, (28, -7))));
        assert_eq!(plot_path((6, 3)), Some((10, (21, -9))));
        assert_eq!(plot_path((9, 0)), Some((5, (30, -6))));
        assert_eq!(plot_path((17, -4)), None);
        assert!(plot_path((6, 9)).is_some());
    }

    #[test]
    fn test_part1() {
        assert_eq!(solve_part1("target area: x=20..30, y=-10..-5"), 45);
    }

    #[test]
    fn test_part2() {
        assert_eq!(solve_part2("target area: x=20..30, y=-10..-5"), 112);
    }

    crate::create_solver_test!(year2021, day17, part1, verify_answer = true);
    crate::create_solver_test!(year2021, day17, part2, verify_answer = true);
}
