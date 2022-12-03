use crate::year2018::day19::{parse_instructions, Cpu, Instruction};
use std::collections::HashSet;

pub fn solve_part1(input: &str) -> usize {
    let (ip_register, instructions) = parse_instructions(input);
    let mut cpu = Cpu::new(ip_register);

    while cpu.instruction_pointer() < instructions.len() {
        let instruction = &instructions[cpu.instruction_pointer()];
        if let Instruction::EqualRegisterRegister(a, b, _) = instruction {
            // There is a single eqrr in the instruction list, which compares a certain register to our input
            // register (=register 0). When the result of that comparison is 1, the program ends. So just
            // returning whatever value is in that other register, is the puzzle's answer.
            return cpu.registers[if *a != 0 { *a } else { *b }];
        }

        cpu.execute_instruction(instruction);
    }

    unreachable!();
}

fn check_for_optimization(cpu: &mut Cpu, instructions: &[Instruction]) -> bool {
    if instructions.len() < 9 {
        return false;
    }

    /*
        seti 0 0 2
        addi 2 1 5
        muli 5 256 5
        gtrr 5 3 5
        addr 5 IP IP
        addi IP 1 IP
        seti 25 6 IP
        addi 2 1 2
        seti 17 8 IP
    =>
        #17 r2 = 0;
        #18 r5 = r2 + 1;
        #19 r5 = r5 * 256;
        #20 r5 = r5 > r3 ? 1 : 0;
        #21 ip += r5;
        #22 ip += 1;
        #23 ip = 25;
        #24 r2 += 1;
        #25 ip = 17;
    =>
        for (r2 = 0; ; r2++) {
            if (r2 + 1) * 256 > r3 {
                break;
            }
        }
     */
    if Instruction::SetImmediate(0, 2) == instructions[0]
        && Instruction::AddImmediate(2, 1, 5) == instructions[1]
        && Instruction::MultiplyImmediate(5, 256, 5) == instructions[2]
        && Instruction::GreaterThanRegisterRegister(5, 3, 5) == instructions[3]
        && Instruction::AddRegister(
            5,
            cpu.instruction_pointer_register,
            cpu.instruction_pointer_register,
        ) == instructions[4]
        && Instruction::AddImmediate(
            cpu.instruction_pointer_register,
            1,
            cpu.instruction_pointer_register,
        ) == instructions[5]
        && Instruction::SetImmediate(25, cpu.instruction_pointer_register) == instructions[6]
        && Instruction::AddImmediate(2, 1, 2) == instructions[7]
        && Instruction::SetImmediate(17, cpu.instruction_pointer_register) == instructions[8]
    {
        cpu.registers[2] = cpu.registers[3] / 256;
        cpu.registers[5] = 1;
        cpu.registers[cpu.instruction_pointer_register] = 26;

        return true;
    }

    false
}

pub fn solve_part2(input: &str) -> usize {
    let (ip_register, instructions) = parse_instructions(input);
    let mut cpu = Cpu::new(ip_register);

    let mut seen_values: HashSet<usize> = HashSet::new();
    let mut last_value: Option<usize> = None;
    while cpu.instruction_pointer() < instructions.len() {
        let ip = cpu.instruction_pointer();
        if check_for_optimization(&mut cpu, &instructions[ip..]) {
            continue;
        }

        let instruction = &instructions[ip];
        if let Instruction::EqualRegisterRegister(a, b, _) = instruction {
            // Same principle as part 1, but we make an assumption that the to-be-checked values
            // are cyclical and we just keep track of all of them. Once we see a value that we've
            // seen before, we're back at the start. Which means that the last seen value is the value
            // that we are looking for.
            let value = cpu.registers[if *a != 0 { *a } else { *b }];
            if seen_values.contains(&value) {
                return last_value.unwrap();
            }

            seen_values.insert(value);
            last_value = Some(value);
        }

        cpu.execute_instruction(instruction);
    }

    unreachable!();
}

#[cfg(test)]
mod tests {
    crate::create_solver_test!(part1);
    crate::create_solver_test!(part2);
}
