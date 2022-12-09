use std::collections::HashSet;

fn ascii_windows(text: &str, size: usize) -> impl Iterator<Item = &str> {
    text.as_bytes()
        .windows(size)
        .map(|b| std::str::from_utf8(b).expect("input string should have been an ASCII string"))
}

fn find_marker(message: &str, length: usize) -> usize {
    let first_match = ascii_windows(message, length)
        .find(|packet| {
            let set: HashSet<char> = HashSet::from_iter(packet.chars());
            set.len() == length
        })
        .expect("a match");

    // SAFETY: `first_match` is always a pointer starting from `message`
    let offset = unsafe { first_match.as_ptr().offset_from(message.as_ptr()) };
    offset as usize + length
}

pub fn solve_part1(input: &str) -> usize {
    find_marker(input, 4)
}

pub fn solve_part2(input: &str) -> usize {
    find_marker(input, 14)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(solve_part1("mjqjpqmgbljsphdztnvjfqwrcgsmlb"), 7);
        assert_eq!(solve_part1("bvwbjplbgvbhsrlpgdmjqwftvncz"), 5);
        assert_eq!(solve_part1("nppdvjthqldpwncqszvftbrmjlhg"), 6);
        assert_eq!(solve_part1("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"), 10);
        assert_eq!(solve_part1("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"), 11);
    }

    #[test]
    fn test_part2() {
        assert_eq!(solve_part2("mjqjpqmgbljsphdztnvjfqwrcgsmlb"), 19);
        assert_eq!(solve_part2("bvwbjplbgvbhsrlpgdmjqwftvncz"), 23);
        assert_eq!(solve_part2("nppdvjthqldpwncqszvftbrmjlhg"), 23);
        assert_eq!(solve_part2("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"), 29);
        assert_eq!(solve_part2("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"), 26);
    }

    crate::create_solver_test!(part1);
    crate::create_solver_test!(part2);
}
