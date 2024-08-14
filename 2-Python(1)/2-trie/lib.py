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