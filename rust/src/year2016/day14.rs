use itertools::{izip, Itertools};
use md5::{Digest, Md5};
use rayon::prelude::*;
use std::io::Write;

fn find_triplet(input: &str) -> Option<char> {
    izip!(input.chars(), input.chars().skip(1), input.chars().skip(2))
        .filter(|(a, b, c)| a == b && b == c)
        .map(|(a, _, _)| a)
        .next()
}

fn calculate_hash(salt: &str, index: usize, rounds: usize) -> String {
    let mut hasher = Md5::new();
    hasher.update(salt);
    hasher.update(index.to_string());
    let mut prev_output: Vec<u8> = Vec::new();
    for _ in 1..rounds {
        write!(&mut prev_output, "{:x}", hasher.finalize_reset()).unwrap();
        hasher.update(&prev_output);
        prev_output.clear();
    }
    format!("{:x}", hasher.finalize())
}

fn generate_key(salt: &str, rounds: usize) -> Option<usize> {
    const BATCH_SIZE: usize = 1000;

    let mut start_index: usize = 0;
    std::iter::from_fn(|| {
        let chunk: Vec<_> = (start_index..start_index + BATCH_SIZE)
            .into_par_iter()
            .map(move |index| (index, calculate_hash(salt, index, rounds)))
            .collect();
        start_index += BATCH_SIZE;

        Some(chunk)
    })
    .flatten()
    .multipeek()
    .batching(|iter| loop {
        let (index, hash) = iter.next().expect("a hash");
        if let Some(c) = find_triplet(&hash) {
            let needle = format!("{}{}{}{}{}", c, c, c, c, c);
            for _ in 0..1000 {
                let (_, hash) = iter.peek().expect("a hash");
                if hash.contains(&needle) {
                    return Some(index);
                }
            }
        }
    })
    .take(64)
    .last()
}

pub fn solve_part1(input: &str) -> usize {
    generate_key(input, 1).expect("a value")
}

pub fn solve_part2(input: &str) -> usize {
    generate_key(input, 2017).expect("a value")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let index = solve_part1("abc");
        assert_eq!(index, 22728);
    }

    #[test]
    fn test_part2() {
        let index = solve_part2("abc");
        assert_eq!(index, 22551);
    }

    crate::create_solver_test!(year2016, day14, part1);
    crate::create_solver_test!(year2016, day14, part2);
}
