#!/usr/bin/env python3
"""Cycle FD: reconstruct consecutive 00 iff U=0 and A=B.

For U=reconstruct(A,B), U_{t+1}=A_t XOR (B_t OR U_t). If U_t=0 then
U_{t+1}=A_t XOR B_t, so consecutive 00 iff some t has U_t=0 and A_t=B_t.
On even-n0 scars this restates Cycle FB: n5 has 00 iff n5=0 on an
n3=n4 agreement, n6 has 00 iff n6=0 on an n4=n5 agreement. The no-00
class is exactly n6=1 on every n4=n5 agreement (ham(n4,n5)=n0 always).
Kills: generic reconstruct pairs do not have has00(U) iff
has00(reconstruct(B,U)); FB's iff is scar-specific. Do not claim an
11-bit gap; do not claim no-00 iff extra 22 or 89; do not claim a
formula for extra 414990; do not bump all n0=16 past 414990. Not a
prize claim.

Run: python3 research/cycle_fd.py --certify
Dump: research/cycle_fd.json
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
from cycle_ca import KNOWN20, packed_center_bits, reconstruct
from cycle_ch import ham
from cycle_dv import mask_bits, odd_copy
from cycle_er import U32
from cycle_ev import has00
from cycle_ew import scar_n3_to_n6

OUT = Path(__file__).resolve().with_suffix(".json")
EZ_JSON = Path(__file__).resolve().parent / "cycle_ez.json"
FB_JSON = Path(__file__).resolve().parent / "cycle_fb.json"
FC_JSON = Path(__file__).resolve().parent / "cycle_fc.json"


def cons00_iff_agree() -> dict:
    """U consecutive 00 iff some t has U_t=0 and A_t=B_t. Length 2..8."""
    n_ok = 0
    n_cons = 0
    for n in range(2, 9):
        for ma in range(1 << n):
            a = [(ma >> t) & 1 for t in range(n)]
            for mb in range(1, 1 << n):
                b = [(mb >> t) & 1 for t in range(n)]
                u = reconstruct(a, b)
                if u is None:
                    continue
                cons = any(u[t] == 0 and u[(t + 1) % n] == 0 for t in range(n))
                meet = any(u[t] == 0 and a[t] == b[t] for t in range(n))
                if cons != meet:
                    return {"ok": False, "n": n, "ma": ma, "mb": mb}
                n_ok += 1
                if cons:
                    n_cons += 1
    return {"ok": n_ok == 86868, "n_ok": n_ok, "n_cons": n_cons}


def generic_f_preserves_00() -> dict:
    """has00(U) iff has00(reconstruct(B,U)) on generic defined pairs."""
    n_ok = 0
    n_cex = 0
    for n in range(2, 9):
        for ma in range(1 << n):
            a = [(ma >> t) & 1 for t in range(n)]
            for mb in range(1, 1 << n):
                b = [(mb >> t) & 1 for t in range(n)]
                u = reconstruct(a, b)
                if u is None:
                    continue
                v = reconstruct(b, u)
                if v is None:
                    continue
                if has00(u) == has00(v):
                    n_ok += 1
                else:
                    n_cex += 1
    return {"ok": n_cex > 0, "n_ok": n_ok, "n_cex": n_cex}


def scar_agree() -> dict:
    """n5/n6 00 iff zero on A=B; no-00 iff one on every agreement."""
    n_ok = 0
    n_no00 = 0
    n_has00 = 0
    ham_ok = True
    for n0 in range(2, 11, 2):
        L = 2 * n0
        for mask in range(1 << n0):
            t = odd_copy(mask_bits(mask, n0))
            n3, n4, n5, n6 = scar_n3_to_n6(t)
            if n6 is None:
                return {"ok": False, "n0": n0, "n6": True}
            if ham(n4, n5) != n0:
                ham_ok = False
                return {"ok": False, "n0": n0, "ham": ham(n4, n5)}
            meet5 = any(n5[t] == 0 and n3[t] == n4[t] for t in range(L))
            meet6 = any(n6[t] == 0 and n4[t] == n5[t] for t in range(L))
            if meet5 != has00(n5) or meet6 != has00(n6):
                return {"ok": False, "n0": n0, "meet": True}
            if has00(n5) != has00(n6):
                return {"ok": False, "n0": n0, "iff": True}
            if has00(n5):
                n_has00 += 1
            else:
                n_no00 += 1
                if any(n6[t] == 0 and n4[t] == n5[t] for t in range(L)):
                    return {"ok": False, "n0": n0, "no00": True}
                if any(n5[t] == 0 and n3[t] == n4[t] for t in range(L)):
                    return {"ok": False, "n0": n0, "no00_n5": True}
            n_ok += 1
    return {
        "ok": n_ok == 1364 and n_no00 == 124 and n_has00 == 1240 and ham_ok,
        "n_ok": n_ok,
        "n_has00": n_has00,
        "n_no00": n_no00,
        "ham_n4_n5_equals_n0": ham_ok,
    }


def tstar() -> dict:
    t = [int(c) for c in U32]
    n3, n4, n5, n6 = scar_n3_to_n6(t)
    L = 32
    ok = (
        n6 is not None
        and ham(n4, n5) == 16
        and has00(n5)
        and has00(n6)
        and any(n5[i] == 0 and n3[i] == n4[i] for i in range(L))
        and any(n6[i] == 0 and n4[i] == n5[i] for i in range(L))
    )
    return {
        "ok": ok,
        "n5_has00": has00(n5),
        "n6_has00": has00(n6),
        "ham_n4_n5": ham(n4, n5),
        "n5_meet": any(n5[i] == 0 and n3[i] == n4[i] for i in range(L)),
        "n6_meet": any(n6[i] == 0 and n4[i] == n5[i] for i in range(L)),
    }


def prefixes() -> dict:
    ez = json.loads(EZ_JSON.read_text())
    fb = json.loads(FB_JSON.read_text())
    fc = json.loads(FC_JSON.read_text())
    ok = (
        ez["checks"]["all_ok"]
        and fb["checks"]["all_ok"]
        and fc["checks"]["all_ok"]
        and ez["verdict"]["cons11_iff_U_meets_zero_of_A"] == "LEMMA"
        and fb["verdict"]["n5_00_iff_n6_00"] == "LEMMA"
        and fc["verdict"]["even_n0_n7_consecutive_11_proved"] == "LEMMA"
        and fc["verdict"]["prize"] == "unsolved"
    )
    return {"ok": ok}


def self_checks(
    c20, gen: dict, killed: dict, scar: dict, ts: dict, pref: dict
) -> dict:
    assert list(c20) == KNOWN20
    assert list(c20) == list(experiment_center_bits(20))
    assert gen["ok"] and killed["ok"] and scar["ok"] and ts["ok"] and pref["ok"]
    return {"all_ok": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certify", action="store_true")
    args = parser.parse_args()
    t0 = time.perf_counter()
    c20 = packed_center_bits(20)
    gen = cons00_iff_agree()
    killed = generic_f_preserves_00()
    scar = scar_agree()
    ts = tstar()
    pref = prefixes()
    checks = self_checks(c20, gen, killed, scar, ts, pref)
    dump = {
        "cycle": "FD",
        "wall_s": round(time.perf_counter() - t0, 3),
        "checks": checks,
        "general": {k: gen[k] for k in gen if k != "ok"},
        "killed_generic": {k: killed[k] for k in killed if k != "ok"},
        "scar": {k: scar[k] for k in scar if k != "ok"},
        "tstar": {k: ts[k] for k in ts if k != "ok"},
        "lemmas": {
            "cons00_iff_U0_and_A_eq_B": True,
            "scar_n5_n6_00_iff_zero_on_agreement": True,
            "no00_class_is_one_on_all_agreements": True,
            "ham_n4_n5_equals_n0": True,
            "generic_has00_U_iff_has00_FU": False,
            "eleven_bit_gap": None,
            "extra_414990_formula": None,
            "at_most_one_odd_all_k": None,
            "period_H_seed_all_k": None,
            "prize": False,
        },
        "verdict": {
            "cons00_iff_U0_and_A_eq_B": "LEMMA",
            "scar_n5_n6_00_iff_zero_on_agreement": "LEMMA",
            "no00_class_is_one_on_all_agreements": "LEMMA",
            "ham_n4_n5_equals_n0": "LEMMA",
            "generic_has00_U_iff_has00_FU": "KILLED",
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
    print("general", dump["general"])
    print("killed_generic", dump["killed_generic"])
    print("scar", dump["scar"])
    print("tstar", dump["tstar"])


if __name__ == "__main__":
    main()
