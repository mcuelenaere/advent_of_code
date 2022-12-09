use itertools::Itertools;
use std::collections::HashMap;

type Filesystem<'a> = HashMap<Vec<&'a str>, usize>;

fn parse_terminal_output(text: &str) -> Filesystem<'_> {
    let mut stack = vec![];
    let mut filesystem = Filesystem::new();
    let mut in_listing = false;
    for line in text.lines() {
        if in_listing && line.starts_with("$ ") {
            in_listing = false;
        }

        if in_listing {
            if line.starts_with("dir ") {
                // ignore
                continue;
            }
            let (size, name) = line.split_once(' ').expect("space separator");

            let mut path = stack.clone();
            path.push(name);

            filesystem.insert(path, size.parse().expect("a valid number"));
        } else {
            if line.starts_with("$ cd ") {
                let name = line.strip_prefix("$ cd ").unwrap();
                if name == ".." {
                    stack.pop().expect("not empty");
                } else {
                    stack.push(name);
                }
            } else if line == "$ ls" {
                in_listing = true;
            }
        }
    }

    filesystem
}

fn calculate_directory_sizes<'fs, 'input: 'fs>(
    fs: &'fs Filesystem<'input>,
) -> impl Iterator<Item = (&'fs [&'input str], usize)> + 'fs {
    // calculate unique prefixes
    let directories = fs
        .keys()
        .flat_map(|path| (1..path.len()).map(|end| &path[0..end]))
        .unique();

    directories.map(|path| {
        let total_size: usize = fs
            .iter()
            .filter(|(other, _)| other.starts_with(path))
            .map(|(_, size)| size)
            .sum();
        (path, total_size)
    })
}

pub fn solve_part1(input: &str) -> usize {
    let fs = parse_terminal_output(input);

    calculate_directory_sizes(&fs)
        .map(|(_, total_size)| total_size)
        .filter(|total_size| *total_size <= 100000usize)
        .sum()
}

pub fn solve_part2(input: &str) -> usize {
    let fs = parse_terminal_output(input);
    let directory_sizes: HashMap<_, _> = calculate_directory_sizes(&fs).collect();

    let root_size = directory_sizes
        .get(vec!["/"].as_slice())
        .expect("root size to be known");
    let unused_space = 70000000usize - root_size;
    let space_needing_to_be_freed = 30000000usize - unused_space;

    directory_sizes
        .values()
        .filter(|size| **size >= space_needing_to_be_freed)
        .min()
        .map(Clone::clone)
        .expect("directory to be available")
}

#[cfg(test)]
mod tests {
    use super::*;

    static TEST_INPUT: &str = r#"$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"#;

    #[test]
    fn test_part1() {
        assert_eq!(solve_part1(TEST_INPUT), 95437);
    }

    #[test]
    fn test_part2() {
        assert_eq!(solve_part2(TEST_INPUT), 24933642);
    }

    crate::create_solver_test!(part1);
    crate::create_solver_test!(part2);
}
