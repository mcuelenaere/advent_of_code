use itertools::Itertools;

fn parse_list(input: &str) -> impl Iterator<Item = Vec<usize>> + '_ {
    input.lines().batching(|it| {
        let mut elf_calories = Vec::<usize>::new();
        loop {
            match it.next() {
                None => {
                    return if elf_calories.is_empty() {
                        None
                    } else {
                        Some(elf_calories)
                    }
                }
                Some("") => return Some(elf_calories),
                Some(calories) => elf_calories.push(calories.parse().unwrap()),
            }
        }
    })
}

pub fn solve_part1(input: &str) -> usize {
    parse_list(input)
        .map(|elf_calories| elf_calories.into_iter().sum())
        .max()
        .unwrap()
}

pub fn solve_part2(input: &str) -> usize {
    parse_list(input)
        .map(|elf_calories| elf_calories.into_iter().sum::<usize>())
        .sorted()
        .rev()
        .take(3)
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let input = "1000
2000
3000

4000

5000
6000

7000
8000
9000

10000";
        assert_eq!(solve_part1(input), 24000);
    }

    #[test]
    fn test_part2() {
        let input = "1000
2000
3000

4000

5000
6000

7000
8000
9000

10000";
        assert_eq!(solve_part2(input), 45000);
    }

    crate::create_solver_test!(year2022, day01, part1, verify_answer = true);
    crate::create_solver_test!(year2022, day01, part2, verify_answer = true);
}
