use std::collections::HashSet;
use std::ops::RangeInclusive;

type Pixel = (isize, isize);

#[derive(Debug)]
struct Image {
    pixels: HashSet<Pixel>,
    bounds_x: RangeInclusive<isize>,
    bounds_y: RangeInclusive<isize>,
    is_background_light: bool,
}

impl Image {
    pub fn new() -> Self {
        Image {
            pixels: HashSet::new(),
            bounds_x: 0..=0,
            bounds_y: 0..=0,
            is_background_light: false,
        }
    }

    pub fn insert(&mut self, pixel: Pixel) {
        let (x, y) = pixel;

        if !self.bounds_x.contains(&x) {
            let (start, end) = (*self.bounds_x.start(), *self.bounds_x.end());
            self.bounds_x = start.min(x)..=end.max(x);
        }

        if !self.bounds_y.contains(&y) {
            let (start, end) = (*self.bounds_y.start(), *self.bounds_y.end());
            self.bounds_y = start.min(y)..=end.max(y);
        }

        self.pixels.insert((x, y));
    }

    pub fn contains(&self, pixel: Pixel) -> bool {
        self.pixels.contains(&pixel)
    }

    pub fn within_bounds(&self, pixel: Pixel) -> bool {
        let (x, y) = pixel;
        self.bounds_x.contains(&x) && self.bounds_y.contains(&y)
    }

    pub fn bounds(&self) -> (RangeInclusive<isize>, RangeInclusive<isize>) {
        (self.bounds_x.clone(), self.bounds_y.clone())
    }

    pub fn lit_pixel_count(&self) -> usize {
        self.pixels.len()
    }
}

struct ImageEnhancementAlgorithm([bool; 512]);

impl ImageEnhancementAlgorithm {
    fn lookup_pixel(&self, value: usize) -> bool {
        self.0[value]
    }

    fn calculate_number(image: &Image, pixel: Pixel) -> usize {
        let (x, y) = pixel;

        let mut number = 0;
        for y_offs in -1..=1 {
            for x_offs in -1..=1 {
                let is_light = {
                    let pixel = (x + x_offs, y + y_offs);
                    if !image.within_bounds(pixel) {
                        image.is_background_light
                    } else {
                        image.contains(pixel)
                    }
                };

                if is_light {
                    number |= 1;
                }
                number <<= 1;
            }
        }
        number >>= 1;

        number
    }

    pub fn apply_on_image(&self, image: Image) -> Image {
        let (bounds_x, bounds_y) = image.bounds();

        let mut new_image = Image::new();
        for y in (bounds_y.start() - 1)..=(bounds_y.end() + 1) {
            for x in (bounds_x.start() - 1)..=(bounds_x.end() + 1) {
                let number = Self::calculate_number(&image, (x, y));
                let is_light = self.lookup_pixel(number);

                if is_light {
                    new_image.insert((x, y));
                }
            }
        }
        if image.is_background_light {
            new_image.is_background_light = self.lookup_pixel(0b111_111_111);
        } else {
            new_image.is_background_light = self.lookup_pixel(0b000_000_000);
        }
        new_image
    }
}

fn parse_input(input: &str) -> (ImageEnhancementAlgorithm, Image) {
    enum ParsingMode {
        ImageEnhancementAlgorithm,
        InitialImage,
    }

    let mut mode = ParsingMode::ImageEnhancementAlgorithm;
    let mut algorithm = Vec::with_capacity(512);
    let mut initial_image = Image::new();
    let mut y = 0isize;

    for line in input.lines() {
        match mode {
            ParsingMode::ImageEnhancementAlgorithm => {
                if line.is_empty() {
                    mode = ParsingMode::InitialImage;
                    continue;
                }

                for c in line.chars() {
                    let is_light = match c {
                        '#' => true,
                        '.' => false,
                        _ => panic!("unknown pixel: {}", c),
                    };
                    algorithm.push(is_light);
                }
            }
            ParsingMode::InitialImage => {
                for (x, c) in line.char_indices() {
                    if c == '#' {
                        initial_image.insert((x as isize, y));
                    }
                }
                y += 1;
            }
        }
    }
    assert_eq!(algorithm.len(), 512);

    (
        ImageEnhancementAlgorithm(algorithm.as_slice().try_into().unwrap()),
        initial_image,
    )
}

pub fn solve_part1(input: &str) -> usize {
    let (algorithm, mut image) = parse_input(input);
    for _ in 0..2 {
        image = algorithm.apply_on_image(image);
    }
    image.lit_pixel_count()
}

pub fn solve_part2(input: &str) -> usize {
    let (algorithm, mut image) = parse_input(input);
    for _ in 0..50 {
        image = algorithm.apply_on_image(image);
    }
    image.lit_pixel_count()
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_INPUT: &str = r#"..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"#;

    #[test]
    fn test_calculate_number() {
        let (_, image) = parse_input(EXAMPLE_INPUT);
        assert_eq!(
            ImageEnhancementAlgorithm::calculate_number(&image, (2, 2)),
            34
        );
    }

    #[test]
    fn test_apply_on_image() {
        let (algorithm, image) = parse_input(EXAMPLE_INPUT);
        assert_eq!(algorithm.apply_on_image(image).lit_pixel_count(), 24);
    }

    #[test]
    fn test_part1() {
        assert_eq!(solve_part1(EXAMPLE_INPUT), 35);
    }

    #[test]
    fn test_part2() {
        assert_eq!(solve_part2(EXAMPLE_INPUT), 3351);
    }

    crate::create_solver_test!(part1);
    crate::create_solver_test!(part2);
}
