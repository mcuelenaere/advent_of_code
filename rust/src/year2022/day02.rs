use itertools::Itertools;

#[derive(Eq, PartialEq, Copy, Clone)]
enum Shape {
    Rock,
    Paper,
    Scissors,
}

impl Shape {
    pub fn score(&self) -> usize {
        match self {
            Self::Rock => 1,
            Self::Paper => 2,
            Self::Scissors => 3,
        }
    }
}

#[derive(Copy, Clone)]
enum Outcome {
    Win,
    Loss,
    Draw,
}

impl Outcome {
    pub fn score(&self) -> usize {
        match self {
            Self::Win => 6,
            Self::Loss => 0,
            Self::Draw => 3,
        }
    }
}

fn parse_strategy_guide(text: &str) -> impl Iterator<Item = (Shape, &str)> + '_ {
    text.lines().map(|line| {
        let (opponent, you) = line.splitn(2, " ").collect_tuple().unwrap();
        let opponent = match opponent {
            "A" => Shape::Rock,
            "B" => Shape::Paper,
            "C" => Shape::Scissors,
            _ => panic!("unknown shape {}", opponent),
        };
        (opponent, you)
    })
}

pub fn solve_part1(input: &str) -> usize {
    parse_strategy_guide(input)
        .map(|(opponent, you)| {
            let you = match you {
                "X" => Shape::Rock,
                "Y" => Shape::Paper,
                "Z" => Shape::Scissors,
                _ => panic!("unknown shape {}", you),
            };
            let outcome = match (you, opponent) {
                (Shape::Rock, Shape::Scissors) => Outcome::Win,
                (Shape::Rock, Shape::Paper) => Outcome::Loss,
                (Shape::Paper, Shape::Rock) => Outcome::Win,
                (Shape::Paper, Shape::Scissors) => Outcome::Loss,
                (Shape::Scissors, Shape::Rock) => Outcome::Loss,
                (Shape::Scissors, Shape::Paper) => Outcome::Win,
                (a, b) if a == b => Outcome::Draw,
                _ => unimplemented!(),
            };
            you.score() + outcome.score()
        })
        .sum()
}

pub fn solve_part2(input: &str) -> usize {
    parse_strategy_guide(input)
        .map(|(opponent, outcome)| {
            let outcome = match outcome {
                "X" => Outcome::Loss,
                "Y" => Outcome::Draw,
                "Z" => Outcome::Win,
                _ => panic!("unknown outcome {}", outcome),
            };
            let you = match (opponent, outcome) {
                (a, Outcome::Draw) => a,
                (Shape::Rock, Outcome::Win) => Shape::Paper,
                (Shape::Paper, Outcome::Win) => Shape::Scissors,
                (Shape::Scissors, Outcome::Win) => Shape::Rock,
                (Shape::Rock, Outcome::Loss) => Shape::Scissors,
                (Shape::Paper, Outcome::Loss) => Shape::Rock,
                (Shape::Scissors, Outcome::Loss) => Shape::Paper,
            };
            you.score() + outcome.score()
        })
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let input = "A Y
B X
C Z";
        assert_eq!(solve_part1(input), 15);
    }

    #[test]
    fn test_part2() {
        let input = "A Y
B X
C Z";
        assert_eq!(solve_part2(input), 12);
    }

    crate::create_solver_test!(year2022, day02, part1);
    crate::create_solver_test!(year2022, day02, part2);
}
