use itertools::Itertools;
use itertools::MinMaxResult::MinMax;
use std::collections::HashMap;

type Element = char;

#[derive(Debug)]
struct PolymerFormula<'a> {
    polymer_template: &'a str,
    pair_insertion_rules: HashMap<(Element, Element), Element>,
}

fn parse_instructions(input: &str) -> PolymerFormula<'_> {
    let mut polymer_template = "";
    let mut pair_insertion_rules = HashMap::new();
    for (idx, line) in input.lines().enumerate() {
        if idx == 0 {
            polymer_template = line;
        } else if idx == 1 {
            continue;
        } else {
            let (left, right) = line.splitn(2, " -> ").collect_tuple().expect("2 strings");
            pair_insertion_rules.insert(
                left.chars().collect_tuple().expect("2 characters"),
                right.chars().next().expect("a character"),
            );
        }
    }
    PolymerFormula {
        polymer_template,
        pair_insertion_rules,
    }
}

fn _solve(formula: PolymerFormula, rounds: usize) -> usize {
    // convert to intermediate format
    let mut pair_counts: HashMap<(Element, Element), usize> = HashMap::new();
    let polymer_template_bigrams = formula
        .polymer_template
        .chars()
        .zip(formula.polymer_template.chars().skip(1));
    for bigram in polymer_template_bigrams {
        *pair_counts.entry(bigram).or_default() += 1;
    }
    let mut first_pair = (
        formula.polymer_template.chars().nth(0).unwrap(),
        formula.polymer_template.chars().nth(1).unwrap(),
    );

    // apply pair insertion
    for _ in 0..rounds {
        pair_counts = {
            let mut new_pair_counts = HashMap::new();
            for (bigram, count) in pair_counts.into_iter() {
                let new_element = formula.pair_insertion_rules.get(&bigram).expect("an entry");
                *new_pair_counts.entry((bigram.0, *new_element)).or_default() += count;
                *new_pair_counts.entry((*new_element, bigram.1)).or_default() += count;
            }

            new_pair_counts
        };
        first_pair = {
            let new_right = formula
                .pair_insertion_rules
                .get(&first_pair)
                .expect("an entry");
            (first_pair.0, *new_right)
        };
    }

    // convert to frequency table of elements
    let mut freq_table: HashMap<Element, usize> = HashMap::new();
    for (bigram, count) in pair_counts.into_iter() {
        if bigram == first_pair {
            *freq_table.entry(bigram.0).or_default() += count;
        }
        *freq_table.entry(bigram.1).or_default() += count;
    }

    if let MinMax(least_common, most_common) =
        freq_table.into_iter().minmax_by_key(|(_, count)| *count)
    {
        most_common.1 - least_common.1
    } else {
        panic!("could not calculate min and max")
    }
}

pub fn solve_part1(input: &str) -> usize {
    let formula = parse_instructions(input);
    _solve(formula, 10)
}

pub fn solve_part2(input: &str) -> usize {
    let formula = parse_instructions(input);
    _solve(formula, 40)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let input = r#"NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"#;
        assert_eq!(solve_part1(input), 1588);
    }

    #[test]
    fn test_part2() {
        let input = r#"NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"#;
        assert_eq!(solve_part2(input), 2188189693529);
    }

    crate::create_solver_test!(part1);
    crate::create_solver_test!(part2);
}
