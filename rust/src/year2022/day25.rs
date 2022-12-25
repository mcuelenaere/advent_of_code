use itertools::Itertools;
use std::collections::VecDeque;

fn parse_snafu_number(snafu: &str) -> usize {
    let mut number = 0isize;
    for (idx, c) in snafu.chars().rev().enumerate() {
        let current = match c {
            '=' => -2,
            '-' => -1,
            '0' => 0,
            '1' => 1,
            '2' => 2,
            _ => panic!("invalid character"),
        };
        number += current * 5isize.pow(idx as u32);
    }

    number as usize
}

fn to_snafu_number(mut number: usize) -> String {
    let mut buffer = VecDeque::new();
    loop {
        let m = number % 5;
        number /= 5;

        if m <= 2 {
            buffer.push_front(('0' as u8 + m as u8) as char);
        } else if m == 3 {
            buffer.push_front('=');
            number += 1;
        } else if m == 4 {
            buffer.push_front('-');
            number += 1;
        }

        if number == 0 {
            break;
        }
    }

    buffer.into_iter().join("")
}

pub fn solve_part1(input: &str) -> String {
    let total = input.lines().map(parse_snafu_number).sum();
    to_snafu_number(total)
}

pub fn solve_part2(input: &str) -> usize {
    0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_snafu_numbers() {
        let testcases: &[(usize, &str)] = &[
            (1, "1"),
            (2, "2"),
            (3, "1="),
            (4, "1-"),
            (5, "10"),
            (6, "11"),
            (7, "12"),
            (8, "2="),
            (9, "2-"),
            (10, "20"),
            (15, "1=0"),
            (20, "1-0"),
            (2022, "1=11-2"),
            (12345, "1-0---0"),
            (314159265, "1121-1110-1=0"),
            (1747, "1=-0-2"),
            (906, "12111"),
            (198, "2=0="),
            (11, "21"),
            (201, "2=01"),
            (31, "111"),
            (1257, "20012"),
            (32, "112"),
            (353, "1=-1="),
            (107, "1-12"),
            (7, "12"),
            (3, "1="),
            (37, "122"),
        ];

        for (number, snafu) in testcases {
            assert_eq!(parse_snafu_number(snafu), *number);
            assert_eq!(to_snafu_number(*number), snafu.to_string());
        }
    }

    static TEST_INPUT: &str = r#"1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"#;

    #[test]
    fn test_part1() {
        assert_eq!(solve_part1(TEST_INPUT), "2=-1=0".to_string());
    }

    crate::create_solver_test!(part1);
}
