use lazy_static::lazy_static;
use regex::Regex;
use std::collections::HashMap;

type BotNumber = usize;
type OutputNumber = usize;
type ChipValue = usize;

#[derive(PartialEq, Eq, Hash, Debug, Clone)]
enum Receiver {
    Bot(BotNumber),
    Output(OutputNumber),
}

#[derive(PartialEq, Eq, Hash, Debug)]
enum Instruction {
    ReceiveValue {
        receiving_bot: BotNumber,
        value: ChipValue,
    },
    RedistributeValue {
        giving_bot: BotNumber,
        low_receiver: Receiver,
        high_receiver: Receiver,
    },
}

lazy_static! {
    static ref RE_RECEIVE_VALUE: Regex = Regex::new(r"value (\d+) goes to bot (\d+)").unwrap();
    static ref RE_REDISTRIBUTE_VALUE: Regex =
        Regex::new(r"bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)")
            .unwrap();
}

fn parse_receiver(captures: &regex::Captures, offset: usize) -> Receiver {
    let number: usize = captures[offset + 1].parse().unwrap();
    match &captures[offset] {
        "bot" => Receiver::Bot(number),
        "output" => Receiver::Output(number),
        _ => panic!("invalid receiver"),
    }
}

fn parse_instructions(instructions: &str) -> impl Iterator<Item = Instruction> + '_ {
    instructions.lines().filter_map(|line| {
        if let Some(m) = RE_RECEIVE_VALUE.captures(line) {
            Some(Instruction::ReceiveValue {
                receiving_bot: m[2].parse().unwrap(),
                value: m[1].parse().unwrap(),
            })
        } else if let Some(m) = RE_REDISTRIBUTE_VALUE.captures(line) {
            Some(Instruction::RedistributeValue {
                giving_bot: m[1].parse().unwrap(),
                low_receiver: parse_receiver(&m, 2),
                high_receiver: parse_receiver(&m, 4),
            })
        } else {
            None
        }
    })
}

fn _solve(input: &str, to_find: (ChipValue, ChipValue)) -> (BotNumber, ChipValue) {
    let mut receivers: HashMap<Receiver, Vec<ChipValue>> = HashMap::new();
    let mut rules: HashMap<BotNumber, (Receiver, Receiver)> = HashMap::new();

    for instruction in parse_instructions(input) {
        match instruction {
            Instruction::ReceiveValue {
                receiving_bot,
                value,
            } => {
                receivers
                    .entry(Receiver::Bot(receiving_bot))
                    .or_default()
                    .push(value);
            }
            Instruction::RedistributeValue {
                giving_bot,
                low_receiver,
                high_receiver,
            } => {
                rules.insert(giving_bot, (low_receiver, high_receiver));
            }
        }
    }

    let mut part1_result: Option<BotNumber> = None;
    loop {
        // find bot with 2 values
        let res = receivers
            .iter()
            .filter(|entry| matches!(entry.0, Receiver::Bot(_)))
            .find(|entry| entry.1.len() == 2);
        let (giving_bot, values) = match res {
            Some((Receiver::Bot(giving_bot), values)) => (giving_bot, values),
            _ => break,
        };

        let (low_receiver, high_receiver) = rules.get(giving_bot).unwrap().clone();
        let lowest_value = *values.iter().min().unwrap();
        let highest_value = *values.iter().max().unwrap();

        if (highest_value, lowest_value) == to_find {
            part1_result = Some(*giving_bot);
        }

        // take values from giver
        let giver = Receiver::Bot(*giving_bot);
        receivers.get_mut(&giver).unwrap().clear();

        // add values to receivers
        receivers
            .entry(low_receiver)
            .or_default()
            .push(lowest_value);
        receivers
            .entry(high_receiver)
            .or_default()
            .push(highest_value);
    }
    let part2_result = receivers.get(&Receiver::Output(0)).unwrap()[0]
        * receivers.get(&Receiver::Output(1)).unwrap()[0]
        * receivers.get(&Receiver::Output(2)).unwrap()[0];

    (part1_result.unwrap(), part2_result)
}

pub fn solve_part1(input: &str) -> BotNumber {
    _solve(input, (61, 17)).0
}

pub fn solve_part2(input: &str) -> ChipValue {
    _solve(input, (61, 17)).1
}

#[cfg(test)]
mod tests {
    #[test]
    fn testcase1() {
        let puzzle = r#"value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2"#;
        let result = super::_solve(puzzle, (5, 2));
        assert_eq!(result.0, 2);
        assert_eq!(result.1, 30);
    }

    crate::create_solver_test!(year2016, day10, part1);
    crate::create_solver_test!(year2016, day10, part2);
}
