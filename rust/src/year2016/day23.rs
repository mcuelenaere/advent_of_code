use crate::year2016::day12::{parse_register_or_value, Register, RegisterOrValue, Registers};

#[derive(Debug, Clone)]
pub(crate) enum Instruction {
    Increment(RegisterOrValue),
    Decrement(RegisterOrValue),
    Copy {
        src: RegisterOrValue,
        dest: RegisterOrValue,
    },
    Jump {
        condition: RegisterOrValue,
        offset: RegisterOrValue,
    },
    Toggle(RegisterOrValue),
}

pub(crate) fn parse_instruction(line: &str) -> Instruction {
    if let Some(stripped) = line.strip_prefix("tgl ") {
        Instruction::Toggle(parse_register_or_value(stripped))
    } else if let Some(stripped) = line.strip_prefix("cpy ") {
        let mut m = stripped.splitn(2, ' ');
        Instruction::Copy {
            src: parse_register_or_value(m.next().expect("have first value")),
            dest: parse_register_or_value(m.next().expect("have second value")),
        }
    } else if let Some(stripped) = line.strip_prefix("inc ") {
        Instruction::Increment(parse_register_or_value(stripped))
    } else if let Some(stripped) = line.strip_prefix("dec ") {
        Instruction::Decrement(parse_register_or_value(stripped))
    } else if let Some(stripped) = line.strip_prefix("jnz ") {
        let mut m = stripped.splitn(2, ' ');
        Instruction::Jump {
            condition: parse_register_or_value(m.next().expect("have first value")),
            offset: parse_register_or_value(m.next().expect("have second value")),
        }
    } else {
        panic!("unknown line");
    }
}

fn parse_instructions(input: &str) -> impl Iterator<Item = Instruction> + '_ {
    input.lines().map(parse_instruction)
}

#[derive(Debug)]
pub(crate) struct Cpu {
    pub(crate) registers: Registers,
    pub(crate) program_counter: usize,
    instructions: Vec<Instruction>,
}

impl Cpu {
    pub fn new(instructions: Vec<Instruction>) -> Self {
        Self {
            registers: Registers::default(),
            program_counter: 0,
            instructions,
        }
    }

    pub fn execute_program(&mut self) {
        while self.program_counter < self.instructions.len() {
            self.check_for_optimisation();
            self.execute_instruction(self.instructions[self.program_counter].clone());
        }
    }

    fn check_for_optimisation(&mut self) {
        // try to detect the following instructions:
        //   copy B C
        //   inc A
        //   dec C
        //   jnz C -2
        //   dec D
        //   jnz D -5
        //
        // which roughly translates to this:
        //   for (; d != 0; d--) {
        //     c = b;
        //     for (; c != 0; c--) {
        //       a++;
        //     }
        //   }
        //
        // which can be simplified to this:
        //   a += b * d;
        //   c = 0;
        //   d = 0;

        let instructions = &self.instructions[self.program_counter..];
        if instructions.len() < 6 {
            return;
        }

        if let Instruction::Copy {
            src: RegisterOrValue::Right(Register::B),
            dest: RegisterOrValue::Right(Register::C),
        } = instructions[0]
        {
            if let Instruction::Increment(RegisterOrValue::Right(Register::A)) = instructions[1] {
                if let Instruction::Decrement(RegisterOrValue::Right(Register::C)) = instructions[2]
                {
                    if let Instruction::Jump {
                        condition: RegisterOrValue::Right(Register::C),
                        offset: RegisterOrValue::Left(-2),
                    } = instructions[3]
                    {
                        if let Instruction::Decrement(RegisterOrValue::Right(Register::D)) =
                            instructions[4]
                        {
                            if let Instruction::Jump {
                                condition: RegisterOrValue::Right(Register::D),
                                offset: RegisterOrValue::Left(-5),
                            } = instructions[5]
                            {
                                // optimisation is possible!
                                self.registers[Register::A] +=
                                    self.registers[Register::B] * self.registers[Register::D];
                                self.registers[Register::C] = 0;
                                self.registers[Register::D] = 0;
                                self.program_counter += 6;
                            }
                        }
                    }
                }
            }
        }
    }

    pub fn execute_instruction(&mut self, instruction: Instruction) {
        match instruction {
            Instruction::Copy { src, dest } => {
                if let RegisterOrValue::Right(dest) = dest {
                    self.registers[dest] = match src {
                        RegisterOrValue::Left(value) => value,
                        RegisterOrValue::Right(register) => self.registers[register],
                    };
                }
                self.program_counter += 1;
            }
            Instruction::Increment(register) => {
                if let RegisterOrValue::Right(register) = register {
                    self.registers[register] += 1;
                }
                self.program_counter += 1;
            }
            Instruction::Decrement(register) => {
                if let RegisterOrValue::Right(register) = register {
                    self.registers[register] -= 1;
                }
                self.program_counter += 1;
            }
            Instruction::Jump { offset, condition } => {
                let offset = match offset {
                    RegisterOrValue::Left(number) => number,
                    RegisterOrValue::Right(register) => self.registers[register],
                };
                let condition = match condition {
                    RegisterOrValue::Left(number) => number,
                    RegisterOrValue::Right(register) => self.registers[register],
                };
                if condition != 0 {
                    self.program_counter = (self.program_counter as isize + offset) as usize;
                } else {
                    self.program_counter += 1;
                }
            }
            Instruction::Toggle(x) => {
                let x = match x {
                    RegisterOrValue::Left(value) => value,
                    RegisterOrValue::Right(register) => self.registers[register],
                };
                let index = {
                    let index = self.program_counter as isize + x;
                    if index < 0 || index as usize >= self.instructions.len() {
                        self.program_counter += 1;
                        return;
                    }
                    index as usize
                };

                self.instructions[index] = match self.instructions[index] {
                    Instruction::Increment(register) => Instruction::Decrement(register),
                    Instruction::Decrement(register) => Instruction::Increment(register),
                    Instruction::Jump { condition, offset } => Instruction::Copy {
                        src: condition,
                        dest: offset,
                    },
                    Instruction::Copy { src, dest } => Instruction::Jump {
                        condition: src,
                        offset: dest,
                    },
                    Instruction::Toggle(x) => Instruction::Increment(x),
                };
                self.program_counter += 1;
            }
        }
    }
}

pub fn solve_part1(input: &str) -> isize {
    let mut cpu = Cpu::new(parse_instructions(input).collect());
    cpu.registers[Register::A] = 7;
    cpu.execute_program();

    cpu.registers[Register::A]
}

pub fn solve_part2(input: &str) -> isize {
    let mut cpu = Cpu::new(parse_instructions(input).collect());
    cpu.registers[Register::A] = 12;
    cpu.execute_program();

    cpu.registers[Register::A]
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_execute_program() {
        let instructions = r#"cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a"#;
        let mut cpu = Cpu::new(parse_instructions(instructions).collect());
        cpu.execute_program();
        assert_eq!(cpu.registers[Register::A], 3);
    }

    crate::create_solver_test!(year2016, day23, part1, verify_answer = true);
    crate::create_solver_test!(year2016, day23, part2, verify_answer = true);
}
