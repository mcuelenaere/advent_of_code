use std::collections::HashSet;

type Coordinate = crate::utils::grid::Coordinate<0, 0, 9, 9>;

#[derive(Debug, Eq, PartialEq)]
struct Grid([[usize; 10]; 10]);

impl Grid {
    fn coordinates() -> impl Iterator<Item = Coordinate> {
        (0..10).flat_map(|y| (0..10).map(move |x| Coordinate::new(x, y).unwrap()))
    }

    pub fn step(&mut self) -> HashSet<Coordinate> {
        let mut flashed = HashSet::new();
        let mut flash_stack = Vec::new();
        for coordinate in Self::coordinates() {
            let x = coordinate.x as usize;
            let y = coordinate.y as usize;
            self.0[x][y] += 1;
            if self.0[x][y] > 9 {
                flash_stack.push(coordinate);
                flashed.insert(coordinate);
                self.0[x][y] = 0;
            }
        }

        while let Some(coordinate) = flash_stack.pop() {
            for neighbour in coordinate.neighbours_all() {
                if flashed.contains(&neighbour) {
                    continue;
                }

                let x = neighbour.x as usize;
                let y = neighbour.y as usize;
                self.0[x][y] += 1;
                if self.0[x][y] > 9 {
                    flash_stack.push(neighbour);
                    flashed.insert(neighbour);
                    self.0[x][y] = 0;
                }
            }
        }

        flashed
    }
}

fn parse_grid(input: &str) -> Grid {
    let mut grid: [[usize; 10]; 10] = Default::default();
    input
        .lines()
        .enumerate()
        .flat_map(|(y, line)| {
            line.char_indices()
                .map(move |(x, c)| ((x, y), c.to_digit(10).unwrap() as usize))
        })
        .for_each(|((x, y), value)| {
            grid[x][y] = value;
        });

    Grid(grid)
}

pub fn solve_part1(input: &str) -> usize {
    let mut grid = parse_grid(input);

    let mut flashes = 0;
    for _ in 0..100 {
        let flashed_octopuses = grid.step();
        flashes += flashed_octopuses.len();
    }

    flashes
}

pub fn solve_part2(input: &str) -> usize {
    let mut grid = parse_grid(input);

    let mut step_counter = 0;
    loop {
        step_counter += 1;
        let flashed_octopuses = grid.step();
        if flashed_octopuses.len() == 100 {
            return step_counter;
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_step() {
        let mut grid = parse_grid(
            r#"5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"#,
        );
        let step_outcomes = [
            "6594254334
3856965822
6375667284
7252447257
7468496589
5278635756
3287952832
7993992245
5957959665
6394862637",
            "8807476555
5089087054
8597889608
8485769600
8700908800
6600088989
6800005943
0000007456
9000000876
8700006848",
            "0050900866
8500800575
9900000039
9700000041
9935080063
7712300000
7911250009
2211130000
0421125000
0021119000",
            "2263031977
0923031697
0032221150
0041111163
0076191174
0053411122
0042361120
5532241122
1532247211
1132230211",
            "4484144000
2044144000
2253333493
1152333274
1187303285
1164633233
1153472231
6643352233
2643358322
2243341322",
            "5595255111
3155255222
3364444605
2263444496
2298414396
2275744344
2264583342
7754463344
3754469433
3354452433",
            "6707366222
4377366333
4475555827
3496655709
3500625609
3509955566
3486694453
8865585555
4865580644
4465574644",
            "7818477333
5488477444
5697666949
4608766830
4734946730
4740097688
6900007564
0000009666
8000004755
6800007755",
            "9060000644
7800000976
6900000080
5840000082
5858000093
6962400000
8021250009
2221130009
9111128097
7911119976",
            "0481112976
0031112009
0041112504
0081111406
0099111306
0093511233
0442361130
5532252350
0532250600
0032240000",
        ]
        .map(parse_grid);

        for expected_outcome in step_outcomes {
            grid.step();
            assert_eq!(grid, expected_outcome);
        }
    }

    #[test]
    fn test_part1() {
        let input = r#"5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"#;
        assert_eq!(solve_part1(input), 1656);
    }

    #[test]
    fn test_part2() {
        let input = r#"5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"#;
        assert_eq!(solve_part2(input), 195);
    }

    crate::create_solver_test!(year2021, day11, part1);
    crate::create_solver_test!(year2021, day11, part2);
}
