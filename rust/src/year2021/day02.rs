#[derive(Debug)]
enum Command {
    Forward(usize),
    Down(usize),
    Up(usize),
}

fn parse_commands(input: &str) -> impl Iterator<Item = Command> + '_ {
    input.lines().map(|line| {
        if let Some(prefix) = line.strip_prefix("forward ") {
            Command::Forward(prefix.parse().expect("a valid number"))
        } else if let Some(prefix) = line.strip_prefix("down ") {
            Command::Down(prefix.parse().expect("a valid number"))
        } else if let Some(prefix) = line.strip_prefix("up ") {
            Command::Up(prefix.parse().expect("a valid number"))
        } else {
            panic!("invalid command: {}", line);
        }
    })
}

pub fn solve_part1(input: &str) -> usize {
    let mut horizontal_position = 0;
    let mut depth = 0;
    for command in parse_commands(input) {
        match command {
            Command::Forward(increment) => {
                horizontal_position += increment;
            }
            Command::Down(increment) => {
                depth += increment;
            }
            Command::Up(decrement) => {
                depth -= decrement;
            }
        }
    }

    horizontal_position * depth
}

pub fn solve_part2(input: &str) -> usize {
    let mut horizontal_position = 0;
    let mut depth = 0;
    let mut aim = 0;
    for command in parse_commands(input) {
        match command {
            Command::Forward(increment) => {
                horizontal_position += increment;
                depth += aim * increment;
            }
            Command::Down(increment) => {
                aim += increment;
            }
            Command::Up(decrement) => {
                aim -= decrement;
            }
        }
    }

    horizontal_position * depth
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let input = r#"forward 5
down 5
forward 8
up 3
down 8
forward 2"#;
        assert_eq!(solve_part1(input), 150);
    }

    #[test]
    fn test_part2() {
        let input = r#"forward 5
down 5
forward 8
up 3
down 8
forward 2"#;
        assert_eq!(solve_part2(input), 900);
    }

    crate::create_solver_test!(part1);
    crate::create_solver_test!(part2);
}
