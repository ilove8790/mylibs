# myGeometry.py
"""Computational Geometry
"""


class MyPoint:
    """한 점의 좌표: (x, y) or (x, y, z)"""
    def __init__(self, x: float | int, y: float | int):
        self.x = x
        self.y = y


class MyLine:
    """2차원 직선 방정식: y = m*x + b"""
    def __init__(self, p1: MyPoint, p2: MyPoint):
        self.x1, self.y1 = p1.x, p1.y
        self.x2, self.y2 = p2.x, p2.y

        if p2.x == p1.x:
            self.m = float('inf')  # 기울기
            self.b = 0. #None  # y절편
        else:
            self.m = (p2.y - p1.y) / (p2.x - p1.x)
            self.b = p1.y - self.m * p1.x


class MySegment:
    """2차원 선분: y = m*x + b"""
    def __init__(self, p1: MyPoint, p2: MyPoint):
        self.x1, self.y1 = p1.x, p1.y
        self.x2, self.y2 = p2.x, p2.y

        if p2.x == p1.x:
            self.m = float('inf')  # 기울기
            self.b = 0. #None  # y절편
        else:
            self.m = (p2.y - p1.y) / (p2.x - p1.x)
            self.b = p1.y - self.m * p1.x

        self.xmin, self.xmax = min(p1.x, p2.x), max(p1.x, p2.x)
        self.ymin, self.ymax = min(p1.y, p2.y), max(p1.y, p2.y)
        self.xlength, self.ylength = (self.xmax - self.xmin), (self.ymax - self.ymin)
        self.length = (self.xlength**2 + self.ylength**2)**0.5


def get_intersection_point(line: MyLine, segment: MySegment):
    """두 직선의 교점을 구하는 함수"""
    # m1, b1 = line.m, line.b  # 직선1의 기울기, 절편
    # m2, b2 = segment.m, segment.b  # 직선2의 기울기, 절편

    # 두 직선이 평행한 경우
    if line.m == segment.m:
        return None

    # 교점 구하기
    if line.m == float('inf'):  # 직선이 수직인 경우
        xi = line.x1
        yi = segment.m * xi + segment.b
    elif segment.m == float('inf'):  # 선분이 수직인 경우
        xi = segment.x1
        yi =  line.m * xi + line.b
    else:
        xi = (segment.b - line.b) / (line.m - segment.m)
        yi = line.m * xi + line.b

    # 교점이 선분위에 있는지 확인
    if (segment.xmin <= xi <= segment.xmax and segment.ymin <= yi <= segment.ymax):
        return (xi, yi)
    else:
        return None


def find_intersection(xy12, xy34):#x1, y1, x2, y2, x3, y3, x4, y4):
    """두 직선의 교점 좌표 구하기

    xy12 (tuple[x1,y1, x2,y2]): 직선을 구성하는 두 점 좌표
    xy34 (tuple[x3,y3, x4,y4]): 직선을 구성하는 두 점 좌표
    """
    x1, y1, x2, y2 = xy12[0], xy12[1], xy12[2], xy12[3]
    x3, y3, x4, y4 = xy34[0], xy34[1], xy34[2], xy34[3]

    # 1st line
    a1 = (y2 - y1)/(x2 - x1)
    b1 = y1 - a1*x1

    # 2nd line
    a2 = (y4 - y3)/(x4 - x3)
    b2 = y3 - a2*x3

    # parallel
    if abs(a1 - a2) < 1e-10:
        return 0, 0

    # find x, y
    x = (b2 - b1)/(a1 - a2)
    y = a1*x + b1

    return x, y