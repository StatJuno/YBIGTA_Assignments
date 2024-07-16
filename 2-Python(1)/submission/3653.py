from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Callable


"""
TODO:
- SegmentTree 구현하기
"""


T = TypeVar("T")
U = TypeVar("U")


class SegmentTree(Generic[T, U]):
    # 구현하세요!
    def __init__(self, size: int, function: Callable[[U, U], U], U = TypeVar("U", bound=int) ):
        self.size = size
        self.tree = [U] * (2 * size)
        self.function = function
        self.default = U

    def update(self, index: int, value: U):
        pos = index + self.size
        self.tree[pos] = value
        while pos > 1:
            pos //= 2
            self.tree[pos] = self.function(self.tree[2 * pos], self.tree[2 * pos + 1])

    def query(self, left: int, right: int) -> U:
        result = self.default
        left += self.size
        right += self.size
        while left < right:
            if left % 2:
                result = self.function(result, self.tree[left])
                left += 1
            if right % 2:
                right -= 1
                result = self.function(result, self.tree[right])
            left //= 2
            right //= 2
        return result
    
    def find_kth(self, k: int) -> int:
        pos = 1
        while pos < self.size:
            if self.tree[2 * pos] >= k:
                pos = 2 * pos
            else:
                k -= self.tree[2 * pos]
                pos = 2 * pos + 1
        return pos - self.size
    
    def change(self, target: int, diff: U, idx: int, start: int, end: int):
        if end < target or target < start:
            return
        
        self.tree[idx] += diff
        if start != end:
            mid = (start + end) // 2
            self.change(target, diff, 2 * idx, start, mid)
            self.change(target, diff, 2 * idx + 1, mid + 1, end)

    def print_sum(self, count: int, idx: int, start: int, end: int) -> int:
        if start == end:  # 리프노드 도달
            return start
        
        mid = (start + end) // 2
        if self.tree[2 * idx] >= count:
            return self.print_sum(count, 2 * idx, start, mid)
        else:
            return self.print_sum(count - self.tree[2 * idx], 2 * idx + 1, mid + 1, end)
        
    def update2(self, index: int, value: U):
        pos = index + self.size
        self.tree[pos] += value
        while pos > 1:
            pos //= 2
            self.tree[pos] = self.function(self.tree[2 * pos], self.tree[2 * pos + 1])


import sys


"""
TODO:
- 일단 SegmentTree부터 구현하기
- main 구현하기
"""


def main() -> None:
    # 구현하세요!
    input = sys.stdin.read().strip()
    if not input:
        return
    data = input.split()
    idx = 0

    T = int(data[idx])
    idx += 1
    results = []

    for _ in range(T):
        n = int(data[idx])
        m = int(data[idx + 1])
        idx += 2
        movies = list(map(int, data[idx:idx + m]))
        idx += m

        # Initialize the segment tree
        MAX_POS = n + m
        seg_tree: SegmentTree[int, int] = SegmentTree(MAX_POS + 1, lambda x, y: x + y, 0)
        position = [0] * (n + 1)
        
        # Initial positions of the DVDs
        for i in range(1, n + 1):
            position[i] = m + i
            seg_tree.update2(position[i], 1)

        current_top = m
        result = []

        for movie in movies:
            pos = position[movie]
            result.append(seg_tree.query(1, pos))
            seg_tree.update2(pos, -1)
            current_top -= 1
            position[movie] = current_top
            seg_tree.update2(position[movie], 1)

        results.append(" ".join(map(str, result)))
    
    print("\n".join(results))


if __name__ == "__main__":
    main()