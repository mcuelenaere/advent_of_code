use std::collections::HashSet;

type Coordinate = crate::utils::grid::Coordinate<0, 0, { isize::MAX }, { isize::MAX }>;

#[derive(Debug)]
struct Map {
    max_x: isize,
    max_y: isize,
    east_facing_sea_cucumbers: HashSet<Coordinate>,
    north_facing_sea_cucumbers: HashSet<Coordinate>,
}

impl Map {
    pub fn step(&mut self) -> bool {
        let mut mutated = false;
        self.east_facing_sea_cucumbers = self
            .east_facing_sea_cucumbers
            .iter()
            .map(|sea_cucumber| {
                let neighbour =
                    Coordinate::new((sea_cucumber.x + 1) % (self.max_x + 1), sea_cucumber.y)
                        .unwrap();
                if self.east_facing_sea_cucumbers.contains(&neighbour)
                    || self.north_facing_sea_cucumbers.contains(&neighbour)
                {
                    *sea_cucumber
                } else {
                    mutated = true;
                    neighbour
                }
            })
            .collect();
        self.north_facing_sea_cucumbers = self
            .north_facing_sea_cucumbers
            .iter()
            .map(|sea_cucumber| {
                let neighbour =
                    Coordinate::new(sea_cucumber.x, (sea_cucumber.y + 1) % (self.max_y + 1))
                        .unwrap();
                if self.east_facing_sea_cucumbers.contains(&neighbour)
                    || self.north_facing_sea_cucumbers.contains(&neighbour)
                {
                    *sea_cucumber
                } else {
                    mutated = true;
                    neighbour
                }
            })
            .collect();
        mutated
    }
}

fn parse_map(input: &str) -> Map {
    let mut map = Map {
        max_x: 0,
        max_y: 0,
        east_facing_sea_cucumbers: HashSet::new(),
        north_facing_sea_cucumbers: HashSet::new(),
    };
    for (y, line) in input.lines().enumerate() {
        for (x, c) in line.char_indices() {
            match c {
                '.' => {}
                '>' => {
                    map.east_facing_sea_cucumbers
                        .insert(Coordinate::new(x as isize, y as isize).unwrap());
                }
                'v' => {
                    map.north_facing_sea_cucumbers
                        .insert(Coordinate::new(x as isize, y as isize).unwrap());
                }
                _ => panic!("unsupported character {}", c),
            }
            map.max_x = x as isize;
        }
        map.max_y = y as isize;
    }
    map
}

pub fn solve_part1(input: &str) -> usize {
    let mut map = parse_map(input);
    let mut step_counter = 0;
    while map.step() {
        step_counter += 1;
    }
    step_counter + 1
}

pub fn solve_part2(_: &str) -> String {
    unimplemented!();
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let input = r#"v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"#;
        assert_eq!(solve_part1(input), 58);
    }

    crate::create_solver_test!(part1);
}
