use itertools::Itertools;
use std::collections::HashSet;

fn parse_priority(letter: char) -> usize {
    match letter {
        'a'..='z' => letter as usize - 'a' as usize + 1,
        'A'..='Z' => letter as usize - 'A' as usize + 27,
        _ => panic!("unknown priority"),
    }
}

pub fn solve_part1(input: &str) -> usize {
    input
        .lines()
        .flat_map(|line| {
            let length = line.len();
            if length % 2 != 0 {
                panic!("expected line length to be divisible by 2");
            }

            let (left, right) = line.split_at(length / 2);
            let left: HashSet<_> = left.chars().collect();
            let right: HashSet<_> = right.chars().collect();

            left.intersection(&right).cloned().collect_vec()
        })
        .map(parse_priority)
        .sum()
}

pub fn solve_part2(input: &str) -> usize {
    input
        .lines()
        .map(|line| line.chars().collect::<HashSet<_>>())
        .chunks(3)
        .into_iter()
        .map(|group| {
            let intersection = group
                .reduce(|a, b| a.intersection(&b).cloned().collect())
                .unwrap();
            assert_eq!(intersection.len(), 1);
            intersection.into_iter().next().unwrap()
        })
        .map(parse_priority)
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_priority() {
        assert_eq!(parse_priority('a'), 1);
        assert_eq!(parse_priority('z'), 26);
        assert_eq!(parse_priority('B'), 28);
        assert_eq!(parse_priority('Y'), 51);
    }

    static TEST_INPUT: &str = r#"vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"#;

    #[test]
    fn test_part1() {
        assert_eq!(solve_part1(TEST_INPUT), 157);
    }

    #[test]
    fn test_part2() {
        assert_eq!(solve_part2(TEST_INPUT), 70);
    }

    crate::create_solver_test!(part1);
    crate::create_solver_test!(part2);
}
