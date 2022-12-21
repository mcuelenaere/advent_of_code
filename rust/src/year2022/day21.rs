use itertools::Itertools;
use std::collections::HashMap;

#[derive(Clone, Copy, PartialEq, Eq)]
enum Operator {
    Add,
    Subtract,
    Multiply,
    Divide,
}

impl Operator {
    pub fn evaluate(&self, left: isize, right: isize) -> isize {
        match self {
            Self::Add => left + right,
            Self::Subtract => left - right,
            Self::Multiply => left * right,
            Self::Divide => left / right,
        }
    }

    pub fn inverse(&self) -> Self {
        match self {
            Self::Add => Self::Subtract,
            Self::Subtract => Self::Add,
            Self::Multiply => Self::Divide,
            Self::Divide => Self::Multiply,
        }
    }
}

enum Monkey<'a> {
    FixedNumber(isize),
    Operation {
        left: &'a str,
        right: &'a str,
        operator: Operator,
    },
    Unknown,
}

type Monkeys<'a> = HashMap<&'a str, Monkey<'a>>;

fn parse_monkeys(text: &str) -> Monkeys<'_> {
    text.lines()
        .map(|line| {
            let (name, job) = line.split_once(": ").unwrap();
            let monkey = if job.contains(' ') {
                let (left, operator, right) = job.splitn(3, ' ').collect_tuple().unwrap();
                let operator = match operator {
                    "+" => Operator::Add,
                    "-" => Operator::Subtract,
                    "*" => Operator::Multiply,
                    "/" => Operator::Divide,
                    _ => panic!("invalid operator"),
                };
                Monkey::Operation {
                    left,
                    right,
                    operator,
                }
            } else {
                Monkey::FixedNumber(job.parse().expect("valid number"))
            };
            (name, monkey)
        })
        .collect()
}

fn evaluate(monkeys: &Monkeys<'_>, name: &str) -> Option<isize> {
    match monkeys.get(name)? {
        Monkey::FixedNumber(number) => Some(*number),
        Monkey::Operation {
            left,
            right,
            operator,
        } => Some(operator.evaluate(evaluate(monkeys, left)?, evaluate(monkeys, right)?)),
        Monkey::Unknown => None,
    }
}

pub fn solve_part1(input: &str) -> isize {
    let monkeys = parse_monkeys(input);
    evaluate(&monkeys, "root").unwrap()
}

pub fn solve_part2(input: &str) -> isize {
    let mut monkeys = parse_monkeys(input);
    monkeys.insert("humn", Monkey::Unknown);

    let (expected_result, to_be_calculated) = match monkeys.get("root") {
        Some(Monkey::Operation { left, right, .. }) => {
            match (evaluate(&monkeys, left), evaluate(&monkeys, right)) {
                (Some(result), None) => (result, *right),
                (None, Some(result)) => (result, *left),
                _ => panic!("invalid state"),
            }
        }
        _ => panic!("invalid root monkey"),
    };

    let mut unknown = expected_result;
    let mut current = to_be_calculated;
    loop {
        match monkeys.get(current).unwrap() {
            Monkey::Unknown => break,
            Monkey::Operation {
                left,
                right,
                operator,
            } => {
                match (evaluate(&monkeys, left), evaluate(&monkeys, right)) {
                    (Some(constant), None) if *operator == Operator::Subtract => {
                        // unk = const - x <=> -(unk - const) = x
                        unknown = -(unknown - constant);
                        current = *right;
                    }
                    (Some(constant), None) if *operator == Operator::Divide => {
                        // unk = const / x <=> const / unk = x
                        unknown = constant / unknown;
                        current = *right;
                    }
                    (Some(constant), None)
                        if *operator == Operator::Add || *operator == Operator::Multiply =>
                    {
                        // unk = const + x <=> unk - const = x
                        // unk = const * x <=> unk / const = x
                        unknown = operator.inverse().evaluate(unknown, constant);
                        current = *right;
                    }
                    (None, Some(constant)) => {
                        // unk = x + const <=> unk - const = x
                        // unk = x - const <=> unk + const = x
                        // unk = x * const <=> unk / const = x
                        // unk = x / const <=> unk * const = x
                        unknown = operator.inverse().evaluate(unknown, constant);
                        current = *left;
                    }
                    _ => panic!("invalid state"),
                };
            }
            _ => panic!("did not expect fixed-number monkey"),
        }
    }

    // sanity check
    monkeys.insert("humn", Monkey::FixedNumber(unknown));
    assert_eq!(evaluate(&monkeys, to_be_calculated), Some(expected_result));

    unknown
}

#[cfg(test)]
mod tests {
    use super::*;

    static TEST_INPUT: &str = r#"root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"#;

    #[test]
    fn test_part1() {
        assert_eq!(solve_part1(TEST_INPUT), 152);
    }

    #[test]
    fn test_part2() {
        assert_eq!(solve_part2(TEST_INPUT), 301);
    }

    crate::create_solver_test!(part1);
    crate::create_solver_test!(part2);
}
