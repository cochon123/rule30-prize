"""Radius-6/7 finite-strip scan of all primitive period-8 and period-9 words."""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from small_period_cert import analyze_any_pair, extend_scan, primitive_necklaces
from strip_graph import self_check


def main():
    self_check()
    rows = []
    for n in (8, 9):
        for w in primitive_necklaces(n):
            rec = {"word": w, "period": n}
            for radius in (6, 7):
                t0 = time.monotonic()
                a = analyze_any_pair(radius, list(map(int, w)))
                rec[f"r{radius}"] = {
                    "excluded_neighbor": a["excluded_neighbor"],
                    "excluded_any_adjacent": a["excluded_any_adjacent"],
                    "residual_sizes": a["residual_neighbor_sizes"],
                    "recurrent": a["recurrent_components"],
                    "elapsed": round(time.monotonic() - t0, 3),
                }
                print(
                    json.dumps(
                        {
                            "word": w,
                            "radius": radius,
                            "excl": a["excluded_neighbor"],
                            "excl_any": a["excluded_any_adjacent"],
                            "res": a["residual_neighbor_sizes"],
                            "sec": rec[f"r{radius}"]["elapsed"],
                        }
                    ),
                    flush=True,
                )
                if a["excluded_neighbor"]:
                    break
            rows.append(rec)

    emptied = [r for r in rows if r.get("r6", {}).get("excluded_neighbor")
               or r.get("r7", {}).get("excluded_neighbor")]
    print("emptied at r6/r7", [(r["word"], "r6" if r.get("r6", {}).get("excluded_neighbor") else "r7")
                               for r in emptied])

    # Incremental extend for isolated-one-like period-9 survivors and r7-small residuals
    extra = []
    for r in rows:
        w = r["word"]
        last = r.get("r7") or r.get("r6")
        if last.get("excluded_neighbor"):
            continue
        ones = w.count("1")
        zeros = w.count("0")
        # isolated one/zero or tiny residual
        if ones == 1 or zeros == 1 or (last["residual_sizes"] and last["residual_sizes"][0] < 80):
            rec = extend_scan(w, max_radius=20, cap=25000)
            extra.append(rec)
            print(json.dumps({"extend": w, "stop": rec["stop"],
                              "last_r": rec["last_radius"],
                              "states": rec["last_states"]}), flush=True)

    path = Path(__file__).resolve().parent / "period_scan_8_9_radius.json"
    path.write_text(json.dumps({"rows": rows, "extend_extra": extra}, indent=2) + "\n")
    print("wrote", path)


if __name__ == "__main__":
    main()
