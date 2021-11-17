use crate::utils::graph::shortest_path;
use itertools::Itertools;
use lazy_static::lazy_static;
use regex::Regex;
use std::collections::HashMap;

type Coordinate = crate::utils::grid::Coordinate<0, 0, { isize::MAX }, { isize::MAX }>;

#[derive(Debug, Clone, Eq, PartialEq, Hash)]
struct Node {
    position: Coordinate,
    size: usize,
    used: usize,
}

impl Node {
    pub fn avail(&self) -> usize {
        self.size - self.used
    }
}

lazy_static! {
    static ref RE_NODE_USAGE: Regex =
        Regex::new(r"/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%").unwrap();
}

fn parse_nodes(input: &str) -> impl Iterator<Item = Node> + '_ {
    input.lines().filter_map(|line| {
        if let Some(m) = RE_NODE_USAGE.captures(line) {
            let size: usize = m[3].parse().expect("a number");
            let used: usize = m[4].parse().expect("a number");
            let avail: usize = m[5].parse().expect("a number");
            assert_eq!(used + avail, size);

            Some(Node {
                position: Coordinate::new(
                    m[1].parse().expect("a number"),
                    m[2].parse().expect("a number"),
                )
                .unwrap(),
                size,
                used,
            })
        } else {
            None
        }
    })
}

pub fn solve_part1(input: &str) -> usize {
    parse_nodes(input)
        .permutations(2)
        .filter(|items| {
            let (a, b) = (&items[0], &items[1]);

            if a.used == 0 || a.position == b.position {
                false
            } else {
                b.avail() >= a.used
            }
        })
        .count()
}

struct Cluster(HashMap<Coordinate, Node>);

impl Cluster {
    pub fn shortest_path(
        &self,
        start: Coordinate,
        end: Coordinate,
        to_avoid: Option<Coordinate>,
    ) -> Option<Vec<Coordinate>> {
        shortest_path(
            self.0[&start].clone(),
            |node: &Node| node.position == end,
            |node: &Node| {
                node.position
                    .neighbours_cross()
                    // avoid requested position, if needed
                    .filter(|position| !matches!(to_avoid, Some(to_avoid) if to_avoid == *position))
                    .filter_map(|position| self.0.get(&position).cloned())
                    // only consider nodes that we can store in ourselves
                    .filter(|other| other.used <= node.size)
                    .collect::<Vec<_>>() // FIXME: remove collect
            },
            |node: &Node| end.manhattan_distance(&node.position),
        )
        .map(|path| path.into_iter().map(|node| node.position).collect())
    }

    pub fn nodes(&self) -> impl Iterator<Item = &Node> + '_ {
        self.0.values()
    }

    pub fn top_right_node(&self) -> Option<&Node> {
        self.nodes()
            .filter(|node| node.position.y == 0)
            .max_by_key(|node| node.position.x)
    }

    pub fn empty_node(&self) -> Option<&Node> {
        self.nodes().min_by_key(|node| node.used)
    }

    pub fn swap_nodes(&mut self, a: Coordinate, b: Coordinate) {
        let mut node_a = self.0.remove(&a).unwrap();
        let mut node_b = self.0.remove(&b).unwrap();
        node_a.position = b;
        node_b.position = a;
        self.0.insert(b, node_a);
        self.0.insert(a, node_b);
    }

    pub fn swap_nodes_on_path(&mut self, path: Vec<Coordinate>) {
        let _ = path
            .into_iter()
            .peekable()
            .batching(|iter| match (iter.next(), iter.peek()) {
                (Some(a), Some(b)) => {
                    self.swap_nodes(a, *b);
                    Some(())
                }
                _ => None,
            })
            .count();
    }
}

pub fn solve_part2(input: &str) -> usize {
    let mut cluster = Cluster(
        parse_nodes(input)
            .map(|node| (node.position, node))
            .collect(),
    );

    let path = cluster
        .shortest_path(
            cluster.top_right_node().unwrap().position,
            Coordinate::new(0, 0).unwrap(),
            None,
        )
        .unwrap();

    let mut total_steps = 0;
    for (current, target) in path.iter().skip(1).zip(path.iter()) {
        // move empty node to current
        let empty = cluster.empty_node().unwrap().position;
        if empty != *current {
            let new_path = cluster
                .shortest_path(empty, *current, Some(*target))
                .unwrap();
            total_steps += new_path.len() - 1;
            cluster.swap_nodes_on_path(new_path);
        }

        // swap target with empty node
        cluster.swap_nodes(*current, *target);
        total_steps += 1;
    }

    total_steps
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part2() {
        let input = r#"Filesystem            Size  Used  Avail  Use%
/dev/grid/node-x0-y0   10T    8T     2T   80%
/dev/grid/node-x0-y1   11T    6T     5T   54%
/dev/grid/node-x0-y2   32T   28T     4T   87%
/dev/grid/node-x1-y0    9T    7T     2T   77%
/dev/grid/node-x1-y1    8T    0T     8T    0%
/dev/grid/node-x1-y2   11T    7T     4T   63%
/dev/grid/node-x2-y0   10T    6T     4T   60%
/dev/grid/node-x2-y1    9T    8T     1T   88%
/dev/grid/node-x2-y2    9T    6T     3T   66%"#;
        assert_eq!(solve_part2(input), 7);
    }

    crate::create_solver_test!(year2016, day22, part1, verify_answer = true);
    crate::create_solver_test!(year2016, day22, part2, verify_answer = true);
}
