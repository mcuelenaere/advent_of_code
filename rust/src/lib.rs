extern crate core;

use pyo3::prelude::*;

pub(crate) mod utils;
mod year2016;
mod year2018;
mod year2021;
mod year2022;

#[cfg(test)]
macro_rules! create_solver_test {
    ($part:ident) => {
        paste::paste! {
            #[test]
            fn [<test_solve_ $part>]() {
                use itertools::Itertools;
                use std::fs::read_to_string;
                use std::path::Path;

                let (year, day) = file!()
                    .strip_prefix("src/").unwrap()
                    .strip_suffix(".rs").unwrap()
                    .splitn(2, "/")
                    .collect_tuple().unwrap()
                ;

                let puzzle_path = Path::new(file!())
                    .parent().unwrap()
                    .join("../../../puzzles/")
                    .join(year)
                    .join(day)
                ;
                assert!(puzzle_path.is_dir());

                let input_path = puzzle_path.join("input.txt");
                assert!(input_path.is_file());

                let input = read_to_string(input_path).unwrap();
                let input = input.strip_suffix("\n").unwrap();

                let actual = super::[<solve_ $part>](input).to_string();
                println!("answer: {}", actual);

                let expected_path = puzzle_path.join(format!("answer-{}.txt", stringify!($part)));
                if expected_path.is_file() {
                    let expected = read_to_string(expected_path).unwrap();
                    assert_eq!(actual, expected);
                } else {
                    println!("expected file not found, could not verify answer");
                }
            }
        }
    };
}

#[cfg(test)]
pub(crate) use create_solver_test;

macro_rules! register_year {
    ($year:ident => [$($day:ident),+]) => {
        $(
            paste::paste! {
                fn [<register_ $year _ $day>](py: Python, parent: &PyModule) -> PyResult<()> {
                    let child = PyModule::new(py, stringify!($day))?;

                    #[pyfunction]
                    fn part1(input: String) -> String {
                        $year::$day::solve_part1(input.as_str()).to_string()
                    }
                    child.add_function(wrap_pyfunction!(part1, child)?)?;

                    #[pyfunction]
                    fn part2(input: String) -> String {
                        $year::$day::solve_part2(input.as_str()).to_string()
                    }
                    child.add_function(wrap_pyfunction!(part2, child)?)?;

                    parent.add_submodule(child)?;
                    Ok(())
                }
            }
        )*

        paste::paste! {
            fn [<register_ $year>](py: Python, parent: &PyModule) -> PyResult<()> {
                let child = PyModule::new(py, stringify!($year))?;
                $(
                    [<register_ $year _ $day>](py, child)?;
                )*
                parent.add_submodule(child)?;
                Ok(())
            }
        }
    };
}

register_year!(year2016 => [
    day10, day11, day12, day13, day14, day15, day16, day17, day18, day19,
    day20, day21, day22, day23, day24, day25
]);
register_year!(year2018 => [day19, day20, day21, day22]);
register_year!(year2021 => [
    day01, day02, day03, day04, day05, day06, day07, day08, day09, day10,
    day11, day12, day13, day14, day15, day16, day17, day18, day20,
    day25
]);
register_year!(year2022 => [
    day01, day02, day03, day04, day05, day06
]);

#[pymodule]
fn aoc_rust(py: Python, m: &PyModule) -> PyResult<()> {
    register_year2016(py, m)?;
    register_year2018(py, m)?;
    register_year2021(py, m)?;
    register_year2022(py, m)?;
    Ok(())
}
