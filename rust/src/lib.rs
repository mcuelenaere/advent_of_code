use pyo3::prelude::*;

mod year2016;
mod year2021;

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

register_year!(year2016 => [day10]);
register_year!(year2021 => [day01]);

#[pymodule]
fn aoc_rust(py: Python, m: &PyModule) -> PyResult<()> {
    register_year2016(py, m)?;
    register_year2021(py, m)?;
    Ok(())
}
