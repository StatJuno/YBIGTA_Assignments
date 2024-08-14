from lib import Trie
import sys


"""
TODO:
- 일단 Trie부터 구현하기
- main 구현하기

힌트: 한 글자짜리 자료에도 그냥 str을 쓰기에는 메모리가 아깝다...
"""


def main() -> None:
    # 구현하세요!
    from typing import Callable
    strify: Callable[[str], list[str]] = lambda l: [name.strip() for name in l.split('\n') if name.strip()]

    lines: list[str] = sys.stdin.readlines()

    N = int(lines[0].strip())
    names: list[str] = strify('\n'.join(lines[1:]))

    def get_common_prefix(str1: str, str2: str) -> str:
        min_length = min(len(str1), len(str2))
        i = 0
        while i < min_length and str1[i] == str2[i]:
            i += 1
        return str1[:i+1]

    def find_prefixes(sorted_names: list[str]) -> list[str]:
        if not sorted_names:
            return []
        
        n = len(sorted_names)
        prefixes = []

        for i in range(n):
            if i == 0:
                prefix = get_common_prefix(sorted_names[i], sorted_names[i+1])
            elif i == n - 1:
                prefix = get_common_prefix(sorted_names[i], sorted_names[i-1])
            else:
                prefix1 = get_common_prefix(sorted_names[i], sorted_names[i-1])
                prefix2 = get_common_prefix(sorted_names[i], sorted_names[i+1])
                prefix = max(prefix1, prefix2, key=len)

            prefixes.append(prefix)
        
        return prefixes
    
    names.sort()
    reduced_names = find_prefixes(names)
    
    trie: Trie[str] = Trie()
    for name in reduced_names:
        trie.push(name + "!")
    
    result = 1
    MOD = 1000000007
    for node in trie:
        if len(node.children) > 1:
            for i in range(1, len(node.children) + 1):
                result = (result * i) % MOD

    print(result)


if __name__ == "__main__":
    main()