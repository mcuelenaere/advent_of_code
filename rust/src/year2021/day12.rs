use crate::utils::graph::{breadth_first_search, NodeVisitor, VisitorAction, VisitorFactory};
use itertools::Itertools;
use std::collections::HashMap;

#[derive(Debug, Copy, Clone, Eq, PartialEq, Hash)]
enum Cave<'a> {
    Start,
    End,
    Small(&'a str),
    Big(&'a str),
}

type CaveMap<'a> = HashMap<Cave<'a>, Vec<Cave<'a>>>;

fn parse_cave_map(input: &str) -> CaveMap<'_> {
    let mut cave = CaveMap::new();
    for line in input.lines() {
        let (src, dst) = line
            .splitn(2, '-')
            .map(|cave| match cave {
                "start" => Cave::Start,
                "end" => Cave::End,
                cave if cave.chars().all(|c| c.is_ascii_lowercase()) => Cave::Small(cave),
                cave if cave.chars().all(|c| c.is_ascii_uppercase()) => Cave::Big(cave),
                cave => panic!("invalid cave: {}", cave),
            })
            .collect_tuple()
            .expect("2 items");
        cave.entry(src).or_default().push(dst);
        cave.entry(dst).or_default().push(src);
    }
    cave
}

fn visit_caves<'a>(cave_map: CaveMap<'a>, visitor: impl NodeVisitor<Node = Cave<'a>>) {
    breadth_first_search(
        Cave::Start,
        |cave| {
            cave_map
                .get(cave)
                .map(|caves| caves.iter().cloned().collect_vec())
                .unwrap_or(vec![])
        },
        visitor,
    );
}

pub fn solve_part1(input: &str) -> usize {
    let cave_map = parse_cave_map(input);

    let mut path_count = 0;
    visit_caves(
        cave_map,
        VisitorFactory::custom_visitor(
            |cave: &Cave<'_>, path: &Vec<Cave<'_>>| {
                match cave {
                    Cave::Start => {
                        // should not revisit start cave
                        false
                    }
                    Cave::End => {
                        // must be able to reach the end cave
                        true
                    }
                    Cave::Big(_) => {
                        // may always (re)visit big caves
                        true
                    }
                    Cave::Small(_) => {
                        // may only visit small caves once
                        !path.contains(cave)
                    }
                }
            },
            |cave: &Cave<'_>, path: &Vec<Cave<'_>>| {
                if *cave == Cave::End {
                    path_count += 1;
                    VisitorAction::Stop
                } else {
                    let mut new_path = path.clone();
                    new_path.push(*cave);
                    VisitorAction::Continue(new_path)
                }
            },
        ),
    );

    path_count
}

pub fn solve_part2(input: &str) -> usize {
    let cave_map = parse_cave_map(input);

    let mut path_count = 0;
    visit_caves(
        cave_map,
        VisitorFactory::custom_visitor(
            |cave: &Cave<'_>, (seen_caves, has_visited_twice): &(Vec<Cave<'_>>, bool)| {
                match cave {
                    Cave::Start => {
                        // should not revisit start cave
                        false
                    }
                    Cave::End => {
                        // must be able to reach the end cave
                        true
                    }
                    Cave::Big(_) => {
                        // may always (re)visit big caves
                        true
                    }
                    Cave::Small(_) => {
                        if *has_visited_twice {
                            // may only visit small caves once
                            !seen_caves.contains(cave)
                        } else {
                            // may visit a small cave twice
                            true
                        }
                    }
                }
            },
            |cave: &Cave<'_>, (seen_caves, has_visited_twice): &(Vec<Cave<'_>>, bool)| {
                if *cave == Cave::End {
                    path_count += 1;
                    VisitorAction::Stop
                } else {
                    let (has_visited_twice, seen_caves) = if matches!(cave, Cave::Small(_)) {
                        let has_visited_twice = *has_visited_twice || seen_caves.contains(cave);
                        let mut seen_caves = seen_caves.clone();
                        seen_caves.push(*cave);
                        (has_visited_twice, seen_caves)
                    } else {
                        (*has_visited_twice, seen_caves.clone())
                    };
                    VisitorAction::Continue((seen_caves, has_visited_twice))
                }
            },
        ),
    );

    path_count
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE1: &str = r#"start-A
start-b
A-c
A-b
b-d
A-end
b-end"#;
    const EXAMPLE2: &str = r#"dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"#;
    const EXAMPLE3: &str = r#"fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"#;

    #[test]
    fn test_part1() {
        assert_eq!(solve_part1(EXAMPLE1), 10);
        assert_eq!(solve_part1(EXAMPLE2), 19);
        assert_eq!(solve_part1(EXAMPLE3), 226);
    }

    #[test]
    fn test_part2() {
        assert_eq!(solve_part2(EXAMPLE1), 36);
        assert_eq!(solve_part2(EXAMPLE2), 103);
        assert_eq!(solve_part2(EXAMPLE3), 3509);
    }

    crate::create_solver_test!(part1);
    crate::create_solver_test!(part2);
}
