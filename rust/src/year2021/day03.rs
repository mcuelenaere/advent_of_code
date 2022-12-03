fn parse_diagnostic_report(input: &str) -> (usize, Vec<u16>) {
    let mut bit_length = 0;
    let diagnostic_report = input
        .lines()
        .map(|line| {
            bit_length = line.len();
            u16::from_str_radix(line, 2).expect("a valid binary number")
        })
        .collect();

    (bit_length, diagnostic_report)
}

fn determine_bit_count(input: &[u16], bit: usize) -> (usize, usize) {
    let mut zero_count = 0;
    let mut one_count = 0;
    for number in input {
        if (number & (1 << bit)) != 0 {
            one_count += 1;
        } else {
            zero_count += 1;
        }
    }

    (zero_count, one_count)
}

pub fn solve_part1(input: &str) -> usize {
    let (bit_length, diagnostic_report) = parse_diagnostic_report(input);

    let mut gamma_rate = 0;
    let mut epsilon_rate = 0;
    for bit in 0..bit_length {
        let (zero_count, one_count) = determine_bit_count(&diagnostic_report, bit);

        if one_count > zero_count {
            gamma_rate |= 1 << bit;
        } else {
            epsilon_rate |= 1 << bit;
        }
    }

    gamma_rate * epsilon_rate
}

pub fn solve_part2(input: &str) -> usize {
    let (bit_length, diagnostic_report) = parse_diagnostic_report(input);

    let determine_rating = |bit_criteria_fn: fn(usize, usize) -> u16| {
        let mut copy = diagnostic_report.clone();
        for bit in (0..bit_length).rev() {
            let (zero_count, one_count) = determine_bit_count(&copy, bit);

            let bit_to_check = bit_criteria_fn(zero_count, one_count) << bit;
            copy.retain(|number| number & (1 << bit) == bit_to_check);

            if copy.len() == 1 {
                break;
            }
        }

        assert_eq!(copy.len(), 1);
        copy[0] as usize
    };

    let oxygen_generator_rating = determine_rating(
        |zero_count, one_count| {
            if one_count >= zero_count {
                1
            } else {
                0
            }
        },
    );

    let co2_scrubber_rating = determine_rating(
        |zero_count, one_count| {
            if zero_count <= one_count {
                0
            } else {
                1
            }
        },
    );

    oxygen_generator_rating * co2_scrubber_rating
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let input = r#"00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"#;
        assert_eq!(solve_part1(input), 198);
    }

    #[test]
    fn test_part2() {
        let input = r#"00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"#;
        assert_eq!(solve_part2(input), 230);
    }

    crate::create_solver_test!(year2021, day03, part1);
    crate::create_solver_test!(year2021, day03, part2);
}
