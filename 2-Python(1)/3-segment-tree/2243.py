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

    n = int(data[idx])
    idx += 1

    MAX_TASTE = 1000000
    tree_size = 2**21

    # Segment Tree for counting candies
    seg_tree: SegmentTree[int, int] = SegmentTree(tree_size, lambda x, y: x + y, 0)
    
    results = []

    for _ in range(n):
        A = int(data[idx])
        B = int(data[idx + 1])

        if A == 1:
            # Find the B-th most delicious candy
            taste_index = seg_tree.print_sum(B, 1, 1, MAX_TASTE)
            results.append(taste_index)
            # Remove that candy by decrementing the count
            seg_tree.change(taste_index, -1, 1, 1, MAX_TASTE)
            idx += 2
        elif A == 2:
            # Update the segment tree with candy addition/removal
            C = int(data[idx + 2])
            seg_tree.change(B, C, 1, 1, MAX_TASTE)
            idx += 3

    for result in results:
        print(result)


if __name__ == "__main__":
    main()