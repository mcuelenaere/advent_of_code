use itertools::Either;
use std::ops::{Index, IndexMut};

#[derive(Debug, Copy, Clone)]
enum Register {
    A,
    B,
    C,
    D,
}

impl TryFrom<&str> for Register {
    type Error = ();

    fn try_from(value: &str) -> Result<Self, Self::Error> {
        match value.chars().next().map(|c| c.to_ascii_lowercase()) {
            Some('a') => Ok(Self::A),
            Some('b') => Ok(Self::B),
            Some('c') => Ok(Self::C),
            Some('d') => Ok(Self::D),
            _ => Err(()),
        }
    }
}

type RegisterOrValue = Either<isize, Register>;

#[derive(Debug)]
enum Instruction {
    Copy {
        src: RegisterOrValue,
        dest: Register,
    },
    Increment(Register),
    Decrement(Register),
    Jump {
        condition: RegisterOrValue,
        offset: isize,
    },
}

fn parse_register_or_value(input: &str) -> RegisterOrValue {
    if let Ok(number) = input.parse::<isize>() {
        Either::Left(number)
    } else {
        Either::Right(Register::try_from(input).expect("valid register"))
    }
}

fn parse_instructions(input: &str) -> impl Iterator<Item = Instruction> + '_ {
    input.lines().map(|line| {
        if let Some(stripped) = line.strip_prefix("cpy ") {
            let mut m = stripped.splitn(2, ' ');
            Instruction::Copy {
                src: parse_register_or_value(m.next().expect("have first value")),
                dest: Register::try_from(m.next().expect("have second value"))
                    .expect("valid register"),
            }
        } else if let Some(stripped) = line.strip_prefix("inc ") {
            Instruction::Increment(Register::try_from(stripped).expect("valid register"))
        } else if let Some(stripped) = line.strip_prefix("dec ") {
            Instruction::Decrement(Register::try_from(stripped).expect("valid register"))
        } else if let Some(stripped) = line.strip_prefix("jnz ") {
            let mut m = stripped.splitn(2, ' ');
            Instruction::Jump {
                condition: parse_register_or_value(m.next().expect("have first value")),
                offset: m
                    .next()
                    .expect("have second value")
                    .parse()
                    .expect("valid number"),
            }
        } else {
            panic!("unknown line");
        }
    })
}

#[derive(Debug, Default)]
struct Registers(isize, isize, isize, isize);

impl Index<Register> for Registers {
    type Output = isize;

    fn index(&self, index: Register) -> &Self::Output {
        match index {
            Register::A => &self.0,
            Register::B => &self.1,
            Register::C => &self.2,
            Register::D => &self.3,
        }
    }
}

impl IndexMut<Register> for Registers {
    fn index_mut(&mut self, index: Register) -> &mut Self::Output {
        match index {
            Register::A => &mut self.0,
            Register::B => &mut self.1,
            Register::C => &mut self.2,
            Register::D => &mut self.3,
        }
    }
}

#[derive(Debug, Default)]
struct Cpu {
    pub registers: Registers,
    pub program_counter: usize,
}

impl Cpu {
    pub fn execute_program(&mut self, instructions: &Vec<Instruction>) {
        while self.program_counter < instructions.len() {
            let instruction = &instructions[self.program_counter];
            self.execute_instruction(instruction);
        }
    }

    pub fn execute_instruction(&mut self, instruction: &Instruction) {
        match instruction {
            Instruction::Copy { src, dest } => {
                self.registers[*dest] = match *src {
                    Either::Left(value) => value,
                    Either::Right(register) => self.registers[register],
                };
                self.program_counter += 1;
            }
            Instruction::Increment(register) => {
                self.registers[*register] += 1;
                self.program_counter += 1;
            }
            Instruction::Decrement(register) => {
                self.registers[*register] -= 1;
                self.program_counter += 1;
            }
            Instruction::Jump { offset, condition } => {
                let condition = match *condition {
                    Either::Left(number) => number,
                    Either::Right(register) => self.registers[register],
                };
                if condition != 0 {
                    self.program_counter = (self.program_counter as isize + *offset) as usize;
                } else {
                    self.program_counter += 1;
                }
            }
        }
    }
}

pub fn solve_part1(input: &str) -> isize {
    let instructions: Vec<_> = parse_instructions(input).collect();
    let mut cpu = Cpu::default();
    cpu.execute_program(&instructions);
    cpu.registers[Register::A]
}

pub fn solve_part2(input: &str) -> isize {
    let instructions: Vec<_> = parse_instructions(input).collect();
    let mut cpu = Cpu::default();
    cpu.registers[Register::C] = 1;
    cpu.execute_program(&instructions);
    cpu.registers[Register::A]
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let input = r#"cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a"#;
        assert_eq!(solve_part1(input), 42);
    }

    crate::create_solver_test!(year2016, day12, part1, verify_answer = true);
    crate::create_solver_test!(year2016, day12, part2, verify_answer = true);
}
