struct SectionAssignment(usize, usize);

impl SectionAssignment {
    pub fn fully_contains(&self, other: &Self) -> bool {
        other.0 >= self.0 && other.1 <= self.1
    }

    pub fn overlaps(&self, other: &Self) -> bool {
        (other.0 >= self.0 && other.0 <= self.1) || (other.1 >= self.0 && other.1 <= self.1)
    }
}

impl From<&str> for SectionAssignment {
    fn from(value: &str) -> Self {
        let (left, right) = value.split_once('-').unwrap();
        let left = left.parse().unwrap();
        let right = right.parse().unwrap();
        SectionAssignment(left, right)
    }
}

fn parse_section_assignment_pairs(
    text: &str,
) -> impl Iterator<Item = (SectionAssignment, SectionAssignment)> + '_ {
    text.lines().map(|line| {
        let (left, right) = line.split_once(',').unwrap();
        (left.into(), right.into())
    })
}

pub fn solve_part1(input: &str) -> usize {
    parse_section_assignment_pairs(input)
        .map(|(left, right)| left.fully_contains(&right) || right.fully_contains(&left))
        .map(usize::from)
        .sum()
}

pub fn solve_part2(input: &str) -> usize {
    parse_section_assignment_pairs(input)
        .map(|(left, right)| left.overlaps(&right) || right.overlaps(&left))
        .map(usize::from)
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    static TEST_INPUT: &str = r#"2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"#;

    #[test]
    fn test_part1() {
        assert_eq!(solve_part1(TEST_INPUT), 2);
    }

    #[test]
    fn test_part2() {
        assert_eq!(solve_part2(TEST_INPUT), 4);
    }

    crate::create_solver_test!(part1);
    crate::create_solver_test!(part2);
}
