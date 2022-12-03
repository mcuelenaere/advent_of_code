use itertools::{chain, izip};
use std::fmt::{Display, Write};

#[derive(Debug, Copy, Clone)]
enum Tile {
    Safe,
    Trap,
}

impl Display for Tile {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Tile::Safe => f.write_char('.'),
            Tile::Trap => f.write_char('^'),
        }
    }
}

fn parse_tiles(input: &str) -> Vec<Tile> {
    input
        .chars()
        .map(|c| match c {
            '.' => Tile::Safe,
            '^' => Tile::Trap,
            _ => unimplemented!(),
        })
        .collect()
}

fn generate_tiles(first_row: Vec<Tile>, number_of_rows: usize) -> impl Iterator<Item = Vec<Tile>> {
    let mut row = first_row;
    (0..number_of_rows).map(move |_| {
        let new_row: Vec<Tile> = izip!(
            chain!([Tile::Safe].iter(), row.iter().take(row.len() - 1)),
            row.iter(),
            chain!(row.iter().skip(1), [Tile::Safe].iter())
        )
        .map(|(left, center, right)| match (left, center, right) {
            (Tile::Trap, Tile::Trap, Tile::Safe) => Tile::Trap,
            (Tile::Safe, Tile::Trap, Tile::Trap) => Tile::Trap,
            (Tile::Trap, Tile::Safe, Tile::Safe) => Tile::Trap,
            (Tile::Safe, Tile::Safe, Tile::Trap) => Tile::Trap,
            _ => Tile::Safe,
        })
        .collect();

        row = new_row.clone();
        new_row
    })
}

fn _solve(input: &str, number_of_rows: usize) -> usize {
    let first_row = parse_tiles(input);
    let other_rows = generate_tiles(first_row.clone(), number_of_rows - 1);
    chain!([first_row].into_iter(), other_rows)
        .flatten()
        .filter(|tile| matches!(tile, Tile::Safe))
        .count()
}

pub fn solve_part1(input: &str) -> usize {
    _solve(input, 40)
}

pub fn solve_part2(input: &str) -> usize {
    _solve(input, 400000)
}

#[cfg(test)]
mod tests {
    use super::*;
    use itertools::Itertools;

    #[test]
    fn test_generate_tiles() {
        assert_eq!(
            generate_tiles(parse_tiles("..^^."), 2)
                .map(|row| row.into_iter().map(|tile| tile.to_string()).join(""))
                .collect::<Vec<_>>(),
            vec![".^^^^", "^^..^"]
        );
        assert_eq!(
            generate_tiles(parse_tiles(".^^.^.^^^^"), 9)
                .map(|row| row.into_iter().map(|tile| tile.to_string()).join(""))
                .collect::<Vec<_>>(),
            vec![
                "^^^...^..^",
                "^.^^.^.^^.",
                "..^^...^^^",
                ".^^^^.^^.^",
                "^^..^.^^..",
                "^^^^..^^^.",
                "^..^^^^.^^",
                ".^^^..^.^^",
                "^^.^^^..^^"
            ]
        );
    }

    #[test]
    fn test_solve() {
        assert_eq!(_solve(".^^.^.^^^^", 10), 38);
    }

    crate::create_solver_test!(part1);
    crate::create_solver_test!(part2);
}
