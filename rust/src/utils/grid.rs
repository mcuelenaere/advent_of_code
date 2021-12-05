use genawaiter::rc::gen;
use genawaiter::yield_;

#[derive(Debug, Copy, Clone, Eq, PartialEq, Ord, PartialOrd, Hash)]
pub struct Coordinate<
    const MIN_X: isize,
    const MIN_Y: isize,
    const MAX_X: isize,
    const MAX_Y: isize,
> {
    pub x: isize,
    pub y: isize,
}

impl<const MIN_X: isize, const MIN_Y: isize, const MAX_X: isize, const MAX_Y: isize>
    Coordinate<MIN_X, MIN_Y, MAX_X, MAX_Y>
{
    pub fn new(x: isize, y: isize) -> Option<Self> {
        if x < MIN_X || x > MAX_X || y < MIN_Y || y > MAX_Y {
            None
        } else {
            Some(Coordinate { x, y })
        }
    }

    const CROSS: [(isize, isize); 4] = [(0, -1), (1, 0), (0, 1), (-1, 0)];
    const DIAGONALS: [(isize, isize); 4] = [(-1, -1), (1, -1), (1, 1), (-1, 1)];

    fn _neighbours(&self, input: [(isize, isize); 4]) -> impl Iterator<Item = Self> + '_ {
        input.into_iter().filter_map(move |(x_off, y_off)| {
            let x = self.x + x_off;
            let y = self.y + y_off;
            Coordinate::new(x, y)
        })
    }

    pub fn neighbours_cross(&self) -> impl Iterator<Item = Self> + '_ {
        self._neighbours(Self::CROSS)
    }

    pub fn neighbours_diagonal(&self) -> impl Iterator<Item = Self> + '_ {
        self._neighbours(Self::DIAGONALS)
    }

    pub fn neighbours_all(&self) -> impl Iterator<Item = Self> + '_ {
        self._neighbours(Self::CROSS)
            .chain(self._neighbours(Self::DIAGONALS))
    }

    pub fn manhattan_distance(&self, other: &Self) -> usize {
        ((self.x - other.x).abs() + (self.y - other.y).abs()) as usize
    }
}

fn plot_line_low<const MIN_X: isize, const MAX_X: isize, const MIN_Y: isize, const MAX_Y: isize>(
    start: Coordinate<MIN_X, MAX_X, MIN_Y, MAX_Y>,
    stop: Coordinate<MIN_X, MAX_X, MIN_Y, MAX_Y>,
) -> impl Iterator<Item = Coordinate<MIN_X, MAX_X, MIN_Y, MAX_Y>> {
    gen!({
        // Bresenham's line algorithm
        // https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm#All_cases
        let dx = stop.x - start.x;
        let mut dy = stop.y - start.y;
        let mut yi = 1;
        if dy < 0 {
            yi = -1;
            dy = -dy;
        }

        let mut D = (2 * dy) - dx;
        let mut y = start.y;
        for x in start.x..=stop.x {
            yield_!(Coordinate::new(x, y).unwrap());
            if D > 0 {
                y += yi;
                D += 2 * (dy - dx);
            }
            D += 2 * dy;
        }
    })
    .into_iter()
}

fn plot_line_high<
    const MIN_X: isize,
    const MAX_X: isize,
    const MIN_Y: isize,
    const MAX_Y: isize,
>(
    start: Coordinate<MIN_X, MAX_X, MIN_Y, MAX_Y>,
    stop: Coordinate<MIN_X, MAX_X, MIN_Y, MAX_Y>,
) -> impl Iterator<Item = Coordinate<MIN_X, MAX_X, MIN_Y, MAX_Y>> {
    gen!({
        // Bresenham's line algorithm
        // https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm#All_cases
        let mut dx = stop.x - start.x;
        let dy = stop.y - start.y;
        let mut xi = 1;
        if dx < 0 {
            xi = -1;
            dx = -dx;
        }

        let mut D = (2 * dx) - dy;
        let mut x = start.x;
        for y in start.y..=stop.y {
            yield_!(Coordinate::new(x, y).unwrap());
            if D > 0 {
                x += xi;
                D += 2 * (dx - dy);
            }
            D += 2 * dx;
        }
    })
    .into_iter()
}

pub fn plot_line<const MIN_X: isize, const MAX_X: isize, const MIN_Y: isize, const MAX_Y: isize>(
    start: Coordinate<MIN_X, MAX_X, MIN_Y, MAX_Y>,
    stop: Coordinate<MIN_X, MAX_X, MIN_Y, MAX_Y>,
) -> Box<dyn Iterator<Item = Coordinate<MIN_X, MAX_X, MIN_Y, MAX_Y>>> {
    // Bresenham's line algorithm
    // https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm#All_cases
    if (stop.y - start.y).abs() < (stop.x - start.x).abs() {
        if start.x > stop.x {
            Box::new(plot_line_low(stop, start))
        } else {
            Box::new(plot_line_low(start, stop))
        }
    } else {
        if start.y > stop.y {
            Box::new(plot_line_high(stop, start))
        } else {
            Box::new(plot_line_high(start, stop))
        }
    }
}
