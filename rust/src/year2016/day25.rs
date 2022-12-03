use crate::year2016::day12::{parse_register_or_value, Register, RegisterOrValue};
use crate::year2016::day23::{
    parse_instruction as parse_old_instruction, Cpu, Instruction as OldInstruction,
};

#[derive(Debug, Clone)]
enum Instruction {
    OldInstruction(OldInstruction),
    Out(RegisterOrValue),
}

fn parse_instructions(input: &str) -> impl Iterator<Item = Instruction> + '_ {
    input.lines().map(|line| {
        if let Some(stripped) = line.strip_prefix("out ") {
            Instruction::Out(parse_register_or_value(stripped))
        } else {
            Instruction::OldInstruction(parse_old_instruction(line))
        }
    })
}

struct SignalGenerator {
    cpu: Cpu,
    instructions: Vec<Instruction>,
}

impl SignalGenerator {
    pub fn new(instructions: Vec<Instruction>, value: isize) -> Self {
        let mut s = Self {
            cpu: Cpu::new(vec![]),
            instructions,
        };
        s.cpu.registers[Register::A] = value;
        s
    }

    fn execute_instruction(&mut self, instruction: Instruction) -> Option<isize> {
        match instruction {
            Instruction::OldInstruction(old_instruction) => {
                self.cpu.execute_instruction(old_instruction);
                None
            }
            Instruction::Out(x) => {
                let x = match x {
                    RegisterOrValue::Left(number) => number,
                    RegisterOrValue::Right(register) => self.cpu.registers[register],
                };
                self.cpu.program_counter += 1;
                Some(x)
            }
        }
    }
}

impl Iterator for SignalGenerator {
    type Item = isize;

    fn next(&mut self) -> Option<Self::Item> {
        loop {
            if self.cpu.program_counter >= self.instructions.len() {
                break None;
            }

            if let Some(signal) =
                self.execute_instruction(self.instructions[self.cpu.program_counter].clone())
            {
                break Some(signal);
            }
        }
    }
}

pub fn solve_part1(input: &str) -> usize {
    let instructions: Vec<_> = parse_instructions(input).collect();
    for value in 0_usize.. {
        let signal_generator = SignalGenerator::new(instructions.clone(), value as isize);
        let found = signal_generator
            .into_iter()
            .take(100)
            .enumerate()
            .all(|(index, signal)| (index as isize) % 2 == signal);
        if found {
            return value;
        }
    }

    unreachable!();
}

pub fn solve_part2(_: &str) -> String {
    unimplemented!();
}

#[cfg(test)]
mod tests {
    crate::create_solver_test!(year2016, day25, part1);
}
