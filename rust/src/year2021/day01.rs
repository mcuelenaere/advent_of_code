use itertools::izip;

fn parse_depths(input: &str) -> Vec<usize> {
    input
        .lines()
        .map(|line| line.parse().expect("a number"))
        .collect()
}

fn count_increases(inputs: Vec<usize>) -> usize {
    let mut increases = 0;
    for (cur, next) in inputs.iter().zip(inputs[1..].iter()) {
        if next > cur {
            increases += 1;
        }
    }

    increases
}

pub fn solve_part1(input: &str) -> usize {
    let depths = parse_depths(input);
    count_increases(depths)
}

pub fn solve_part2(input: &str) -> usize {
    let depths = parse_depths(input);
    let sums: Vec<usize> = izip!(depths.iter(), depths[1..].iter(), depths[2..].iter())
        .map(|(a, b, c)| a + b + c)
        .collect();
    count_increases(sums)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let input = r#"199
200
208
210
200
207
240
269
260
263"#;
        assert_eq!(solve_part1(input), 7);
    }

    #[test]
    fn test_part2() {
        let input = r#"199
200
208
210
200
207
240
269
260
263"#;
        assert_eq!(solve_part2(input), 5);
    }

    crate::create_solver_test!(year2021, day01, part1);
    crate::create_solver_test!(year2021, day01, part2);
}
