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
