from lib import Trie
import sys


"""
TODO:
- 일단 Trie부터 구현하기
- count 구현하기
- main 구현하기
"""


def count(trie: Trie, query_seq: str) -> int:
    """
    trie - 이름 그대로 trie
    query_seq - 단어 ("hello", "goodbye", "structures" 등)

    returns: query_seq의 단어를 입력하기 위해 버튼을 눌러야 하는 횟수
    """
    pointer = 0
    cnt = 0

    for element in query_seq:
        if len(trie[pointer].children) > 1 or trie[pointer].is_end:
            cnt += 1

        new_index = trie.find_next_index(pointer, element) # 구현하세요!

        pointer = new_index

    return cnt + int(len(trie[0].children) == 1)


def main() -> None:
    # 구현하세요!
    input = sys.stdin.read
    data = input().split()
    idx = 0

    results = []

    while idx < len(data):
        N = int(data[idx])
        idx += 1
        words = data[idx:idx + N]
        idx += N

        trie = Trie()
        for word in words:
            trie.push(word)

        total_presses = sum(count(trie, word) for word in words)
        average_presses = total_presses / N
        results.append(f"{average_presses:.2f}")

    for result in results:
        print(result)


if __name__ == "__main__":
    main()