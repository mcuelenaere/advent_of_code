use itertools::Itertools;

fn is_matching(a: char, b: char) -> bool {
    match (a, b) {
        ('(', ')') => true,
        ('[', ']') => true,
        ('{', '}') => true,
        ('<', '>') => true,
        _ => false,
    }
}

#[derive(Debug, Eq, PartialEq)]
enum VerificationStatus {
    Ok,
    Incomplete { suffix: String },
    Corrupt { position: usize },
}

fn verify_chunks(input: &str) -> VerificationStatus {
    let mut stack = Vec::new();
    for (pos, c) in input.char_indices() {
        match c {
            '(' | '[' | '{' | '<' => stack.push(c),
            ')' | ']' | '}' | '>' => match stack.pop() {
                Some(opener) if is_matching(opener, c) => continue,
                Some(_) => return VerificationStatus::Corrupt { position: pos },
                None => {
                    return VerificationStatus::Incomplete {
                        suffix: String::new(),
                    };
                }
            },
            _ => panic!("unsupported character {}", c),
        }
    }

    if stack.is_empty() {
        VerificationStatus::Ok
    } else {
        let suffix = stack
            .into_iter()
            .rev()
            .map(|c| match c {
                '(' => ')',
                '[' => ']',
                '{' => '}',
                '<' => '>',
                _ => panic!("invalid character {}", c),
            })
            .join("");

        VerificationStatus::Incomplete { suffix }
    }
}

fn corrupt_character_score(c: char) -> usize {
    match c {
        ')' => 3,
        ']' => 57,
        '}' => 1197,
        '>' => 25137,
        _ => 0,
    }
}

pub fn solve_part1(input: &str) -> usize {
    let mut score = 0;
    for line in input.lines() {
        match verify_chunks(line) {
            VerificationStatus::Ok | VerificationStatus::Incomplete { .. } => continue,
            VerificationStatus::Corrupt { position } => {
                score += corrupt_character_score(line.chars().nth(position).unwrap());
            }
        }
    }
    score
}

fn incomplete_character_score(c: char) -> usize {
    match c {
        ')' => 1,
        ']' => 2,
        '}' => 3,
        '>' => 4,
        _ => 0,
    }
}

pub fn solve_part2(input: &str) -> usize {
    let mut scores = Vec::new();
    for line in input.lines() {
        match verify_chunks(line) {
            VerificationStatus::Ok | VerificationStatus::Corrupt { .. } => continue,
            VerificationStatus::Incomplete { suffix } => {
                let mut score = 0;
                for c in suffix.chars() {
                    score *= 5;
                    score += incomplete_character_score(c);
                }
                scores.push(score);
            }
        }
    }

    scores.sort_unstable();
    scores[scores.len() / 2]
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_verify_chunks() {
        let legal_inputs = vec![
            "()",
            "[]",
            "([])",
            "{()()()}",
            "<([{}])>",
            "[<>({}){}[([])<>]]",
            "(((((((((())))))))))",
        ];
        for input in legal_inputs {
            assert_eq!(verify_chunks(input), VerificationStatus::Ok);
        }

        let corrupt_inputs = vec![
            ("(]", 1),
            ("{()()()>", 7),
            ("(((()))}", 7),
            ("<([]){()}[{}])", 13),
            ("{([(<{}[<>[]}>{[]{[(<()>", 12),
            ("[[<[([]))<([[{}[[()]]]", 8),
            ("[{[{({}]{}}([{[{{{}}([]", 7),
            ("[<(<(<(<{}))><([]([]()", 10),
            ("<{([([[(<>()){}]>(<<{{", 16),
        ];
        for (input, expected_position) in corrupt_inputs {
            assert_eq!(
                verify_chunks(input),
                VerificationStatus::Corrupt {
                    position: expected_position
                }
            );
        }

        let incomplete_inputs = vec![
            ("[({(<(())[]>[[{[]{<()<>>", "}}]])})]"),
            ("[(()[<>])]({[<{<<[]>>(", ")}>]})"),
            ("(((({<>}<{<{<>}{[]{[]{}", "}}>}>))))"),
            ("{<[[]]>}<{[{[{[]{()[[[]", "]]}}]}]}>"),
            ("<{([{{}}[<[[[<>{}]]]>[]]", "])}>"),
        ];
        for (input, expected_suffix) in incomplete_inputs {
            assert_eq!(
                verify_chunks(input),
                VerificationStatus::Incomplete {
                    suffix: expected_suffix.to_string()
                }
            );
        }
    }

    #[test]
    fn test_part1() {
        let input = r#"[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"#;
        assert_eq!(solve_part1(input), 26397);
    }

    #[test]
    fn test_part2() {
        let input = r#"[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"#;
        assert_eq!(solve_part2(input), 288957);
    }

    crate::create_solver_test!(part1);
    crate::create_solver_test!(part2);
}
