from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Iterable


"""
TODO:
- Trie.push 구현하기
- (필요할 경우) Trie에 추가 method 구현하기
"""


T = TypeVar("T")


@dataclass
class TrieNode(Generic[T]):
    body: Optional[T] = None
    children: list[int] = field(default_factory=lambda: [])
    is_end: bool = False


class Trie(list[TrieNode[T]]):
    def __init__(self) -> None:
        super().__init__()
        self.append(TrieNode(body=None))

    def push(self, seq: Iterable[T]) -> None:
        """
        seq: T의 열 (list[int]일 수도 있고 str일 수도 있고 등등...)

        action: trie에 seq을 저장하기
        """
        # 구현하세요!
        pointer = 0
        for element in seq:
            found = False
            for child_index in self[pointer].children:
                if self[child_index].body == element:
                    pointer = child_index
                    found = True
                    break
            if not found:
                new_node = TrieNode(body=element)
                self.append(new_node)
                self[pointer].children.append(len(self) - 1)
                pointer = len(self) - 1
        self[pointer].is_end = True

    # 구현하세요!
    def find_next_index(self, pointer: int, element: T) -> Optional[int]:

        for child_index in self[pointer].children:
            if self[child_index].body == element:
                return child_index
        return None
    
    def search(self, seq: Iterable[T]) -> bool:
        pointer = 0
        for element in seq:
            next_pointer = self.find_next_index(pointer, element)
            if next_pointer is None:
                return False
            pointer = next_pointer
        return self[pointer].is_end


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

        if new_index is None:
            break        
        
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

        # 타입 주석 추가
        trie: Trie = Trie()
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