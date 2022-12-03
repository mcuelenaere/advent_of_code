use crate::utils::grid::plot_line;
use itertools::Itertools;
use std::collections::HashMap;

type Coordinate = crate::utils::grid::Coordinate<0, 0, { isize::MAX }, { isize::MAX }>;

#[derive(Debug)]
struct Line {
    start: Coordinate,
    stop: Coordinate,
}

fn parse_lines(input: &str) -> impl Iterator<Item = Line> + '_ {
    input.lines().map(|line| {
        let (start, stop) = line
            .splitn(2, " -> ")
            .map(|part| {
                part.splitn(2, ',')
                    .map(|coord| coord.parse::<isize>().expect("a number"))
                    .collect_tuple()
                    .map(|(x, y)| Coordinate::new(x, y))
                    .flatten()
                    .expect("a coordinate")
            })
            .collect_tuple()
            .expect("2 coordinates");

        Line { start, stop }
    })
}

fn count_overlapping_points(lines: impl Iterator<Item = Line>) -> usize {
    let mut points: HashMap<Coordinate, usize> = HashMap::new();
    for line in lines {
        for coordinate in plot_line(line.start, line.stop) {
            points
                .entry(coordinate)
                .and_modify(|count| {
                    *count += 1;
                })
                .or_insert(1);
        }
    }

    points.into_values().filter(|count| *count > 1).count()
}

pub fn solve_part1(input: &str) -> usize {
    count_overlapping_points(
        parse_lines(input)
            .filter(|line| line.start.x == line.stop.x || line.start.y == line.stop.y),
    )
}

pub fn solve_part2(input: &str) -> usize {
    count_overlapping_points(parse_lines(input))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let input = r#"0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"#;
        assert_eq!(solve_part1(input), 5);
    }

    #[test]
    fn test_part2() {
        let input = r#"0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"#;
        assert_eq!(solve_part2(input), 12);
    }

    crate::create_solver_test!(year2021, day05, part1);
    crate::create_solver_test!(year2021, day05, part2);
}
