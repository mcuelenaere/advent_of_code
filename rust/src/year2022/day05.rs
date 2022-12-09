use itertools::Itertools;
use lazy_static::lazy_static;
use regex::Regex;
use std::collections::VecDeque;

type CrateStacks = Vec<VecDeque<char>>;

#[derive(Debug)]
struct RearrangementStep {
    amount: usize,
    from: usize,
    to: usize,
}

lazy_static! {
    static ref RE_REARRANGEMENT_STEP: Regex =
        Regex::new(r"^move (\d+) from (\d+) to (\d+)$").unwrap();
}

fn parse_xxx(input: &str) -> (CrateStacks, Vec<RearrangementStep>) {
    let mut crate_stacks = CrateStacks::new();
    let mut rearrangement_steps = Vec::new();
    let mut is_parsing_steps = false;
    for line in input.lines() {
        if line.is_empty() {
            is_parsing_steps = true;
            continue;
        }

        if is_parsing_steps {
            let m = RE_REARRANGEMENT_STEP.captures(line).expect("valid step");
            rearrangement_steps.push(RearrangementStep {
                amount: m[1].parse().unwrap(),
                from: m[2].parse().unwrap(),
                to: m[3].parse().unwrap(),
            });
        } else {
            for (idx, c) in line.char_indices() {
                if (idx + 1) % 4 != 2 {
                    // not the middle of the crate definition
                    continue;
                }

                if c == ' ' || c.is_ascii_digit() {
                    // empty crate or crate number
                    continue;
                }

                let crate_position = idx / 4;
                while crate_stacks.len() <= crate_position {
                    crate_stacks.push(VecDeque::new());
                }
                crate_stacks[crate_position].push_back(c);
            }
        }
    }
    (crate_stacks, rearrangement_steps)
}

pub fn solve_part1(input: &str) -> String {
    let (mut stacks, steps) = parse_xxx(input);
    for step in steps {
        for _ in 0..step.amount {
            let item = stacks[step.from - 1].pop_front().unwrap();
            stacks[step.to - 1].push_front(item);
        }
    }
    stacks.iter().map(|stack| stack.front().unwrap()).join("")
}

pub fn solve_part2(input: &str) -> String {
    let (mut stacks, steps) = parse_xxx(input);
    for step in steps {
        for item in stacks[step.from - 1]
            .iter()
            .take(step.amount)
            .rev()
            .cloned()
            .collect_vec()
        {
            stacks[step.to - 1].push_front(item);
        }
        for _ in 0..step.amount {
            stacks[step.from - 1].pop_front();
        }
    }
    stacks.iter().map(|stack| stack.front().unwrap()).join("")
}

#[cfg(test)]
mod tests {
    use super::*;

    static TEST_INPUT: &str = r#"    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"#;

    #[test]
    fn test_part1() {
        assert_eq!(solve_part1(TEST_INPUT), "CMZ".to_string());
    }

    #[test]
    fn test_part2() {
        assert_eq!(solve_part2(TEST_INPUT), "MCD".to_string());
    }

    crate::create_solver_test!(part1);
    crate::create_solver_test!(part2);
}
