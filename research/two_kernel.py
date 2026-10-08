#!/usr/bin/env python3
"""2-kernel / k-automaticity screen of the Rule 30 centre (Cycle I).

Cobham sampling of c at n and 2n+1. Not linear complexity L(N), not
substitution tilings, not time-digit matrices, not the bivariate Cartier
attack on U(z,w). Stdlib only. Packed integers. Not a prize claim.

Run: python3 research/two_kernel.py
Writes research/two_kernel.json.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiment import center_bits as experiment_center_bits

# ---------------------------------------------------------------------------
# Frozen experiment
# ---------------------------------------------------------------------------

N_BITS = 1 << 19
PREFIX_LENS = (64, 128)
K_MAX_2 = 13
K_MAX_3 = 8
MORPHISM_RADII = tuple(range(0, 9))
VERIFY_LEN = 256
KNOWN20 = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1]
OUT_JSON = ROOT / "research" / "two_kernel.json"

KILL_CRITERION = (
    "If the number of distinct length-128 prefixes saturates at some "
    "K0 <= 64 for all larger k that the data supports, the finite-kernel "
    "hypothesis survives the screen (then try to identify a 2-DFA; if you "
    "cannot, still report saturation). Finite kernel does NOT prove "
    "periodicity (Thue-Morse), so that is NOT a prize claim; it kills THIS "
    "route as a nonperiodicity proof unless you can still prove the "
    "identified automatic sequence is not eventually periodic AND equals c, "
    "which is a much stronger claim — do not claim it without a proof. "
    "If distinct prefixes grow like 2^k (full kernel) through k=12, the "
    "screen does not kill automaticity-of-small-kernel, but also does NOT "
    "prove infinite kernel. Optionally try a structural lemma (e.g. a "
    "family r_k where kernel words disagree at a predicted index using the "
    "CA). If no lemma, kill the proof-via-automaticity route."
)


def packed_center_bits(count: int) -> bytearray:
    """Rule 30 centre: row=1; row=(row<<2)^((row<<1)|row); bit t is (row>>t)&1."""
    row = 1
    out = bytearray(count)
    for t in range(count):
        out[t] = (row >> t) & 1
        row = (row << 2) ^ ((row << 1) | row)
    return out


def thue_morse(count: int) -> bytearray:
    out = bytearray(count)
    for n in range(count):
        out[n] = n.bit_count() & 1
    return out


def periodic_01(count: int) -> bytearray:
    out = bytearray(count)
    for n in range(count):
        out[n] = n & 1
    return out


def max_k_for(n_bits: int, L: int, base: int) -> int:
    """Largest k with base^k * L <= n_bits."""
    if L > n_bits:
        return -1
    k = 0
    span = L
    while span * base <= n_bits:
        span *= base
        k += 1
    return k


def kernel_prefixes(bits: bytearray, k: int, L: int, base: int) -> list[int]:
    """Length-L prefixes of c[base^k n + r], packed MSB-first (n=0 is high bit)."""
    step = base ** k
    nres = step
    prefs = [0] * nres
    for n in range(L):
        base_idx = n * step
        for r in range(nres):
            prefs[r] = (prefs[r] << 1) | bits[base_idx + r]
    return prefs


def take_parity(word: int, length: int, parity: int) -> int:
    """Extract even (parity=0) or odd (parity=1) bits; MSB is index 0."""
    out = 0
    for i in range(parity, length, 2):
        out = (out << 1) | ((word >> (length - 1 - i)) & 1)
    return out


def count_level(bits: bytearray, k: int, L: int, base: int,
                prev_set: set[int] | None) -> dict:
    n_bits = len(bits)
    step = base ** k
    nres = step
    supported = step * L <= n_bits
    row = {
        "k": k,
        "base": base,
        "residues": nres,
        "prefix_len": L,
        "supported": supported,
        "distinct": None,
        "full_kernel": None,
        "new_vs_prev": None,
        "new_vs_union": None,
        "colliding_classes": None,
        "birthday": None,
        "birthday_safe": None,
    }
    if not supported:
        return row, set()
    prefs = kernel_prefixes(bits, k, L, base)
    uniq = set(prefs)
    distinct = len(uniq)
    colliding = nres - distinct
    birthday = (distinct * distinct) / (2.0 * (2 ** min(L, 60)))
    row["distinct"] = distinct
    row["full_kernel"] = distinct == nres
    row["colliding_classes"] = colliding
    row["birthday"] = birthday
    row["birthday_safe"] = birthday < 0.01
    if prev_set is None:
        row["new_vs_prev"] = distinct
        row["new_vs_union"] = distinct
    else:
        row["new_vs_prev"] = len(uniq - prev_set)
    return row, uniq


def screen_kernel(bits: bytearray, L: int, base: int, k_cap: int) -> dict:
    n_bits = len(bits)
    k_max = min(k_cap, max_k_for(n_bits, L, base))
    rows = []
    prev: set[int] | None = None
    union: set[int] = set()
    for k in range(0, k_max + 1):
        row, uniq = count_level(bits, k, L, base, prev)
        row["new_vs_union"] = len(uniq - union)
        union |= uniq
        row["union_distinct"] = len(union)
        rows.append(row)
        prev = uniq
    return {
        "L": L,
        "base": base,
        "k_max": k_max,
        "rows": rows,
        "union_distinct": len(union),
    }


def closure_2(bits: bytearray, L: int, k_max_parent: int) -> dict:
    """(k,r) even/odd length-L decimations equal (k+1, r) and (k+1, r+2^k)."""
    n_bits = len(bits)
    checks = []
    all_ok = True
    for k in range(0, k_max_parent + 1):
        # Need 2L samples at level k and L samples at level k+1.
        if (1 << k) * (2 * L) > n_bits or (1 << (k + 1)) * L > n_bits:
            checks.append({
                "k": k,
                "supported": False,
                "mismatches": None,
                "residues_checked": None,
            })
            continue
        parent = kernel_prefixes(bits, k, 2 * L, 2)
        child = kernel_prefixes(bits, k + 1, L, 2)
        step = 1 << k
        bad = 0
        for r in range(step):
            even = take_parity(parent[r], 2 * L, 0)
            odd = take_parity(parent[r], 2 * L, 1)
            if even != child[r] or odd != child[r + step]:
                bad += 1
        checks.append({
            "k": k,
            "supported": True,
            "mismatches": bad,
            "residues_checked": step,
            "ok": bad == 0,
        })
        if bad:
            all_ok = False
    return {"L": L, "all_ok": all_ok, "levels": checks}


def closure_p(bits: bytearray, L: int, base: int, k_max_parent: int) -> dict:
    """General base: child residue base*r + d is the d-decimation of parent r."""
    n_bits = len(bits)
    checks = []
    all_ok = True
    for k in range(0, k_max_parent + 1):
        if base ** k * (base * L) > n_bits or base ** (k + 1) * L > n_bits:
            checks.append({"k": k, "supported": False, "mismatches": None})
            continue
        parent = kernel_prefixes(bits, k, base * L, base)
        child = kernel_prefixes(bits, k + 1, L, base)
        nparent = base ** k
        bad = 0
        for r in range(nparent):
            for d in range(base):
                dec = 0
                word = parent[r]
                length = base * L
                for m in range(L):
                    idx = base * m + d
                    dec = (dec << 1) | ((word >> (length - 1 - idx)) & 1)
                # Child residue is r + d * base^k, not base*r + d
                # (the latter is only correct at k=0).
                if dec != child[r + d * nparent]:
                    bad += 1
        checks.append({
            "k": k,
            "supported": True,
            "mismatches": bad,
            "parents_checked": nparent,
            "ok": bad == 0,
        })
        if bad:
            all_ok = False
    return {"L": L, "base": base, "all_ok": all_ok, "levels": checks}


def morphism_window(bits: bytearray, radius: int) -> dict:
    """Is (c_{2n}, c_{2n+1}) a function of the window c[n-r..n+r]?"""
    n_bits = len(bits)
    table: dict[int, int] = {}
    conflicts = 0
    first = None
    n_hi = (n_bits - 1) // 2
    n_lo = radius
    n_hi = min(n_hi, n_bits - 1 - radius)
    for n in range(n_lo, n_hi + 1):
        key = 0
        for j in range(n - radius, n + radius + 1):
            key = (key << 1) | bits[j]
        val = (bits[2 * n] << 1) | bits[2 * n + 1]
        prev = table.get(key)
        if prev is None:
            table[key] = val
        elif prev != val:
            conflicts += 1
            if first is None:
                w = [int(bits[j]) for j in range(n - radius, n + radius + 1)]
                first = {
                    "n": n,
                    "window": w,
                    "old_c2n_c2n1": [(prev >> 1) & 1, prev & 1],
                    "new_c2n_c2n1": [(val >> 1) & 1, val & 1],
                    "c_n": int(bits[n]),
                    "index_2n": 2 * n,
                    "index_2n1": 2 * n + 1,
                }
    return {
        "radius": radius,
        "window_len": 2 * radius + 1,
        "samples": n_hi - n_lo + 1 if n_hi >= n_lo else 0,
        "distinct_windows": len(table),
        "conflicts": conflicts,
        "consistent": conflicts == 0,
        "first_conflict": first,
    }


def morphism_2n1_only(bits: bytearray, radius: int) -> dict:
    """Is c_{2n+1} a function of the window c[n-r..n+r]?"""
    n_bits = len(bits)
    table: dict[int, int] = {}
    conflicts = 0
    first = None
    n_hi = (n_bits - 1) // 2
    n_lo = radius
    n_hi = min(n_hi, n_bits - 1 - radius)
    for n in range(n_lo, n_hi + 1):
        key = 0
        for j in range(n - radius, n + radius + 1):
            key = (key << 1) | bits[j]
        val = bits[2 * n + 1]
        prev = table.get(key)
        if prev is None:
            table[key] = val
        elif prev != val:
            conflicts += 1
            if first is None:
                first = {
                    "n": n,
                    "old": int(prev),
                    "new": int(val),
                    "c_n": int(bits[n]),
                }
    return {
        "radius": radius,
        "conflicts": conflicts,
        "consistent": conflicts == 0,
        "first_conflict": first,
    }


def first_disagree(bits: bytearray, k1: int, r1: int, k2: int, r2: int,
                   max_n: int) -> int | None:
    n_bits = len(bits)
    s1, s2 = 1 << k1, 1 << k2
    i1, i2 = r1, r2
    n = 0
    while i1 < n_bits and i2 < n_bits and n < max_n:
        if bits[i1] != bits[i2]:
            return n
        i1 += s1
        i2 += s2
        n += 1
    return None


def family_disagreements(bits: bytearray) -> dict:
    """Search for a one-parameter family with a uniform disagreement index."""
    n_bits = len(bits)
    even_chain = []
    k_hi = min(18, n_bits.bit_length() - 2)
    for k in range(0, k_hi):
        max_n = n_bits // (1 << (k + 1))
        n_star = first_disagree(bits, k, 0, k + 1, 0, max_n)
        even_chain.append({
            "k": k,
            "family": "r=0 vs even decimation (k+1,0)",
            "first_disagree_n": n_star,
            "index_left": None if n_star is None else n_star << k,
            "index_right": None if n_star is None else n_star << (k + 1),
        })

    odd_chain = []
    for k in range(0, min(16, k_hi)):
        r_k = (1 << k) - 1
        r_next = (1 << (k + 1)) - 1
        max_n = (n_bits - max(r_k, r_next)) // (1 << (k + 1))
        n_star = first_disagree(bits, k, r_k, k + 1, r_next, max_n)
        odd_chain.append({
            "k": k,
            "family": "r=2^k-1 vs r=2^{k+1}-1",
            "first_disagree_n": n_star,
        })

    sibling = []
    for k in range(1, min(13, k_hi + 1)):
        half = 1 << (k - 1)
        max_n = n_bits // (1 << k)
        n_star = first_disagree(bits, k, 0, k, half, max_n)
        sibling.append({
            "k": k,
            "family": "(k,0) vs (k, 2^{k-1})",
            "first_disagree_n": n_star,
        })

    # Predicted-index candidates: n=1,3,5. Count how often they work on even chain.
    pred = {}
    for pred_n in (1, 3, 5, 7):
        hits = 0
        misses = []
        for k in range(0, k_hi):
            i1 = pred_n << k
            i2 = pred_n << (k + 1)
            if i2 >= n_bits:
                break
            if bits[i1] != bits[i2]:
                hits += 1
            else:
                misses.append(k)
        pred[str(pred_n)] = {"hits": hits, "miss_k": misses}

    even_ns = [row["first_disagree_n"] for row in even_chain]
    uniform = (
        even_ns
        and None not in even_ns
        and len(set(even_ns)) == 1
    )
    return {
        "even_decimation_chain": even_chain,
        "all_ones_residue_chain": odd_chain,
        "sibling_half": sibling,
        "predicted_n_even_chain": pred,
        "uniform_disagree_index_on_even_chain": uniform,
        "lemma_found": False,
        "lemma_note": (
            "No CA-predicted index n_* that distinguishes v_k=(c_{2^k n}) "
            "from v_{k+1} for every computed k. n=1 fails (e.g. c(4)=c(8)=1). "
            "A finite table of first-disagreement indices is not a lemma."
        ),
    }


def saturation_report(screen_128: dict) -> dict:
    rows = [r for r in screen_128["rows"] if r["supported"]]
    distincts = [r["distinct"] for r in rows]
    full = all(r["full_kernel"] for r in rows if r["k"] <= 12)
    k12 = next((r for r in rows if r["k"] == 12), None)
    # Saturates at K0<=64 if some tail is bounded by 64.
    sat = False
    k0 = None
    k0_bound = None
    for i, row in enumerate(rows):
        cap = row["distinct"]
        if cap is None or cap > 64:
            continue
        tail = rows[i:]
        if tail and all(t["distinct"] is not None and t["distinct"] <= cap
                        for t in tail):
            sat = True
            k0 = row["k"]
            k0_bound = cap
            break
    return {
        "saturation": sat,
        "k0": k0,
        "K0": k0_bound,
        "full_kernel_through_k12": bool(k12 and k12["full_kernel"] and full),
        "distinct_vs_k": [{"k": r["k"], "distinct": r["distinct"],
                           "residues": r["residues"]} for r in rows],
        "max_distinct": max((d for d in distincts if d is not None), default=0),
    }


def identify_2dfa(screen_128: dict, sat: dict) -> dict:
    if not sat["saturation"]:
        return {
            "attempted": False,
            "reason": (
                "No saturation: each depth-k length-128 prefix class is a "
                "fresh binary tree of size 2^k through the data horizon. "
                "A 2-DFA would need at least max_distinct states; none "
                "identified."
            ),
            "state_lower_bound": sat["max_distinct"],
        }
    return {
        "attempted": True,
        "identified": False,
        "reason": "Saturation at <=64 states, but no 2-DFA constructed.",
        "state_lower_bound": sat["K0"],
    }


def verdict_from(sat: dict, lemma: dict, morph_broken: bool) -> dict:
    if sat["saturation"]:
        status = (
            "finite-kernel hypothesis survives the screen; not a prize claim"
        )
        kill = (
            "THIS route is killed as a nonperiodicity proof: a finite 2-kernel "
            "does not prove periodicity (Thue–Morse). No 2-DFA of c was "
            "identified, and even if it were, equality with an aperiodic "
            "automatic sequence would still need a proof."
        )
        route = "killed_as_nonperiodicity_proof_finite_kernel_not_enough"
    elif sat["full_kernel_through_k12"]:
        status = (
            "distinct length-128 prefixes grow like 2^k (full kernel) "
            "through k=12"
        )
        if lemma["lemma_found"]:
            kill = (
                "Structural family distinguishes infinitely many kernel "
                "words; review before any prize claim."
            )
            route = "lemma_claimed_review_required"
        else:
            kill = (
                "Screen does not prove an infinite kernel. No structural "
                "lemma with a CA-predicted disagreement index. Kill the "
                "proof-via-automaticity route. Not a prize claim."
            )
            route = "killed_proof_via_automaticity_no_lemma"
    else:
        status = "partial growth, neither saturation nor full 2^k through k=12"
        kill = (
            "Inconclusive screen; still no infinite-kernel lemma. "
            "Kill the proof-via-automaticity route. Not a prize claim."
        )
        route = "killed_proof_via_automaticity_inconclusive"
    return {
        "saturation": sat["saturation"],
        "full_kernel_through_k12": sat["full_kernel_through_k12"],
        "morphisms_on_visible_bits_broken": morph_broken,
        "lemma_found": lemma["lemma_found"],
        "status": status,
        "kill_verdict": kill,
        "route": route,
        "prize_claim": False,
    }


def control_screens() -> dict:
    """Thue–Morse saturates at 2; period-2 saturates at 2 from k=1."""
    tm = thue_morse(1 << 14)
    per = periodic_01(1 << 14)
    tm_s = screen_kernel(tm, 128, 2, 10)
    per_s = screen_kernel(per, 128, 2, 10)
    tm_distinct = [r["distinct"] for r in tm_s["rows"] if r["supported"]]
    per_distinct = [r["distinct"] for r in per_s["rows"] if r["supported"]]
    tm_ok = tm_distinct and tm_distinct[0] == 1 and all(d == 2 for d in tm_distinct[1:])
    per_ok = (
        per_distinct
        and per_distinct[0] == 1
        and all(d == 2 for d in per_distinct[1:])
    )
    if not tm_ok:
        raise AssertionError(f"Thue-Morse kernel screen failed: {tm_distinct}")
    if not per_ok:
        raise AssertionError(f"period-01 kernel screen failed: {per_distinct}")
    return {
        "thue_morse_L128": {
            "distinct_vs_k": tm_distinct,
            "saturates_at_2": True,
        },
        "periodic_01_L128": {
            "distinct_vs_k": per_distinct,
            "saturates_at_2_from_k1": True,
        },
    }


def self_check(bits: bytearray) -> dict:
    exp = experiment_center_bits(VERIFY_LEN)
    match = list(bits[:VERIFY_LEN]) == list(exp)
    if not match:
        raise AssertionError("packed centre bits != experiment.center_bits")
    if list(bits[:20]) != KNOWN20:
        raise AssertionError("packed centre bits miss the known 20-bit prefix")
    # Independent tiny generator.
    row = 1
    for t in range(64):
        if ((row >> t) & 1) != bits[t]:
            raise AssertionError("packed replay mismatch")
        row = (row << 2) ^ ((row << 1) | row)
    controls = control_screens()
    # Closure on a short prefix of the real centre.
    cl = closure_2(bits[: 1 << 14], 32, 6)
    if not cl["all_ok"]:
        raise AssertionError("2-kernel closure failed on the 2^14 prefix")
    cl3 = closure_p(bits[: 1 << 14], 16, 3, 4)
    if not cl3["all_ok"]:
        raise AssertionError("3-kernel closure failed on the 2^14 prefix")
    return {
        "experiment_center_bits_prefix": VERIFY_LEN,
        "match_experiment_center_bits": True,
        "known20": True,
        "controls": controls,
        "closure_self_check_ok": True,
        "closure3_self_check_ok": True,
    }


def summarize_table(screen: dict) -> list[dict]:
    out = []
    for r in screen["rows"]:
        out.append({
            "k": r["k"],
            "residues": r["residues"],
            "distinct": r["distinct"],
            "new_vs_prev": r["new_vs_prev"],
            "new_vs_union": r["new_vs_union"],
            "full_kernel": r["full_kernel"],
            "birthday_safe": r["birthday_safe"],
            "supported": r["supported"],
        })
    return out


def main() -> None:
    t0 = time.perf_counter()
    bits = packed_center_bits(N_BITS)
    t_gen = time.perf_counter()
    checks = self_check(bits)
    t_check = time.perf_counter()

    screens2 = {}
    for L in PREFIX_LENS:
        screens2[str(L)] = screen_kernel(bits, L, 2, K_MAX_2)
    t_k2 = time.perf_counter()

    closures2 = {}
    for L in PREFIX_LENS:
        k_parent = min(K_MAX_2 - 1, max_k_for(N_BITS, 2 * L, 2))
        closures2[str(L)] = closure_2(bits, L, k_parent)
    t_cl2 = time.perf_counter()

    screens3 = {}
    closures3 = {}
    for L in PREFIX_LENS:
        screens3[str(L)] = screen_kernel(bits, L, 3, K_MAX_3)
        k_parent = min(K_MAX_3 - 1, max_k_for(N_BITS, 3 * L, 3))
        closures3[str(L)] = closure_p(bits, L, 3, k_parent)
    t_k3 = time.perf_counter()

    morph_pair = [morphism_window(bits, r) for r in MORPHISM_RADII]
    morph_odd = [morphism_2n1_only(bits, r) for r in MORPHISM_RADII]
    morph_broken = (not morph_pair[0]["consistent"]) and all(
        not m["consistent"] for m in morph_pair
    )
    t_morph = time.perf_counter()

    lemma = family_disagreements(bits)
    sat = saturation_report(screens2["128"])
    dfa = identify_2dfa(screens2["128"], sat)
    verdict = verdict_from(sat, lemma, morph_broken)
    t1 = time.perf_counter()

    sha = hashlib.sha256(bytes(bits)).hexdigest()
    report = {
        "status": "finite evidence only; no prize problem solved",
        "attack": "2-kernel / k-automaticity of the Rule 30 centre",
        "not": [
            "linear-complexity L(N)",
            "substitution tilings",
            "time-digit matrices",
            "bivariate Cartier operators on U(z,w)",
        ],
        "kill_criterion": KILL_CRITERION,
        "N": N_BITS,
        "generator": "row=1; row=(row<<2)^((row<<1)|row); bit t = (row>>t)&1",
        "sha256_one_byte_per_bit": sha,
        "self_check": checks,
        "wall_time_seconds": {
            "generate": t_gen - t0,
            "self_check": t_check - t_gen,
            "two_kernel": t_k2 - t_check,
            "closure_2": t_cl2 - t_k2,
            "three_kernel": t_k3 - t_cl2,
            "morphism": t_morph - t_k3,
            "total": t1 - t0,
        },
        "two_kernel": {L: summarize_table(screens2[L]) for L in ("64", "128")},
        "two_kernel_union_distinct": {
            L: screens2[L]["union_distinct"] for L in ("64", "128")
        },
        "two_kernel_raw": screens2,
        "closure_2": closures2,
        "three_kernel": {L: summarize_table(screens3[L]) for L in ("64", "128")},
        "three_kernel_union_distinct": {
            L: screens3[L]["union_distinct"] for L in ("64", "128")
        },
        "three_kernel_raw": screens3,
        "closure_3": closures3,
        "cobham_morphism_c2n_c2n1_from_window": morph_pair,
        "cobham_morphism_c2n1_from_window": morph_odd,
        "family_lemma_screen": lemma,
        "saturation": sat,
        "two_dfa": dfa,
        "kill": verdict,
    }
    OUT_JSON.write_text(json.dumps(report, indent=2) + "\n")
    summary = {
        "N": N_BITS,
        "wall_time_total": report["wall_time_seconds"]["total"],
        "match_experiment_center_bits": True,
        "two_kernel_L128": summarize_table(screens2["128"]),
        "two_kernel_L64": summarize_table(screens2["64"]),
        "three_kernel_L128": summarize_table(screens3["128"]),
        "closure_2_L128_ok": closures2["128"]["all_ok"],
        "closure_3_L128_ok": closures3["128"]["all_ok"],
        "morphism_radii_consistent": [m["consistent"] for m in morph_pair],
        "saturation": sat["saturation"],
        "full_kernel_through_k12": sat["full_kernel_through_k12"],
        "kill_verdict": verdict["kill_verdict"],
        "route": verdict["route"],
        "prize_claim": False,
        "json": str(OUT_JSON),
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
