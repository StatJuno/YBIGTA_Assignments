from lib import SegmentTree
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