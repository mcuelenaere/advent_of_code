use itertools::Itertools;

#[derive(Debug, Eq, PartialEq, Ord, PartialOrd)]
struct IpRange {
    min: u32,
    max: u32,
}

impl IpRange {
    pub fn count(&self) -> u32 {
        self.max - self.min + 1
    }

    pub fn overlaps(&self, other: &Self) -> bool {
        other.min >= self.min && other.min <= self.max
            || (other.max >= self.min && other.max <= self.max)
    }
}

fn parse_ip_ranges(input: &str) -> impl Iterator<Item = IpRange> + '_ {
    input.lines().filter_map(|line| {
        if let Some((min, max)) = line.split_once('-') {
            Some(IpRange {
                min: min.parse().expect("a valid number"),
                max: max.parse().expect("a valid number"),
            })
        } else {
            None
        }
    })
}

pub fn solve_part1(input: &str) -> u32 {
    let blacklist: Vec<_> = parse_ip_ranges(input).sorted().collect();

    let mut lowest_valid_ip = 0;
    for IpRange { min, max } in blacklist {
        if lowest_valid_ip >= min && lowest_valid_ip <= max {
            lowest_valid_ip = max + 1;
        }
    }

    lowest_valid_ip
}

pub fn solve_part2(input: &str) -> u32 {
    let blacklist = parse_ip_ranges(input)
        .sorted()
        .multipeek()
        .batching(|iter| {
            if let Some(mut ip_range) = iter.next() {
                // merge ranges as long as there is an overlap
                loop {
                    match iter.peek() {
                        Some(other) if ip_range.overlaps(other) => {
                            // merge other into ip_range
                            ip_range.min = std::cmp::min(ip_range.min, other.min);
                            ip_range.max = std::cmp::max(ip_range.max, other.max);

                            // consume this IP range
                            iter.next();
                        }
                        _ => break,
                    };
                }

                Some(ip_range)
            } else {
                None
            }
        });
    let total_valid_ips = u32::MAX - blacklist.map(|ip_range| ip_range.count()).sum::<u32>() + 1;

    total_valid_ips
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let input = "5-8\n0-2\n4-7";
        assert_eq!(solve_part1(input), 3);
    }

    crate::create_solver_test!(part1);
    crate::create_solver_test!(part2);
}
