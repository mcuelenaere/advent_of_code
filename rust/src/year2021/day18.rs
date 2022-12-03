use itertools::Itertools;
use num::Integer;
use std::cell::RefCell;
use std::fmt::{Debug, Formatter};
use std::ops::Add;
use std::rc::Rc;

#[derive(Eq, PartialEq)]
enum SnailFish {
    Element(usize),
    Pair(Rc<RefCell<SnailFish>>, Rc<RefCell<SnailFish>>),
}

impl Debug for SnailFish {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Element(number) => number.fmt(f),
            Self::Pair(left, right) => f
                .debug_list()
                .entry(&*left.as_ref().borrow())
                .entry(&*right.as_ref().borrow())
                .finish(),
        }
    }
}

impl Clone for SnailFish {
    fn clone(&self) -> Self {
        match self {
            Self::Element(number) => Self::Element(*number),
            Self::Pair(left, right) => Self::pair(
                left.as_ref().borrow().clone(),
                right.as_ref().borrow().clone(),
            ),
        }
    }
}

impl SnailFish {
    pub fn pair(left: Self, right: Self) -> Self {
        Self::Pair(Rc::new(RefCell::new(left)), Rc::new(RefCell::new(right)))
    }

    pub fn from_str(input: &str) -> Self {
        let mut stack = Vec::new();
        for c in input.chars() {
            match c {
                '[' => {
                    // do nothing
                }
                ']' => {
                    assert!(stack.len() >= 2);
                    let right = stack.pop().unwrap();
                    let left = stack.pop().unwrap();
                    stack.push(SnailFish::pair(left, right));
                }
                ',' => {
                    // do nothing
                }
                c if c.is_digit(10) => {
                    // we currently assume there is only 1 digit per number
                    let number = c.to_digit(10).unwrap() as usize;
                    stack.push(SnailFish::Element(number));
                }
                _ => panic!("unexpected character {}", c),
            }
        }

        assert_eq!(stack.len(), 1);
        stack.pop().unwrap()
    }

    fn add_to_left(&mut self, to_add: usize) {
        match self {
            Self::Element(number) => {
                *number += to_add;
            }
            Self::Pair(left, _) => {
                left.as_ref().borrow_mut().add_to_left(to_add);
            }
        }
    }

    fn add_to_right(&mut self, to_add: usize) {
        match self {
            Self::Element(number) => {
                *number += to_add;
            }
            Self::Pair(_, right) => {
                right.as_ref().borrow_mut().add_to_right(to_add);
            }
        }
    }

    fn try_explode(&self) -> bool {
        #[derive(Debug, Copy, Clone)]
        enum Side {
            Left,
            Right,
        }

        type RcSnailFish = Rc<RefCell<SnailFish>>;

        fn find_explodable(
            snailfish: &SnailFish,
            mut parents: Vec<((RcSnailFish, RcSnailFish), Side)>,
        ) -> Option<(Option<RcSnailFish>, RcSnailFish, Option<RcSnailFish>)> {
            match snailfish {
                SnailFish::Element(_) => {
                    if parents.len() - 1 >= 4 {
                        // get rid of the SnailFish::Element entry
                        parents.pop();

                        // find left, middle and right snailfish
                        let mut left = None;
                        let mut middle = None;
                        let mut right = None;
                        while let Some(((parent_left, parent_right), side)) = parents.pop() {
                            if middle.is_none() {
                                middle = match side {
                                    Side::Left => Some(parent_left.clone()),
                                    Side::Right => Some(parent_right.clone()),
                                };
                            }

                            match side {
                                Side::Left if right.is_none() => {
                                    right = Some(parent_right);
                                }
                                Side::Right if left.is_none() => {
                                    left = Some(parent_left);
                                }
                                _ => {}
                            }
                        }
                        assert!(left.is_some() || right.is_some());

                        return Some((left, middle.unwrap(), right));
                    }
                }
                SnailFish::Pair(left, right) => {
                    let mut left_parents = parents.clone();
                    left_parents.push(((left.clone(), right.clone()), Side::Left));
                    if let Some(result) = find_explodable(&*left.as_ref().borrow(), left_parents) {
                        return Some(result);
                    }

                    let mut right_parents = parents;
                    right_parents.push(((left.clone(), right.clone()), Side::Right));
                    if let Some(result) = find_explodable(&*right.as_ref().borrow(), right_parents)
                    {
                        return Some(result);
                    }
                }
            }

            None
        }

        if let Some((left_snailfish, exploder, right_snailfish)) = find_explodable(self, Vec::new())
        {
            let (left_number, right_number) = match &*exploder.as_ref().borrow() {
                Self::Pair(left, right) => {
                    match (&*left.as_ref().borrow(), &*right.as_ref().borrow()) {
                        (&SnailFish::Element(left), &SnailFish::Element(right)) => (left, right),
                        _ => unreachable!(),
                    }
                }
                _ => unreachable!(),
            };

            if let Some(fish) = left_snailfish {
                fish.borrow_mut().add_to_right(left_number);
            }
            *exploder.borrow_mut() = Self::Element(0);
            if let Some(fish) = right_snailfish {
                fish.borrow_mut().add_to_left(right_number);
            }

            true
        } else {
            false
        }
    }

    fn try_split(&mut self) -> bool {
        match self {
            Self::Element(number) => {
                if *number >= 10 {
                    let left = number.div_floor(&2);
                    let right = number.div_ceil(&2);
                    *self = Self::pair(Self::Element(left), Self::Element(right));

                    true
                } else {
                    false
                }
            }
            Self::Pair(left, right) => {
                if left.as_ref().borrow_mut().try_split() {
                    return true;
                }

                if right.as_ref().borrow_mut().try_split() {
                    return true;
                }

                false
            }
        }
    }

    fn reduce(mut self) -> Self {
        loop {
            if self.try_explode() {
                continue;
            }

            if self.try_split() {
                continue;
            }

            break;
        }

        self
    }

    pub fn magnitude(&self) -> usize {
        match self {
            Self::Element(number) => *number,
            Self::Pair(left, right) => {
                left.as_ref().borrow().magnitude() * 3 + right.as_ref().borrow().magnitude() * 2
            }
        }
    }
}

impl Add for SnailFish {
    type Output = SnailFish;

    fn add(self, other: Self) -> Self::Output {
        SnailFish::pair(self, other).reduce()
    }
}

fn parse_snailfish(input: &str) -> impl Iterator<Item = SnailFish> + '_ {
    input.lines().map(SnailFish::from_str)
}

pub fn solve_part1(input: &str) -> usize {
    parse_snailfish(input)
        .reduce(|a, b| a + b)
        .unwrap()
        .magnitude()
}

pub fn solve_part2(input: &str) -> usize {
    parse_snailfish(input)
        .combinations(2)
        .map(|mut pair| {
            let a = pair.pop().unwrap();
            let b = pair.pop().unwrap();
            (a + b).magnitude()
        })
        .max()
        .unwrap()
}

#[cfg(test)]
mod tests {
    use super::*;

    macro_rules! snailfish {
        ($number:literal) => {
            SnailFish::Element($number)
        };
        ([$left:tt, $right:tt]) => {
            SnailFish::pair(snailfish!($left), snailfish!($right))
        };
    }

    #[test]
    fn test_from_str() {
        let testcases = vec![
            ("[1,2]", snailfish!([1, 2])),
            ("[[1,2],3]", snailfish!([[1, 2], 3])),
            ("[9,[8,7]]", snailfish!([9, [8, 7]])),
            ("[[1,9],[8,5]]", snailfish!([[1, 9], [8, 5]])),
            (
                "[[[[1,2],[3,4]],[[5,6],[7,8]]],9]",
                snailfish!([[[[1, 2], [3, 4]], [[5, 6], [7, 8]]], 9]),
            ),
            (
                "[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]",
                snailfish!([[[9, [3, 8]], [[0, 9], 6]], [[[3, 7], [4, 9]], 3]]),
            ),
            (
                "[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]",
                snailfish!([
                    [[[1, 3], [5, 3]], [[1, 3], [8, 7]]],
                    [[[4, 9], [6, 9]], [[8, 2], [7, 3]]]
                ]),
            ),
        ];
        for (left, right) in testcases {
            assert_eq!(SnailFish::from_str(left), right);
        }
    }

    #[test]
    fn test_reduce() {
        let testcases = vec![
            ("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]"),
            ("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]"),
            ("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]"),
            (
                "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]",
                "[[3,[2,[8,0]]],[9,[5,[7,0]]]]",
            ),
        ];
        for (left, right) in testcases {
            assert_eq!(
                SnailFish::from_str(left).reduce(),
                SnailFish::from_str(right)
            );
        }

        assert_eq!(
            snailfish!([[[[4, 3], 4], 4], [7, [[8, 4], 9]]]) + snailfish!([1, 1]),
            snailfish!([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]])
        );
    }

    #[test]
    fn test_add() {
        let testcases = vec![
            (
                "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]",
                "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]",
                "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]",
            ),
            (
                "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]",
                "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]",
                "[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]",
            ),
            (
                "[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]",
                "[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]",
                "[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]",
            ),
            (
                "[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]",
                "[7,[5,[[3,8],[1,4]]]]",
                "[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]",
            ),
            (
                "[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]",
                "[[2,[2,2]],[8,[8,1]]]",
                "[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]",
            ),
            (
                "[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]",
                "[2,9]",
                "[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]",
            ),
            (
                "[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]",
                "[1,[[[9,3],9],[[9,0],[0,7]]]]",
                "[[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]",
            ),
            (
                "[[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]",
                "[[[5,[7,4]],7],1]",
                "[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]",
            ),
            (
                "[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]",
                "[[[[4,2],2],6],[8,7]]",
                "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]",
            ),
        ];
        for (a, b, c) in testcases {
            let a = SnailFish::from_str(a);
            let b = SnailFish::from_str(b);
            let c = SnailFish::from_str(c);
            assert_eq!(a + b, c);
        }
    }

    #[test]
    fn test_parse_snailfish() {
        let testcases = vec![
            (
                "[1,1]
[2,2]
[3,3]
[4,4]",
                "[[[[1,1],[2,2]],[3,3]],[4,4]]",
            ),
            (
                "[1,1]
[2,2]
[3,3]
[4,4]
[5,5]",
                "[[[[3,0],[5,3]],[4,4]],[5,5]]",
            ),
            (
                "[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]",
                "[[[[5,0],[7,4]],[5,5]],[6,6]]",
            ),
            (
                "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]",
                "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]",
            ),
        ];

        for (left, right) in testcases {
            assert_eq!(
                parse_snailfish(left)
                    .reduce(|left, right| left + right)
                    .unwrap(),
                SnailFish::from_str(right)
            );
        }
    }

    #[test]
    fn test_magnitude() {
        let testcases: Vec<(&str, usize)> = vec![
            ("[[1,2],[[3,4],5]]", 143),
            ("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384),
            ("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445),
            ("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791),
            ("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137),
            (
                "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]",
                3488,
            ),
        ];
        for (input, magnitude) in testcases {
            assert_eq!(SnailFish::from_str(input).magnitude(), magnitude);
        }
    }

    #[test]
    fn test_part1() {
        let input = r#"[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"#;
        assert_eq!(solve_part1(input), 4140);
    }

    #[test]
    fn test_part2() {
        let input = r#"[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"#;
        assert_eq!(solve_part2(input), 3993);
    }

    crate::create_solver_test!(part1);
    crate::create_solver_test!(part2);
}
