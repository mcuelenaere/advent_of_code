use itertools::EitherOrBoth;
use itertools::Itertools;
use std::cmp::Ordering;

#[derive(Debug, Eq, PartialEq, Clone)]
enum Packet {
    Integer(usize),
    List(Vec<Self>),
}

impl PartialOrd<Self> for Packet {
    fn partial_cmp(&self, right: &Self) -> Option<Ordering> {
        match (self, right) {
            (Self::Integer(left), Self::Integer(right)) => left.partial_cmp(right),
            (Self::List(left), Self::List(right)) => {
                for either in left.iter().zip_longest(right.iter()) {
                    match either {
                        EitherOrBoth::Both(left, right) => {
                            let cmp_result = left.partial_cmp(right).unwrap();
                            if cmp_result != Ordering::Equal {
                                return Some(cmp_result);
                            }
                            continue;
                        }
                        EitherOrBoth::Left(_) => return Some(Ordering::Greater),
                        EitherOrBoth::Right(_) => return Some(Ordering::Less),
                    }
                }

                Some(Ordering::Equal)
            }
            (Self::List(_), Self::Integer(right)) => {
                let right = Self::List(vec![Self::Integer(*right)]);
                self.partial_cmp(&right)
            }
            (Self::Integer(left), Self::List(_)) => {
                let left = Self::List(vec![Self::Integer(*left)]);
                left.partial_cmp(right)
            }
        }
    }
}

impl Ord for Packet {
    fn cmp(&self, other: &Self) -> Ordering {
        self.partial_cmp(other).unwrap()
    }
}

impl<'a> From<&'a str> for Packet {
    fn from(line: &'a str) -> Self {
        let mut stack = Vec::new();
        let mut result = None;
        let mut buffer = vec![];
        for c in line.chars() {
            if (c == ']' || c == ',') && !buffer.is_empty() {
                if let Some(Self::List(items)) = stack.last_mut() {
                    items.push(Self::Integer(
                        String::from_iter(buffer.iter())
                            .parse()
                            .expect("valid number"),
                    ));
                } else {
                    panic!("expected stack to contain at least 1 list");
                }
                buffer.clear();
            }

            match c {
                '[' => {
                    stack.push(Self::List(Vec::new()));
                }
                ']' => {
                    let item = stack.pop().expect("item to be present");
                    match stack.last_mut() {
                        Some(Self::List(items)) => {
                            items.push(item);
                        }
                        None => {
                            if let Some(_) = result.replace(item) {
                                panic!("cannot have multiple results");
                            }
                        }
                        _ => unreachable!(),
                    }
                }
                ',' => {
                    // ignore
                }
                '0'..='9' => {
                    buffer.push(c);
                }
                _ => panic!("unsupported character"),
            }
        }

        result.expect("valid packet")
    }
}

fn parse_packet_data(text: &str) -> impl Iterator<Item = (Packet, Packet)> + '_ {
    text.lines().batching(|line| {
        let left = match line.next() {
            Some(line) => line,
            None => return None,
        };
        let right = line.next().expect("right line if we have a left line");
        match line.next() {
            Some("") | None => {}
            _ => panic!("expected empty line"),
        };

        Some((left.into(), right.into()))
    })
}

pub fn solve_part1(input: &str) -> usize {
    parse_packet_data(input)
        .enumerate()
        .filter_map(
            |(idx, (left, right))| {
                if left < right {
                    Some(idx + 1)
                } else {
                    None
                }
            },
        )
        .sum()
}

pub fn solve_part2(input: &str) -> usize {
    let divider_packets = vec![Packet::from("[[2]]"), Packet::from("[[6]]")];
    parse_packet_data(input)
        .flat_map(|(left, right)| vec![left, right])
        .chain(divider_packets.clone().into_iter())
        .sorted()
        .enumerate()
        .filter_map(|(idx, packet)| {
            if divider_packets.contains(&packet) {
                Some(idx + 1)
            } else {
                None
            }
        })
        .reduce(|a, b| a * b)
        .unwrap()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ordering() {
        assert!(Packet::from("[1,1,3,1,1]") < Packet::from("[1,1,5,1,1]"));
        assert!(Packet::from("[[1],[2,3,4]]") < Packet::from("[[1],4]"));
        assert!(Packet::from("[9]") >= Packet::from("[[8,7,6]]"));
        assert!(Packet::from("[[4,4],4,4]") < Packet::from("[[4,4],4,4,4]"));
        assert!(Packet::from("[7,7,7,7]") >= Packet::from("[7,7,7]"));
    }

    static TEST_INPUT: &str = r#"[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"#;

    #[test]
    fn test_part1() {
        assert_eq!(solve_part1(TEST_INPUT), 13);
    }

    #[test]
    fn test_part2() {
        assert_eq!(solve_part2(TEST_INPUT), 140);
    }

    crate::create_solver_test!(part1);
    crate::create_solver_test!(part2);
}
