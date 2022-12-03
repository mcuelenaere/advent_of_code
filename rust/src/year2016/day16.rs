use itertools::Itertools;
use num::Integer;

fn apply_dragon_curve(input: &str) -> String {
    let b: String = input
        .chars()
        .rev()
        .map(|c| match c {
            '1' => '0',
            '0' => '1',
            _ => unimplemented!(),
        })
        .collect();
    format!("{}0{}", input, b)
}

fn calculate_checksum(input: &str) -> String {
    let checksum: String = input
        .chars()
        .step_by(2)
        .zip_eq(input.chars().skip(1).step_by(2))
        .map(|(a, b)| if a == b { '1' } else { '0' })
        .collect();
    if checksum.len().is_even() {
        calculate_checksum(&checksum)
    } else {
        checksum
    }
}

fn solve(input: &str, disk_length: usize) -> String {
    let mut cur = input.to_string();
    while cur.len() < disk_length {
        cur = apply_dragon_curve(&cur);
    }
    calculate_checksum(&cur[0..disk_length])
}

pub fn solve_part1(input: &str) -> String {
    solve(input, 272)
}

pub fn solve_part2(input: &str) -> String {
    solve(input, 35651584)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_apply_dragon_curve() {
        assert_eq!(apply_dragon_curve("1"), "100");
        assert_eq!(apply_dragon_curve("0"), "001");
        assert_eq!(apply_dragon_curve("11111"), "11111000000");
        assert_eq!(
            apply_dragon_curve("111100001010"),
            "1111000010100101011110000"
        );
    }

    #[test]
    fn test_calculate_checksum() {
        assert_eq!(calculate_checksum("110010110100"), "100");
    }

    #[test]
    fn test_solve() {
        assert_eq!(solve("10000", 20), "01100");
    }

    crate::create_solver_test!(part1);
    crate::create_solver_test!(part2);
}
