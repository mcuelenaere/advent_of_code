use itertools::Itertools;
use std::cmp::Ordering;

#[derive(Debug, Eq, PartialEq)]
enum Operation {
    Sum,
    Product,
    Minimum,
    Maximum,
    GreaterThan,
    LessThan,
    EqualTo,
}

impl Operation {
    pub fn evaluate(&self, packets: &[Packet]) -> usize {
        match self {
            Operation::Sum | Operation::Product | Operation::Minimum | Operation::Maximum => {
                let iter = packets.iter().map(|p| p.value());
                match self {
                    Operation::Sum => iter.sum(),
                    Operation::Product => iter.product(),
                    Operation::Minimum => iter.min().unwrap(),
                    Operation::Maximum => iter.max().unwrap(),
                    _ => unreachable!(),
                }
            }
            Operation::GreaterThan | Operation::LessThan | Operation::EqualTo => {
                assert_eq!(packets.len(), 2);
                let (a, b) = (packets[0].value(), packets[1].value());

                let ordering = match self {
                    Operation::GreaterThan => Ordering::Greater,
                    Operation::LessThan => Ordering::Less,
                    Operation::EqualTo => Ordering::Equal,
                    _ => unreachable!(),
                };

                if a.cmp(&b) == ordering {
                    1
                } else {
                    0
                }
            }
        }
    }
}

trait BitReader {
    fn read_bits(&mut self, n: usize) -> Option<usize>;

    fn read_u8(&mut self, n: usize) -> Option<u8> {
        assert!(n <= 8);
        self.read_bits(n).map(|b| b as u8)
    }

    fn read_u16(&mut self, n: usize) -> Option<u16> {
        assert!(n <= 16);
        self.read_bits(n).map(|b| b as u16)
    }
}

impl<I: Iterator<Item = bool>> BitReader for I {
    fn read_bits(&mut self, n: usize) -> Option<usize> {
        let mut byte = 0;
        for i in (0..n).rev() {
            let bit = if self.next()? { 1 } else { 0 };
            byte |= bit << i;
        }
        Some(byte)
    }
}

#[derive(Debug, Eq, PartialEq)]
enum Packet {
    Operator {
        version: u8,
        operation: Operation,
        sub_packets: Vec<Packet>,
    },
    LiteralValue {
        version: u8,
        number: usize,
    },
}

impl Packet {
    pub fn from_bitstream(bitstream: &mut impl Iterator<Item = bool>) -> Self {
        let version = bitstream.read_u8(3).unwrap();
        let type_id = bitstream.read_u8(3).unwrap();

        if type_id == 4 {
            let mut number: usize = 0;
            loop {
                let group = bitstream.read_u8(5).unwrap();

                number <<= 4;
                number |= (group & 0b1111) as usize;

                if group & 0b10000 == 0 {
                    break;
                }
            }

            Packet::LiteralValue { version, number }
        } else {
            let length_type_id = bitstream.next().unwrap();
            let sub_packets = if length_type_id {
                let sub_packets_count = bitstream.read_u16(11).unwrap();

                (0..sub_packets_count)
                    .map(|_| Packet::from_bitstream(bitstream))
                    .collect_vec()
            } else {
                let sub_packets_bit_length = bitstream.read_u16(15).unwrap();

                // we need to cast the impl Iterator to a trait object, otherwise the compiler
                // complains about recursive generics
                (Box::new(bitstream) as Box<dyn Iterator<Item = bool>>)
                    .take(sub_packets_bit_length as usize)
                    .peekable()
                    .batching(|bitstream| {
                        if bitstream.peek().is_none() {
                            None
                        } else {
                            Some(Packet::from_bitstream(bitstream))
                        }
                    })
                    .collect_vec()
            };

            let operation = match type_id {
                0 => Operation::Sum,
                1 => Operation::Product,
                2 => Operation::Minimum,
                3 => Operation::Maximum,
                5 => Operation::GreaterThan,
                6 => Operation::LessThan,
                7 => Operation::EqualTo,
                _ => panic!("unknown type {}", type_id),
            };

            Packet::Operator {
                version,
                operation,
                sub_packets,
            }
        }
    }

    pub fn version_sum(&self) -> usize {
        match self {
            Packet::LiteralValue { version, .. } => *version as usize,
            Packet::Operator {
                version,
                sub_packets,
                ..
            } => sub_packets.iter().map(|p| p.version_sum()).sum::<usize>() + (*version as usize),
        }
    }

    pub fn value(&self) -> usize {
        match self {
            Packet::LiteralValue { number, .. } => *number,
            Packet::Operator {
                sub_packets,
                operation,
                ..
            } => operation.evaluate(sub_packets),
        }
    }
}

fn parse_transmission(input: &str) -> Packet {
    let mut bitstream = input.chars().flat_map(|c| {
        let half_byte = c.to_digit(16).expect("valid hex") as u8;
        (0..4).rev().map(move |i| half_byte & (1 << i) != 0)
    });

    Packet::from_bitstream(&mut bitstream)
}

pub fn solve_part1(input: &str) -> usize {
    parse_transmission(input).version_sum()
}

pub fn solve_part2(input: &str) -> usize {
    parse_transmission(input).value()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse() {
        assert_eq!(
            parse_transmission("D2FE28"),
            Packet::LiteralValue {
                version: 6,
                number: 2021
            }
        );
        assert_eq!(
            parse_transmission("38006F45291200"),
            Packet::Operator {
                version: 1,
                operation: Operation::LessThan,
                sub_packets: vec![
                    Packet::LiteralValue {
                        version: 6,
                        number: 10
                    },
                    Packet::LiteralValue {
                        version: 2,
                        number: 20
                    }
                ]
            }
        );
        assert_eq!(
            parse_transmission("EE00D40C823060"),
            Packet::Operator {
                version: 7,
                operation: Operation::Maximum,
                sub_packets: vec![
                    Packet::LiteralValue {
                        version: 2,
                        number: 1
                    },
                    Packet::LiteralValue {
                        version: 4,
                        number: 2
                    },
                    Packet::LiteralValue {
                        version: 1,
                        number: 3
                    }
                ]
            }
        );
    }

    #[test]
    fn test_part1() {
        assert_eq!(solve_part1("8A004A801A8002F478"), 16);
        assert_eq!(solve_part1("620080001611562C8802118E34"), 12);
        assert_eq!(solve_part1("C0015000016115A2E0802F182340"), 23);
        assert_eq!(solve_part1("A0016C880162017C3686B18A3D4780"), 31);
    }

    #[test]
    fn test_part2() {
        assert_eq!(solve_part2("C200B40A82"), 3);
        assert_eq!(solve_part2("04005AC33890"), 54);
        assert_eq!(solve_part2("880086C3E88112"), 7);
        assert_eq!(solve_part2("CE00C43D881120"), 9);
        assert_eq!(solve_part2("D8005AC2A8F0"), 1);
        assert_eq!(solve_part2("F600BC2D8F"), 0);
        assert_eq!(solve_part2("9C005AC2F8F0"), 0);
        assert_eq!(solve_part2("9C0141080250320F1802104A08"), 1);
    }

    crate::create_solver_test!(year2021, day16, part1);
    crate::create_solver_test!(year2021, day16, part2);
}
