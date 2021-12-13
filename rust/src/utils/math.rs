use num::Integer;

#[allow(clippy::many_single_char_names)]
fn egcd<T: Integer + Copy>(a: T, b: T) -> (T, T, T) {
    if a == T::zero() {
        (b, T::zero(), T::one())
    } else {
        let (g, x, y) = egcd(b % a, a);
        (g, y - (b / a) * x, x)
    }
}

// adapted from https://stackoverflow.com/a/9758173
fn modinverse<T: Integer + Copy>(a: T, m: T) -> Option<T> {
    let (g, x, _) = egcd(a, m);
    if g != T::one() {
        None
    } else {
        Some(x.mod_floor(&m))
    }
}

#[allow(non_snake_case)]
pub fn chinese_remainder_theorem<T: Integer + Copy>(
    entries: impl IntoIterator<Item = (T, T)>,
) -> Option<T> {
    // We solve this using Chinese Remainder Theorem (https://math.stackexchange.com/a/1108148):
    //  x = sum(a(n) * M(n) * M'(n)) % mult(m)
    let entries: Vec<_> = entries.into_iter().collect();
    let m_multiplied = entries.iter().map(|(_, m)| *m).fold(T::one(), |x, y| x * y);

    let mut result: T = T::zero();
    for (a, m) in entries {
        let M = m_multiplied / m;
        let M_accent = match modinverse(M, m) {
            Some(m) => m,
            None => return None,
        };
        result = result + a * M * M_accent;
    }
    Some(result.mod_floor(&m_multiplied))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_chinese_remainder_theorem() {
        assert_eq!(
            chinese_remainder_theorem(vec![(1, 3), (4, 5), (6, 7)]),
            Some(34)
        );
        assert_eq!(chinese_remainder_theorem(vec![(2, 3), (3, 8)]), Some(11));
        assert_eq!(
            chinese_remainder_theorem(vec![(2, 6), (5, 9), (7, 15)]),
            None
        );
        assert_eq!(chinese_remainder_theorem(vec![(-1, 25), (1, 4)]), Some(49));
    }
}
