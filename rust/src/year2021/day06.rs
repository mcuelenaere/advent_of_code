use itertools::Itertools;

fn parse_fish(input: &str) -> impl Iterator<Item = u8> + '_ {
    input
        .split(',')
        .map(|str| str.parse().expect("a valid number"))
}

fn count_spawned_fish(fish: impl Iterator<Item = u8>, number_of_days: usize) -> usize {
    let mut compressed_fish = fish
        .map(|spawn_countdown| (1, spawn_countdown))
        .collect_vec();

    for _ in 0..number_of_days {
        let mut new_fish_count = 0;
        for (fish_count, spawn_countdown) in compressed_fish.iter_mut() {
            if *spawn_countdown == 0 {
                *spawn_countdown = 6;
                new_fish_count += *fish_count;
            } else {
                *spawn_countdown -= 1;
            }
        }

        if new_fish_count > 0 {
            compressed_fish.push((new_fish_count, 8));
        }
    }

    compressed_fish
        .into_iter()
        .map(|(fish_count, _)| fish_count)
        .sum()
}

pub fn solve_part1(input: &str) -> usize {
    count_spawned_fish(parse_fish(input), 80)
}

pub fn solve_part2(input: &str) -> usize {
    count_spawned_fish(parse_fish(input), 256)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let input = "3,4,3,1,2";
        assert_eq!(solve_part1(input), 5934);
    }

    #[test]
    fn test_part2() {
        let input = "3,4,3,1,2";
        assert_eq!(solve_part2(input), 26984457539);
    }

    crate::create_solver_test!(year2021, day06, part1);
    crate::create_solver_test!(year2021, day06, part2);
}
