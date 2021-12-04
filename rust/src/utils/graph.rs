use itertools::Itertools;
use std::cmp::Ordering;
use std::collections::{BinaryHeap, HashMap, HashSet, VecDeque};
use std::hash::Hash;
use std::marker::PhantomData;
use std::ops::Add;

pub enum VisitorAction<S> {
    Continue(S),
    Stop,
}

pub trait NodeVisitor {
    type Node;
    type State: Default;

    fn should_visit(&self, node: &Self::Node, state: &Self::State) -> bool;
    fn visit(&mut self, node: &Self::Node, state: &Self::State) -> VisitorAction<Self::State>;
}

struct ClosureVisitorWithVisitedNodesTracking<N, S, F1>
where
    N: Hash + Eq + Clone,
    F1: FnMut(&N, &S) -> VisitorAction<S>,
{
    visited_nodes: HashSet<N>,
    visit_fn: F1,
    _phantom: PhantomData<S>,
}

impl<N, S, F1> NodeVisitor for ClosureVisitorWithVisitedNodesTracking<N, S, F1>
where
    N: Hash + Eq + Clone,
    F1: FnMut(&N, &S) -> VisitorAction<S>,
    S: Default,
{
    type Node = N;
    type State = S;

    fn should_visit(&self, node: &N, _: &S) -> bool {
        !self.visited_nodes.contains(node)
    }

    fn visit(&mut self, node: &N, state: &S) -> VisitorAction<S> {
        self.visited_nodes.insert(node.clone());
        (self.visit_fn)(node, state)
    }
}

struct ClosureVisitor<N, S, F1, F2>
where
    N: Hash + Eq + Clone,
    F1: FnMut(&N, &S) -> VisitorAction<S>,
    F2: Fn(&N, &S) -> bool,
{
    visit_fn: F1,
    should_visit_fn: F2,
    _phantom: PhantomData<(N, S)>,
}

impl<N, S, F1, F2> NodeVisitor for ClosureVisitor<N, S, F1, F2>
where
    N: Hash + Eq + Clone,
    F1: FnMut(&N, &S) -> VisitorAction<S>,
    F2: Fn(&N, &S) -> bool,
    S: Default,
{
    type Node = N;
    type State = S;

    fn should_visit(&self, node: &N, state: &S) -> bool {
        (self.should_visit_fn)(node, state)
    }

    fn visit(&mut self, node: &N, state: &S) -> VisitorAction<S> {
        (self.visit_fn)(node, state)
    }
}

pub struct VisitorFactory;

impl VisitorFactory {
    pub fn with_visit<N, S, F>(visit: F) -> impl NodeVisitor<Node = N, State = S>
    where
        N: Hash + Eq + Clone,
        F: FnMut(&N, &S) -> VisitorAction<S>,
        S: Default,
    {
        ClosureVisitorWithVisitedNodesTracking {
            visited_nodes: HashSet::new(),
            visit_fn: visit,
            _phantom: PhantomData,
        }
    }

    pub fn custom<N, S, F1, F2>(
        should_visit: F2,
        visit: F1,
    ) -> impl NodeVisitor<Node = N, State = S>
    where
        N: Hash + Eq + Clone,
        F1: FnMut(&N, &S) -> VisitorAction<S>,
        F2: Fn(&N, &S) -> bool,
        S: Default,
    {
        ClosureVisitor {
            visit_fn: visit,
            should_visit_fn: should_visit,
            _phantom: PhantomData,
        }
    }
}

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

pub fn breadth_first_search<N, S>(
    start_node: N,
    graph: impl GetNeighbours<N>,
    mut node_visitor: impl NodeVisitor<Node = N, State = S>,
) where
    N: Hash + Eq + Clone,
    S: Default,
{
    let mut stack = VecDeque::new();

    match node_visitor.visit(&start_node, &S::default()) {
        VisitorAction::Continue(new_state) => stack.push_back((start_node.clone(), new_state)),
        VisitorAction::Stop => return,
    };

    while let Some((node, state)) = stack.pop_front() {
        for neighbour in graph.get_neighbours(&node) {
            if !node_visitor.should_visit(&neighbour, &state) {
                continue;
            }

            match node_visitor.visit(&neighbour, &state) {
                VisitorAction::Continue(new_state) => {
                    stack.push_back((neighbour, new_state));
                }
                VisitorAction::Stop => {}
            }
        }
    }
}

pub fn depth_first_search<N, S>(
    start_node: N,
    graph: impl GetNeighbours<N>,
    mut node_visitor: impl NodeVisitor<Node = N, State = S>,
) where
    N: Hash + Eq + Clone,
    S: Default,
{
    let mut stack = VecDeque::new();

    match node_visitor.visit(&start_node, &S::default()) {
        VisitorAction::Continue(new_state) => {
            stack.push_back((graph.get_neighbours(&start_node).into_iter(), new_state))
        }
        VisitorAction::Stop => return,
    };

    while let Some((ref mut iter, state)) = stack.front_mut() {
        if let Some(node) = iter.next() {
            if node_visitor.should_visit(&node, state) {
                match node_visitor.visit(&node, state) {
                    VisitorAction::Continue(new_state) => {
                        stack.push_back((graph.get_neighbours(&node).into_iter(), new_state));
                    }
                    VisitorAction::Stop => {}
                };
            }
        } else {
            stack.pop_front();
        }
    }
}

pub fn shortest_path<N>(
    start_node: N,
    is_goal: impl Fn(&N) -> bool,
    graph: impl GetNeighbours<N>,
    heuristic: impl Fn(&N) -> usize,
) -> Option<Vec<N>>
where
    N: Hash + Eq + Clone,
{
    shortest_path_with_cost(
        start_node,
        0,
        is_goal,
        |node| graph.get_neighbours(node).into_iter().map(|node| (node, 1)),
        heuristic,
    )
    .map(|path| path.into_iter().map(|(node, _)| node).collect_vec())
}

pub fn shortest_path_with_cost<N, C, I>(
    start_node: N,
    start_cost: C,
    is_goal: impl Fn(&N) -> bool,
    mut get_neighbours: impl FnMut(&N) -> I,
    heuristic: impl Fn(&N) -> C,
) -> Option<Vec<(N, C)>>
where
    N: Hash + Eq + Clone,
    C: Ord + Add<Output = C> + Clone,
    I: IntoIterator<Item = (N, C)>,
{
    #[derive(Eq, PartialEq)]
    struct State<N: Eq, C: Ord + Clone> {
        node: N,
        cost: C,
    }

    impl<N: Eq, C: Ord + Clone> PartialOrd for State<N, C> {
        fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
            Some(self.cmp(other))
        }
    }

    impl<N: Eq, C: Ord + Clone> Ord for State<N, C> {
        fn cmp(&self, other: &Self) -> Ordering {
            other.cost.cmp(&self.cost)
        }
    }

    let mut open_set = BinaryHeap::new();
    let mut dist: HashMap<N, C> = HashMap::new();
    open_set.push(State {
        node: start_node.clone(),
        cost: start_cost.clone(),
    });
    dist.insert(start_node, start_cost);

    let mut path: HashMap<N, N> = HashMap::new();
    while let Some(state) = open_set.pop() {
        let State {
            node: min_node,
            cost: _,
        } = state;

        if is_goal(&min_node) {
            let mut stack = Vec::new();
            let mut current = Some(min_node);
            while let Some(node) = current {
                stack.push((node.clone(), dist[&node].clone()));
                current = path.remove(&node);
            }
            stack.reverse();

            return Some(stack);
        }

        let current_cost = dist[&min_node].clone();
        for (neighbour, cost) in get_neighbours(&min_node) {
            let cost = current_cost.clone() + cost;

            if !dist.contains_key(&neighbour) || cost < dist[&neighbour] {
                if !open_set.iter().map(|s| &s.node).contains(&neighbour) {
                    open_set.push(State {
                        node: neighbour.clone(),
                        cost: cost.clone() + heuristic(&neighbour),
                    });
                }
                dist.insert(neighbour.clone(), cost);
                path.insert(neighbour, min_node.clone());
            }
        }
    }

    None
}
