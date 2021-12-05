use crate::utils::graph::shortest_path;
use itertools::Itertools;
use std::cell::RefCell;
use std::collections::HashMap;

type Coordinate = crate::utils::grid::Coordinate<0, 0, { isize::MAX }, { isize::MAX }>;

#[derive(Debug, Clone)]
enum Tile {
    Wall,
    Location(usize),
}

fn parse_tiles(input: &str) -> impl Iterator<Item = (Coordinate, Tile)> + '_ {
    input.lines().enumerate().flat_map(|(y, line)| {
        line.char_indices().filter_map(move |(x, char)| match char {
            '#' => Some((Coordinate::new(x as isize, y as isize).unwrap(), Tile::Wall)),
            '.' => None,
            digit if digit.is_digit(10) => Some((
                Coordinate::new(x as isize, y as isize).unwrap(),
                Tile::Location(digit.to_digit(10).unwrap() as usize),
            )),
            _ => panic!("unknown character: {}", char),
        })
    })
}

#[derive(Debug)]
struct Map {
    tiles: HashMap<Coordinate, Tile>,
    cached_paths: RefCell<HashMap<(Coordinate, Coordinate), Vec<Coordinate>>>,
}

impl Map {
    pub fn from_text(input: &str) -> Self {
        Self {
            tiles: parse_tiles(input).collect(),
            cached_paths: RefCell::new(HashMap::new()),
        }
    }

    pub fn start_tile(&self) -> Coordinate {
        self.tiles
            .iter()
            .find(|(_, tile)| matches!(tile, Tile::Location(0)))
            .map(|(coordinate, _)| coordinate)
            .expect("first tile to be present")
            .clone()
    }

    pub fn locations(&self) -> Vec<(Coordinate, Tile)> {
        self.tiles
            .iter()
            .filter(|(_, tile)| matches!(tile, Tile::Location(number) if *number != 0))
            .map(|(coordinate, tile)| (*coordinate, tile.clone()))
            .collect()
    }

    pub fn path_length_between(&self, from: Coordinate, to: Coordinate) -> usize {
        self.cached_paths
            .borrow_mut()
            .entry((from, to))
            .or_insert_with(|| {
                shortest_path(
                    from,
                    |c: &Coordinate| c == &to,
                    |c: &Coordinate| {
                        c.neighbours_cross()
                            .filter(|neighbour| {
                                if let Some(neighbour) = self.tiles.get(neighbour) {
                                    !matches!(neighbour, Tile::Wall)
                                } else {
                                    true
                                }
                            })
                            .collect::<Vec<_>>() // FIXME: don't collect
                    },
                    |c: &Coordinate| c.manhattan_distance(&to),
                )
                .unwrap()
            })
            .len()
    }
}

pub fn solve_part1(input: &str) -> usize {
    let map = Map::from_text(input);

    let start = map.start_tile();
    let locations: Vec<_> = map.locations();
    let locations_count = locations.len();

    locations
        .into_iter()
        .permutations(locations_count)
        .map(|locations| {
            let mut total_steps = 0;
            let mut current = start;
            for (coordinate, _) in locations {
                let path_length = map.path_length_between(current, coordinate);

                current = coordinate;
                total_steps += path_length - 1;
            }

            total_steps
        })
        .min()
        .unwrap()
}

pub fn solve_part2(input: &str) -> usize {
    let map = Map::from_text(input);

    let start = map.start_tile();
    let locations: Vec<_> = map.locations();
    let locations_count = locations.len();

    locations
        .into_iter()
        .permutations(locations_count)
        .map(|locations| {
            let mut total_steps = 0;
            let mut current = start;
            for (coordinate, _) in locations {
                let path_length = map.path_length_between(current, coordinate);

                current = coordinate;
                total_steps += path_length - 1;
            }

            // return to 0
            let path_length = map.path_length_between(current, start);
            total_steps += path_length - 1;

            total_steps
        })
        .min()
        .unwrap()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let map = r#"###########
#0.1.....2#
#.#######.#
#4.......3#
###########"#;
        assert_eq!(solve_part1(map), 14);
    }

    crate::create_solver_test!(year2016, day24, part1, verify_answer = true);
    crate::create_solver_test!(year2016, day24, part2, verify_answer = true);
}
