use itertools::Itertools;
use std::cmp::{max, min};

fn parse_positions(input: &str) -> Vec<usize> {
    input
        .split(',')
        .map(|s| s.parse().expect("a valid number"))
        .collect_vec()
}

fn find_alignment_position(
    positions: Vec<usize>,
    calculate_cost: impl Fn(usize, usize) -> usize,
) -> (usize, usize) {
    let max_position = positions.iter().max().cloned().unwrap();

    let (best_position, lowest_cost) = (1..=max_position)
        .into_iter()
        .map(|x| {
            let cost = positions.iter().map(|pos| calculate_cost(*pos, x)).sum();
            (x, cost)
        })
        .min_by_key(|(_, cost)| *cost)
        .unwrap();

    (best_position, lowest_cost)
}

pub fn solve_part1(input: &str) -> usize {
    let positions = parse_positions(input);
    let (_, cost) = find_alignment_position(positions, |pos, x| max(pos, x) - min(pos, x));

    cost
}

pub fn solve_part2(input: &str) -> usize {
    let positions = parse_positions(input);
    let (_, cost) = find_alignment_position(positions, |pos, x| {
        let diff = max(pos, x) - min(pos, x);
        (diff * (diff + 1)) / 2
    });

    cost
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let input = "16,1,2,0,4,2,7,1,2,14";
        assert_eq!(solve_part1(input), 37);
    }

    #[test]
    fn test_part2() {
        let input = "16,1,2,0,4,2,7,1,2,14";
        assert_eq!(solve_part2(input), 168);
    }

    crate::create_solver_test!(year2021, day07, part1, verify_answer = true);
    crate::create_solver_test!(year2021, day07, part2, verify_answer = true);
}
