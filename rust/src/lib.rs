use pyo3::prelude::*;

pub(crate) mod utils;
mod year2016;
mod year2018;
mod year2021;
mod year2022;

#[cfg(test)]
macro_rules! create_solver_test {
    ($year:ident, $day:ident, $part:ident, verify_answer = true) => {
        paste::paste! {
            #[test]
            fn [<test_solve_ $part>]() {
                let input = include_str!(concat!(
                    "../../../puzzles/",
                    stringify!($year),
                    "/",
                    stringify!($day),
                    "/input.txt"
                )).strip_suffix("\n").unwrap();
                let expected = include_str!(concat!(
                    "../../../puzzles/",
                    stringify!($year),
                    "/",
                    stringify!($day),
                    "/answer-",
                    stringify!($part),
                    ".txt"
                ));
                let actual = crate::$year::$day::[<solve_ $part>](input).to_string();
                assert_eq!(actual, expected);
            }
        }
    };
    ($year:ident, $day:ident, $part:ident) => {
        paste::paste! {
            #[test]
            fn [<test_solve_ $part>]() {
                let input = include_str!(concat!(
                    "../../../puzzles/",
                    stringify!($year),
                    "/",
                    stringify!($day),
                    "/input.txt"
                )).strip_suffix("\n").unwrap();
                println!("answer: {}", crate::$year::$day::[<solve_ $part>](input));
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
    day01, day02
]);

#[pymodule]
fn aoc_rust(py: Python, m: &PyModule) -> PyResult<()> {
    register_year2016(py, m)?;
    register_year2018(py, m)?;
    register_year2021(py, m)?;
    register_year2022(py, m)?;
    Ok(())
}
