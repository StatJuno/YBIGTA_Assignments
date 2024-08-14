from lib import SegmentTree
import sys


"""
TODO:
- 일단 SegmentTree부터 구현하기
- main 구현하기
"""


class Pair(tuple[int, int]):
    """
    힌트: 2243, 3653에서 int에 대한 세그먼트 트리를 만들었다면 여기서는 Pair에 대한 세그먼트 트리를 만들 수 있을지도...?
    """
    def __new__(cls, a: int, b: int) -> 'Pair':
        return super().__new__(cls, (a, b))

    @staticmethod
    def default() -> 'Pair':
        """
        기본값
        이게 왜 필요할까...?
        """
        return Pair(0, 0)

    @staticmethod
    def f_conv(w: int) -> 'Pair':
        """
        원본 수열의 값을 대응되는 Pair 값으로 변환하는 연산
        이게 왜 필요할까...?
        """
        return Pair(w, 0)

    @staticmethod
    def f_merge(a: Pair, b: Pair) -> 'Pair':
        """
        두 Pair를 하나의 Pair로 합치는 연산
        이게 왜 필요할까...?
        """
        return Pair(*sorted([*a, *b], reverse=True)[:2])

    def sum(self) -> int:
        return self[0] + self[1]


def main() -> None:
    # 구현하세요!
    input = sys.stdin.read().strip()
    if not input:
        return
    data = input.split()
    idx = 0

    n = int(data[idx])
    idx += 1
    arr = list(map(int, data[idx:idx + n]))
    idx += n
    m = int(data[idx])
    idx += 1

    seg_tree: SegmentTree[Pair, Pair] = SegmentTree(n, Pair.f_merge, Pair.default())

    for i in range(n):
        seg_tree.update(i, Pair.f_conv(arr[i]))

    result = []
    for _ in range(m):
        query_type = int(data[idx])
        if query_type == 1:
            i = int(data[idx + 1]) - 1
            v = int(data[idx + 2])
            seg_tree.update(i, Pair.f_conv(v))
            idx += 3
        elif query_type == 2:
            l = int(data[idx + 1]) - 1
            r = int(data[idx + 2])
            result.append(str(seg_tree.query(l, r).sum()))
            idx += 3

    print("\n".join(result))


if __name__ == "__main__":
    main()