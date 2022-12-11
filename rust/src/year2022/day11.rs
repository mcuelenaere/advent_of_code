use itertools::Itertools;

type Item = usize;
type MonkeyId = usize;

#[derive(Debug, Clone, Copy)]
enum Operation {
    OldPlusValue(usize),
    OldMultipliedWithValue(usize),
    OldSquared,
}

impl Operation {
    pub fn evaluate(&self, old: usize) -> usize {
        match self {
            Self::OldPlusValue(value) => old + *value,
            Self::OldMultipliedWithValue(value) => old * *value,
            Self::OldSquared => old * old,
        }
    }
}

#[derive(Debug, Clone)]
struct Monkey {
    items: Vec<Item>,
    operation: Operation,
    test_divisor: usize,
    next_monkey_id_if_test_is_true: MonkeyId,
    next_monkey_id_if_test_is_false: MonkeyId,
}

fn parse_notes(notes: &str) -> impl Iterator<Item = (MonkeyId, Monkey)> + '_ {
    notes.lines().batching(|lines| {
        let id = match lines.next() {
            Some(line) if line.starts_with("Monkey ") => line
                .strip_prefix("Monkey ")
                .unwrap()
                .strip_suffix(':')
                .unwrap()
                .parse()
                .expect("valid number"),
            Some(_) => panic!("invalid monkey line"),
            None => return None,
        };

        let items = match lines.next() {
            Some(line) if line.starts_with("  Starting items: ") => line
                .strip_prefix("  Starting items: ")
                .unwrap()
                .split(", ")
                .map(|item| item.parse().expect("valid number"))
                .collect_vec(),
            _ => panic!("invalid starting items line"),
        };

        let operation = match lines.next() {
            Some(line) if line.starts_with("  Operation: new = old + ") => Operation::OldPlusValue(
                line.strip_prefix("  Operation: new = old + ")
                    .unwrap()
                    .parse()
                    .expect("valid number"),
            ),
            Some(line) if line == "  Operation: new = old * old" => Operation::OldSquared,
            Some(line) if line.starts_with("  Operation: new = old * ") => {
                Operation::OldMultipliedWithValue(
                    line.strip_prefix("  Operation: new = old * ")
                        .unwrap()
                        .parse()
                        .expect("valid number"),
                )
            }
            _ => panic!("invalid operation line"),
        };

        let test_divisor = match lines.next() {
            Some(line) if line.starts_with("  Test: divisible by ") => line
                .strip_prefix("  Test: divisible by ")
                .unwrap()
                .parse()
                .expect("valid number"),
            _ => panic!("invalid test divisor line"),
        };

        let next_monkey_id_if_test_is_true = match lines.next() {
            Some(line) if line.starts_with("    If true: throw to monkey ") => line
                .strip_prefix("    If true: throw to monkey ")
                .unwrap()
                .parse()
                .expect("valid number"),
            _ => panic!("invalid next monkey if test is true line"),
        };

        let next_monkey_id_if_test_is_false = match lines.next() {
            Some(line) if line.starts_with("    If false: throw to monkey ") => line
                .strip_prefix("    If false: throw to monkey ")
                .unwrap()
                .parse()
                .expect("valid number"),
            _ => panic!("invalid next monkey if test is true line"),
        };

        match lines.next() {
            Some("") | None => {}
            _ => panic!("expected empty line separator"),
        };

        Some((
            id,
            Monkey {
                items,
                operation,
                test_divisor,
                next_monkey_id_if_test_is_true,
                next_monkey_id_if_test_is_false,
            },
        ))
    })
}

fn solve<const ROUNDS: usize, const DIVIDE_BY_THREE: bool>(input: &str) -> usize {
    let mut monkeys = parse_notes(input)
        .sorted_by_key(|(id, _)| *id)
        .map(|(_, monkey)| monkey)
        .collect_vec();
    let mut monkey_inspections = vec![0usize; monkeys.len()];

    let test_divisor_lcm = monkeys
        .iter()
        .map(|monkey| monkey.test_divisor)
        .reduce(num::integer::lcm)
        .unwrap();

    for _ in 1..=ROUNDS {
        for monkey_id in 0..monkeys.len() {
            let monkey = monkeys[monkey_id].clone();
            for mut worry_level in monkey.items.into_iter() {
                worry_level = monkey.operation.evaluate(worry_level);
                if DIVIDE_BY_THREE {
                    worry_level /= 3;
                } else {
                    worry_level %= test_divisor_lcm;
                }

                let new_monkey_id = if worry_level % monkey.test_divisor == 0 {
                    monkey.next_monkey_id_if_test_is_true
                } else {
                    monkey.next_monkey_id_if_test_is_false
                };

                monkeys[new_monkey_id].items.push(worry_level);
                monkey_inspections[monkey_id] += 1;
            }
            monkeys[monkey_id].items.clear();
        }
    }

    monkey_inspections
        .into_iter()
        .sorted()
        .rev()
        .take(2)
        .reduce(|a, b| a * b)
        .unwrap()
}

pub fn solve_part1(input: &str) -> usize {
    solve::<20, true>(input)
}

pub fn solve_part2(input: &str) -> usize {
    solve::<10000, false>(input)
}

#[cfg(test)]
mod tests {
    use super::*;

    static TEST_INPUT: &str = r#"Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"#;

    #[test]
    fn test_part1() {
        assert_eq!(solve_part1(TEST_INPUT), 10605);
    }

    #[test]
    fn test_part2() {
        assert_eq!(solve_part2(TEST_INPUT), 2713310158);
    }

    crate::create_solver_test!(part1);
    crate::create_solver_test!(part2);
}
