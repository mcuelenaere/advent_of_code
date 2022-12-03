use itertools::Itertools;
use std::collections::{HashMap, HashSet};

fn sort_string(s: &str) -> String {
    String::from_iter(s.chars().sorted())
}

#[derive(Debug)]
struct NoteEntry<'a> {
    inputs: Vec<&'a str>,
    output: Vec<&'a str>,
}

impl NoteEntry<'_> {
    fn find_digits(&self) -> impl Iterator<Item = (&str, usize)> + '_ {
        let mut mapping: HashMap<usize, &str> = HashMap::new();

        // first find the easy ones
        let mut six_segments = Vec::new();
        let mut five_segments = Vec::new();
        for signal_pattern in &self.inputs {
            match signal_pattern.len() {
                2 => {
                    mapping.insert(1, *signal_pattern);
                }
                3 => {
                    mapping.insert(7, *signal_pattern);
                }
                4 => {
                    mapping.insert(4, *signal_pattern);
                }
                7 => {
                    mapping.insert(8, *signal_pattern);
                }
                5 => {
                    five_segments.push(*signal_pattern);
                }
                6 => {
                    six_segments.push(*signal_pattern);
                }
                _ => {}
            }
        }
        assert_eq!(mapping.len(), 4);
        assert_eq!(five_segments.len(), 3);
        assert_eq!(six_segments.len(), 3);

        // to find 9, we look for a six_segment that is closest to 4+7
        {
            let four_and_seven: HashSet<char> =
                HashSet::from_iter(mapping[&4].chars().chain(mapping[&7].chars()));
            six_segments.retain(|signal_pattern| {
                let overlap = signal_pattern
                    .chars()
                    .filter(|c| four_and_seven.contains(c))
                    .count();
                if overlap == 5 {
                    mapping.insert(9, *signal_pattern);
                    false
                } else {
                    true
                }
            });
        }
        assert_eq!(mapping.len(), 5);
        assert_eq!(six_segments.len(), 2);

        // to find 6 and 0, we look for the overlap with 1 in the remaining two six_segments
        {
            let one: HashSet<char> = HashSet::from_iter(mapping[&1].chars());
            six_segments.retain(|signal_pattern| {
                let overlap = signal_pattern.chars().filter(|c| one.contains(c)).count();
                match overlap {
                    2 => {
                        // this is 0
                        mapping.insert(0, *signal_pattern);
                        false
                    }
                    1 => {
                        // this is 6
                        mapping.insert(6, *signal_pattern);
                        false
                    }
                    _ => true,
                }
            });
        }
        assert_eq!(mapping.len(), 7);
        assert_eq!(six_segments.len(), 0);

        // to find 2, 3 and 5, we compare each with 6 and 9 and count the overlapping segments
        {
            let six: HashSet<char> = HashSet::from_iter(mapping[&6].chars());
            let nine: HashSet<char> = HashSet::from_iter(mapping[&9].chars());
            five_segments.retain(|signal_pattern| {
                let six_overlap = signal_pattern.chars().filter(|c| six.contains(c)).count();
                let nine_overlap = signal_pattern.chars().filter(|c| nine.contains(c)).count();

                match (six_overlap, nine_overlap) {
                    (5, 5) => {
                        // this is 5
                        mapping.insert(5, *signal_pattern);
                        false
                    }
                    (4, 4) => {
                        // this is 2
                        mapping.insert(2, *signal_pattern);
                        false
                    }
                    (4, 5) => {
                        // this is 3
                        mapping.insert(3, *signal_pattern);
                        false
                    }
                    _ => true,
                }
            })
        }
        assert_eq!(mapping.len(), 10);
        assert_eq!(five_segments.len(), 0);

        mapping
            .into_iter()
            .map(|(number, signal_pattern)| (signal_pattern, number))
    }

    pub fn decode_output(&self) -> usize {
        let mapping: HashMap<_, _> = self
            .find_digits()
            .map(|(signal_pattern, digit)| (sort_string(signal_pattern), digit))
            .collect();

        let mut value = 0usize;
        for signal_pattern in &self.output {
            value *= 10;
            value += mapping[&sort_string(signal_pattern)];
        }
        value
    }
}

fn parse_notes(input: &str) -> impl Iterator<Item = NoteEntry<'_>> + '_ {
    input.lines().map(|line| {
        let (left, right) = line.splitn(2, " | ").collect_tuple().expect("2 strings");
        NoteEntry {
            inputs: left.split(' ').collect_vec(),
            output: right.split(' ').collect_vec(),
        }
    })
}

pub fn solve_part1(input: &str) -> usize {
    parse_notes(input)
        .flat_map(|note| note.output)
        .filter(|signal_pattern| {
            signal_pattern.len() == 2
                || signal_pattern.len() == 3
                || signal_pattern.len() == 4
                || signal_pattern.len() == 7
        })
        .count()
}

pub fn solve_part2(input: &str) -> usize {
    parse_notes(input).map(|entry| entry.decode_output()).sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let input = r#"be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"#;
        assert_eq!(solve_part1(input), 26);
    }

    #[test]
    fn test_decode_output() {
        let notes = parse_notes(
            r#"acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"#,
        )
        .collect_vec();
        println!("{:?}", notes);

        assert_eq!(notes[0].decode_output(), 5353);

        let notes = parse_notes(
            r#"be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"#,
        )
            .collect_vec();

        assert_eq!(
            notes
                .into_iter()
                .map(|note| note.decode_output())
                .collect_vec(),
            vec![8394, 9781, 1197, 9361, 4873, 8418, 4548, 1625, 8717, 4315,]
        );
    }

    #[test]
    fn test_part2() {
        let input = r#"be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"#;
        assert_eq!(solve_part2(input), 61229);
    }

    crate::create_solver_test!(part1);
    crate::create_solver_test!(part2);
}
