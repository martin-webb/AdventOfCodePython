# flake8: noqa[E501]
from dataclasses import dataclass
from functools import partial
from itertools import combinations
import math
from time import time
from typing import Optional

YEAR = 2023
DAY = 24
NAME = "Never Tell Me The Odds"


@dataclass
class Vec2:
    x: float
    y: float

    def __add__(self, other: "Vec2") -> "Vec2":
        if not isinstance(other, Vec2):
            raise TypeError(
                f"Expected Vec2, got '{other.__class__.__name__}'")
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vec2") -> "Vec2":
        if not isinstance(other, Vec2):
            raise NotImplementedError
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float) -> "Vec2":
        if not isinstance(other, int) and not isinstance(other, float):
            raise TypeError(
                f"Expected float, got '{other.__class__.__name__}'")
        return Vec2(self.x * other, self.y * other)

    __rmul__ = __mul__

    def length(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y)

    def normalise(self) -> "Vec2":
        length = self.length()
        return Vec2(self.x / length, self.y / length)

    def dot(self, other: "Vec2") -> float:
        if not isinstance(other, Vec2):
            raise TypeError(f"Expected Vec2, got '{other.__class__.__name__}'")
        return (self.x * other.x + self.y * other.y)

    def perpendicular(self) -> "Vec2":
        return Vec2(-self.y, self.x)


@dataclass(eq=True, order=True)
class Vec3:
    x: float
    y: float
    z: float


@dataclass
class Hailstone:
    p: Vec3
    v: Vec3


@dataclass
class Range:
    min: float
    max: float


@dataclass
class Intersection2:
    s: float
    t: float
    position: Vec2


def line_line_intersection_2d(
    o1: Vec2,
    o2: Vec2,
    d1: Vec2,
    d2: Vec2
) -> Optional[Intersection2]:

    if d1.dot(d2.perpendicular()) == 0.0:
        return None

    s = ((o2 - o1).dot(d2.perpendicular())) / (d1.dot(d2.perpendicular()))
    t = ((o1 - o2).dot(d1.perpendicular())) / (d2.dot(d1.perpendicular()))
    rs = o1 + (d1 * s)
    rt = o2 + (d2 * t)

    if not (math.isclose(rs.x, rt.x) and math.isclose(rs.y, rt.y)):
        return None

    return Intersection2(s=s, t=t, position=rs)


def count_collisions_2d(hailstones: list[Hailstone], r: Range) -> int:
    num_collisions = 0

    for a, b in combinations(hailstones, 2):
        o1 = Vec2(a.p.x, a.p.y)
        o2 = Vec2(b.p.x, b.p.y)
        d1 = Vec2(a.v.x, a.v.y).normalise()
        d2 = Vec2(b.v.x, b.v.y).normalise()
        intersection = line_line_intersection_2d(o1, o2, d1, d2)

        if intersection is not None:
            intersects_x = r.min <= intersection.position.x <= r.max
            intersects_y = r.min <= intersection.position.y <= r.max
            intersects_in_past = intersection.s < 0.0 or intersection.t < 0.0
            if intersects_x and intersects_y and not intersects_in_past:
                num_collisions += 1

    return num_collisions


def gauss_jordan(M: list[list[float]]) -> list[float]:
    n = len(M)

    for i in range(0, n):
        col_values = sorted([(k, abs(M[k][i])) for k in range(i+1, n)],
                            key=lambda item: item[1],
                            reverse=True)
        p = col_values[0][0] if len(col_values) > 0 else i

        for k in range(i, n+1):
            M[p][k], M[i][k] = M[i][k], M[p][k]

        for k in range(i+1, n):
            c = -M[k][i] / M[i][i]
            for j in range(i, n+1):
                if i == j:
                    M[k][j] = 0
                else:
                    M[k][j] += c * M[i][j]

    x = [0.0] * n
    for i in range(n-1, -1, -1):
        x[i] = M[i][n] / M[i][i]
        for k in range(i-1, -1, -1):
            M[k][n] -= M[k][i] * x[i]

    return x


def parse_input(input: str) -> list[Hailstone]:
    hailstones = []

    for line in input.strip().split("\n"):
        position_str, velocity_str = line.split("@")
        position = Vec3(*[float(n) for n in position_str.split(",")])
        velocity = Vec3(*[float(n) for n in velocity_str.split(",")])
        hailstones.append(Hailstone(position, velocity))

    return hailstones


def part1(input: str, r: Range) -> int:
    h = parse_input(input)
    num_collisions = count_collisions_2d(h, r)
    return num_collisions


def part2(input: str) -> int:
    h = parse_input(input)

    # 1) For a hailstone h1:
    # rx + (t * rdx) = h1x + (t * h1dx)
    # ry + (t * rdy) = h1y + (t * h1dy)
    # rz + (t * rdz) = h1z + (t * h1dz)

    # 2) Rearrange to solve for t:
    # t = (rx - h1x) / (h1dx - rdx)
    # t = (ry - h1y) / (h1dy - rdy)
    # t = (rz - h1z) / (h1dz - rdz)

    # 3) Taking two axes (here X and Y):
    # (rx - h1x) / (h1dx - rdx) = (ry - h1y) / (h1dy - rdy)
    # (rx - h1x)(h1dy - rdy) = (ry - h1y)(h1dx - rdx)
    # (rx * h1dy) - (rx * rdy) - (h1x * h1dy) + (rdy * h1x) = (ry * h1dx) - (ry * rdx) - (h1y * h1dx) + (rdx * h1y)

    # 4) Rearrange to put rock variables on LHS:
    # (ry * rdx) - (rx * rdy) = (ry * h1dx) - (rx * h1dy) + (rdx * h1y) - (rdy * h1x) - (h1y * h1dx) + (h1x * h1dy)

    # 5) For a second hailstone h2:
    # (ry * rdx) - (rx * rdy) = (ry * h2dx) - (rx * h2dy) + (rdx * h2y) - (rdy * h2x) - (h2y * h2dx) + (h2x * h2dy)

    # 6) Equality of h1 and h2, both equal to (ry * rdx) - (rx * rdy):
    # (ry * h1dx) - (rx * h1dy) + (rdx * h1y) - (rdy * h1x) - (h1y * h1dx) + (h1x * h1dy) = (ry * h2dx) - (rx * h2dy) + (rdx * h2y) - (rdy * h2x) - (h2y * h2dx) + (h2x * h2dy)

    # 7) Unknown coefficients (4) on LHS:
    # (rx * h2dy) - (rx * h1dy) + (ry * h1dx) - (ry * h2dx) + (rdx * h1y) - (rdx * h2y) + (rdy * h2x) - (rdy * h1x) = (h1y * h1dx) - (h1x * h1dy) + (h2x * h2dy) - (h2y * h2dx)
    # (h2dy - h1dy)rx + (h1dx - h2dx)ry + (h1y - h2y)rdx + (h2x - h1x)rdy = (h1y * h1dx) - (h1x * h1dy) + (h2x * h2dy) - (h2y * h2dx)

    # 8) With another three hailstones, four unknowns and four equations:
    # (h2dy - h1dy)rx + (h1dx - h2dx)ry + (h1y - h2y)rdx + (h2x - h1x)rdy = (h1y * h1dx) - (h1x * h1dy) + (h2x * h2dy) - (h2y * h2dx)
    # (h3dy - h1dy)rx + (h1dx - h3dx)ry + (h1y - h3y)rdx + (h3x - h1x)rdy = (h1y * h1dx) - (h1x * h1dy) + (h3x * h3dy) - (h3y * h3dx)
    # (h4dy - h1dy)rx + (h1dx - h4dx)ry + (h1y - h4y)rdx + (h4x - h1x)rdy = (h1y * h1dx) - (h1x * h1dy) + (h4x * h4dy) - (h4y * h4dx)
    # (h5dy - h1dy)rx + (h1dx - h5dx)ry + (h1y - h5y)rdx + (h5x - h1x)rdy = (h1y * h1dx) - (h1x * h1dy) + (h5x * h5dy) - (h5y * h5dx)

    # 9) Solves for Rx, Ry, Rdx and Rdy
    m00 = h[1].v.y - h[0].v.y
    m01 = h[0].v.x - h[1].v.x
    m02 = h[0].p.y - h[1].p.y
    m03 = h[1].p.x - h[0].p.x
    m04 = (h[0].p.y * h[0].v.x) - (h[0].p.x * h[0].v.y) \
        + (h[1].p.x * h[1].v.y) - (h[1].p.y * h[1].v.x)

    m10 = h[2].v.y - h[0].v.y
    m11 = h[0].v.x - h[2].v.x
    m12 = h[0].p.y - h[2].p.y
    m13 = h[2].p.x - h[0].p.x
    m14 = (h[0].p.y * h[0].v.x) - (h[0].p.x * h[0].v.y) \
        + (h[2].p.x * h[2].v.y) - (h[2].p.y * h[2].v.x)

    m20 = h[3].v.y - h[0].v.y
    m21 = h[0].v.x - h[3].v.x
    m22 = h[0].p.y - h[3].p.y
    m23 = h[3].p.x - h[0].p.x
    m24 = (h[0].p.y * h[0].v.x) - (h[0].p.x * h[0].v.y) \
        + (h[3].p.x * h[3].v.y) - (h[3].p.y * h[3].v.x)

    m30 = h[4].v.y - h[0].v.y
    m31 = h[0].v.x - h[4].v.x
    m32 = h[0].p.y - h[4].p.y
    m33 = h[4].p.x - h[0].p.x
    m34 = (h[0].p.y * h[0].v.x) - (h[0].p.x * h[0].v.y) \
        + (h[4].p.x * h[4].v.y) - (h[4].p.y * h[4].v.x)

    M = [[m00, m01, m02, m03, m04],
         [m10, m11, m12, m13, m14],
         [m20, m21, m22, m23, m24],
         [m30, m31, m32, m33, m34]]

    # Rx, Ry, Rdx, Rdy
    x = gauss_jordan(M)

    # 10) Repeat the above from 3) but now for X and Z:
    # (rx - h1x) / (h1dx - rdx) = (rz - h1z) / (h1dz - rdz)
    # (rx - h1x)(h1dz - rdz) = (rz - h1z)(h1dx - rdx)
    # (rx * h1dz) - (rx * rdz) - (h1x * h1dz) + (rdz * h1x) = (rz * h1dx) - (rz * rdx) - (h1z * h1dx) + (rdx * h1z)

    # 11) Rearrange to put rock variables on LHS:
    # (rz * rdx) - (rx * rdz) = (rz * h1dx) - (h1z * h1dx) + (rdx * h1z) + (h1x * h1dz) - (rx * h1dz) - (rdz * h1x)

    # 12) For a second hailstone h2:
    # (rz * rdx) - (rx * rdz) = (rz * h2dx) - (h2z * h2dx) + (rdx * h2z) + (h2x * h2dz) - (rx * h2dz) - (rdz * h2x)

    # 13) Equality of h1 and h2, both equal to (rx * rdz) - (rz * rdx):
    # (rz * h1dx) - (h1z * h1dx) + (rdx * h1z) + (h1x * h1dz) - (rx * h1dz) - (rdz * h1x) = (rz * h2dx) - (h2z * h2dx) + (rdx * h2z) + (h2x * h2dz) - (rx * h2dz) - (rdz * h2x)

    # 14) Unknown coefficients (4) on LHS:
    # (rx * h2dz) - (rx * h1dz) + (rz * h1dx) - (rz * h2dx) + (rdx * h1z) - (rdx * h2z) + (rdz * h2x) - (rdz * h1x) = (h2x * h2dz) - (h1x * h1dz) + (h1z * h1dx) - (h2z * h2dx)
    # (h2dz - h1dz)rx + (h1dx - h2dx)rz +  rdx(h1z - h2z) + rdz(h2x - h1x) = (h2x * h2dz) - (h1x * h1dz) + (h1z * h1dx) - (h2z * h2dx)

    # 15) With another three hailstones, four unknowns and four equations:
    # (h2dz - h1dz)rx + (h1dx - h2dx)rz + rdx(h1z - h2z) + rdz(h2x - h1x) = (h2x * h2dz) - (h1x * h1dz) + (h1z * h1dx) - (h2z * h2dx)
    # (h3dz - h1dz)rx + (h1dx - h3dx)rz + rdx(h1z - h3z) + rdz(h3x - h1x) = (h3x * h3dz) - (h1x * h1dz) + (h1z * h1dx) - (h3z * h3dx)
    # (h4dz - h1dz)rx + (h1dx - h4dx)rz + rdx(h1z - h4z) + rdz(h4x - h1x) = (h4x * h4dz) - (h1x * h1dz) + (h1z * h1dx) - (h4z * h4dx)
    # (h5dz - h1dz)rx + (h1dx - h5dx)rz + rdx(h1z - h5z) + rdz(h5x - h1x) = (h5x * h5dz) - (h1x * h1dz) + (h1z * h1dx) - (h5z * h5dx)

    # 16) Solves for Rx, Rz, Rdx and Rdz
    m00 = h[1].v.z - h[0].v.z
    m01 = h[0].v.x - h[1].v.x
    m02 = h[0].p.z - h[1].p.z
    m03 = h[1].p.x - h[0].p.x
    m04 = (h[1].p.x * h[1].v.z) - (h[0].p.x * h[0].v.z) \
        + (h[0].p.z * h[0].v.x) - (h[1].p.z * h[1].v.x)

    m10 = h[2].v.z - h[0].v.z
    m11 = h[0].v.x - h[2].v.x
    m12 = h[0].p.z - h[2].p.z
    m13 = h[2].p.x - h[0].p.x
    m14 = (h[2].p.x * h[2].v.z) - (h[0].p.x * h[0].v.z) \
        + (h[0].p.z * h[0].v.x) - (h[2].p.z * h[2].v.x)

    m20 = h[3].v.z - h[0].v.z
    m21 = h[0].v.x - h[3].v.x
    m22 = h[0].p.z - h[3].p.z
    m23 = h[3].p.x - h[0].p.x
    m24 = (h[3].p.x * h[3].v.z) - (h[0].p.x * h[0].v.z) \
        + (h[0].p.z * h[0].v.x) - (h[3].p.z * h[3].v.x)

    m30 = h[4].v.z - h[0].v.z
    m31 = h[0].v.x - h[4].v.x
    m32 = h[0].p.z - h[4].p.z
    m33 = h[4].p.x - h[0].p.x
    m34 = (h[4].p.x * h[4].v.z) - (h[0].p.x * h[0].v.z) \
        + (h[0].p.z * h[0].v.x) - (h[4].p.z * h[4].v.x)

    M = [[m00, m01, m02, m03, m04],
         [m10, m11, m12, m13, m14],
         [m20, m21, m22, m23, m24],
         [m30, m31, m32, m33, m34]]

    # Rx, Rz, Rdx, Rdz
    x2 = gauss_jordan(M)

    rx, ry, rz = x[0], x[1], x2[1]
    result = int(round(rx)) + int(round(ry)) + int(round(rz))
    return result


def main() -> None:
    for (label, filename, func, expected) in (
        ("Part 1", "inputs/day24_example.txt",
         partial(part1, r=Range(7, 27)), 2),
        ("Part 1", "inputs/day24_full.txt",
         partial(part1, r=Range(2 * 10**14, 4 * 10**14)), 20361),
        ("Part 2", "inputs/day24_example.txt", part2, 47),
        ("Part 2", "inputs/day24_full.txt", part2, 558415252330828),
    ):
        with open(filename) as f:
            contents = f.read()

        t1 = time()
        result = func(contents)
        t2 = time()

        print(f"{label} [{filename}]:", result, f"({(t2-t1)*1000.0:.3f}ms)")

        if expected is not None:
            assert result == expected


if __name__ == "__main__":
    main()
