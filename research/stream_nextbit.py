#!/usr/bin/env python3
"""Streaming next-centre-bit from the packed Rule 30 row (Problem 3).

Astra ideas10 item 1 / leftover ideas9 item 5. After row t is known as a
packed integer z, the next centre bit is the three-bit local rule

    c_{t+1} = x(t,-1) XOR (x(t,0) OR x(t,1)).

Packing is experiment.py: z_0 = 1, z <- (z<<2)^((z<<1)|z),
x(t,j) = (z>>(j+t))&1. Not a prize claim.

Freeze of candidate o(t) summaries of z at time t, for t=8..4096:
  popcount(z), popcount(z & ((1<<k)-1)) for k=8,16,32;
  v2(z), v2(z+1), v2(z XOR (z<<1)), v2(z XOR (1<<t));
  popcount(z & (z<<1)) = N_t from packed_valuation.py;
  length-<=8 windows of z, but only a FIXED set of at most 16 bit
  positions, or positions depending on t only through popcount/v2
  (an arbitrary window still costs a bit read at that index);
  the same scalars on z XOR (z<<1) and z AND (z<<1).

Ask: does any statistic equal c_{t+1} for all t=8..4096? Does any
determine the triple (x(t,-1),x(t,0),x(t,1))?

The three centre-adjacent bits are a baseline that works: O(1) word-RAM
given z, but they use the growing index t. Problem 3 is producing z
(or those bits) without Theta(t^2) work; this freeze only kills cheap
summaries of an already-known z.

Does not modify experiment.py, strip_graph.py, or strip_extend.py.
Stdlib only.

Run: python3 research/stream_nextbit.py
"""
from __future__ import annotations

import json
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiment import center_bits as experiment_center_bits

OUT_JSON = Path(__file__).with_name("stream_nextbit.json")
OUT_MD = Path(__file__).with_name("stream_nextbit.md")

T_LO = 8
T_HI = 4096
# First t where bits 0..31 are disjoint from the triple at indices t-1..t+1.
T_CLEAN = 32
PREFIX_CHECK = 256
KNOWN20 = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1]
# packed_valuation.py sample (N_t agrees across packings).
N_SAMPLE = {0: 0, 1: 2, 2: 1, 8: 3, 16: 8, 31: 25}
FIXED_BIT_CAP = 16
FIXED_OFFSET_CAP = 32
WINDOW_LENS = (1, 2, 3, 4, 5, 6, 7, 8)
LOW_K = (8, 16, 32)


def v2(n: int):
    """2-adic valuation; None encodes +∞."""
    if n == 0:
        return None
    n = abs(n)
    return (n & -n).bit_length() - 1


def v2_int(n: int) -> int:
    """Finite stand-in for maps; None (+∞) becomes -1."""
    got = v2(n)
    return -1 if got is None else got


def experiment_update(row: int) -> int:
    return (row << 2) ^ ((row << 1) | row)


def window(z: int, start: int, length: int) -> int:
    if start < 0:
        return 0
    return (z >> start) & ((1 << length) - 1)


def triple_of(z: int, t: int) -> tuple[int, int, int]:
    """(x(t,-1), x(t,0), x(t,1)) under experiment.py packing."""
    return ((z >> (t - 1)) & 1, (z >> t) & 1, (z >> (t + 1)) & 1)


def next_from_triple(tr: tuple[int, int, int]) -> int:
    xm1, x0, x1 = tr
    return xm1 ^ (x0 | x1)


def pack_triple(tr: tuple[int, int, int]) -> int:
    xm1, x0, x1 = tr
    return xm1 | (x0 << 1) | (x1 << 2)


def gather_bits(z: int, positions) -> int:
    w = 0
    for i, p in enumerate(positions):
        if p >= 0 and ((z >> p) & 1):
            w |= 1 << i
    return w


def t_dep_positions(t: int) -> list[int]:
    """At most 16 indices depending on t only through popcount and v2."""
    pc = t.bit_count()
    vt = v2_int(t) if t else 0
    if vt < 0:
        vt = 0
    vt1 = v2_int(t + 1)
    vtm1 = v2_int(t - 1) if t > 1 else 0
    if vtm1 < 0:
        vtm1 = 0
    pc1 = (t + 1).bit_count()
    pcm1 = (t - 1).bit_count() if t else 0
    return [
        pc,
        vt,
        vt1,
        vtm1,
        pc1,
        pcm1,
        pc + vt,
        pc + vt1,
        vt + vt1,
        pc + 1,
        pc + 2,
        vt1 + 1,
        vt1 + 2,
        pc + vt + vt1,
        abs(pc - vt1),
        pc ^ vt ^ vt1,
    ]


T_OFFSET_FNS = (
    ("popcount(t)", lambda t: t.bit_count()),
    ("v2(t)", lambda t: 0 if t == 0 else v2_int(t)),
    ("v2(t+1)", lambda t: v2_int(t + 1)),
    ("v2(t-1)", lambda t: 0 if t <= 1 else v2_int(t - 1)),
    ("popcount(t-1)", lambda t: (t - 1).bit_count() if t else 0),
    ("popcount(t+1)", lambda t: (t + 1).bit_count()),
    ("popcount(t)+v2(t)", lambda t: t.bit_count() + (0 if t == 0 else v2_int(t))),
    ("popcount(t)+v2(t+1)", lambda t: t.bit_count() + v2_int(t + 1)),
    ("v2(t)+v2(t+1)", lambda t: (0 if t == 0 else v2_int(t)) + v2_int(t + 1)),
    ("popcount(t)+1", lambda t: t.bit_count() + 1),
    ("popcount(t)+2", lambda t: t.bit_count() + 2),
    ("v2(t+1)+1", lambda t: v2_int(t + 1) + 1),
    ("v2(t+1)+2", lambda t: v2_int(t + 1) + 2),
    ("|popcount(t)-v2(t+1)|", lambda t: abs(t.bit_count() - v2_int(t + 1))),
    ("popcount(t) XOR v2(t) XOR v2(t+1)",
     lambda t: t.bit_count() ^ (0 if t == 0 else v2_int(t)) ^ v2_int(t + 1)),
    ("popcount(t)+v2(t)+v2(t+1)",
     lambda t: t.bit_count() + (0 if t == 0 else v2_int(t)) + v2_int(t + 1)),
)


def packed_rows_and_bits(max_t: int):
    """Rows z_t for t=0..max_t and centre bits c_0..c_{max_t+1}."""
    row = 1
    rows = [0] * (max_t + 1)
    bits = bytearray(max_t + 2)
    for t in range(max_t + 2):
        bits[t] = (row >> t) & 1
        if t <= max_t:
            rows[t] = row
        row = experiment_update(row)
    return rows, bits


def jsonable(x):
    if x is None or isinstance(x, (bool, int, float, str)):
        return x
    if isinstance(x, tuple):
        return [jsonable(y) for y in x]
    if isinstance(x, list):
        return [jsonable(y) for y in x]
    if isinstance(x, dict):
        return {str(k): jsonable(v) for k, v in x.items()}
    return x


def analyse_series(values, triples, next_bits, t_lo: int, t_hi: int) -> dict:
    """Collision / equality screen of one integer (or hashable) series."""
    n = t_hi - t_lo + 1
    n_eq = 0
    n_par = 0
    eq_fail = None
    par_fail = None
    val_triples = defaultdict(set)
    val_nexts = defaultdict(set)
    val_count = defaultdict(int)
    val_first = {}
    amb_triple = None
    amb_next = None
    for t in range(t_lo, t_hi + 1):
        v = values[t]
        tr = triples[t]
        nb = next_bits[t]
        if v == nb:
            n_eq += 1
        elif eq_fail is None:
            eq_fail = {"t": t, "got": jsonable(v), "want": nb}
        pv = None
        if isinstance(v, int) and v >= 0:
            pv = v & 1
            if pv == nb:
                n_par += 1
            elif par_fail is None:
                par_fail = {"t": t, "got": pv, "want": nb}
        if v not in val_first:
            val_first[v] = t
        val_count[v] += 1
        val_triples[v].add(tr)
        val_nexts[v].add(nb)
        if amb_triple is None and len(val_triples[v]) > 1:
            prev = next(iter(s for s in val_triples[v] if s != tr))
            amb_triple = {
                "t": t,
                "t_prev": val_first[v],
                "value": jsonable(v),
                "triple": list(tr),
                "triple_prev": list(prev),
            }
        if amb_next is None and len(val_nexts[v]) > 1:
            prevb = next(iter(s for s in val_nexts[v] if s != nb))
            amb_next = {
                "t": t,
                "t_prev": val_first[v],
                "value": jsonable(v),
                "next": nb,
                "next_prev": prevb,
            }
    n_values = len(val_count)
    n_reuse = sum(1 for c in val_count.values() if c >= 2)
    n_amb_triple = sum(1 for s in val_triples.values() if len(s) > 1)
    n_amb_next = sum(1 for s in val_nexts.values() if len(s) > 1)
    collision_ok_triple = n_amb_triple == 0
    collision_ok_next = n_amb_next == 0
    injective = n_reuse == 0
    return {
        "t_lo": t_lo,
        "t_hi": t_hi,
        "n": n,
        "equals_next_bit": eq_fail is None,
        "parity_equals_next_bit": par_fail is None and n_par == n,
        "n_eq": n_eq,
        "n_parity": n_par,
        "eq_frac": n_eq / n,
        "parity_frac": n_par / n,
        "first_eq_fail": eq_fail,
        "first_parity_fail": par_fail,
        "n_values": n_values,
        "n_reuse_values": n_reuse,
        "n_ambiguous_triple": n_amb_triple,
        "n_ambiguous_next": n_amb_next,
        "injective": injective,
        "collision_consistent_triple": collision_ok_triple,
        "collision_consistent_next": collision_ok_next,
        "determines_triple_witnessed": collision_ok_triple and n_reuse > 0,
        "determines_next_witnessed": collision_ok_next and n_reuse > 0,
        "first_triple_ambiguity": amb_triple,
        "first_next_ambiguity": amb_next,
    }


def attach_meta(rec: dict, name: str, formula: str, cost: str, family: str) -> dict:
    out = {
        "name": name,
        "formula": formula,
        "cost": cost,
        "family": family,
        **rec,
    }
    return out


def histogram_value(z: int, width: int, length: int) -> tuple:
    counts = [0] * (1 << length)
    last = width - length
    mask = (1 << length) - 1
    for s in range(last + 1):
        counts[(z >> s) & mask] += 1
    return tuple(counts)


def self_check(rows, bits) -> dict:
    ref = experiment_center_bits(PREFIX_CHECK)
    centre_ok = list(bits[:PREFIX_CHECK]) == list(ref)
    known_ok = list(bits[:20]) == KNOWN20
    formula_ok = True
    packing_ok = True
    n_ok = True
    v2_z_ok = True
    v2_plus_ok = True
    baseline_ok = True
    for t in range(T_HI + 1):
        z = rows[t]
        if ((z >> t) & 1) != bits[t]:
            packing_ok = False
            break
        if t >= 1:
            tr = triple_of(z, t)
            if next_from_triple(tr) != bits[t + 1]:
                formula_ok = False
                break
            if pack_triple(tr) != window(z, t - 1, 3):
                baseline_ok = False
                break
            if t >= T_LO:
                if window(z, t - 1, 3) != pack_triple(tr):
                    baseline_ok = False
                    break
        if t in N_SAMPLE and (z & (z << 1)).bit_count() != N_SAMPLE[t]:
            n_ok = False
            break
        if v2_int(z) != 0:
            v2_z_ok = False
            break
        if t >= 2 and v2_int(z + 1) != 2:
            v2_plus_ok = False
            break
    # Independent walk vs experiment.center_bits through T_HI+1.
    long_ref = experiment_center_bits(T_HI + 2)
    long_ok = list(bits) == list(long_ref)
    # t-dep positions stay O(log t) and miss the triple for t >= T_CLEAN.
    tdep_small = True
    tdep_miss_centre = True
    for t in range(T_CLEAN, T_HI + 1):
        pos = t_dep_positions(t)
        if len(pos) > FIXED_BIT_CAP:
            tdep_small = False
            break
        if max(pos) >= t - 1:
            tdep_miss_centre = False
            break
        for _name, fn in T_OFFSET_FNS:
            if fn(t) >= t - 1:
                tdep_miss_centre = False
                break
        if not tdep_miss_centre:
            break
    # Word-RAM baseline: three bit tests.
    z8 = rows[8]
    base_triple = triple_of(z8, 8)
    base_next = next_from_triple(base_triple)
    return {
        "centre_matches_experiment_256": centre_ok,
        "known20": known_ok,
        "formula_matches_next_centre": formula_ok,
        "packing_centre_bit": packing_ok,
        "N_t_sample_matches_packed_valuation": n_ok,
        "v2_z_eq_0": v2_z_ok,
        "experiment_v2_z_plus_1_eq_2_for_t_ge_2": v2_plus_ok,
        "baseline_window_is_triple": baseline_ok,
        "bits_match_experiment_through_T_HI_plus_1": long_ok,
        "tdep_at_most_16": tdep_small,
        "tdep_misses_triple_for_t_ge_32": tdep_miss_centre,
        "baseline_t8_triple": list(base_triple),
        "baseline_t8_next": base_next,
        "checked_through": T_HI,
    }


def cheap_ok(rec: dict) -> bool:
    """True if this O(1) summary actually evaluates next bit / triple."""
    if rec["cost"] != "O(1)":
        return False
    if rec["family"] == "baseline":
        return False
    return bool(
        rec["equals_next_bit"]
        or rec["parity_equals_next_bit"]
        or rec["determines_triple_witnessed"]
        or rec["determines_next_witnessed"]
    )


def is_killed(stats: list[dict], joints: list[dict]) -> dict:
    baseline = [s for s in stats if s["family"] == "baseline"]
    o1 = [s for s in stats if s["cost"] == "O(1)" and s["family"] != "baseline"]
    theta = [s for s in stats if s["cost"] == "Theta(t)"]
    o1_equals = [s["name"] for s in o1 if s["equals_next_bit"] or s["parity_equals_next_bit"]]
    o1_det_triple = [s["name"] for s in o1 if s["determines_triple_witnessed"]]
    o1_det_next = [s["name"] for s in o1 if s["determines_next_witnessed"]]
    theta_equals = [s["name"] for s in theta if s["equals_next_bit"] or s["parity_equals_next_bit"]]
    theta_det = [s["name"] for s in theta if s["determines_triple_witnessed"]]
    joint_cheap = [
        j for j in joints
        if j["cost"] == "O(1)" and (
            j["determines_triple_witnessed"]
            or j["equals_next_bit"]
            or j["parity_equals_next_bit"]
            or j["determines_next_witnessed"]
        )
    ]
    baseline_works = all(
        b["determines_triple_witnessed"] and b["determines_next_witnessed"]
        for b in baseline
        if b["name"] == "baseline_window(t-1,3)"
    )
    # Vacuous injectivity of a wide key is not an evaluator.
    fired = (
        baseline_works
        and not o1_equals
        and not o1_det_triple
        and not o1_det_next
        and not joint_cheap
    )
    return {
        "fired": fired,
        "baseline_works": baseline_works,
        "o1_equals_next": o1_equals,
        "o1_determines_triple_witnessed": o1_det_triple,
        "o1_determines_next_witnessed": o1_det_next,
        "theta_t_equals_next": theta_equals,
        "theta_t_determines_triple_witnessed": theta_det,
        "joint_o1_survivors": [j["name"] for j in joint_cheap],
        "n_o1_tested": len(o1),
        "n_theta_tested": len(theta),
        "n_baseline": len(baseline),
    }


def yn(flag: bool) -> str:
    return "yes" if flag else "no"


def compact_window(rec: dict) -> dict:
    """Keep witnesses and flags; drop bulky nested analyse copies."""
    amb = rec.get("first_triple_ambiguity")
    eqf = rec.get("first_eq_fail")
    clean = rec.get("clean") or {}
    camb = clean.get("first_triple_ambiguity")
    ceqf = clean.get("first_eq_fail")
    return {
        "name": rec["name"],
        "formula": rec["formula"],
        "equals_next_bit": rec["equals_next_bit"],
        "parity_equals_next_bit": rec["parity_equals_next_bit"],
        "determines_triple_witnessed": rec["determines_triple_witnessed"],
        "determines_next_witnessed": rec["determines_next_witnessed"],
        "injective": rec["injective"],
        "n_values": rec["n_values"],
        "n_reuse_values": rec["n_reuse_values"],
        "n_ambiguous_triple": rec["n_ambiguous_triple"],
        "eq_frac": rec["eq_frac"],
        "parity_frac": rec["parity_frac"],
        "first_eq_fail_t": None if eqf is None else eqf["t"],
        "first_triple_amb_t": None if amb is None else amb["t"],
        "clean": {
            "equals_next_bit": clean.get("equals_next_bit"),
            "parity_equals_next_bit": clean.get("parity_equals_next_bit"),
            "determines_triple_witnessed": clean.get("determines_triple_witnessed"),
            "determines_next_witnessed": clean.get("determines_next_witnessed"),
            "injective": clean.get("injective"),
            "n_ambiguous_triple": clean.get("n_ambiguous_triple"),
            "first_eq_fail_t": None if ceqf is None else ceqf["t"],
            "first_triple_amb_t": None if camb is None else camb["t"],
        },
    }


def compact_clean(rec: dict) -> dict:
    """Drop per-value maps; keep flags and first witnesses."""
    keys = (
        "equals_next_bit", "parity_equals_next_bit",
        "n_eq", "n_parity", "eq_frac", "parity_frac",
        "first_eq_fail", "first_parity_fail",
        "n_values", "n_reuse_values",
        "n_ambiguous_triple", "n_ambiguous_next",
        "injective",
        "collision_consistent_triple", "collision_consistent_next",
        "determines_triple_witnessed", "determines_next_witnessed",
        "first_triple_ambiguity", "first_next_ambiguity",
        "t_lo", "t_hi", "n",
    )
    return {k: rec[k] for k in keys if k in rec}


def write_markdown(payload: dict) -> str:
    kill = payload["kill"]
    scalars = payload["scalars"]
    windows = payload["window_summary"]
    joints = payload["joints"]
    lines = []
    a = lines.append
    a("# Streaming the next centre bit from the packed row")
    a("")
    a(
        "Attack on prize problem 3, as specified in "
        "[_astra_ideas10.md](_astra_ideas10.md) item 1 (leftover "
        "[_astra_ideas9.md](_astra_ideas9.md) item 5). Finite evidence only. "
        "**Not a prize claim.**"
    )
    a("")
    a("Certifier: `research/stream_nextbit.py`. Dump: `research/stream_nextbit.json`.")
    a("Does not modify `experiment.py`, `strip_graph.py`, or `strip_extend.py`.")
    a("")
    a("## Local rule and packing")
    a("")
    a("Rule 30 is")
    a("")
    a(r"\[")
    a(r"x(t+1,j)=x(t,j-1)\oplus\bigl(x(t,j)\lor x(t,j+1)\bigr).")
    a(r"\]")
    a("")
    a(r"The next centre bit is therefore three bits of row \(t\):")
    a("")
    a(r"\[")
    a(r"c_{t+1}=x(t,-1)\oplus\bigl(x(t,0)\lor x(t,1)\bigr).")
    a(r"\]")
    a("")
    a(
        (
            r"Packing is `experiment.py`: \(z_0=1\), "
            r"`z=(z<<2)^((z<<1)|z)`, and \(x(t,j)=(z>>(j+t))\&1\). "
            r"The centre is bit \(t\); the triple sits at indices \(t-1,t,t+1\). "
            "Centre bits match `experiment.center_bits` through "
            "{}, including the known 20-bit word "
            r"`11011100110001011001`. \(N_t=\operatorname{{popcount}}(z\land(z{{\ll}}1))\) "
            "agrees with [packed_valuation.md](packed_valuation.md) on the "
            "published sample times."
        ).format(payload["t_hi"] + 1)
    )
    a("")
    a("## Word-RAM baseline (allowed only as a control)")
    a("")
    a(
        r"Given \(z\) and the index \(t\), three bit tests plus a few "
        r"Boolean operations return \(c_{t+1}\). That is \(O(1)\) in the "
        r"word-RAM / Python-bigint model (bit \(k\) of an integer is a "
        r"constant-time word operation). It still *uses the growing index* "
        r"\(t\). The three-bit formula is therefore not a streaming "
        r"shortcut: Problem 3 is producing \(z_t\) or those three bits "
        r"without \(\Theta(t^2)\) bit operations (each of the \(t\) packed "
        r"updates XORs a \(\Theta(t)\)-bit word). This freeze only kills "
        r"cheap *summaries* of an already-known \(z\)."
    )
    a("")
    a(
        r"The length-3 window at offset \(t-1\) is exactly the packed "
        r"triple. On \(t=8\ldots 4096\) it witnessed-determines both the "
        r"triple and \(c_{t+1}\) (8 values, every value reused, no "
        r"ambiguity). Exact integer equality with the single next bit "
        r"fails, as expected for a 3-bit word."
    )
    a("")
    a("## Freeze")
    a("")
    a(r"Candidate \(o(t)\) statistics of \(z\) at time \(t\le 4096\):")
    a("")
    a(r"- \(\operatorname{popcount}(z)\), and \(\operatorname{popcount}(z\land((1{\ll}k)-1))\) for \(k=8,16,32\)")
    a(r"- \(v_2(z)\), \(v_2(z+1)\), \(v_2(z\oplus(z{\ll}1))\), \(v_2(z\oplus(1{\ll}t))\)")
    a(r"- \(\operatorname{popcount}(z\land(z{\ll}1))=N_t\)")
    a(
        r"- every length-\(\le 8\) bit window, but only at a *fixed* set of "
        r"at most 16 bit positions (offsets \(0..31\)), or at offsets that "
        r"depend on \(t\) only through \(\operatorname{popcount}\) and "
        r"\(v_2\) (16 frozen arithmetic combinations); extracting a window "
        r"at an arbitrary index still costs reading those bits"
    )
    a(r"- the same scalars on \(z\oplus(z{\ll}1)\) and \(z\land(z{\ll}1)\)")
    a("")
    a(
        r"A statistic *equals* the next centre bit if its raw value (or, "
        r"separately, its parity) equals \(c_{t+1}\) for every "
        r"\(t=8\ldots 4096\). It *determines the triple* if every reused "
        r"value is compatible with a single triple (witnessed: some value "
        r"appears at least twice). Injectivity on this finite prefix is "
        r"not an evaluator: a 32-bit left-edge key is expected to be "
        r"unique by the birthday paradox and does not extend."
    )
    a("")
    a(
        r"Costs: \(v_2\) and any window / popcount of \(O(1)\) low bits "
        r"are \(O(1)\) bit operations. Full \(\operatorname{popcount}(z)\), "
        r"\(N_t\), and a histogram of all sliding windows read "
        r"\(\Theta(t)\) bits of a \((2t+1)\)-bit word. Those last are "
        r"killed even if they accidentally determined the triple."
    )
    a("")
    a(r"Primary range \(t=8..4096\). Clean range \(t=32..4096\) makes the")
    a(r"32 LSBs disjoint from the triple (so small-\(t\) overlap cannot")
    a("fake a determination).")
    a("")
    a("## Scalar statistics")
    a("")
    a(
        r"| statistic | cost | eq \(c_{t+1}\) | parity eq | det triple | det next | "
        r"values | reuse | amb triple | first eq fail |"
    )
    a("|---|---|---|---|---|---|---:|---:|---:|---|")
    for rec in scalars:
        fail = rec["first_eq_fail"]
        fail_s = "—" if fail is None else "t={}".format(fail["t"])
        a(
            "| `{name}` | {cost} | {eq} | {par} | {dt} | {dn} | {nv} | {nr} | {na} | {fail} |".format(
                name=rec["name"],
                cost=rec["cost"],
                eq=yn(rec["equals_next_bit"]),
                par=yn(rec["parity_equals_next_bit"]),
                dt=yn(rec["determines_triple_witnessed"]),
                dn=yn(rec["determines_next_witnessed"]),
                nv=rec["n_values"],
                nr=rec["n_reuse_values"],
                na=rec["n_ambiguous_triple"],
                fail=fail_s,
            )
        )
    a("")
    a(
        r"On this orbit \(z\) is always odd, so \(v_2(z)=0\). For the "
        r"experiment packing, \(v_2(z+1)=2\) at every \(t\ge 2\) "
        r"([packed_valuation.md](packed_valuation.md)). "
        r"\(v_2(z\oplus(z{\ll}1))=0\) and \(v_2(z\oplus(1{\ll}t))=0\) "
        r"for \(t>0\) (XOR with bit \(t\) does not touch the LSB). These "
        r"valuations are constants and cannot separate eight triples."
    )
    a("")
    a(
        (
            r"Full \(\operatorname{{popcount}}(z)\) and \(N_t\) have many reused "
            r"values and many ambiguous triples; their parities agree with "
            r"\(c_{{t+1}}\) on about half the times "
            "(popcount parity frac {pc:.3f}, "
            r"\(N_t\) parity frac {nt:.3f}). They also "
            r"read \(\Theta(t)\) bits."
        ).format(
            pc=payload["popcount_parity_frac"],
            nt=payload["N_parity_frac"],
        )
    )
    a("")
    a(r"## Length-\(\le 8\) windows")
    a("")
    a(
        (
            r"Fixed offsets \(0\ldots 31\), lengths \(1\ldots 8\): "
            r"{n_fixed} windows. T-dependent offsets through popcount/\(v_2\) "
            r"({n_fn} frozen functions), same lengths: {n_tdep} windows. "
            r"The second row of each family is the clean range \(t=32..4096\)."
        ).format(
            n_fixed=windows["n_fixed"],
            n_fn=windows["n_t_fns"],
            n_tdep=windows["n_tdep"],
        )
    )
    a("")
    a("| family | tested | eq next | parity eq | det triple | det next | injective |")
    a("|---|---:|---:|---:|---:|---:|---:|")
    for row in windows["tables"]:
        a(
            "| {fam} | {n} | {eq} | {par} | {dt} | {dn} | {inj} |".format(
                fam=row["family"],
                n=row["tested"],
                eq=row["n_equals_next"],
                par=row["n_parity_equals"],
                dt=row["n_determines_triple"],
                dn=row["n_determines_next"],
                inj=row["n_injective"],
            )
        )
    a("")
    a(
        r"No fixed window and no popcount/\(v_2\)-of-\(t\) window equals "
        r"the next bit, equals it in parity, or witnessed-determines the "
        r"triple or the next bit, on either range. First ambiguities occur "
        r"early (typical \(t<64\)); JSON `windows_fixed` / `windows_tdep` "
        r"store the first equality-fail and first triple-ambiguity time "
        r"of each window."
    )
    a("")
    a(
        r"The 16 frozen t-dependent positions are all \(O(\log t)\) and, "
        r"for \(t\ge 32\), lie strictly left of index \(t-1\). They never "
        r"secretly read the triple. The packed 16-bit word at those "
        r"positions is an \(O(1)\) statistic in the scalar table "
        r"(`tdep16`); it collides with distinct triples. The 16 LSBs "
        r"(`low16`) likewise fail on the clean range, where they are "
        r"disjoint from the centre."
    )
    a("")
    a(r"## Joint freeze and \(\Theta(t)\) histograms")
    a("")
    a("| joint | cost | det triple | det next | values | reuse | amb triple | injective |")
    a("|---|---|---|---|---:|---:|---:|---|")
    for rec in joints:
        a(
            "| `{name}` | {cost} | {dt} | {dn} | {nv} | {nr} | {na} | {inj} |".format(
                name=rec["name"],
                cost=rec["cost"],
                dt=yn(rec["determines_triple_witnessed"]),
                dn=yn(rec["determines_next_witnessed"]),
                nv=rec["n_values"],
                nr=rec["n_reuse_values"],
                na=rec["n_ambiguous_triple"],
                inj=yn(rec["injective"]),
            )
        )
    a("")
    a(
        r"The joint of every \(O(1)\) scalar in the freeze (low popcounts, "
        r"valuations, 16 LSBs, t-dep 16-bit gather, length-8 windows at "
        r"popcount(\(t\)) and \(v_2(t+1)\)) remains ambiguous for the "
        r"triple: distinct triples share the same cheap summary. "
        r"Histograms of all length-1/3/8 windows read \(\Theta(t)\) bits "
        r"and are injective fingerprints of the scanned rows (no reuse), "
        r"which is not an \(o(t)\) formula."
    )
    a("")
    a("## Why it died")
    a("")
    a(kill["text"])
    a("")
    a(
        r"A cheap exact formula for \(c_{t+1}\) given \(z_t\) would not by "
        r"itself have been a prize claim: the three-bit local rule already "
        r"is that formula. The missing piece is still an algorithm that "
        r"produces \(z_n\) (or bit \(n\) of it) in \(o(n^2)\) bit "
        r"operations. Not a prize claim."
    )
    a("")
    a("Wall time: `{:.3f}` seconds.".format(payload["elapsed_sec"]))
    a("")
    a(
        r"Self-check: packed centre agrees with `experiment.center_bits` "
        r"on 256 bits and on \(0..4097\); three-bit formula matches "
        r"\(c_{t+1}\) for \(t=1..4096\); \(N_t\) sample matches "
        r"`packed_valuation.json`; \(v_2(z)=0\), \(v_2(z+1)=2\) (\(t\ge 2\))."
    )
    a("")
    return "\n".join(lines) + "\n"


def main() -> None:
    t0 = time.time()
    rows, bits = packed_rows_and_bits(T_HI)
    checks = self_check(rows, bits)
    if not all(
        checks[k] is True
        for k in (
            "centre_matches_experiment_256",
            "known20",
            "formula_matches_next_centre",
            "packing_centre_bit",
            "N_t_sample_matches_packed_valuation",
            "v2_z_eq_0",
            "experiment_v2_z_plus_1_eq_2_for_t_ge_2",
            "baseline_window_is_triple",
            "bits_match_experiment_through_T_HI_plus_1",
            "tdep_at_most_16",
            "tdep_misses_triple_for_t_ge_32",
        )
    ):
        raise AssertionError(f"self-check failed: {checks}")

    triples = [None] * (T_HI + 1)
    next_bits = [None] * (T_HI + 1)
    for t in range(1, T_HI + 1):
        tr = triple_of(rows[t], t)
        triples[t] = tr
        nxt = next_from_triple(tr)
        if nxt != bits[t + 1]:
            raise AssertionError(f"formula mismatch at t={t}")
        next_bits[t] = nxt

    def series(fn):
        out = [None] * (T_HI + 1)
        for t in range(T_LO, T_HI + 1):
            out[t] = fn(t, rows[t])
        return out

    # ---- scalar freeze ----
    scalar_specs = []

    def add_scalar(name, formula, cost, family, fn):
        scalar_specs.append((name, formula, cost, family, fn))

    add_scalar("popcount(z)", "popcount(z)", "Theta(t)", "popcount",
               lambda t, z: z.bit_count())
    for k in LOW_K:
        mask = (1 << k) - 1
        add_scalar(
            f"popcount_low{k}",
            f"popcount(z & ((1<<{k})-1))",
            "O(1)",
            "popcount_low",
            lambda t, z, mask=mask: (z & mask).bit_count(),
        )
    add_scalar("v2(z)", "v2(z)", "O(1)", "v2", lambda t, z: v2_int(z))
    add_scalar("v2(z+1)", "v2(z+1)", "O(1)", "v2", lambda t, z: v2_int(z + 1))
    add_scalar("v2(z XOR (z<<1))", "v2(z XOR (z<<1))", "O(1)", "v2",
               lambda t, z: v2_int(z ^ (z << 1)))
    add_scalar("v2(z XOR (1<<t))", "v2(z XOR (1<<t))", "O(1)", "v2",
               lambda t, z: v2_int(z ^ (1 << t)))
    add_scalar("N_t", "popcount(z & (z<<1))", "Theta(t)", "overlap",
               lambda t, z: (z & (z << 1)).bit_count())
    add_scalar("low16", "z & ((1<<16)-1)", "O(1)", "fixed_bits",
               lambda t, z: z & 0xFFFF)
    add_scalar("low8", "z & 0xFF", "O(1)", "fixed_bits",
               lambda t, z: z & 0xFF)
    add_scalar("tdep16", "16 bits at popcount/v2-of-t positions", "O(1)",
               "tdep_bits",
               lambda t, z: gather_bits(z, t_dep_positions(t)))
    add_scalar("popcount(z XOR (z<<1))", "popcount(z XOR (z<<1))", "Theta(t)",
               "derived", lambda t, z: (z ^ (z << 1)).bit_count())
    add_scalar("v2(z AND (z<<1))", "v2(z AND (z<<1))", "O(1)", "derived",
               lambda t, z: v2_int(z & (z << 1)))
    for k in LOW_K:
        mask = (1 << k) - 1
        add_scalar(
            f"popcount_low{k}(z XOR (z<<1))",
            f"popcount((z XOR (z<<1)) & ((1<<{k})-1))",
            "O(1)",
            "derived",
            lambda t, z, mask=mask: ((z ^ (z << 1)) & mask).bit_count(),
        )
        add_scalar(
            f"popcount_low{k}(z AND (z<<1))",
            f"popcount((z AND (z<<1)) & ((1<<{k})-1))",
            "O(1)",
            "derived",
            lambda t, z, mask=mask: ((z & (z << 1)) & mask).bit_count(),
        )
    add_scalar(
        "baseline_window(t-1,3)",
        "(z>>(t-1)) & 7",
        "O(1) word-RAM, index t",
        "baseline",
        lambda t, z: window(z, t - 1, 3),
    )
    add_scalar(
        "baseline_next_bit",
        "x(t,-1) XOR (x(t,0) OR x(t,1))",
        "O(1) word-RAM, index t",
        "baseline",
        lambda t, z: next_from_triple(triple_of(z, t)),
    )

    scalars = []
    scalar_values = {}
    for name, formula, cost, family, fn in scalar_specs:
        vals = series(fn)
        rec = analyse_series(vals, triples, next_bits, T_LO, T_HI)
        rec_clean = analyse_series(vals, triples, next_bits, T_CLEAN, T_HI)
        rec["clean"] = compact_clean(rec_clean)
        scalars.append(attach_meta(rec, name, formula, cost, family))
        scalar_values[name] = vals

    # ---- windows ----
    windows_fixed = []
    windows_tdep = []
    for L in WINDOW_LENS:
        for off in range(FIXED_OFFSET_CAP):
            vals = series(lambda t, z, L=L, off=off: window(z, off, L))
            rec = analyse_series(vals, triples, next_bits, T_LO, T_HI)
            rec_clean = analyse_series(vals, triples, next_bits, T_CLEAN, T_HI)
            rec["clean"] = {
                "equals_next_bit": rec_clean["equals_next_bit"],
                "parity_equals_next_bit": rec_clean["parity_equals_next_bit"],
                "determines_triple_witnessed": rec_clean["determines_triple_witnessed"],
                "determines_next_witnessed": rec_clean["determines_next_witnessed"],
                "injective": rec_clean["injective"],
                "n_ambiguous_triple": rec_clean["n_ambiguous_triple"],
                "first_triple_ambiguity": rec_clean["first_triple_ambiguity"],
                "first_eq_fail": rec_clean["first_eq_fail"],
            }
            windows_fixed.append(attach_meta(
                rec,
                f"window_L{L}_off{off}",
                f"(z>>{off})&((1<<{L})-1)",
                "O(1)",
                "window_fixed",
            ))
        for fname, fn in T_OFFSET_FNS:
            vals = series(lambda t, z, L=L, fn=fn: window(z, fn(t), L))
            rec = analyse_series(vals, triples, next_bits, T_LO, T_HI)
            rec_clean = analyse_series(vals, triples, next_bits, T_CLEAN, T_HI)
            rec["clean"] = {
                "equals_next_bit": rec_clean["equals_next_bit"],
                "parity_equals_next_bit": rec_clean["parity_equals_next_bit"],
                "determines_triple_witnessed": rec_clean["determines_triple_witnessed"],
                "determines_next_witnessed": rec_clean["determines_next_witnessed"],
                "injective": rec_clean["injective"],
                "n_ambiguous_triple": rec_clean["n_ambiguous_triple"],
                "first_triple_ambiguity": rec_clean["first_triple_ambiguity"],
                "first_eq_fail": rec_clean["first_eq_fail"],
            }
            windows_tdep.append(attach_meta(
                rec,
                f"window_L{L}_{fname}",
                f"(z>>({fname}))&((1<<{L})-1)",
                "O(1)",
                "window_tdep",
            ))

    def window_table(recs, label, use_clean=False):
        src = []
        for r in recs:
            d = r["clean"] if use_clean else r
            src.append(d)
        return {
            "family": label,
            "tested": len(recs),
            "n_equals_next": sum(1 for d in src if d["equals_next_bit"]),
            "n_parity_equals": sum(1 for d in src if d["parity_equals_next_bit"]),
            "n_determines_triple": sum(1 for d in src if d["determines_triple_witnessed"]),
            "n_determines_next": sum(1 for d in src if d["determines_next_witnessed"]),
            "n_injective": sum(1 for d in src if d["injective"]),
        }

    window_summary = {
        "n_fixed": len(windows_fixed),
        "n_tdep": len(windows_tdep),
        "n_t_fns": len(T_OFFSET_FNS),
        "fixed_offset_cap": FIXED_OFFSET_CAP,
        "bit_cap": FIXED_BIT_CAP,
        "lengths": list(WINDOW_LENS),
        "tables": [
            window_table(windows_fixed, "fixed offset 0..31, t=8..4096"),
            window_table(windows_fixed, "fixed offset 0..31, t=32..4096", True),
            window_table(windows_tdep, "popcount/v2-of-t offset, t=8..4096"),
            window_table(windows_tdep, "popcount/v2-of-t offset, t=32..4096", True),
        ],
    }

    # ---- joints ----
    def joint_of(names):
        out = [None] * (T_HI + 1)
        for t in range(T_LO, T_HI + 1):
            out[t] = tuple(scalar_values[n][t] for n in names)
        return out

    o1_names = [
        "popcount_low8", "popcount_low16", "popcount_low32",
        "v2(z)", "v2(z+1)", "v2(z XOR (z<<1))", "v2(z XOR (1<<t))",
        "low16", "tdep16",
        "v2(z AND (z<<1))",
        "popcount_low8(z XOR (z<<1))",
        "popcount_low8(z AND (z<<1))",
    ]
    joint_specs = [
        ("joint_O(1)_scalars", "O(1)", o1_names),
        ("joint_low_popcounts", "O(1)",
         ["popcount_low8", "popcount_low16", "popcount_low32"]),
        ("joint_v2", "O(1)",
         ["v2(z)", "v2(z+1)", "v2(z XOR (z<<1))", "v2(z XOR (1<<t))"]),
        ("joint_Theta(t)_popcount_N", "Theta(t)",
         ["popcount(z)", "N_t", "popcount(z XOR (z<<1))"]),
    ]
    # length-8 windows at two t-dep offsets, bundled with low16.
    w_pc = series(lambda t, z: window(z, t.bit_count(), 8))
    w_v = series(lambda t, z: window(z, v2_int(t + 1), 8))
    joint_extra = [None] * (T_HI + 1)
    for t in range(T_LO, T_HI + 1):
        joint_extra[t] = tuple(scalar_values[n][t] for n in o1_names) + (
            w_pc[t], w_v[t],
        )

    joints = []
    for name, cost, names in joint_specs:
        vals = joint_of(names)
        rec = analyse_series(vals, triples, next_bits, T_LO, T_HI)
        rec_clean = analyse_series(vals, triples, next_bits, T_CLEAN, T_HI)
        rec["clean"] = compact_clean(rec_clean)
        rec["components"] = names
        joints.append(attach_meta(rec, name, "+".join(names), cost, "joint"))
    rec = analyse_series(joint_extra, triples, next_bits, T_LO, T_HI)
    rec_clean = analyse_series(joint_extra, triples, next_bits, T_CLEAN, T_HI)
    rec["clean"] = compact_clean(rec_clean)
    rec["components"] = o1_names + ["window_L8_popcount(t)", "window_L8_v2(t+1)"]
    joints.append(attach_meta(
        rec,
        "joint_O(1)_plus_tdep_windows",
        "O(1) scalars + L8 at popcount(t) and v2(t+1)",
        "O(1)",
        "joint",
    ))

    hist_recs = []
    for L in (1, 3, 8):
        vals = [None] * (T_HI + 1)
        for t in range(T_LO, T_HI + 1):
            vals[t] = histogram_value(rows[t], 2 * t + 1, L)
        rec = analyse_series(vals, triples, next_bits, T_LO, T_HI)
        rec_clean = analyse_series(vals, triples, next_bits, T_CLEAN, T_HI)
        rec["clean"] = compact_clean(rec_clean)
        hist_recs.append(attach_meta(
            rec,
            f"histogram_all_windows_L{L}",
            f"counts of every length-{L} window of z",
            "Theta(t)",
            "histogram",
        ))
    joints.extend(hist_recs)

    all_for_kill = scalars + windows_fixed + windows_tdep
    kill_struct = is_killed(all_for_kill, joints)
    if kill_struct["fired"]:
        text = (
            "Killed. Every statistic in the freeze fails to equal the next "
            "centre bit, and fails to witnessed-determine the triple (or "
            "the next bit), on t=8..4096; the same holds on the clean "
            "range t=32..4096 where fixed low bits are disjoint from the "
            "triple. Full popcount, N_t, XOR-popcount, and all-window "
            "histograms secretly read Theta(t) bits. The three "
            "centre-adjacent bits (length-3 window at offset t-1) work as "
            "a baseline: O(1) word-RAM given z, but they use the growing "
            "index t. The three-bit formula is already O(1) in word RAM "
            "given z, so Problem 3 is really about producing z or those "
            "bits without Theta(t^2) work. This freeze only kills cheap "
            "summaries of z."
        )
    else:
        text = (
            "A non-baseline O(1) statistic equalled the next bit or "
            "witnessed-determined the triple on this prefix. That is still "
            "not a prize claim without a Rule 30 identity. See JSON "
            "survivors."
        )

    sample = []
    for t in range(T_LO, min(32, T_HI) + 1):
        z = rows[t]
        tr = triples[t]
        sample.append({
            "t": t,
            "c": int(bits[t]),
            "c_next": int(next_bits[t]),
            "triple": list(tr),
            "popcount": z.bit_count(),
            "popcount_low8": (z & 0xFF).bit_count(),
            "popcount_low16": (z & 0xFFFF).bit_count(),
            "popcount_low32": (z & ((1 << 32) - 1)).bit_count(),
            "v2_z": v2_int(z),
            "v2_z_plus_1": v2_int(z + 1),
            "v2_z_xor_shift": v2_int(z ^ (z << 1)),
            "v2_z_xor_1_t": v2_int(z ^ (1 << t)),
            "N_t": (z & (z << 1)).bit_count(),
            "low16": z & 0xFFFF,
            "tdep16": gather_bits(z, t_dep_positions(t)),
            "baseline_window": window(z, t - 1, 3),
        })

    pop_rec = next(s for s in scalars if s["name"] == "popcount(z)")
    n_rec = next(s for s in scalars if s["name"] == "N_t")
    elapsed = time.time() - t0
    payload = {
        "not_a_prize_claim": True,
        "ideas": "ideas10 item 1 / leftover ideas9 item 5",
        "problem": 3,
        "packing": (
            "experiment.py: z_0=1, z=(z<<2)^((z<<1)|z), "
            "x(t,j)=(z>>(j+t))&1; triple at bits t-1,t,t+1; "
            "c_{t+1}=x(t,-1) XOR (x(t,0) OR x(t,1))"
        ),
        "not_this_attack": [
            "packed_valuation.md (valuations/overlaps as a formula for c_t itself)",
            "trace_product.md (matrix product in the bits of t)",
            "the three-bit local rule given z, which is already O(1) word-RAM",
        ],
        "t_lo": T_LO,
        "t_hi": T_HI,
        "t_clean": T_CLEAN,
        "self_check": checks,
        "popcount_parity_frac": pop_rec["parity_frac"],
        "N_parity_frac": n_rec["parity_frac"],
        "scalars": scalars,
        "windows_fixed": [compact_window(r) for r in windows_fixed],
        "windows_tdep": [compact_window(r) for r in windows_tdep],
        "window_summary": window_summary,
        "joints": joints,
        "sample_t_8_31": sample,
        "kill": {**kill_struct, "text": text},
        "elapsed_sec": elapsed,
    }
    # Drop nested analyse_series bulk from scalars' clean (keep it; it is small).
    OUT_JSON.write_text(json.dumps(jsonable(payload), indent=2) + "\n")
    OUT_MD.write_text(write_markdown(payload))

    n_o1_cheap = sum(1 for s in scalars + windows_fixed + windows_tdep if cheap_ok(s))
    print(json.dumps({
        "wrote": [str(OUT_JSON), str(OUT_MD)],
        "self_check_ok": True,
        "kill_fired": kill_struct["fired"],
        "n_o1_scalars": sum(1 for s in scalars if s["cost"] == "O(1)"),
        "n_windows_fixed": len(windows_fixed),
        "n_windows_tdep": len(windows_tdep),
        "n_o1_survivors": n_o1_cheap,
        "baseline_works": kill_struct["baseline_works"],
        "window_summary": window_summary["tables"],
        "elapsed_sec": elapsed,
        "kill_text": text,
    }, indent=2))


if __name__ == "__main__":
    main()
