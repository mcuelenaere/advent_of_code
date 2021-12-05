type Register = usize;

#[derive(Debug, Eq, PartialEq)]
pub enum Instruction {
    AddRegister(Register, Register, Register),
    AddImmediate(Register, usize, Register),
    MultiplyRegister(Register, Register, Register),
    MultiplyImmediate(Register, usize, Register),
    BitwiseAndRegister(Register, Register, Register),
    BitwiseAndImmediate(Register, usize, Register),
    BitwiseOrRegister(Register, Register, Register),
    BitwiseOrImmediate(Register, usize, Register),
    SetRegister(Register, Register),
    SetImmediate(usize, Register),
    GreaterThanImmediateRegister(usize, Register, Register),
    GreaterThanRegisterImmediate(Register, usize, Register),
    GreaterThanRegisterRegister(Register, Register, Register),
    EqualImmediateRegister(usize, Register, Register),
    EqualRegisterImmediate(Register, usize, Register),
    EqualRegisterRegister(Register, Register, Register),
}

fn parse_numbers(input: &str) -> (usize, usize, usize) {
    let mut it = input
        .splitn(3, ' ')
        .map(|part| part.parse::<usize>().expect("a number"));

    (
        it.next().expect("an entry"),
        it.next().expect("an entry"),
        it.next().expect("an entry"),
    )
}

pub fn parse_instructions(input: &str) -> (Register, Vec<Instruction>) {
    let mut instruction_pointer_register: Option<Register> = None;

    let instructions = input
        .lines()
        .filter(|line| {
            if let Some(line) = line.strip_prefix("#ip ") {
                instruction_pointer_register = Some(line.parse().expect("a number"));
                false
            } else {
                true
            }
        })
        .map(|line| {
            if let Some(line) = line.strip_prefix("addr ") {
                let (a, b, c) = parse_numbers(line);
                Instruction::AddRegister(a, b, c)
            } else if let Some(line) = line.strip_prefix("addi ") {
                let (a, b, c) = parse_numbers(line);
                Instruction::AddImmediate(a, b, c)
            } else if let Some(line) = line.strip_prefix("mulr ") {
                let (a, b, c) = parse_numbers(line);
                Instruction::MultiplyRegister(a, b, c)
            } else if let Some(line) = line.strip_prefix("muli ") {
                let (a, b, c) = parse_numbers(line);
                Instruction::MultiplyImmediate(a, b, c)
            } else if let Some(line) = line.strip_prefix("banr ") {
                let (a, b, c) = parse_numbers(line);
                Instruction::BitwiseAndRegister(a, b, c)
            } else if let Some(line) = line.strip_prefix("bani ") {
                let (a, b, c) = parse_numbers(line);
                Instruction::BitwiseAndImmediate(a, b, c)
            } else if let Some(line) = line.strip_prefix("borr ") {
                let (a, b, c) = parse_numbers(line);
                Instruction::BitwiseOrRegister(a, b, c)
            } else if let Some(line) = line.strip_prefix("bori ") {
                let (a, b, c) = parse_numbers(line);
                Instruction::BitwiseOrImmediate(a, b, c)
            } else if let Some(line) = line.strip_prefix("setr ") {
                let (a, _, c) = parse_numbers(line);
                Instruction::SetRegister(a, c)
            } else if let Some(line) = line.strip_prefix("seti ") {
                let (a, _, c) = parse_numbers(line);
                Instruction::SetImmediate(a, c)
            } else if let Some(line) = line.strip_prefix("gtir ") {
                let (a, b, c) = parse_numbers(line);
                Instruction::GreaterThanImmediateRegister(a, b, c)
            } else if let Some(line) = line.strip_prefix("gtri ") {
                let (a, b, c) = parse_numbers(line);
                Instruction::GreaterThanRegisterImmediate(a, b, c)
            } else if let Some(line) = line.strip_prefix("gtrr ") {
                let (a, b, c) = parse_numbers(line);
                Instruction::GreaterThanRegisterRegister(a, b, c)
            } else if let Some(line) = line.strip_prefix("eqir ") {
                let (a, b, c) = parse_numbers(line);
                Instruction::EqualImmediateRegister(a, b, c)
            } else if let Some(line) = line.strip_prefix("eqri ") {
                let (a, b, c) = parse_numbers(line);
                Instruction::EqualRegisterImmediate(a, b, c)
            } else if let Some(line) = line.strip_prefix("eqrr ") {
                let (a, b, c) = parse_numbers(line);
                Instruction::EqualRegisterRegister(a, b, c)
            } else {
                panic!("Invalid instruction: {}", line);
            }
        })
        .collect();

    (
        instruction_pointer_register.expect("an instruction pointer register"),
        instructions,
    )
}

#[derive(Debug)]
pub struct Cpu {
    pub registers: [usize; 6],
    pub instruction_pointer_register: Register,
}

impl Cpu {
    pub fn new(instruction_pointer_register: Register) -> Self {
        Self {
            registers: [0; 6],
            instruction_pointer_register,
        }
    }

    pub fn instruction_pointer(&self) -> usize {
        self.registers[self.instruction_pointer_register]
    }

    pub fn execute_instruction(&mut self, instruction: &Instruction) {
        match instruction {
            Instruction::AddRegister(a, b, c) => {
                self.registers[*c] = self.registers[*a] + self.registers[*b];
            }
            Instruction::AddImmediate(a, b, c) => {
                self.registers[*c] = self.registers[*a] + b;
            }
            Instruction::MultiplyRegister(a, b, c) => {
                self.registers[*c] = self.registers[*a] * self.registers[*b];
            }
            Instruction::MultiplyImmediate(a, b, c) => {
                self.registers[*c] = self.registers[*a] * b;
            }
            Instruction::BitwiseAndRegister(a, b, c) => {
                self.registers[*c] = self.registers[*a] & self.registers[*b];
            }
            Instruction::BitwiseAndImmediate(a, b, c) => {
                self.registers[*c] = self.registers[*a] & b;
            }
            Instruction::BitwiseOrRegister(a, b, c) => {
                self.registers[*c] = self.registers[*a] | self.registers[*b];
            }
            Instruction::BitwiseOrImmediate(a, b, c) => {
                self.registers[*c] = self.registers[*a] | b;
            }
            Instruction::SetRegister(a, c) => {
                self.registers[*c] = self.registers[*a];
            }
            Instruction::SetImmediate(a, c) => {
                self.registers[*c] = *a;
            }
            Instruction::GreaterThanRegisterImmediate(a, b, c) => {
                self.registers[*c] = if self.registers[*a] > *b { 1 } else { 0 };
            }
            Instruction::GreaterThanImmediateRegister(a, b, c) => {
                self.registers[*c] = if *a > self.registers[*b] { 1 } else { 0 };
            }
            Instruction::GreaterThanRegisterRegister(a, b, c) => {
                self.registers[*c] = if self.registers[*a] > self.registers[*b] {
                    1
                } else {
                    0
                };
            }
            Instruction::EqualRegisterImmediate(a, b, c) => {
                self.registers[*c] = if self.registers[*a] == *b { 1 } else { 0 };
            }
            Instruction::EqualImmediateRegister(a, b, c) => {
                self.registers[*c] = if *a == self.registers[*b] { 1 } else { 0 };
            }
            Instruction::EqualRegisterRegister(a, b, c) => {
                self.registers[*c] = if self.registers[*a] == self.registers[*b] {
                    1
                } else {
                    0
                };
            }
        }

        self.registers[self.instruction_pointer_register] += 1;
    }
}

fn check_for_optimization(cpu: &mut Cpu, instructions: &[Instruction]) -> bool {
    if instructions.len() < 9 {
        return false;
    }

    /*
        mulr 3 5 2
        eqrr 2 4 2
        addr 2 IP IP
        addi IP 1 IP
        addr 3 0 0
        addi 5 1 5
        gtrr 5 4 2
        addr IP 2 IP
        seti 2 6 IP
    =>
        for (; r[5] <= r[4]; r[5] += 1) {
            r[2] = r[3] * r[5];
            if (r[2] == r[4]) {
                r[0] += r[3];
            }
        }

    =>
        if (r[4] % r[3] == 0) {
            r[0] += r[3];
        }
        r[2] = 1;
        r[5] = r[4] + 1;
     */
    if Instruction::MultiplyRegister(3, 5, 2) == instructions[0]
        && Instruction::EqualRegisterRegister(2, 4, 2) == instructions[1]
        && Instruction::AddRegister(
            2,
            cpu.instruction_pointer_register,
            cpu.instruction_pointer_register,
        ) == instructions[2]
        && Instruction::AddImmediate(
            cpu.instruction_pointer_register,
            1,
            cpu.instruction_pointer_register,
        ) == instructions[3]
        && Instruction::AddRegister(3, 0, 0) == instructions[4]
        && Instruction::AddImmediate(5, 1, 5) == instructions[5]
        && Instruction::GreaterThanRegisterRegister(5, 4, 2) == instructions[6]
        && Instruction::AddRegister(
            cpu.instruction_pointer_register,
            2,
            cpu.instruction_pointer_register,
        ) == instructions[7]
        && Instruction::SetImmediate(2, cpu.instruction_pointer_register) == instructions[8]
    {
        if cpu.registers[4] % cpu.registers[3] == 0 {
            cpu.registers[0] += cpu.registers[3];
        }
        cpu.registers[2] = 1;
        cpu.registers[5] = cpu.registers[4] + 1;
        cpu.registers[cpu.instruction_pointer_register] += 9;

        return true;
    }

    false
}

fn execute_program(mut cpu: &mut Cpu, instructions: &[Instruction]) {
    while cpu.instruction_pointer() < instructions.len() {
        let ip = cpu.instruction_pointer();
        if check_for_optimization(&mut cpu, &instructions[ip..]) {
            continue;
        }

        cpu.execute_instruction(&instructions[ip]);
    }
}

pub fn solve_part1(input: &str) -> usize {
    let (instruction_pointer_register, instructions) = parse_instructions(input);
    let mut cpu = Cpu::new(instruction_pointer_register);
    execute_program(&mut cpu, &instructions);

    cpu.registers[0]
}

pub fn solve_part2(input: &str) -> usize {
    let (instruction_pointer_register, instructions) = parse_instructions(input);
    let mut cpu = Cpu::new(instruction_pointer_register);
    cpu.registers[0] = 1;
    execute_program(&mut cpu, &instructions);

    cpu.registers[0]
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let input = r#"#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5"#;
        assert_eq!(solve_part1(input), 7);
    }

    crate::create_solver_test!(year2018, day19, part1, verify_answer = true);
    crate::create_solver_test!(year2018, day19, part2, verify_answer = true);
}
