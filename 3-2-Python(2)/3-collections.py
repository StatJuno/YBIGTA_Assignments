from typing import (
    Callable,
    Generic,
    TypeVar,
    Hashable
)


K = TypeVar("K", bound=Hashable)
V = TypeVar("V")

class defaultdict(dict[K, V], Generic[K, V]):
    def __init__(self, default_factory: Callable[[], V]) -> None:
        super().__init__()
        self.default_factory = default_factory

    def __getitem__(self, k: K) -> V:
        return self.setdefault(k, self.default_factory())


if __name__ == "__main__":
    test_keys = ["asdf", 892340, 3+4j, -2345, (4, 2, "a")]

    try:
        test_dict_1: defaultdict[Hashable, int] = defaultdict(int)
        for key in test_keys:
            assert test_dict_1[key] == 0
            test_dict_1[key] += 5
            assert test_dict_1[key] == 5

        test_dict_2: defaultdict[Hashable, dict[str, int]] = defaultdict(dict)
        for key in test_keys:
            assert len(test_dict_2[key]) == 0
            test_dict_2[key]["a"] = 1
            test_dict_2[key]["b"] = 2
            assert str(test_dict_2[key]) == "{'a': 1, 'b': 2}"

        test_dict_3: defaultdict[Hashable, list[int]] = defaultdict(lambda: [0, 1])
        for key in test_keys:
            assert len(test_dict_3[key]) == 2
            test_dict_3[key].append(2)
            assert str(test_dict_3[key] + [3, 4]) == '[0, 1, 2, 3, 4]'

    except Exception as e:
        print("something's wrong...", e.__class__.__name__)
    else:
        print("well done!")
    finally:
        print("goodbye!")