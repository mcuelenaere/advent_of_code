use itertools::Itertools;
use std::collections::HashSet;

type Coordinate = crate::utils::grid::Coordinate<0, 0, { isize::MAX }, { isize::MAX }>;

#[derive(Debug)]
enum Fold {
    AlongY(isize),
    AlongX(isize),
}

fn parse_instructions(input: &str) -> (Vec<Coordinate>, Vec<Fold>) {
    #[derive(Debug, Eq, PartialEq)]
    enum ParseMode {
        Dots,
        Folds,
    }

    let mut dots = Vec::new();
    let mut folds = Vec::new();
    let mut mode = ParseMode::Dots;
    for line in input.lines() {
        if line.is_empty() {
            assert_eq!(mode, ParseMode::Dots);
            mode = ParseMode::Folds;
            continue;
        }

        match mode {
            ParseMode::Dots => {
                let (x, y) = line
                    .splitn(2, ',')
                    .map(|s| s.parse::<isize>().expect("a number"))
                    .collect_tuple()
                    .expect("2 numbers");
                dots.push(Coordinate::new(x, y).expect("a valid coordinate"));
            }
            ParseMode::Folds => {
                if let Some(suffix) = line.strip_prefix("fold along ") {
                    if let Some(number) = suffix.strip_prefix("x=") {
                        folds.push(Fold::AlongX(number.parse().expect("a number")));
                    } else if let Some(number) = suffix.strip_prefix("y=") {
                        folds.push(Fold::AlongY(number.parse().expect("a number")));
                    } else {
                        panic!("invalid fold type: {}", suffix);
                    }
                } else {
                    panic!("invalid fold: {}", line);
                }
            }
        }
    }

    (dots, folds)
}

fn fold_dots(dots: Vec<Coordinate>, folds: impl Iterator<Item = Fold>) -> HashSet<Coordinate> {
    let mut dots: HashSet<Coordinate> = HashSet::from_iter(dots);
    for fold in folds {
        dots = dots
            .into_iter()
            .map(|dot| match fold {
                Fold::AlongY(y) => {
                    assert_ne!(dot.y, y);
                    if dot.y < y {
                        dot
                    } else {
                        Coordinate::new(dot.x, y * 2 - dot.y).unwrap()
                    }
                }
                Fold::AlongX(x) => {
                    assert_ne!(dot.x, x);
                    if dot.x < x {
                        dot
                    } else {
                        Coordinate::new(x * 2 - dot.x, dot.y).unwrap()
                    }
                }
            })
            .collect();
    }

    dots
}

pub fn solve_part1(input: &str) -> usize {
    let (dots, folds) = parse_instructions(input);
    fold_dots(dots, folds.into_iter().take(1)).len()
}

pub fn solve_part2(input: &str) -> String {
    let (dots, folds) = parse_instructions(input);
    let folded_dots = fold_dots(dots, folds.into_iter());

    let max_x = folded_dots.iter().map(|c| c.x).max().unwrap();
    let max_y = folded_dots.iter().map(|c| c.y).max().unwrap();

    (0..=max_y)
        .map(|y| {
            (0..=max_x)
                .map(|x| {
                    let dot = Coordinate::new(x, y).unwrap();
                    if folded_dots.contains(&dot) {
                        '#'
                    } else {
                        '.'
                    }
                })
                .join("")
        })
        .join("\n")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let input = r#"6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"#;
        assert_eq!(solve_part1(input), 17);
    }

    crate::create_solver_test!(part1);
    crate::create_solver_test!(part2);
}
