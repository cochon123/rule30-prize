"""Scan all primitive binary necklaces of period 7 with strip_extend."""
import json
import time
from pathlib import Path
from strip_extend import initial, extend


def canonical(w):
    rotations = [w[i:] + w[:i] for i in range(len(w))]
    return min(rotations)


def primitive_necklaces_7():
    words = []
    for mask in range(1 << 7):
        w = [(mask >> i) & 1 for i in range(7)]
        if canonical(w) == w and not (all(x == w[0] for x in w)):
            words.append(w)
    return words


def scan(word, max_radius=30, cap=20_000):
    states, out, stats = initial(word)
    records = []
    for radius in range(1, max_radius + 1):
        records.append({
            "radius": radius,
            "surviving_states": len(states),
            "surviving_edges": sum(map(len, out)),
            "elapsed_seconds": round(time.monotonic() - started, 6),
            "components": stats,
        })
        if not states or len(states) > cap or radius == max_radius:
            break
        states, out, stats = extend(states, out, radius)
    return records


started = time.monotonic()
results = []
for word in primitive_necklaces_7():
    started = time.monotonic()
    records = scan(word)
    results.append({
        "word": "".join(map(str, word)),
        "records": records,
        "status": ("empty" if not records[-1]["surviving_states"]
                   else "cap_or_radius"),
        "elapsed_seconds": round(time.monotonic() - started, 6),
    })

Path("research/period_scan_7.json").write_text(
    json.dumps({"period": 7, "results": results}, indent=2) + "\n"
)
