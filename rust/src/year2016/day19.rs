use itertools::Itertools;

#[derive(Debug, Clone)]
struct Elf {
    number: usize,
    presents_count: usize,
}

fn part1(number_of_elves: usize) -> usize {
    let mut elves: Vec<Elf> = Vec::with_capacity(number_of_elves);
    for number in 1..=number_of_elves {
        elves.push(Elf {
            number,
            presents_count: 1,
        });
    }

    while elves.len() > 1 {
        let mut should_fixup = false;
        elves = elves
            .iter()
            .batching(|iter| match (iter.next(), iter.next()) {
                (Some(cur), Some(next)) => {
                    assert!(cur.presents_count > 0);

                    Some(Elf {
                        number: cur.number,
                        presents_count: cur.presents_count + next.presents_count,
                    })
                }
                (Some(elf), None) => {
                    should_fixup = true;

                    Some(elf.clone())
                }
                _ => None,
            })
            .collect();

        if should_fixup {
            let next = elves.remove(0);
            let cur = elves.last_mut().unwrap();
            assert!(cur.presents_count > 0);
            cur.presents_count += next.presents_count;
        }
    }

    let winner = elves.first().unwrap();
    assert_eq!(winner.presents_count, number_of_elves);

    winner.number
}

pub fn solve_part1(input: &str) -> usize {
    let number_of_elves: usize = input.parse().expect("a valid number");
    part1(number_of_elves)
}

#[allow(dead_code)]
fn part2_naive(number_of_elves: usize) -> usize {
    let mut elves: Vec<Elf> = Vec::with_capacity(number_of_elves);
    for number in 1..=number_of_elves {
        elves.push(Elf {
            number,
            presents_count: 1,
        });
    }

    let mut current_index = 0;
    while elves.len() > 1 {
        let opposite_index = (current_index + (elves.len() / 2)) % elves.len();
        elves[current_index].presents_count += elves[opposite_index].presents_count;
        elves.remove(opposite_index);
        if opposite_index < current_index {
            current_index -= 1;
        }
        current_index = (current_index + 1) % elves.len();
    }
    let winner = &elves[0];
    assert_eq!(winner.presents_count, number_of_elves);

    winner.number
}

fn part2_optimized(number_of_elves: usize) -> usize {
    // After running part2_naive() on 1..100 and entering the integer sequence
    // on OEIS, we get the following solution: https://oeis.org/A334473
    fn highest_power_of_3(n: usize) -> usize {
        let mut option: u32 = 0;
        while 3_usize.pow(option) <= n {
            option += 1;
        }
        3_usize.pow(option - 1)
    }

    let x = highest_power_of_3(number_of_elves);
    if x == number_of_elves {
        x
    } else if number_of_elves < 2 * x {
        number_of_elves % x
    } else {
        x + 2 * (number_of_elves % x)
    }
}

pub fn solve_part2(input: &str) -> usize {
    let number_of_elves: usize = input.parse().expect("a valid number");
    part2_optimized(number_of_elves)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(part1(5), 3);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2_naive(5), 2);
        assert_eq!(part2_optimized(5), 2);
    }

    crate::create_solver_test!(year2016, day19, part1, verify_answer = true);
    crate::create_solver_test!(year2016, day19, part2, verify_answer = true);
}
