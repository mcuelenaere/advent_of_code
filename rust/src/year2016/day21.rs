use lazy_static::lazy_static;
use num::Integer;
use regex::Regex;

#[derive(Debug)]
enum Direction {
    Left,
    Right,
}

#[derive(Debug)]
enum Operation {
    SwapPositions(usize, usize),
    SwapLetters(char, char),
    RotateSteps(Direction, usize),
    RotateByLetterPosition(char),
    ReversePositions(usize, usize),
    MovePositions(usize, usize),
}

impl Operation {
    pub fn scramble(&self, password: &str) -> String {
        match self {
            Self::SwapPositions(x, y) => {
                let mut output: Vec<u8> = password.into();
                output.swap(*y, *x);
                String::from_utf8(output).unwrap()
            }
            Self::SwapLetters(x, y) => password
                .chars()
                .map(|char| {
                    if char == *x {
                        *y
                    } else if char == *y {
                        *x
                    } else {
                        char
                    }
                })
                .collect(),
            Self::RotateSteps(direction, steps) => {
                let steps = {
                    match direction {
                        Direction::Left => (*steps % password.len()),
                        Direction::Right => password.len() - (*steps % password.len()),
                    }
                };
                password
                    .chars()
                    .cycle()
                    .skip(steps)
                    .take(password.len())
                    .collect()
            }
            Self::RotateByLetterPosition(letter) => {
                let (mut index, _) = password.char_indices().find(|(_, c)| c == letter).unwrap();
                if index >= 4 {
                    index += 2;
                } else {
                    index += 1;
                }

                Self::RotateSteps(Direction::Right, index).scramble(password)
            }
            Self::ReversePositions(x, y) => {
                format!(
                    "{}{}{}",
                    &password[..*x],
                    &password[*x..=*y].chars().rev().collect::<String>(),
                    &password[*y + 1..]
                )
            }
            Self::MovePositions(x, y) => {
                let mut output = password.to_string();
                let c = output.remove(*x);
                output.insert(*y, c);
                output
            }
        }
    }

    pub fn unscramble(&self, password: &str) -> String {
        match self {
            Self::SwapPositions(_, _) => self.scramble(password),
            Self::SwapLetters(_, _) => self.scramble(password),
            Self::RotateSteps(direction, steps) => {
                let opposite_direction = {
                    match direction {
                        Direction::Left => Direction::Right,
                        Direction::Right => Direction::Left,
                    }
                };
                Self::RotateSteps(opposite_direction, *steps).scramble(password)
            }
            Self::RotateByLetterPosition(letter) => {
                let (mut index, _) = password.char_indices().find(|(_, c)| c == letter).unwrap();
                if index.is_odd() || index == 0 {
                    index = index / 2 + 1;
                } else {
                    index = index / 2 + 5;
                }

                Self::RotateSteps(Direction::Left, index).scramble(password)
            }
            Self::ReversePositions(_, _) => self.scramble(password),
            Self::MovePositions(x, y) => Self::MovePositions(*y, *x).scramble(password),
        }
    }
}

lazy_static! {
    static ref RE_SWAP_POSITIONS: Regex =
        Regex::new(r"swap position (\d+) with position (\d+)").unwrap();
    static ref RE_SWAP_LETTERS: Regex = Regex::new(r"swap letter (\w) with letter (\w)").unwrap();
    static ref RE_ROTATE_STEPS: Regex = Regex::new(r"rotate (left|right) (\d+) steps?").unwrap();
    static ref RE_ROTATE_BY_LETTER_POSITION: Regex =
        Regex::new(r"rotate based on position of letter (\w)").unwrap();
    static ref RE_REVERSE_POSITIONS: Regex =
        Regex::new(r"reverse positions (\d+) through (\d+)").unwrap();
    static ref RE_MOVE_POSITIONS: Regex =
        Regex::new(r"move position (\d+) to position (\d+)").unwrap();
}

fn parse_operations(input: &str) -> impl Iterator<Item = Operation> + '_ {
    input.lines().map(|line| {
        if let Some(m) = RE_SWAP_POSITIONS.captures(line) {
            Operation::SwapPositions(
                m[1].parse().expect("a number"),
                m[2].parse().expect("a number"),
            )
        } else if let Some(m) = RE_SWAP_LETTERS.captures(line) {
            Operation::SwapLetters(
                m[1].chars().next().expect("a letter"),
                m[2].chars().next().expect("a letter"),
            )
        } else if let Some(m) = RE_ROTATE_STEPS.captures(line) {
            let direction = match &m[1] {
                "left" => Direction::Left,
                "right" => Direction::Right,
                _ => unimplemented!(),
            };
            Operation::RotateSteps(direction, m[2].parse().expect("a number"))
        } else if let Some(m) = RE_ROTATE_BY_LETTER_POSITION.captures(line) {
            Operation::RotateByLetterPosition(m[1].chars().next().expect("a letter"))
        } else if let Some(m) = RE_REVERSE_POSITIONS.captures(line) {
            Operation::ReversePositions(
                m[1].parse().expect("a number"),
                m[2].parse().expect("a number"),
            )
        } else if let Some(m) = RE_MOVE_POSITIONS.captures(line) {
            Operation::MovePositions(
                m[1].parse().expect("a number"),
                m[2].parse().expect("a number"),
            )
        } else {
            panic!("unsupported line: {}", line);
        }
    })
}

fn scramble_password(password: &str, operations: Vec<Operation>) -> String {
    let mut password = password.to_string();
    for operation in operations {
        password = operation.scramble(&password);
    }
    password
}

pub fn solve_part1(input: &str) -> String {
    let operations = parse_operations(input).collect();
    scramble_password("abcdefgh", operations)
}

fn unscramble_password(password: &str, operations: Vec<Operation>) -> String {
    let mut password = password.to_string();
    for operation in operations.iter().rev() {
        password = operation.unscramble(&password);
    }
    password
}

pub fn solve_part2(input: &str) -> String {
    let operations = parse_operations(input).collect();
    unscramble_password("fbgdceah", operations)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_operation_scramble() {
        assert_eq!(
            Operation::SwapPositions(4, 0).scramble("abcde"),
            "ebcda".to_string()
        );
        assert_eq!(
            Operation::SwapLetters('d', 'b').scramble("ebcda"),
            "edcba".to_string()
        );
        assert_eq!(
            Operation::ReversePositions(0, 4).scramble("edcba"),
            "abcde".to_string()
        );
        assert_eq!(
            Operation::RotateSteps(Direction::Left, 1).scramble("abcde"),
            "bcdea".to_string()
        );
        assert_eq!(
            Operation::MovePositions(1, 4).scramble("bcdea"),
            "bdeac".to_string()
        );
        assert_eq!(
            Operation::MovePositions(3, 0).scramble("bdeac"),
            "abdec".to_string()
        );
        assert_eq!(
            Operation::RotateByLetterPosition('b').scramble("abdec"),
            "ecabd".to_string()
        );
        assert_eq!(
            Operation::RotateByLetterPosition('d').scramble("ecabd"),
            "decab".to_string()
        );
    }

    #[test]
    fn test_scramble_password() {
        assert_eq!(
            scramble_password(
                "abcde",
                vec![
                    Operation::SwapPositions(4, 0),
                    Operation::SwapLetters('d', 'b'),
                    Operation::ReversePositions(0, 4),
                    Operation::RotateSteps(Direction::Left, 1),
                    Operation::MovePositions(1, 4),
                    Operation::MovePositions(3, 0),
                    Operation::RotateByLetterPosition('b'),
                    Operation::RotateByLetterPosition('d'),
                ]
            ),
            "decab"
        );
    }

    #[test]
    fn test_operation_unscramble() {
        assert_eq!(
            Operation::SwapPositions(4, 0).unscramble("ebcda"),
            "abcde".to_string()
        );
        assert_eq!(
            Operation::SwapLetters('d', 'b').unscramble("edcba"),
            "ebcda".to_string()
        );
        assert_eq!(
            Operation::ReversePositions(0, 4).unscramble("abcde"),
            "edcba".to_string()
        );
        assert_eq!(
            Operation::RotateSteps(Direction::Left, 1).unscramble("bcdea"),
            "abcde".to_string()
        );
        assert_eq!(
            Operation::MovePositions(1, 4).unscramble("bdeac"),
            "bcdea".to_string()
        );
        assert_eq!(
            Operation::MovePositions(3, 0).unscramble("abdec"),
            "bdeac".to_string()
        );
        assert_eq!(
            Operation::RotateByLetterPosition('b').unscramble("ecabd"),
            "abdec".to_string()
        );
        assert_eq!(
            Operation::RotateByLetterPosition('d').unscramble("decab"),
            "ecabd".to_string()
        );
    }

    #[test]
    fn test_unscramble_password() {
        assert_eq!(
            unscramble_password(
                "decab",
                vec![
                    Operation::SwapPositions(4, 0),
                    Operation::SwapLetters('d', 'b'),
                    Operation::ReversePositions(0, 4),
                    Operation::RotateSteps(Direction::Left, 1),
                    Operation::MovePositions(1, 4),
                    Operation::MovePositions(3, 0),
                    Operation::RotateByLetterPosition('b'),
                    Operation::RotateByLetterPosition('d'),
                ]
            ),
            "abcde"
        );
    }

    crate::create_solver_test!(year2016, day21, part1);
    crate::create_solver_test!(year2016, day21, part2);
}
