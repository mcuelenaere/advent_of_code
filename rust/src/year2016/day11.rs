use crate::utils::graph::shortest_path;
use itertools::{chain, Itertools};
use lazy_static::lazy_static;
use regex::Regex;
use std::hash::{Hash, Hasher};
use std::ops::{Index, IndexMut};
use std::rc::Rc;

#[derive(Debug, Eq, PartialEq, Clone, Hash, Ord, PartialOrd)]
enum Component {
    Microchip(Rc<String>),
    Generator(Rc<String>),
    Elevator,
}

impl Component {
    fn new_microchip(radiation_type: &str) -> Self {
        Component::Microchip(Rc::new(radiation_type.into()))
    }

    fn new_generator(radiation_type: &str) -> Self {
        Component::Generator(Rc::new(radiation_type.into()))
    }
}

type Floor = Vec<Component>;

fn is_valid_floor(floor: &Floor) -> bool {
    floor.iter().all(|component| match component {
        Component::Generator(_) => true,
        Component::Microchip(rad_type) => {
            floor.contains(&Component::Generator(rad_type.clone()))
                || floor
                    .iter()
                    .filter(|c| matches!(c, Component::Generator(_)))
                    .count()
                    == 0
        }
        Component::Elevator => true,
    })
}

#[derive(Debug, PartialEq, Eq, Hash, Clone)]
struct Arrangement {
    floors: [Floor; 4],
}

impl Index<usize> for Arrangement {
    type Output = Floor;

    fn index(&self, index: usize) -> &Self::Output {
        &self.floors[index - 1]
    }
}

impl IndexMut<usize> for Arrangement {
    fn index_mut(&mut self, index: usize) -> &mut Self::Output {
        &mut self.floors[index - 1]
    }
}

impl Arrangement {
    pub fn new(floors: [Floor; 4]) -> Self {
        Self { floors }
    }
}

#[derive(Debug, Eq, Clone)]
struct ArrangementWrapper {
    inner: Arrangement,
    simplified_state: u64,
}

impl PartialEq for ArrangementWrapper {
    fn eq(&self, other: &Self) -> bool {
        self.simplified_state.eq(&other.simplified_state)
    }
}

impl Hash for ArrangementWrapper {
    fn hash<H: Hasher>(&self, state: &mut H) {
        state.write_u64(self.simplified_state);
    }
}

impl ArrangementWrapper {
    pub fn new(arrangement: Arrangement) -> Self {
        Self {
            simplified_state: Self::calculate_simplified_state(&arrangement),
            inner: arrangement,
        }
    }

    /// This calculates a simplified state of the Arrangement.
    ///
    /// Every component is packed into a certain amount of bits and they are laid out
    /// per floor, by bit shifting them to the left (for every increasing floor number).
    ///
    /// Eg: if we have 4 distinct radiation types in an arrangement, we will allocate 9 bits for
    /// every floor (1 for the elevator, 4 for the microchips and another 4 for the generators).
    ///
    /// NOTE: since we are packing this in an u64, that means we only have 16 bits per floor and
    /// thus only room for 7 different radiation types
    fn calculate_simplified_state(arrangement: &Arrangement) -> u64 {
        let mut radiation_types = Vec::new();
        for component in arrangement.floors.iter().flatten() {
            match component {
                Component::Microchip(radiation_type) | Component::Generator(radiation_type) => {
                    if !radiation_types.contains(&radiation_type) {
                        radiation_types.push(radiation_type);
                    }
                }
                _ => {}
            };
        }

        let mut result: u64 = 0;
        for (floor_index, floor) in arrangement.floors.iter().enumerate() {
            for component in floor {
                let component_code: u64 = match component {
                    Component::Elevator => 1,
                    Component::Microchip(radiation_type) => {
                        1 << (1 + radiation_types
                            .iter()
                            .position(|r| *r == radiation_type)
                            .unwrap())
                    }
                    Component::Generator(radiation_type) => {
                        1 << (1
                            + radiation_types.len()
                            + radiation_types
                                .iter()
                                .position(|r| *r == radiation_type)
                                .unwrap())
                    }
                };

                result |= component_code << (floor_index * 16);
            }
        }

        result
    }
}

lazy_static! {
    static ref RE_FLOOR_CONTAINS: Regex = Regex::new(r"The (\w+) floor contains (.+)\.").unwrap();
    static ref RE_SPLIT: Regex = Regex::new(r"(,( and)? | and )").unwrap();
}

fn parse_floor_level(floor: &str) -> Option<usize> {
    match floor {
        "first" => Some(1),
        "second" => Some(2),
        "third" => Some(3),
        "fourth" => Some(4),
        _ => None,
    }
}

fn parse_arrangement(input: &str) -> Arrangement {
    const EMPTY_FLOOR: Floor = Floor::new();
    let mut floors = [EMPTY_FLOOR; 4];

    input
        .lines()
        .filter_map(|line| {
            if let Some(m) = RE_FLOOR_CONTAINS.captures(line) {
                let floor_number = parse_floor_level(&m[1]).expect("should be valid floor number");
                let components: Floor = RE_SPLIT
                    .split(&m[2])
                    .filter_map(|s| {
                        if let Some(s) = s.strip_prefix("a ") {
                            if let Some(radiation_type) = s.strip_suffix("-compatible microchip") {
                                Some(Component::new_microchip(radiation_type))
                            } else if let Some(radiation_type) = s.strip_suffix(" generator") {
                                Some(Component::new_generator(radiation_type))
                            } else {
                                panic!("component with unknown suffix: {}", s)
                            }
                        } else if s == "nothing relevant" {
                            None
                        } else {
                            panic!("unknown component: {}", s)
                        }
                    })
                    .collect();
                Some((floor_number, components))
            } else {
                None
            }
        })
        .for_each(|(floor_number, mut components)| {
            components.sort();
            floors[floor_number - 1] = components;
        });

    // elevator always starts at the first floor
    floors[0].push(Component::Elevator);
    floors[0].sort();

    Arrangement::new(floors)
}

fn generate_floor_moves(
    arrangement: &Arrangement,
    current_floor_number: usize,
    new_floor_number: usize,
) -> impl Iterator<Item = (Vec<&Component>, Arrangement)> + '_ {
    arrangement[current_floor_number]
        .iter()
        .filter(|component| !matches!(component, Component::Elevator))
        .powerset()
        .filter_map(move |combination| {
            if combination.is_empty() || combination.len() > 2 {
                return None;
            }

            let mut new_floor = arrangement[new_floor_number].clone();
            new_floor.push(Component::Elevator);
            for component in &combination {
                new_floor.push((*component).clone());
            }
            new_floor.sort();

            if !is_valid_floor(&new_floor) {
                return None;
            }

            let mut new_arrangement = arrangement.clone();
            let old_floor = &mut new_arrangement[current_floor_number];
            old_floor.retain(|component| !new_floor.contains(component));
            old_floor.sort();
            new_arrangement[new_floor_number] = new_floor;

            Some((combination, new_arrangement))
        })
}

fn generate_combinations(arrangement: &Arrangement) -> impl Iterator<Item = Arrangement> + '_ {
    let elevator_floor_number = (1usize..)
        .find(|number| arrangement[*number].contains(&Component::Elevator))
        .expect("arrangement should have elevator");

    let lower_floor_number = if elevator_floor_number > 1 {
        let all_are_empty = (1..=elevator_floor_number - 1)
            .map(|n| &arrangement[n])
            .all(|floor| floor.is_empty());
        if all_are_empty {
            // Don't bother moving components down if all the below floors are empty
            None
        } else {
            Some(elevator_floor_number - 1)
        }
    } else {
        None
    };
    let higher_floor_number = if elevator_floor_number < 4 {
        Some(elevator_floor_number + 1)
    } else {
        None
    };

    let lower = lower_floor_number
        .into_iter()
        .flat_map(move |new_floor_number| {
            let moves: Vec<_> =
                generate_floor_moves(arrangement, elevator_floor_number, new_floor_number)
                    .collect();

            let has_move_of_one = moves.iter().any(|(combination, _)| combination.len() == 1);

            moves
                .into_iter()
                .filter(move |(combination, _)| {
                    if has_move_of_one {
                        // if we can move 1 item down, ignore the combinations moving 2
                        combination.len() == 1
                    } else {
                        true
                    }
                })
                .map(|(_, a)| a)
        });
    let higher = higher_floor_number
        .into_iter()
        .flat_map(move |new_floor_number| {
            let moves: Vec<_> =
                generate_floor_moves(arrangement, elevator_floor_number, new_floor_number)
                    .collect();

            let has_move_of_two = moves.iter().any(|(combination, _)| combination.len() == 2);

            moves
                .into_iter()
                .filter(move |(combination, _)| {
                    if has_move_of_two {
                        // if we can move 2 items up, ignore the combinations moving only 1
                        combination.len() == 2
                    } else {
                        true
                    }
                })
                .map(|(_, a)| a)
        });

    chain!(lower, higher)
}

fn _solve(arrangement: Arrangement) -> usize {
    let target = Arrangement::new([
        vec![],
        vec![],
        vec![],
        arrangement
            .floors
            .iter()
            .flatten()
            .sorted()
            .cloned()
            .collect(),
    ]);

    let min_path = shortest_path(
        ArrangementWrapper::new(arrangement),
        |arrangement: &ArrangementWrapper| arrangement.inner == target,
        |arrangement: &ArrangementWrapper| {
            generate_combinations(&arrangement.inner)
                .map(ArrangementWrapper::new)
                .collect::<Vec<_>>() // FIXME: don't collect
        },
        |_: &ArrangementWrapper| 0,
    );

    min_path.expect("a solution").len() - 1
}

pub fn solve_part1(input: &str) -> usize {
    let arrangement = parse_arrangement(input);
    _solve(arrangement)
}

pub fn solve_part2(input: &str) -> usize {
    let mut arrangement = parse_arrangement(input);
    arrangement[1].extend(vec![
        Component::new_generator("elerium"),
        Component::new_microchip("elerium"),
        Component::new_generator("dilithium"),
        Component::new_microchip("dilithium"),
    ]);

    _solve(arrangement)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parsing() {
        let input = r#"The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant."#;
        assert_eq!(
            parse_arrangement(input),
            Arrangement::new([
                vec![
                    Component::new_microchip("hydrogen"),
                    Component::new_microchip("lithium"),
                    Component::Elevator
                ],
                vec![Component::new_generator("hydrogen")],
                vec![Component::new_generator("lithium")],
                vec![],
            ])
        );
    }

    #[test]
    fn test_is_valid_floor() {
        // valid floors
        assert!(is_valid_floor(&vec![]));
        assert!(is_valid_floor(&vec![
            Component::Elevator,
            Component::new_generator("bar")
        ]));
        assert!(is_valid_floor(&vec![
            Component::new_generator("foo"),
            Component::new_microchip("foo")
        ]));
        assert!(is_valid_floor(&vec![Component::new_microchip("bar")]));

        // invalid floors
        assert!(!is_valid_floor(&vec![
            Component::new_generator("bar"),
            Component::new_microchip("foo")
        ]));
    }

    #[test]
    fn test_arrangement_wrapper() {
        let arr = ArrangementWrapper::new(Arrangement::new([
            vec![
                Component::new_microchip("hydrogen"),
                Component::new_microchip("lithium"),
                Component::Elevator,
            ],
            vec![Component::new_generator("hydrogen")],
            vec![Component::new_generator("lithium")],
            vec![],
        ]));
        let expected: u64 = (1 << 2 | 1 << 1 | 1) << 0 | (1 << 3) << 16 | (1 << 4) << 32 | 0 << 24;

        assert_eq!(
            format!("{:0128b}", arr.simplified_state),
            format!("{:0128b}", expected)
        );
    }

    #[test]
    fn test_part1() {
        let input = r#"The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant."#;
        assert_eq!(solve_part1(input), 11);
    }

    crate::create_solver_test!(year2016, day11, part1, verify_answer = true);
    crate::create_solver_test!(year2016, day11, part2, verify_answer = true);
}
