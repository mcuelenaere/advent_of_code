use crate::utils::math::chinese_remainder_theorem;
use lazy_static::lazy_static;
use regex::Regex;

#[derive(Debug)]
struct Disc {
    number: usize,
    number_of_positions: usize,
    start_position: usize,
}

impl Disc {
    pub fn position_at(&self, timestamp: usize) -> usize {
        (self.start_position + timestamp) % self.number_of_positions
    }
}

lazy_static! {
    static ref RE_DISC_POSITIONS: Regex =
        Regex::new(r"Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+).")
            .unwrap();
}

fn parse_discs(input: &str) -> Vec<Disc> {
    input
        .lines()
        .filter_map(|line| {
            if let Some(c) = RE_DISC_POSITIONS.captures(line) {
                Some(Disc {
                    number: c[1].parse().expect("a valid disc number"),
                    number_of_positions: c[2]
                        .parse()
                        .expect("valid number for number of positions"),
                    start_position: c[3].parse().expect("valid number for start position"),
                })
            } else {
                None
            }
        })
        .collect()
}

fn _solve(discs: Vec<Disc>) -> usize {
    // t + start_position + disc_number = 0 mod number_of_positions <=> t = -start_position - disc_number mod number_of_positions
    let timestamp = chinese_remainder_theorem(discs.iter().map(|disc| {
        let start_position = disc.start_position as isize;
        let number = disc.number as isize;
        let number_of_positions = disc.number_of_positions as isize;

        (-start_position - number, number_of_positions)
    }))
    .unwrap() as usize;

    // sanity check
    assert!(discs
        .iter()
        .map(|disc| disc.position_at(timestamp + disc.number))
        .all(|position| position == 0));

    timestamp
}

pub fn solve_part1(input: &str) -> usize {
    let discs = parse_discs(input);

    _solve(discs)
}

pub fn solve_part2(input: &str) -> usize {
    let mut discs = parse_discs(input);
    discs.push(Disc {
        number: 7,
        number_of_positions: 11,
        start_position: 0,
    });

    _solve(discs)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let puzzle = r#"Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1."#;
        let result = solve_part1(puzzle);
        assert_eq!(result, 5);
    }

    crate::create_solver_test!(year2016, day15, part1);
    crate::create_solver_test!(year2016, day15, part2);
}
