use crate::utils::graph::shortest_path_with_cost;
use itertools::Itertools;
use std::cell::RefCell;
use std::collections::HashMap;

#[derive(Debug, Copy, Clone)]
enum RegionType {
    Rocky,
    Wet,
    Narrow,
}

type Coordinate = crate::utils::grid::Coordinate<0, 0, { isize::MAX }, { isize::MAX }>;

fn parse_depth_target(input: &str) -> (usize, Coordinate) {
    let mut depth = None;
    let mut target = None;
    for line in input.lines() {
        if let Some(s) = line.strip_prefix("depth: ") {
            depth = s.parse::<usize>().ok();
        } else if let Some(s) = line.strip_prefix("target: ") {
            let (x, y) = s
                .splitn(2, ',')
                .map(|s| s.parse::<usize>().expect("a valid number"))
                .collect_tuple::<(usize, usize)>()
                .expect("a valid target");
            target = Coordinate::new(x as isize, y as isize);
        }
    }

    (depth.expect("a depth"), target.expect("a target"))
}

struct RegionCalculator {
    depth: usize,
    target: Coordinate,
    erosion_levels: RefCell<HashMap<(isize, isize), usize>>,
}

impl RegionCalculator {
    pub fn new(depth: usize, target: Coordinate) -> Self {
        Self {
            depth,
            target,
            erosion_levels: RefCell::new(HashMap::new()),
        }
    }

    fn calculate_erosion_level(&self, (x, y): (isize, isize)) -> usize {
        let erosion_level = {
            let erosion_levels = self.erosion_levels.borrow();
            erosion_levels.get(&(x, y)).cloned()
        };
        match erosion_level {
            Some(erosion_level) => erosion_level,
            None => {
                let geologic_index = {
                    if (x, y) == (0, 0) || (x, y) == (self.target.x, self.target.y) {
                        0
                    } else if y == 0 {
                        (x as usize) * 16807
                    } else if x == 0 {
                        (y as usize) * 48271
                    } else {
                        self.calculate_erosion_level((x - 1, y))
                            * self.calculate_erosion_level((x, y - 1))
                    }
                };
                let erosion_level = (geologic_index + self.depth) % 20183;
                self.erosion_levels
                    .borrow_mut()
                    .insert((x, y), erosion_level);
                erosion_level
            }
        }
    }

    pub fn region_type_for(&self, coordinate: &Coordinate) -> RegionType {
        match self.calculate_erosion_level((coordinate.x, coordinate.y)) % 3 {
            0 => RegionType::Rocky,
            1 => RegionType::Wet,
            2 => RegionType::Narrow,
            _ => unreachable!(),
        }
    }
}

pub fn solve_part1(input: &str) -> usize {
    let (depth, target) = parse_depth_target(input);
    let regions = RegionCalculator::new(depth, target);

    let mut risk_level = 0;
    for y in 0..=target.y {
        for x in 0..=target.x {
            risk_level += match regions.region_type_for(&Coordinate::new(x, y).unwrap()) {
                RegionType::Rocky => 0,
                RegionType::Wet => 1,
                RegionType::Narrow => 2,
            };
        }
    }

    risk_level
}

#[derive(Debug, Eq, PartialEq, Hash, Copy, Clone)]
enum ToolType {
    Torch,
    ClimbingGear,
    Neither,
}

impl ToolType {
    pub fn is_compatible_with(&self, region: RegionType) -> bool {
        match self {
            Self::Torch => matches!(region, RegionType::Rocky | RegionType::Narrow),
            Self::ClimbingGear => matches!(region, RegionType::Rocky | RegionType::Wet),
            Self::Neither => matches!(region, RegionType::Wet | RegionType::Narrow),
        }
    }

    pub fn compatible_tools_for(region: RegionType) -> Vec<ToolType> {
        match region {
            RegionType::Rocky => vec![ToolType::ClimbingGear, ToolType::Torch],
            RegionType::Wet => vec![ToolType::ClimbingGear, ToolType::Neither],
            RegionType::Narrow => vec![ToolType::Torch, ToolType::Neither],
        }
    }
}

pub fn solve_part2(input: &str) -> usize {
    let (depth, target) = parse_depth_target(input);
    let regions = RegionCalculator::new(depth, target);

    let path = shortest_path_with_cost(
        (Coordinate::new(0, 0).unwrap(), ToolType::Torch),
        0usize,
        |(coordinate, tool_type)| coordinate == &target && tool_type == &ToolType::Torch,
        |(coordinate, tool_type)| {
            coordinate
                .neighbours_cross()
                .flat_map(|neighbour| {
                    let mut results = Vec::new();
                    let neighbour_region = regions.region_type_for(&neighbour);

                    if tool_type.is_compatible_with(neighbour_region) {
                        results.push(((neighbour, *tool_type), 1));
                    }

                    ToolType::compatible_tools_for(neighbour_region)
                        .into_iter()
                        .filter(|other_tool_type| {
                            other_tool_type != tool_type
                                && other_tool_type
                                    .is_compatible_with(regions.region_type_for(coordinate))
                        })
                        .for_each(|other_tool_type| {
                            results.push(((neighbour, other_tool_type), 7 + 1));
                        });

                    results
                })
                .collect_vec() // FIXME: should not collect
        },
        |(coordinate, _)| target.manhattan_distance(coordinate),
    )
    .expect("a valid path");

    let (_, cost) = path.last().unwrap();
    *cost
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let input = r#"depth: 510
target: 10,10"#;
        assert_eq!(solve_part1(input), 114);
    }

    #[test]
    fn test_part2() {
        let input = r#"depth: 510
target: 10,10"#;
        assert_eq!(solve_part2(input), 45);
    }

    crate::create_solver_test!(year2018, day22, part1);
    crate::create_solver_test!(year2018, day22, part2);
}
