use genawaiter::rc::gen;
use genawaiter::yield_;
use itertools::Itertools;

#[derive(Debug, Copy, Clone)]
enum Instruction {
    Noop,
    Addx(isize),
}

fn parse_instructions(text: &str) -> impl Iterator<Item = Instruction> + '_ {
    text.lines().map(|line| {
        if line == "noop" {
            Instruction::Noop
        } else if line.starts_with("addx ") {
            let offset = line
                .strip_prefix("addx ")
                .unwrap()
                .parse()
                .expect("valid number");
            Instruction::Addx(offset)
        } else {
            panic!("unsupported instruction");
        }
    })
}

fn simulate_cpu(
    mut instructions: impl Iterator<Item = Instruction>,
) -> impl Iterator<Item = (usize, isize)> {
    gen!({
        let mut cycle_counter = 1usize;
        let mut register_x = 1isize;
        loop {
            let instruction = match instructions.next() {
                Some(instruction) => instruction,
                None => break,
            };

            match instruction {
                Instruction::Noop => {
                    yield_!((cycle_counter, register_x));
                    cycle_counter += 1;
                }
                Instruction::Addx(new_x_value) => {
                    yield_!((cycle_counter, register_x));
                    cycle_counter += 1;
                    yield_!((cycle_counter, register_x));
                    cycle_counter += 1;
                    register_x += new_x_value;
                }
            }
        }
    })
    .into_iter()
}

pub fn solve_part1(input: &str) -> isize {
    simulate_cpu(parse_instructions(input))
        .filter(|(cycle, _)| (*cycle - 20) % 40 == 0 && *cycle >= 20 && *cycle <= 220)
        .map(|(cycle, x)| cycle as isize * x)
        .sum()
}

pub fn solve_part2(input: &str) -> String {
    simulate_cpu(parse_instructions(input))
        .map(|(cycle, x)| {
            let crt_position = ((cycle - 1) % 40) as isize;
            if crt_position >= x - 1 && crt_position <= x + 1 {
                '#'
            } else {
                '.'
            }
        })
        .chunks(40)
        .into_iter()
        .map(|mut chunk| chunk.join(""))
        .join("\n")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_simulate_cpu() {
        let instructions = r#"noop
addx 3
addx -5"#;
        let mut it = simulate_cpu(parse_instructions(instructions));
        assert_eq!(it.next(), Some((1, 1)));
        assert_eq!(it.next(), Some((2, 1)));
        assert_eq!(it.next(), Some((3, 1)));
        assert_eq!(it.next(), Some((4, 4)));
        assert_eq!(it.next(), Some((5, 4)));
        assert_eq!(it.next(), None);
    }

    static TEST_INPUT: &str = r#"addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"#;

    #[test]
    fn test_part1() {
        assert_eq!(solve_part1(TEST_INPUT), 13140);
    }

    #[test]
    fn test_part2() {
        let expected_output = r#"##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######....."#;
        assert_eq!(solve_part2(TEST_INPUT), expected_output.to_string());
    }

    crate::create_solver_test!(part1);
    crate::create_solver_test!(part2);
}
