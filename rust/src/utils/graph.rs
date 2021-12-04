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

struct SmallestCostHolder<N, C> {
    node: N,
    cost: C,
    estimated_cost: C,
}

impl<N, C: PartialEq> PartialEq for SmallestCostHolder<N, C> {
    fn eq(&self, other: &Self) -> bool {
        other.cost.eq(&self.cost) && other.estimated_cost.eq(&self.estimated_cost)
    }
}

impl<N, C: PartialEq> Eq for SmallestCostHolder<N, C> {}

impl<N, C: Ord> PartialOrd for SmallestCostHolder<N, C> {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl<N, C: Ord> Ord for SmallestCostHolder<N, C> {
    fn cmp(&self, other: &Self) -> Ordering {
        match other.estimated_cost.cmp(&self.estimated_cost) {
            Ordering::Equal => self.cost.cmp(&other.cost),
            o => o,
        }
    }
}

pub fn shortest_path_with_cost<N, C, I>(
    start_node: N,
    start_cost: C,
    is_goal: impl Fn(&N) -> bool,
    get_neighbours: impl Fn(&N) -> I,
    heuristic: impl Fn(&N) -> C,
) -> Option<Vec<(N, C)>>
where
    N: Hash + Eq + Clone,
    C: Ord + Add<Output = C> + Copy,
    I: IntoIterator<Item = (N, C)>,
{
    let mut open_set = BinaryHeap::new();
    let mut costs: HashMap<N, C> = HashMap::new();
    let mut estimated_costs: HashMap<N, C> = HashMap::new();

    costs.insert(start_node.clone(), start_cost);
    estimated_costs.insert(start_node.clone(), start_cost + heuristic(&start_node));
    open_set.push(SmallestCostHolder {
        node: start_node.clone(),
        cost: start_cost,
        estimated_cost: start_cost + heuristic(&start_node),
    });

    let mut path: HashMap<N, N> = HashMap::new();
    while let Some(state) = open_set.pop() {
        let SmallestCostHolder {
            node: min_node,
            cost: min_node_cost,
            ..
        } = state;

        if min_node_cost > estimated_costs[&min_node] {
            // We may have inserted a node several time into the binary heap if we found
            // a better way to access it. Ensure that we are currently dealing with the
            // best path and discard the others.
            continue;
        }

        if is_goal(&min_node) {
            let mut stack = Vec::new();
            let mut current = Some(min_node);
            while let Some(node) = current {
                stack.push((node.clone(), costs[&node]));
                current = path.remove(&node);
            }
            stack.reverse();

            return Some(stack);
        }

        let current_cost = costs[&min_node];
        for (neighbour, cost) in get_neighbours(&min_node) {
            let neighbour_cost = current_cost + cost;

            if !costs.contains_key(&neighbour) || neighbour_cost < costs[&neighbour] {
                let neighbour_estimated_cost = neighbour_cost + heuristic(&neighbour);

                costs.insert(neighbour.clone(), neighbour_cost);
                estimated_costs.insert(neighbour.clone(), neighbour_estimated_cost);
                path.insert(neighbour.clone(), min_node.clone());
                open_set.push(SmallestCostHolder {
                    node: neighbour.clone(),
                    cost: neighbour_cost,
                    estimated_cost: neighbour_estimated_cost,
                });
            }
        }
    }

    None
}
