"""Exhaustive certificate: center 1^9 0 1 forces left neighbor 1 at 0.

Uses literal Rule 30 cell updates, independent of strip_graph's packed
transition formula. Outer bits are free at every step, so every genuine
spacetime restriction is included. No seed or onset bound is assumed.
Run: python3 research/review_long_run_certificate.py
"""


def certify():
    width, center = 13, 6
    successors = {}
    for row in range(1 << width):
        bits = [(row >> j) & 1 for j in range(width)]
        interior = sum(
            (bits[j - 1] ^ (bits[j] | bits[j + 1])) << j
            for j in range(1, width - 1)
        )
        successors[row] = tuple(
            interior | left | (right << (width - 1))
            for left in range(2) for right in range(2)
        )

    def image(rows, next_center):
        return {
            nxt for row in rows for nxt in successors[row]
            if ((nxt >> center) & 1) == next_center
        }

    # Possible rows at the last 1 after nine consecutive center 1s.
    rows = {row for row in successors if (row >> center) & 1}
    counts = [len(rows)]
    for _ in range(8):
        rows = image(rows, 1)
        counts.append(len(rows))
    assert counts == [4096, 3200, 2944, 2816, 2560, 2304, 2048, 1664, 1408]
    zero_rows = image(rows, 0)
    bad = {row for row in zero_rows if not ((row >> (center - 1)) & 1)}
    good = zero_rows - bad
    assert len(bad) == 512
    assert not image(bad, 1)
    assert image(good, 1)  # The imposed center word itself is possible.
    print("Possible rows after each consecutive 1:", counts)
    print("Zero rows with left neighbor 0:", len(bad))
    print("Those rows surviving the next center 1: 0")
    print("CERTIFIED: center 1^9 0 1 forces left neighbor 1 at the zero.")


if __name__ == "__main__":
    certify()
