use itertools::Itertools;
use std::cmp::Ordering;
use std::collections::{BinaryHeap, HashMap};
use std::hash::Hash;

pub trait GetNeighbours<N> {
    type Iterator: IntoIterator<Item = N>;

    fn get_neighbours(&self, node: &N) -> Self::Iterator;
}

impl<F, I, N> GetNeighbours<N> for F
where
    F: Fn(&N) -> I,
    I: IntoIterator<Item = N>,
{
    type Iterator = I;

    fn get_neighbours(&self, node: &N) -> Self::Iterator {
        self(node)
    }
}

pub fn shortest_path<N>(
    start_node: N,
    end_node: N,
    graph: impl GetNeighbours<N>,
    heuristic: impl Fn(&N) -> usize,
) -> Option<Vec<N>>
where
    N: Hash + Eq + Clone,
{
    #[derive(Eq, PartialEq)]
    struct State<N: Eq> {
        node: N,
        cost: usize,
    }

    impl<N: Eq> PartialOrd for State<N> {
        fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
            Some(self.cmp(other))
        }
    }

    impl<N: Eq> Ord for State<N> {
        fn cmp(&self, other: &Self) -> Ordering {
            other.cost.cmp(&self.cost)
        }
    }

    let mut open_set = BinaryHeap::new();
    let mut dist: HashMap<N, usize> = HashMap::new();
    open_set.push(State {
        node: start_node.clone(),
        cost: 0,
    });
    dist.insert(start_node, 0);

    let mut path: HashMap<N, N> = HashMap::new();
    while let Some(state) = open_set.pop() {
        let State {
            node: min_node,
            cost: _,
        } = state;

        if min_node == end_node {
            let mut stack = Vec::new();
            let mut current = Some(end_node);
            while let Some(node) = current {
                stack.push(node.clone());
                current = path.remove(&node);
            }
            stack.reverse();

            return Some(stack);
        }

        let current_cost = dist[&min_node];
        for neighbour in graph.get_neighbours(&min_node) {
            let cost = current_cost + 1;

            if !dist.contains_key(&neighbour) || cost < dist[&neighbour] {
                if !open_set.iter().map(|s| &s.node).contains(&neighbour) {
                    open_set.push(State {
                        node: neighbour.clone(),
                        cost: cost + heuristic(&neighbour),
                    });
                }
                dist.insert(neighbour.clone(), cost);
                path.insert(neighbour, min_node.clone());
            }
        }
    }

    None
}
