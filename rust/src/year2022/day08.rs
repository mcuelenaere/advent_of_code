use std::collections::HashMap;

type Coordinate = crate::utils::grid::Coordinate<0, 0, { isize::MAX }, { isize::MAX }>;
type TreeMap = HashMap<Coordinate, usize>;

fn parse_tree_map(text: &str) -> TreeMap {
    let mut tree_map = TreeMap::new();
    for (y, line) in text.lines().enumerate() {
        for (x, c) in line.char_indices() {
            tree_map.insert(
                Coordinate::new(x as isize, y as isize).unwrap(),
                c.to_digit(10).expect("valid digit") as usize,
            );
        }
    }
    tree_map
}

pub fn solve_part1(input: &str) -> usize {
    let tree_map = parse_tree_map(input);
    tree_map
        .iter()
        .filter(|(coordinate, height)| {
            for offset in Coordinate::CROSS {
                let mut neighbour = Some(**coordinate);
                loop {
                    neighbour = neighbour.unwrap() + offset;
                    match neighbour.and_then(|neighbour| tree_map.get(&neighbour)) {
                        Some(neighbour_height) => {
                            if neighbour_height >= height {
                                break;
                            } else {
                                continue;
                            }
                        }
                        None => return true,
                    }
                }
            }

            false
        })
        .count()
}

pub fn solve_part2(input: &str) -> usize {
    let tree_map = parse_tree_map(input);
    tree_map
        .iter()
        .map(|(coordinate, height)| {
            let mut viewing_distances = vec![];
            for offset in Coordinate::CROSS {
                let mut viewing_distance: usize = 0;
                let mut neighbour = Some(*coordinate);
                loop {
                    neighbour = neighbour.unwrap() + offset;
                    match neighbour.and_then(|neighbour| tree_map.get(&neighbour)) {
                        Some(neighbour_height) => {
                            viewing_distance += 1;
                            if neighbour_height >= height {
                                break;
                            } else {
                                continue;
                            }
                        }
                        None => break,
                    }
                }
                viewing_distances.push(viewing_distance);
            }

            viewing_distances
                .into_iter()
                .reduce(|a, b| a * b)
                .unwrap_or(0)
        })
        .max()
        .unwrap()
}

#[cfg(test)]
mod tests {
    use super::*;

    static TEST_INPUT: &str = r#"30373
25512
65332
33549
35390"#;

    #[test]
    fn test_part1() {
        assert_eq!(solve_part1(TEST_INPUT), 21);
    }

    #[test]
    fn test_part2() {
        assert_eq!(solve_part2(TEST_INPUT), 8);
    }

    crate::create_solver_test!(part1);
    crate::create_solver_test!(part2);
}
