use crate::utils::graph::shortest_path_with_cost;
use itertools::Itertools;
use std::collections::HashMap;

type Coordinate = crate::utils::grid::Coordinate<0, 0, { isize::MAX }, { isize::MAX }>;
type RiskLevel = u8;

#[derive(Debug)]
struct Cavern(HashMap<Coordinate, RiskLevel>);

impl Cavern {
    pub fn top_left(&self) -> Coordinate {
        *self.0.keys().min().unwrap()
    }

    pub fn bottom_right(&self) -> Coordinate {
        *self.0.keys().max().unwrap()
    }

    pub fn size(&self) -> usize {
        let len = self.0.len() as f64;
        len.sqrt() as usize
    }

    pub fn find_shortest_path(
        &self,
        start: Coordinate,
        end: Coordinate,
    ) -> Vec<(Coordinate, usize)> {
        shortest_path_with_cost(
            start,
            0,
            |c| c == &end,
            |c| {
                c.neighbours_cross()
                    .filter_map(|neighbour| {
                        self.0
                            .get(&neighbour)
                            .map(|risk_level| (neighbour, *risk_level as usize))
                    })
                    .collect_vec() // FIXME: should not collect
            },
            |c| end.manhattan_distance(c),
        )
        .expect("a shortest path")
    }
}

fn parse_cavern(input: &str) -> Cavern {
    let risk_levels = input
        .lines()
        .enumerate()
        .flat_map(|(y, line)| {
            line.char_indices().map(move |(x, c)| {
                (
                    Coordinate::new(x as isize, y as isize).unwrap(),
                    c.to_digit(10).expect("a valid number") as RiskLevel,
                )
            })
        })
        .collect();
    Cavern(risk_levels)
}

pub fn solve_part1(input: &str) -> usize {
    let cavern = parse_cavern(input);
    let path = cavern.find_shortest_path(cavern.top_left(), cavern.bottom_right());
    let (_, total_risk) = path.last().unwrap();
    *total_risk
}

fn expand_cavern(cavern: &mut Cavern, times: usize) {
    let coordinates = cavern
        .0
        .iter()
        .map(|(coordinate, risk_level)| (*coordinate, *risk_level))
        .collect_vec();
    let cavern_size = cavern.size() as isize;

    for x in 0..(times as isize) {
        for y in 0..(times as isize) {
            if (x, y) == (0, 0) {
                continue;
            }

            let risk_increase = (x + y) as u8;
            for (coordinate, risk_level) in coordinates.iter() {
                let mut risk_level = (risk_level + risk_increase) % 9;
                if risk_level == 0 {
                    risk_level = 9;
                }
                let coordinate = Coordinate::new(
                    coordinate.x + x * cavern_size,
                    coordinate.y + y * cavern_size,
                )
                .unwrap();
                cavern.0.insert(coordinate, risk_level);
            }
        }
    }

    // sanity check
    assert_eq!(cavern.size(), cavern_size as usize * times);
}

pub fn solve_part2(input: &str) -> usize {
    let mut cavern = parse_cavern(input);
    expand_cavern(&mut cavern, 5);

    let path = cavern.find_shortest_path(cavern.top_left(), cavern.bottom_right());
    let (_, total_risk) = path.last().unwrap();
    *total_risk
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let input = r#"1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"#;
        assert_eq!(solve_part1(input), 40);
    }

    #[test]
    fn test_part2() {
        let input = r#"1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"#;
        assert_eq!(solve_part2(input), 315);
    }

    crate::create_solver_test!(year2021, day15, part1, verify_answer = true);
    crate::create_solver_test!(year2021, day15, part2, verify_answer = true);
}
