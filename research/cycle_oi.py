#!/usr/bin/env python3
"""Cycle OI: pal-right T-xor of G(j-1) is 1 iff n is odd.

Even n: if G(n,j)=1 then j is even, so j-1 is odd, so G(n,j-1)=0
(Green even-n / odd-d). Pal-right T-xor and T-fire therefore vanish
on every even n. That is a lemma, not a finite certificate.

Odd n<2048: pal-right xor of G(n,j-1) on G=1 is identically 1
(CERTIFIED; not claimed for all odd n). Each odd n contributes 1
and even n contribute 0, so the dyadic band B_k is the number of
odd n in [2^{k-1}, 2^k) mod 2. For k<=11 this proves Cycle OH's
vanish (B_k=0 for 3<=k<=11) from the per-n identity, not a re-walk
of bands. Do not claim the odd-n xor is 1 for all odd n. Do not
claim pal-right T-xor vanishes on odd n. Do not claim T is 1 iff
k=2 for all k. Do not walk k=12 T-bands. Do not catalogue further
S/T subregions unless the experiment answers why E_k=0. Do not
claim J6=J10=0 implies J18=1 for all k; do not push even-spine
past k=18; do not bump all n0=16 past 414990. Not a prize claim.

Run: python3 research/cycle_oi.py --certify
Dump: research/cycle_oi.json
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
from cycle_oh import WANT as OH_WANT
from cycle_oh import want_t_band

OUT = Path(__file__).resolve().with_suffix(".json")
OH_JSON = Path(__file__).resolve().parent / "cycle_oh.json"
OG_JSON = Path(__file__).resolve().parent / "cycle_og.json"

N_ODD = 2048
N_EVEN_CHECK = 2048


def pal_right_t(n: int) -> tuple[int, int, int]:
    """Pal-right G=1 xor of G(j-1), cell count, fire count."""
    xor_t = n_t = n_fire = 0
    for j in range(n + 1, 2 * n + 1):
        if G(n, j) == 0:
            continue
        n_t += 1
        b = G(n, j - 1)
        xor_t ^= b
        n_fire += b
    return xor_t, n_t, n_fire


def even_n_odd_d_zero(n_hi: int) -> dict:
    """If n even and d odd then G(n,d)=0, n<n_hi. Green even-n clause."""
    n_checked = 0
    for n in range(0, n_hi, 2):
        for d in range(1, 2 * n + 1, 2):
            if G(n, d) != 0:
                return {"ok": False, "n": n, "d": d}
            n_checked += 1
    return {"ok": True, "n_even": n_hi // 2, "n_odd_d": n_checked}


def even_t_from_green(n: int, j: int) -> int:
    """Lemma: even n and G(n,j)=1 imply G(n,j-1)=0."""
    if n % 2:
        raise ValueError("even n required")
    if G(n, j) == 0:
        return 0
    if j % 2:
        raise AssertionError("even n cannot have G=1 at odd j")
    return G(n, j - 1)


def walk_n(n_hi: int) -> dict:
    """n<n_hi: even pal-right T-fire 0; odd pal-right T-xor 1."""
    n_t_even = n_fire_even = n_t_odd = n_fire_odd = 0
    n_odd = n_even_g1 = 0
    odd_bad = even_bad = None
    bands = {
        k: {"xor": 0, "n_t": 0, "n_fire": 0, "n_t_odd": 0, "n_t_even": 0, "n_odd": 0}
        for k in range(0, 12)
    }
    sample_odd = {}
    for n in range(0, n_hi):
        xor_t, n_t, n_fire = pal_right_t(n)
        k = 0 if n == 0 else n.bit_length()
        if k <= 11:
            bands[k]["xor"] ^= xor_t
            bands[k]["n_t"] += n_t
            bands[k]["n_fire"] += n_fire
            if n % 2:
                bands[k]["n_t_odd"] += n_t
                bands[k]["n_odd"] += 1
            else:
                bands[k]["n_t_even"] += n_t
        if n % 2 == 0:
            if xor_t != 0 or n_fire != 0:
                even_bad = {"n": n, "xor": xor_t, "n_fire": n_fire}
                break
            n_t_even += n_t
            n_fire_even += n_fire
            if n_t:
                n_even_g1 += 1
            for j in range(n + 1, 2 * n + 1):
                if G(n, j) == 0:
                    continue
                if even_t_from_green(n, j) != 0:
                    even_bad = {"n": n, "j": j, "lemma": 1}
                    break
            if even_bad:
                break
        else:
            if xor_t != 1:
                odd_bad = {"n": n, "xor": xor_t, "n_t": n_t, "n_fire": n_fire}
                break
            n_t_odd += n_t
            n_fire_odd += n_fire
            n_odd += 1
            if n < 64:
                sample_odd[str(n)] = {
                    "xor": xor_t,
                    "n_t": n_t,
                    "n_fire": n_fire,
                }
    if even_bad is not None:
        return {"ok": False, "even_bad": even_bad}
    if odd_bad is not None:
        return {"ok": False, "odd_bad": odd_bad}
    for k in range(0, 12):
        pk = OH_WANT[k]
        if (
            bands[k]["xor"] != pk["xor"]
            or bands[k]["n_t"] != pk["n_t"]
            or bands[k]["n_fire"] != pk["n_fire"]
            or bands[k]["xor"] != want_t_band(k)
        ):
            return {"ok": False, "k": k, "band": bands[k], "want": pk}
        if k >= 2 and bands[k]["n_odd"] != (1 << (k - 2)):
            return {"ok": False, "k": k, "n_odd": bands[k]["n_odd"]}
        if k >= 3 and bands[k]["xor"] != 0:
            return {"ok": False, "k": k, "xor": bands[k]["xor"]}
    acc = 0
    tcum = {}
    for k in range(0, 12):
        tcum[str(k)] = {"cover_T": acc}
        acc ^= bands[k]["xor"]
        tcum[str(k)]["tcum"] = acc
        if tcum[str(k)]["cover_T"] != int(k == 2):
            return {"ok": False, "cover_T": tcum, "k": k}
    ok = (
        n_odd == n_hi // 2
        and n_fire_even == 0
        and n_t_even > 0
        and sample_odd["1"]["xor"] == 1
        and sample_odd["1"]["n_t"] == 1
        and sample_odd["1"]["n_fire"] == 1
        and all(sample_odd[str(n)]["xor"] == 1 for n in range(1, 64, 2))
        and bands[1]["xor"] == 1
        and bands[2]["xor"] == 1
        and bands[11]["n_t"] == 164352
        and bands[11]["n_fire"] == 62976
        and n_t_even + n_t_odd == 237568
        and n_fire_even + n_fire_odd == 91136
    )
    return {
        "ok": ok,
        "n_hi": n_hi,
        "n_odd": n_odd,
        "n_even_g1": n_even_g1,
        "n_t_even": n_t_even,
        "n_fire_even": n_fire_even,
        "n_t_odd": n_t_odd,
        "n_fire_odd": n_fire_odd,
        "sample_odd": sample_odd,
        "bands": {
            str(k): {
                "xor": bands[k]["xor"],
                "n_t": bands[k]["n_t"],
                "n_fire": bands[k]["n_fire"],
                "n_t_odd": bands[k]["n_t_odd"],
                "n_t_even": bands[k]["n_t_even"],
                "n_odd": bands[k]["n_odd"],
                "cover_T": tcum[str(k)]["cover_T"],
                "tcum": tcum[str(k)]["tcum"],
            }
            for k in range(0, 12)
        },
    }


def killed_odd_zero(walk: dict) -> dict:
    r = walk["sample_odd"]["1"]
    ok = r["xor"] == 1 and r["n_t"] == 1
    return {"ok": ok, "n": 1, "xor": r["xor"], "n_t": r["n_t"]}


def killed_even_fire(walk: dict) -> dict:
    ok = walk["n_fire_even"] == 0 and walk["n_t_even"] > 0
    return {
        "ok": ok,
        "n_fire_even": walk["n_fire_even"],
        "n_t_even": walk["n_t_even"],
        "n_even_g1": walk["n_even_g1"],
    }


def killed_odd_empty(walk: dict) -> dict:
    r = walk["sample_odd"]["1"]
    ok = r["n_t"] == 1
    return {"ok": ok, "n": 1, "n_t": r["n_t"]}


def prefixes() -> dict:
    oh = json.loads(OH_JSON.read_text())
    og = json.loads(OG_JSON.read_text())
    ok = (
        oh["checks"]["all_ok"]
        and og["checks"]["all_ok"]
        and oh["verdict"]["t_band_ge3"] == "CERTIFIED"
        and og["verdict"]["E_q10_10"] == "CERTIFIED"
        and oh["verdict"]["prize"] == "unsolved"
        and want_t_band(2) == 1
        and want_t_band(11) == 0
    )
    return {"ok": ok}


def self_checks(c20, green, walk, ko, ke, kem, sc, pref) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert (
        green["ok"]
        and walk["ok"]
        and ko["ok"]
        and ke["ok"]
        and kem["ok"]
        and sc["ok"]
        and pref["ok"]
    )
    assert walk["n_fire_even"] == 0
    assert walk["n_odd"] == N_ODD // 2
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    green = even_n_odd_d_zero(N_EVEN_CHECK)
    walk = walk_n(N_ODD)
    ko = killed_odd_zero(walk)
    ke = killed_even_fire(walk)
    kem = killed_odd_empty(walk)
    sc = g4_xor_cover()
    pref = prefixes()
    checks = self_checks(c20, green, walk, ko, ke, kem, sc, pref)
    dump = {
        "cycle": "OI",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "even_n_odd_d": {k: green[k] for k in green if k != "ok"},
        "walk_n": {k: walk[k] for k in walk if k != "ok"},
        "g4_xor_cover": {
            "n_ok": sc["n_ok"],
            "n_g1": sc["n_g1"],
            "n_eq_pack": sc["n_eq_pack"],
        },
        "killed_odd_zero": {k: ko[k] for k in ko if k != "ok"},
        "killed_even_fire": {k: ke[k] for k in ke if k != "ok"},
        "killed_odd_empty": {k: kem[k] for k in kem if k != "ok"},
        "lemmas": {
            "even_t_vanish": True,
            "odd_t_xor_2048": True,
            "t_band_ge3": True,
            "E_q10_10": True,
            "odd_zero": False,
            "even_fire": False,
            "odd_empty": False,
            "odd_t_xor_all_n": False,
            "T_iff_k2_all_k": False,
            "prize": False,
        },
        "verdict": {
            "even_t_vanish": "LEMMA",
            "odd_t_xor_2048": "CERTIFIED",
            "t_band_ge3": "CERTIFIED",
            "E_q10_10": "CERTIFIED",
            "odd_zero": "KILLED",
            "even_fire": "KILLED",
            "odd_empty": "KILLED",
            "odd_t_xor_all_n": "PREFIX",
            "T_iff_k2_all_k": "PREFIX",
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
    print(
        "walk_n n_odd",
        dump["walk_n"]["n_odd"],
        "n_t_odd",
        dump["walk_n"]["n_t_odd"],
        "n_t_even",
        dump["walk_n"]["n_t_even"],
        "n_fire_even",
        dump["walk_n"]["n_fire_even"],
    )
    print("g4_xor_cover", dump["g4_xor_cover"])
    print("killed_odd_zero", dump["killed_odd_zero"])
    print("killed_even_fire", dump["killed_even_fire"])
    print("killed_odd_empty", dump["killed_odd_empty"])


if __name__ == "__main__":
    main()
