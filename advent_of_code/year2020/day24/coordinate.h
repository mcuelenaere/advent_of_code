#ifndef __COORDINATE_H_
#define __COORDINATE_H_

class Coordinate {
public:
    int x, y;

    Coordinate(): x(0), y(0) {}
    Coordinate(int _x, int _y): x(_x), y(_y) {}
    bool operator==(const Coordinate &o) const {
        return x == o.x && y == o.y;
    }
    friend Coordinate operator+(const Coordinate &left, const Coordinate &right) {
        Coordinate result = left;
        result.x += right.x;
        result.y += right.y;
        return result;
    }
};

class CoordinateHasher {
public:
    size_t operator()(const Coordinate& c) const
    {
        return c.x + (c.y << 8);
    }
};

#endif /* __COORDINATE_H_ */
