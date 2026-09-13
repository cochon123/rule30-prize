#!/usr/bin/env python3
"""Cycle OJ: pal-right T-xor of G(j-1) is 1 for every odd n.

Let n=2m+1. Pal-right j in [n+1, 2n]. Green doubling gives
G(n,2k)=G(m,k) xor G(m,k-1) and G(n,2k+1)=G(m,k). The pal-right
xor of G(n,j-1) on G(n,j)=1 equals 1 xor the XOR of consecutive
differences of G(m,i) from i=m to i=2m, which telescopes to
1 xor G(m,m) xor G(m,2m)=1 xor 1 xor 1=1. Combined with Cycle
OI's even-n vanish, pal-right T-xor equals n&1 for every n, so
covering T_k (n<2^{k-1}) is 1 iff k=2. Do not claim E_k=0 for
all k. Do not claim T equals rest or S or J_full. Do not claim
pal-right T-xor vanishes on odd n. Do not catalogue further
S/T subregions unless the experiment answers why E_k=0. Do not
claim J6=J10=0 implies J18=1 for all k; do not push even-spine
past k=18; do not bump all n0=16 past 414990. Do not walk k=12
T-bands. Not a prize claim.

Run: python3 research/cycle_oj.py --certify
Dump: research/cycle_oj.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from experiment import center_bits as experiment_center_bits

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cycle_al import G
from cycle_ca import KNOWN20, packed_center_bits
from cycle_kh import g4_xor_cover
from cycle_oi import pal_right_t

OUT = Path(__file__).resolve().with_suffix(".json")
OI_JSON = Path(__file__).resolve().parent / "cycle_oi.json"
OG_JSON = Path(__file__).resolve().parent / "cycle_og.json"

N_ALG = 256
M_ALG = 128


def want_cover_t(k: int) -> int:
    """Covering T on n<2^{k-1} is 1 iff k==2, all k."""
    return int(k == 2)


def xor_flips(bits: list[int]) -> int:
    """XOR of consecutive differences; equals first xor last."""
    acc = 0
    for i in range(len(bits) - 1):
        acc ^= bits[i] ^ bits[i + 1]
    return acc


def boolean_telescope() -> dict:
    """Any bit-string: xor of adjacent diffs equals endpoints xor."""
    n_ok = 0
    for bits in (
        [1],
        [1, 1],
        [1, 0, 1],
        [1, 0, 0, 1],
        [1, 1, 0, 1],
        [0, 1, 0],
        [0],
        [1, 0, 1, 0, 1],
    ):
        got = xor_flips(bits)
        want = bits[0] ^ bits[-1] if bits else 0
        if got != want:
            return {"ok": False, "bits": bits, "got": got, "want": want}
        n_ok += 1
    return {"ok": True, "n_ok": n_ok}


def green_center_corner_pal(n_hi: int) -> dict:
    """G(n,n)=G(n,0)=G(n,2n)=1; G(n,j)=G(n,2n-j)."""
    n_ok = 0
    for n in range(0, n_hi):
        if G(n, n) != 1:
            return {"ok": False, "center": n}
        if G(n, 0) != 1 or G(n, 2 * n) != 1:
            return {"ok": False, "corner": n}
        if G(n, 2 * n + 1) != 0 or G(n, -1) != 0:
            return {"ok": False, "range": n}
        for j in range(0, n + 1):
            if G(n, j) != G(n, 2 * n - j):
                return {"ok": False, "pal": n, "j": j}
            n_ok += 1
    return {"ok": True, "n_hi": n_hi, "n_ok": n_ok}


def doubling_slots(m_hi: int) -> dict:
    """G(2m+1, 2k)=G(m,k) xor G(m,k-1); G(2m+1, 2k+1)=G(m,k)."""
    n_ok = 0
    for m in range(0, m_hi):
        n = 2 * m + 1
        for k in range(0, 2 * m + 2):
            even = G(m, k) ^ G(m, k - 1)
            odd = G(m, k)
            if G(n, 2 * k) != even or G(n, 2 * k + 1) != odd:
                return {"ok": False, "m": m, "k": k}
            n_ok += 1
    return {"ok": True, "m_hi": m_hi, "n_ok": n_ok}


def odd_t_from_parent(m_hi: int) -> dict:
    """Pal-right T(2m+1) = 1 xor G(m,m) xor G(m,2m) = 1."""
    n_ok = n_even_c = n_odd_c = 0
    sample = {}
    for m in range(0, m_hi):
        n = 2 * m + 1
        xor_t, n_t, n_fire = pal_right_t(n)
        ev = od = 0
        for k in range(m + 1, 2 * m + 1):
            if G(m, k - 1) != G(m, k):
                if G(m, k - 1) == 1 and G(m, k) == 0:
                    ev ^= 1
                    n_even_c += 1
                else:
                    od ^= 1
                    n_odd_c += 1
        # k=2m+1 even-j corner: always G(m,2m)=1, G(m,2m+1)=0
        if G(m, 2 * m) != 1 or G(m, 2 * m + 1) != 0:
            return {"ok": False, "corner": m}
        ev ^= 1
        bits = [G(m, i) for i in range(m, 2 * m + 1)]
        tr = xor_flips(bits)
        tel = G(m, m) ^ G(m, 2 * m)
        if (
            xor_t != 1
            or xor_t != (ev ^ od)
            or xor_t != (1 ^ tr)
            or xor_t != (1 ^ tel)
            or tr != 0
            or tel != 0
            or G(m, m) != 1
        ):
            return {
                "ok": False,
                "m": m,
                "xor": xor_t,
                "ev": ev,
                "od": od,
                "tr": tr,
                "tel": tel,
            }
        n_ok += 1
        if n < 16:
            sample[str(n)] = {"xor": xor_t, "n_t": n_t, "n_fire": n_fire}
    ok = (
        n_ok == m_hi
        and sample["1"]["xor"] == 1
        and sample["1"]["n_t"] == 1
        and sample["3"]["xor"] == 1
        and want_cover_t(0) == 0
        and want_cover_t(1) == 0
        and want_cover_t(2) == 1
        and want_cover_t(3) == 0
        and want_cover_t(11) == 0
        and want_cover_t(100) == 0
    )
    return {
        "ok": ok,
        "m_hi": m_hi,
        "n_ok": n_ok,
        "n_even_c": n_even_c,
        "n_odd_c": n_odd_c,
        "sample": sample,
    }


def small_cover_t() -> dict:
    """Covering T_k = xor of n<2^{k-1} pal-right T equals want_cover_t, k<=6."""
    rows = {}
    acc = 0
    for k in range(0, 7):
        lo = 0 if k == 0 else 1 << (k - 1)
        hi = 1 << k
        bx = 0
        n_t = 0
        for n in range(lo, hi):
            xor_t, nt, _ = pal_right_t(n)
            if xor_t != (n & 1):
                return {"ok": False, "n": n, "xor": xor_t}
            bx ^= xor_t
            n_t += nt
        cover = acc
        acc ^= bx
        want = want_cover_t(k)
        if cover != want or (k >= 3 and bx != 0):
            return {"ok": False, "k": k, "cover": cover, "B": bx}
        rows[str(k)] = {
            "B": bx,
            "cover_T": cover,
            "tcum": acc,
            "want": want,
            "n_t": n_t,
        }
    ok = (
        rows["0"]["B"] == 0
        and rows["1"]["B"] == 1
        and rows["2"]["B"] == 1
        and all(rows[str(k)]["B"] == 0 for k in range(3, 7))
        and all(rows[str(k)]["cover_T"] == want_cover_t(k) for k in range(0, 7))
    )
    return {"ok": ok, "rows": rows}


def killed_odd_zero(odd: dict) -> dict:
    r = odd["sample"]["1"]
    ok = r["xor"] == 1
    return {"ok": ok, "n": 1, "xor": r["xor"]}


def killed_t_zero_k2(cover: dict) -> dict:
    r = cover["rows"]["2"]
    ok = r["cover_T"] == 1 and r["B"] == 1
    return {"ok": ok, "k": 2, "cover_T": r["cover_T"], "B": r["B"]}


def killed_eq_e(cover: dict) -> dict:
    """T_2=1 while E_2=0 on q=10."""
    r = cover["rows"]["2"]
    ok = r["cover_T"] == 1
    return {"ok": ok, "k": 2, "T": 1, "E": 0}


def prefixes() -> dict:
    oi = json.loads(OI_JSON.read_text())
    og = json.loads(OG_JSON.read_text())
    ok = (
        oi["checks"]["all_ok"]
        and og["checks"]["all_ok"]
        and oi["verdict"]["even_t_vanish"] == "LEMMA"
        and oi["verdict"]["odd_t_xor_2048"] == "CERTIFIED"
        and oi["verdict"]["odd_t_xor_all_n"] == "PREFIX"
        and oi["verdict"]["T_iff_k2_all_k"] == "PREFIX"
        and og["verdict"]["E_q10_10"] == "CERTIFIED"
        and oi["verdict"]["prize"] == "unsolved"
        and want_cover_t(2) == 1
        and want_cover_t(12) == 0
    )
    return {"ok": ok}


def self_checks(c20, tel, gcp, slots, odd, cover, ko, kt, ke, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        tel["ok"]
        and gcp["ok"]
        and slots["ok"]
        and odd["ok"]
        and cover["ok"]
        and ko["ok"]
        and kt["ok"]
        and ke["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    tel = boolean_telescope()
    gcp = green_center_corner_pal(N_ALG)
    slots = doubling_slots(M_ALG)
    odd = odd_t_from_parent(M_ALG)
    cover = small_cover_t()
    ko = killed_odd_zero(odd)
    kt = killed_t_zero_k2(cover)
    ke = killed_eq_e(cover)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, tel, gcp, slots, odd, cover, ko, kt, ke, sc, pref)
    dump = {
        "cycle": "OJ",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "boolean_telescope": {k: tel[k] for k in tel if k != "ok"},
        "green_center_corner_pal": {k: gcp[k] for k in gcp if k != "ok"},
        "doubling_slots": {k: slots[k] for k in slots if k != "ok"},
        "odd_t_from_parent": {k: odd[k] for k in odd if k != "ok"},
        "small_cover_t": {k: cover[k] for k in cover if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_odd_zero": {k: ko[k] for k in ko if k != "ok"},
        "killed_t_zero_k2": {k: kt[k] for k in kt if k != "ok"},
        "killed_eq_e": {k: ke[k] for k in ke if k != "ok"},
        "lemmas": {
            "odd_t_xor_all_n": True,
            "even_t_vanish": True,
            "T_iff_k2_all_k": True,
            "t_band_ge3": True,
            "E_q10_10": True,
            "odd_zero": False,
            "t_zero_k2": False,
            "eq_e": False,
            "E_all_k": False,
            "prize": False,
        },
        "verdict": {
            "odd_t_xor_all_n": "LEMMA",
            "even_t_vanish": "LEMMA",
            "T_iff_k2_all_k": "LEMMA",
            "t_band_ge3": "LEMMA",
            "E_q10_10": "CERTIFIED",
            "odd_zero": "KILLED",
            "t_zero_k2": "KILLED",
            "eq_e": "KILLED",
            "E_all_k": "PREFIX",
            "J6_J10_0_implies_J18_1_all_k": "PREFIX",
            "eleven_bit_gap": "PREFIX",
            "extra_414990_formula": "PREFIX",
            "at_most_one_odd_all_k": "PREFIX",
            "period_H_seed_all_k": "PREFIX",
            "pi_formula_all_k": "PREFIX",
            "fermat_cover_359_all_k": "PREFIX",
            "I_1_infinitely_often": "OPEN",
            "some_phi_1_infinitely_often": "OPEN",
            "prize": "unsolved",
        },
    }
    if args.certify:
        OUT.write_text(json.dumps(dump, indent=2) + "\n")
        print("wrote", OUT)
    print(json.dumps(dump["verdict"], indent=2))
    print("wall_s", dump["wall_s"])
    print("odd_t_from_parent", dump["odd_t_from_parent"]["n_ok"], "m_hi", dump["odd_t_from_parent"]["m_hi"])
    print("small_cover_t", dump["small_cover_t"]["rows"]["2"])
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_odd_zero", dump["killed_odd_zero"])
    print("killed_t_zero_k2", dump["killed_t_zero_k2"])
    print("killed_eq_e", dump["killed_eq_e"])


if __name__ == "__main__":
    main()
