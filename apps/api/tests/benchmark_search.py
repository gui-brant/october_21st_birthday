import random
import string
import time


def generate_titles(n: int) -> list[str]:
    titles = []
    for _ in range(n):
        word = "".join(random.choice(string.ascii_letters) for _ in range(8))
        titles.append(f"Project {word}")
    return titles


def baseline_filter(query: str, titles: list[str]) -> list[str]:
    needle = "".join(query.lower().split())
    return [t for t in titles if needle in "".join(t.lower().split())]


if __name__ == "__main__":
    titles = generate_titles(50_000)
    start = time.perf_counter()
    _ = baseline_filter("projecta", titles)
    elapsed_ms = (time.perf_counter() - start) * 1000
    print(f"baseline_filter_elapsed_ms={elapsed_ms:.2f}")
