use genawaiter::rc::gen;
use genawaiter::yield_;

type RandomNumbers = Vec<usize>;

#[derive(Debug, Default)]
struct Board {
    lines: [[(usize, bool); 5]; 5],
}

impl Board {
    pub fn mark(&mut self, number_to_mark: usize) {
        for line in &mut self.lines {
            for (number, marked) in line {
                if *number == number_to_mark {
                    *marked = true;
                }
            }
        }
    }

    fn line(&self, y: usize) -> impl Iterator<Item = &(usize, bool)> {
        self.lines[y].iter()
    }

    fn column(&self, x: usize) -> impl Iterator<Item = &(usize, bool)> {
        gen!({
            for y in 0..self.lines.len() {
                yield_!(&self.lines[y][x]);
            }
        })
        .into_iter()
    }

    pub fn is_winning(&self) -> bool {
        for y in 0..self.lines.len() {
            if self.line(y).all(|(_, marked)| *marked) {
                return true;
            }
        }

        for x in 0..self.lines.len() {
            if self.column(x).all(|(_, marked)| *marked) {
                return true;
            }
        }

        false
    }

    pub fn score(&self) -> usize {
        self.lines
            .iter()
            .flat_map(|line| line.iter())
            .filter_map(|(number, marked)| {
                if *marked == false {
                    Some(*number)
                } else {
                    None
                }
            })
            .sum()
    }
}

fn parse_boards(input: &str) -> (RandomNumbers, Vec<Board>) {
    let mut random_numbers = Vec::new();
    let mut boards = Vec::new();

    let mut current_board: Option<Board> = None;
    let mut current_board_line_index = 0;
    for (index, line) in input.lines().enumerate() {
        if index == 0 {
            random_numbers.extend(
                line.split(',')
                    .map(|text| text.parse::<usize>().expect("a valid number")),
            );
        } else if line == "" {
            // indicates a new board is about to start
            if let Some(board) = current_board.take() {
                boards.push(board);
            }
            current_board = Some(Board::default());
            current_board_line_index = 0;
        } else {
            if let Some(ref mut board) = current_board {
                line.split_ascii_whitespace()
                    .map(|text| text.parse::<usize>().expect("a valid number"))
                    .enumerate()
                    .for_each(|(index, number)| {
                        board.lines[current_board_line_index][index] = (number, false);
                    });
                current_board_line_index += 1;
            }
        }
    }

    if let Some(board) = current_board {
        boards.push(board);
    }

    (random_numbers, boards)
}

fn pick_winners(random_numbers: Vec<usize>, mut boards: Vec<Board>) -> impl Iterator<Item = usize> {
    gen!({
        for random_number in random_numbers {
            for board in &mut boards {
                board.mark(random_number);

                // check if we have a winner
                if board.is_winning() {
                    yield_!(random_number * board.score());
                }
            }

            // remove winning boards
            boards.retain(|board| !board.is_winning());
        }
    })
    .into_iter()
}

pub fn solve_part1(input: &str) -> usize {
    let (random_numbers, boards) = parse_boards(input);

    pick_winners(random_numbers, boards)
        .next()
        .expect("a winner")
}

pub fn solve_part2(input: &str) -> usize {
    let (random_numbers, boards) = parse_boards(input);

    pick_winners(random_numbers, boards)
        .last()
        .expect("a winner")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let input = r#"7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"#;
        assert_eq!(solve_part1(input), 4512);
    }

    #[test]
    fn test_part2() {
        let input = r#"7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"#;
        assert_eq!(solve_part2(input), 1924);
    }

    crate::create_solver_test!(year2021, day04, part1);
    crate::create_solver_test!(year2021, day04, part2);
}
