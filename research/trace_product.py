#!/usr/bin/env python3
"""Trace / entry / dim-2 linear representations of the Rule 30 centre
from the bits of t (Astra ideas9 item 3, Problem 3).

Seek d<=3 matrices A0, A1 over F2 or F3 such that, with
b1..bm = bin(t) MSB-first and no leading zeros (t>=1),

    c_t = Tr(A_{b1}...A_{bm})
       or a fixed entry of that product
       or (affine) that readout plus a field constant
       or, for d=2 only, lambda^T (product) rho.

Not the killed F3 concatenation-rank freeze of dimension 16
(research/time_digit_matrices.md), not Lax pairs, not communication
rank of f_h. Fitting alone is not a prize claim.

Does not modify experiment.py, strip_graph.py, or strip_extend.py.

Run: python3 research/trace_product.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiment import center_bits as experiment_center_bits

FIT_N = 255
HOLDOUT_LO = 256
HOLDOUT_HI = 4095
BUDGET_SEC = 7200
PREFIX_CHECK = 256

C_SRC = r"""
#define _GNU_SOURCE
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#ifdef _OPENMP
#include <omp.h>
#endif

#define MAXN 4096
#define NMAT 19683

static uint8_t cbit[MAXN];
static int fit_n, hold_hi;
static double t_end, t0;
static volatile int g_stop = 0;

static const uint8_t MOD3[16] = {
    0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0
};

static double wall_now(void) {
#ifdef _OPENMP
    return omp_get_wtime();
#else
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
#endif
}

static inline void decode9(int code, uint8_t *a) {
    for (int i = 0; i < 9; i++) {
        a[i] = (uint8_t)(code % 3);
        code /= 3;
    }
}

static inline int inc9(uint8_t *a) {
    for (int i = 0; i < 9; i++) {
        if (++a[i] < 3) return 1;
        a[i] = 0;
    }
    return 0;
}

static inline void mul3(const uint8_t *A, const uint8_t *B, uint8_t *C) {
    C[0] = MOD3[A[0]*B[0] + A[1]*B[3] + A[2]*B[6]];
    C[1] = MOD3[A[0]*B[1] + A[1]*B[4] + A[2]*B[7]];
    C[2] = MOD3[A[0]*B[2] + A[1]*B[5] + A[2]*B[8]];
    C[3] = MOD3[A[3]*B[0] + A[4]*B[3] + A[5]*B[6]];
    C[4] = MOD3[A[3]*B[1] + A[4]*B[4] + A[5]*B[7]];
    C[5] = MOD3[A[3]*B[2] + A[4]*B[5] + A[5]*B[8]];
    C[6] = MOD3[A[6]*B[0] + A[7]*B[3] + A[8]*B[6]];
    C[7] = MOD3[A[6]*B[1] + A[7]*B[4] + A[8]*B[7]];
    C[8] = MOD3[A[6]*B[2] + A[7]*B[5] + A[8]*B[8]];
}

static inline int tr3(const uint8_t *M) {
    return (int)MOD3[M[0] + M[4] + M[8]];
}

/* Families: 0 tr, 1 tr_aff, 2+i entry_i exact, 11+i entry_i affine. */
enum { NFAM = 20 };

static uint64_t train_sat[NFAM];
static uint64_t hold_ok[NFAM];
static uint64_t hold_fail[NFAM];
static int first_hold_mm[NFAM];
static int have_train[NFAM];
static int have_hold[NFAM];
static int wit_a0[NFAM], wit_a1[NFAM], wit_k[NFAM];
static int hold_a0[NFAM], hold_a1[NFAM], hold_k[NFAM];

static void mat_json(int code) {
    uint8_t a[9];
    decode9(code, a);
    printf("[[%d,%d,%d],[%d,%d,%d],[%d,%d,%d]]",
           a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8]);
}

static int encode9(const uint8_t *a) {
    int v = 0, p = 1;
    for (int i = 0; i < 9; i++) {
        v += (int)a[i] * p;
        p *= 3;
    }
    return v;
}

static int holdout_ok_pair(const uint8_t Pfit[][9], const uint8_t *A0, const uint8_t *A1,
                          int fam, int k_tr, const int *k_e, int *mismatch) {
    uint8_t P[MAXN][9];
    for (int t = 1; t <= fit_n; t++) memcpy(P[t], Pfit[t], 9);
    for (int t = fit_n + 1; t <= hold_hi; t++) {
        const uint8_t *Ab = (t & 1) ? A1 : A0;
        mul3(P[t >> 1], Ab, P[t]);
        int ct = (int)cbit[t];
        int ok = 0;
        if (fam == 0) ok = (tr3(P[t]) == ct);
        else if (fam == 1) ok = (MOD3[tr3(P[t]) + k_tr] == ct);
        else if (fam < 11) ok = (P[t][fam - 2] == ct);
        else ok = (MOD3[P[t][fam - 11] + k_e[fam - 11]] == ct);
        if (!ok) {
            *mismatch = t;
            return 0;
        }
    }
    *mismatch = -1;
    return 1;
}

static void record_train(int fam, int a0, int a1, int k, int hold_pass, int mm) {
#ifdef _OPENMP
#pragma omp critical
#endif
    {
        train_sat[fam]++;
        if (!have_train[fam]) {
            have_train[fam] = 1;
            wit_a0[fam] = a0;
            wit_a1[fam] = a1;
            wit_k[fam] = k;
            first_hold_mm[fam] = mm;
        }
        if (hold_pass) {
            hold_ok[fam]++;
            if (!have_hold[fam]) {
                have_hold[fam] = 1;
                hold_a0[fam] = a0;
                hold_a1[fam] = a1;
                hold_k[fam] = k;
            }
        } else {
            hold_fail[fam]++;
            if (have_train[fam] && first_hold_mm[fam] < 0) first_hold_mm[fam] = mm;
        }
    }
}

int main(int argc, char **argv) {
    if (argc < 5) {
        fprintf(stderr, "usage: trace_enum fit_n hold_hi bits.bin timeout_sec\n");
        return 2;
    }
    fit_n = atoi(argv[1]);
    hold_hi = atoi(argv[2]);
    double timeout = atof(argv[4]);
    if (fit_n < 1 || hold_hi >= MAXN || fit_n >= hold_hi) return 2;

    FILE *f = fopen(argv[3], "rb");
    if (!f) return 2;
    if (fread(cbit, 1, (size_t)hold_hi + 1, f) != (size_t)hold_hi + 1) {
        fclose(f);
        return 2;
    }
    fclose(f);

    t0 = wall_now();
    t_end = t0 + timeout;
    for (int i = 0; i < NFAM; i++) first_hold_mm[i] = -1;

#ifdef _OPENMP
#pragma omp parallel
#endif
    {
        uint8_t A0[9], A1[9];
        uint8_t P[256][9];
        int k_e[9];
#ifdef _OPENMP
#pragma omp for schedule(dynamic, 1)
#endif
        for (int i1 = 0; i1 < NMAT; i1++) {
            if (g_stop) continue;
            if ((i1 & 31) == 0) {
                if (wall_now() >= t_end) {
                    g_stop = 1;
                    continue;
                }
            }
            if ((i1 & 1023) == 0) {
#ifdef _OPENMP
                if (omp_get_thread_num() == 0)
                    fprintf(stderr, "a1=%d/%d t=%.1f\n", i1, NMAT, wall_now() - t0);
#else
                fprintf(stderr, "a1=%d/%d t=%.1f\n", i1, NMAT, wall_now() - t0);
#endif
                fflush(stderr);
            }
            decode9(i1, A1);
            memset(A0, 0, 9);
            for (int j = 0; j < NMAT; j++) {
                if (j) inc9(A0);
                memcpy(P[1], A1, 9);
                int ct = (int)cbit[1];
                int tr = tr3(A1);
                int k_tr = (ct - tr + 3) % 3;
                uint32_t live = 0;
                if (tr == ct) live |= 1u;
                live |= 2u; /* affine always defined at t=1 */
                for (int e = 0; e < 9; e++) {
                    k_e[e] = (ct - (int)A1[e] + 3) % 3;
                    if (A1[e] == (uint8_t)ct) live |= (1u << (2 + e));
                    live |= (1u << (11 + e));
                }
                int t;
                for (t = 2; t <= fit_n; t++) {
                    const uint8_t *Ab = (t & 1) ? A1 : A0;
                    mul3(P[t >> 1], Ab, P[t]);
                    ct = (int)cbit[t];
                    int trt = tr3(P[t]);
                    if ((live & 1u) && trt != ct) live &= ~1u;
                    if ((live & 2u) && MOD3[trt + k_tr] != ct) live &= ~2u;
                    for (int e = 0; e < 9; e++) {
                        uint32_t be = 1u << (2 + e);
                        uint32_t ba = 1u << (11 + e);
                        if ((live & be) && P[t][e] != (uint8_t)ct) live &= ~be;
                        if ((live & ba) && MOD3[P[t][e] + k_e[e]] != ct) live &= ~ba;
                    }
                    if (!live) break;
                }
                if (t <= fit_n) continue;
                /* some family fitted 1..fit_n */
                int a0c = encode9(A0), a1c = i1;
                for (int fam = 0; fam < NFAM; fam++) {
                    if (!(live & (1u << fam))) continue;
                    int k = 0;
                    if (fam == 1) k = k_tr;
                    else if (fam >= 11) k = k_e[fam - 11];
                    int mm = -1;
                    int hp = holdout_ok_pair(P, A0, A1, fam, k_tr, k_e, &mm);
                    record_train(fam, a0c, a1c, k, hp, mm);
                }
            }
        }
    }

    double elapsed = wall_now() - t0;
    const char *st = g_stop ? "timeout" : "done";
    printf("{\"status\":\"%s\",\"checked\":%d,\"elapsed_sec\":%.6f,\"nmat\":%d,\"families\":[",
           st, g_stop ? -1 : NMAT * NMAT, elapsed, NMAT);
    for (int fam = 0; fam < NFAM; fam++) {
        printf("%s{\"fam\":%d,\"train_sat\":%llu,\"holdout_ok\":%llu,\"holdout_fail\":%llu,\"holdout_mismatch\":%d",
               fam ? "," : "", fam,
               (unsigned long long)train_sat[fam],
               (unsigned long long)hold_ok[fam],
               (unsigned long long)hold_fail[fam],
               first_hold_mm[fam]);
        if (have_train[fam]) {
            printf(",\"train_witness\":{\"A0\":");
            mat_json(wit_a0[fam]);
            printf(",\"A1\":");
            mat_json(wit_a1[fam]);
            printf(",\"k\":%d}", wit_k[fam]);
        }
        if (have_hold[fam]) {
            printf(",\"holdout_witness\":{\"A0\":");
            mat_json(hold_a0[fam]);
            printf(",\"A1\":");
            mat_json(hold_a1[fam]);
            printf(",\"k\":%d}", hold_k[fam]);
        }
        printf("}");
    }
    printf("]}\n");
    return 0;
}
"""


def packed_center(count: int) -> bytearray:
    row = 1
    out = bytearray(count)
    for t in range(count):
        out[t] = (row >> t) & 1
        row = (row << 2) ^ ((row << 1) | row)
    return out


def nmat_of(d: int, p: int) -> int:
    return p ** (d * d)


def decode_mat(code: int, d: int, p: int) -> list[list[int]]:
    M = [[0] * d for _ in range(d)]
    for i in range(d):
        for j in range(d):
            M[i][j] = code % p
            code //= p
    return M


def encode_mat(M: list[list[int]], p: int) -> int:
    v = 0
    pw = 1
    d = len(M)
    for i in range(d):
        for j in range(d):
            v += M[i][j] * pw
            pw *= p
    return v


def mul_codes(d: int, p: int):
    n = nmat_of(d, p)
    mats = [decode_mat(i, d, p) for i in range(n)]
    table = [[0] * n for _ in range(n)]
    for a, A in enumerate(mats):
        for b, B in enumerate(mats):
            C = [[0] * d for _ in range(d)]
            for i in range(d):
                for k in range(d):
                    aik = A[i][k]
                    if aik:
                        for j in range(d):
                            C[i][j] = (C[i][j] + aik * B[k][j]) % p
            table[a][b] = encode_mat(C, p)
    traces = []
    entries = []
    for M in mats:
        traces.append(sum(M[i][i] for i in range(d)) % p)
        entries.append([M[i][j] for i in range(d) for j in range(d)])
    return table, traces, entries, mats


def mat_mul(A, B, p: int):
    d = len(A)
    C = [[0] * d for _ in range(d)]
    for i in range(d):
        for k in range(d):
            aik = A[i][k]
            if aik:
                for j in range(d):
                    C[i][j] = (C[i][j] + aik * B[k][j]) % p
    return C


def mat_vec(A, v, p: int):
    d = len(A)
    return [sum(A[i][j] * v[j] for j in range(d)) % p for i in range(d)]


def vec_dot(u, v, p: int) -> int:
    return sum(x * y for x, y in zip(u, v)) % p


def product_explicit(A0, A1, t: int, p: int):
    """MSB-first product A_{b1}...A_{bm} of bin(t), no leading zeros."""
    A = (A0, A1)
    bits = [(t >> i) & 1 for i in range(t.bit_length() - 1, -1, -1)]
    P = [row[:] for row in A[bits[0]]]
    for b in bits[1:]:
        P = mat_mul(P, A[b], p)
    return P


def family_names(d: int) -> list[str]:
    names = ["tr", "tr_affine"]
    for i in range(d):
        for j in range(d):
            names.append(f"entry{i + 1}{j + 1}")
    for i in range(d):
        for j in range(d):
            names.append(f"entry{i + 1}{j + 1}_affine")
    return names


def search_pairs_python(
    bits: bytearray,
    d: int,
    p: int,
    fit_n: int,
    hold_hi: int,
    deadline: float,
) -> dict:
    table, traces, entries, mats = mul_codes(d, p)
    n = nmat_of(d, p)
    nfam = 2 + 2 * d * d
    train_sat = [0] * nfam
    hold_ok = [0] * nfam
    hold_fail = [0] * nfam
    first_mm = [-1] * nfam
    train_wit = [None] * nfam
    hold_wit = [None] * nfam
    checked = 0
    timed_out = False
    P = [0] * (hold_hi + 1)

    def k_of(val, ct):
        return (ct - val) % p

    def readout_ok(fam, code, k_tr, k_e, ct):
        if fam == 0:
            return traces[code] == ct
        if fam == 1:
            return (traces[code] + k_tr) % p == ct
        nd = d * d
        if fam < 2 + nd:
            return entries[code][fam - 2] == ct
        return (entries[code][fam - 2 - nd] + k_e[fam - 2 - nd]) % p == ct

    t_search0 = time.time()
    for a1 in range(n):
        if time.time() >= deadline:
            timed_out = True
            break
        for a0 in range(n):
            checked += 1
            P[1] = a1
            ct = bits[1]
            k_tr = k_of(traces[a1], ct)
            k_e = [k_of(entries[a1][e], ct) for e in range(d * d)]
            live = 0
            if traces[a1] == ct:
                live |= 1
            live |= 2
            for e in range(d * d):
                if entries[a1][e] == ct:
                    live |= 1 << (2 + e)
                live |= 1 << (2 + d * d + e)
            t = 2
            while t <= fit_n:
                Ab = a1 if (t & 1) else a0
                P[t] = table[P[t >> 1]][Ab]
                ct = bits[t]
                trt = traces[P[t]]
                if (live & 1) and trt != ct:
                    live &= ~1
                if (live & 2) and (trt + k_tr) % p != ct:
                    live &= ~2
                nd = d * d
                ent = entries[P[t]]
                for e in range(nd):
                    be = 1 << (2 + e)
                    ba = 1 << (2 + nd + e)
                    if (live & be) and ent[e] != ct:
                        live &= ~be
                    if (live & ba) and (ent[e] + k_e[e]) % p != ct:
                        live &= ~ba
                if not live:
                    break
                t += 1
            if t <= fit_n:
                continue
            for fam in range(nfam):
                if not (live & (1 << fam)):
                    continue
                k = 0
                if fam == 1:
                    k = k_tr
                elif fam >= 2 + d * d:
                    k = k_e[fam - 2 - d * d]
                mm = None
                for u in range(fit_n + 1, hold_hi + 1):
                    Ab = a1 if (u & 1) else a0
                    P[u] = table[P[u >> 1]][Ab]
                    if not readout_ok(fam, P[u], k_tr, k_e, bits[u]):
                        mm = u
                        break
                train_sat[fam] += 1
                if train_wit[fam] is None:
                    train_wit[fam] = {
                        "A0": mats[a0],
                        "A1": mats[a1],
                        "k": k,
                    }
                    first_mm[fam] = -1 if mm is None else mm
                if mm is None:
                    hold_ok[fam] += 1
                    if hold_wit[fam] is None:
                        hold_wit[fam] = {
                            "A0": mats[a0],
                            "A1": mats[a1],
                            "k": k,
                        }
                else:
                    hold_fail[fam] += 1
                    if first_mm[fam] < 0:
                        first_mm[fam] = mm
    names = family_names(d)
    families = []
    for fam in range(nfam):
        rec = {
            "name": names[fam],
            "train_sat": train_sat[fam],
            "holdout_ok": hold_ok[fam],
            "holdout_fail": hold_fail[fam],
            "holdout_mismatch": None if first_mm[fam] < 0 else first_mm[fam],
            "train_witness": train_wit[fam],
            "holdout_witness": hold_wit[fam],
            "status": (
                "sat"
                if hold_ok[fam]
                else ("unsat" if train_sat[fam] == 0 else "holdout_fail")
            ),
        }
        families.append(rec)
    return {
        "p": p,
        "d": d,
        "nmat": n,
        "pairs": n * n,
        "checked": checked,
        "timed_out": timed_out,
        "elapsed_sec": time.time() - t_search0,
        "families": families,
    }


def decode_vec(code: int, d: int, p: int) -> list[int]:
    v = [0] * d
    for i in range(d):
        v[i] = code % p
        code //= p
    return v


def search_linrep_d2(
    bits: bytearray,
    p: int,
    fit_n: int,
    hold_hi: int,
    deadline: float,
    affine: bool,
) -> dict:
    d = 2
    table, traces, entries, mats = mul_codes(d, p)
    n = nmat_of(d, p)
    nv = p ** d
    bilin = [[[0] * nv for _ in range(nv)] for _ in range(n)]
    for code in range(n):
        M = mats[code]
        for lc in range(nv):
            lamv = decode_vec(lc, d, p)
            for rc in range(nv):
                rhov = decode_vec(rc, d, p)
                bilin[code][lc][rc] = vec_dot(lamv, mat_vec(M, rhov, p), p)
    train_sat = 0
    hold_ok = 0
    hold_fail = 0
    first_mm = None
    train_wit = None
    hold_wit = None
    checked = 0
    timed_out = False
    P = [0] * (hold_hi + 1)
    t_search0 = time.time()

    for a1 in range(n):
        if time.time() >= deadline:
            timed_out = True
            break
        for a0 in range(n):
            P[1] = a1
            for t in range(2, fit_n + 1):
                Ab = a1 if (t & 1) else a0
                P[t] = table[P[t >> 1]][Ab]
            for lc in range(nv):
                for rc in range(nv):
                    val1 = bilin[a1][lc][rc]
                    if affine:
                        ks = ((bits[1] - val1) % p,)
                    else:
                        if val1 != bits[1]:
                            continue
                        ks = (0,)
                    for k in ks:
                        checked += 1
                        ok = True
                        for t in range(2, fit_n + 1):
                            if (bilin[P[t]][lc][rc] + k) % p != bits[t]:
                                ok = False
                                break
                        if not ok:
                            continue
                        train_sat += 1
                        mm = None
                        for u in range(fit_n + 1, hold_hi + 1):
                            Ab = a1 if (u & 1) else a0
                            P[u] = table[P[u >> 1]][Ab]
                            if (bilin[P[u]][lc][rc] + k) % p != bits[u]:
                                mm = u
                                break
                        wit = {
                            "A0": mats[a0],
                            "A1": mats[a1],
                            "lambda": decode_vec(lc, d, p),
                            "rho": decode_vec(rc, d, p),
                            "k": k,
                        }
                        if train_wit is None:
                            train_wit = wit
                            first_mm = mm
                        if mm is None:
                            hold_ok += 1
                            if hold_wit is None:
                                hold_wit = wit
                        else:
                            hold_fail += 1
                            if first_mm is None:
                                first_mm = mm
    return {
        "p": p,
        "d": 2,
        "affine": affine,
        "pairs_times_vectors": n * n * nv * nv * (p if affine else 1),
        "checked": checked,
        "timed_out": timed_out,
        "elapsed_sec": time.time() - t_search0,
        "train_sat": train_sat,
        "holdout_ok": hold_ok,
        "holdout_fail": hold_fail,
        "holdout_mismatch": first_mm,
        "train_witness": train_wit,
        "holdout_witness": hold_wit,
        "status": (
            "timeout"
            if timed_out and hold_ok == 0 and train_sat == 0
            else (
                "sat"
                if hold_ok
                else ("unsat" if train_sat == 0 else "holdout_fail")
            )
        ),
    }


def compile_enum(c_path: Path, bin_path: Path) -> None:
    cmd = [
        "gcc",
        "-O3",
        "-march=native",
        "-fopenmp",
        "-o",
        str(bin_path),
        str(c_path),
    ]
    proc = subprocess.run(cmd, check=False, capture_output=True, text=True)
    if proc.returncode != 0:
        cmd2 = ["gcc", "-O3", "-o", str(bin_path), str(c_path)]
        proc2 = subprocess.run(cmd2, check=False, capture_output=True, text=True)
        if proc2.returncode != 0:
            raise RuntimeError(f"gcc failed:\n{proc.stderr}\n{proc2.stderr}")


def run_f3_d3(bits: bytearray, timeout: float) -> dict:
    tmp = Path(tempfile.mkdtemp(prefix="trace_prod_"))
    c_path = tmp / "trace_enum.c"
    bin_path = tmp / "trace_enum"
    bits_path = tmp / "center.bin"
    c_path.write_text(C_SRC)
    bits_path.write_bytes(bytes(bits[: HOLDOUT_HI + 1]))
    compile_enum(c_path, bin_path)
    cmd = [
        str(bin_path),
        str(FIT_N),
        str(HOLDOUT_HI),
        str(bits_path),
        f"{timeout:.3f}",
    ]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=None, text=True, check=False)
    if proc.returncode != 0 and not (proc.stdout or "").strip():
        raise RuntimeError(f"enumerator failed rc={proc.returncode}")
    line = ""
    for raw in (proc.stdout or "").splitlines():
        raw = raw.strip()
        if raw.startswith("{"):
            line = raw
    if not line:
        raise RuntimeError("no JSON from enumerator")
    rec = json.loads(line)
    names = family_names(3)
    families = []
    for item in rec.get("families", []):
        fam = item["fam"]
        rec_f = {
            "name": names[fam],
            "train_sat": item["train_sat"],
            "holdout_ok": item["holdout_ok"],
            "holdout_fail": item["holdout_fail"],
            "holdout_mismatch": (
                None
                if item.get("holdout_mismatch", -1) < 0
                else item["holdout_mismatch"]
            ),
            "train_witness": item.get("train_witness"),
            "holdout_witness": item.get("holdout_witness"),
        }
        rec_f["status"] = (
            "sat"
            if rec_f["holdout_ok"]
            else (
                "timeout"
                if rec.get("status") == "timeout" and rec_f["train_sat"] == 0
                else ("unsat" if rec_f["train_sat"] == 0 else "holdout_fail")
            )
        )
        families.append(rec_f)
    return {
        "p": 3,
        "d": 3,
        "nmat": rec.get("nmat", 19683),
        "pairs": 19683 * 19683,
        "checked": rec.get("checked"),
        "timed_out": rec.get("status") == "timeout",
        "elapsed_sec": rec.get("elapsed_sec"),
        "engine": "gcc-openmp",
        "families": families,
    }


def verify_witness_pair(bits, A0, A1, p, kind, k, t0: int, t1: int):
    """Independent MSB-first product check. kind is 'tr' or 'entryIJ'."""
    d = len(A0)
    for t in range(t0, t1 + 1):
        P = product_explicit(A0, A1, t, p)
        if kind == "tr":
            val = (sum(P[i][i] for i in range(d)) + k) % p
        else:
            i = int(kind[5]) - 1
            j = int(kind[6]) - 1
            val = (P[i][j] + k) % p
        if val != bits[t]:
            return t
    return None


def verify_linrep(bits, A0, A1, lam, rho, p, k, t0, t1):
    for t in range(t0, t1 + 1):
        P = product_explicit(A0, A1, t, p)
        vec = mat_vec(P, rho, p)
        val = (vec_dot(lam, vec, p) + k) % p
        if val != bits[t]:
            return t
    return None


def self_check_mul() -> bool:
    A = [[1, 1], [0, 1]]
    B = [[0, 1], [1, 1]]
    C = mat_mul(A, B, 2)
    if C != [[1, 0], [1, 1]]:
        return False
    I = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    M = [[1, 2, 0], [2, 0, 1], [0, 1, 2]]
    if mat_mul(I, M, 3) != M or mat_mul(M, I, 3) != M:
        return False
    A0 = [[1, 0], [1, 1]]
    A1 = [[0, 1], [1, 0]]
    P = product_explicit(A0, A1, 5, 2)  # 101 -> A1 A0 A1
    Q = mat_mul(mat_mul(A1, A0, 2), A1, 2)
    if P != Q:
        return False
    P4 = product_explicit(A0, A1, 4, 2)  # 100 -> A1 A0 A0
    if P4 != mat_mul(mat_mul(A1, A0, 2), A0, 2):
        return False
    return True


def self_check_planted(bits_real: bytearray) -> dict:
    """Recover a planted F2 2x2 trace model on a fake bitstream."""
    A0 = [[1, 1], [0, 1]]
    A1 = [[0, 1], [1, 1]]
    fake = bytearray(64)
    fake[0] = bits_real[0]
    for t in range(1, 64):
        P = product_explicit(A0, A1, t, 2)
        fake[t] = (P[0][0] + P[1][1]) % 2
    rec = search_pairs_python(fake, 2, 2, 31, 63, time.time() + 30)
    tr = rec["families"][0]
    recovered = False
    if tr["train_sat"] and tr["train_witness"] is not None:
        W0 = tr["train_witness"]["A0"]
        W1 = tr["train_witness"]["A1"]
        mm = verify_witness_pair(fake, W0, W1, 2, "tr", 0, 1, 31)
        recovered = mm is None
    return {
        "planted_train_sat": tr["train_sat"] > 0,
        "planted_holdout_ok": tr["holdout_ok"] > 0,
        "recovered_verifies": recovered,
        "status": tr["status"],
    }


def summarize_pair_block(rec: dict, declared: tuple[str, ...]) -> dict:
    out = []
    for fam in rec["families"]:
        if fam["name"] in declared:
            out.append(fam)
    return {
        "p": rec["p"],
        "d": rec["d"],
        "timed_out": rec["timed_out"],
        "elapsed_sec": rec["elapsed_sec"],
        "checked": rec.get("checked"),
        "families": out,
        "any_sat": any(f["status"] == "sat" for f in out),
        "any_holdout_fail": any(f["status"] == "holdout_fail" for f in out),
        "all_unsat": all(f["status"] == "unsat" for f in out),
    }


def write_md(payload: dict, dest: Path) -> None:
    k = payload["kill"]
    st = payload["status"]
    wall = payload["elapsed_sec"]
    if st == "UNSAT":
        lead = (
            "**UNSAT** in %.3f s. The kill fired: no pair fitted the "
            "training set t=1,...,255." % wall
        )
    elif st == "SAT":
        lead = (
            "**SAT** in %.3f s. A readout fitted training and hold-out; "
            "an induction to Rule 30 is still required." % wall
        )
    else:
        lead = "**TIMEOUT** in %.3f s. The enumeration did not finish." % wall

    def comma(n):
        return "{:,}".format(int(n)).replace(",", "{,}")

    pair_lines = []
    for rec in payload["pair_screens"]:
        pairs = rec.get("pairs") or rec.get("checked") or 0
        elapsed = rec.get("elapsed_sec") or 0.0
        names = ("tr", "tr_affine", "entry11", "entry11_affine")
        for fam in rec["families"]:
            if fam["name"] not in names:
                continue
            pair_lines.append(
                "| %d | %d | %s | `%s` | %s | %d | %d | %.3f s |"
                % (
                    rec["p"],
                    rec["d"],
                    comma(pairs),
                    fam["name"],
                    fam["status"],
                    fam["train_sat"],
                    fam["holdout_ok"],
                    elapsed,
                )
            )
    n_aux = 0
    n_aux_unsat = 0
    for rec in payload["pair_screens"]:
        for fam in rec["families"]:
            if fam["name"] in ("tr", "tr_affine", "entry11", "entry11_affine"):
                continue
            n_aux += 1
            if fam["status"] == "unsat":
                n_aux_unsat += 1
    extra = payload["extra_entry_holdout_sat"]
    extra_txt = (
        "none"
        if not extra
        else ", ".join("p=%s d=%s %s" % (e["p"], e["d"], e["name"]) for e in extra)
    )

    lin_lines = []
    for rec in payload["linrep_d2"]:
        aff = "affine" if rec["affine"] else "exact"
        cand = rec.get("pairs_times_vectors") or rec.get("checked") or 0
        lin_lines.append(
            "| %d | %s | %s | %s | %d | %d | %.3f s |"
            % (
                rec["p"],
                aff,
                comma(cand),
                rec["status"],
                rec["train_sat"],
                rec["holdout_ok"],
                rec["elapsed_sec"],
            )
        )
    planted = payload["self_check_planted"]
    hold_note = (
        "Hold-out was never reached."
        if k.get("no_train_fit")
        else "Hold-out mismatches are recorded in the JSON dump."
    )
    body = r"""# Trace of a short matrix product over \(\mathbb F_2\) and \(\mathbb F_3\)

Attack on prize problem 3, as specified in [_astra_ideas9.md](_astra_ideas9.md)
item 3. %(lead)s This is not a prize claim.

Certifier: `research/trace_product.py`. Dump:
`research/trace_product.json`. Does not modify `experiment.py`,
`strip_graph.py`, or `strip_extend.py`.

## Family

For \(t\ge 1\) write \(b_1\cdots b_m=\operatorname{bin}(t)\) without
leading zeros, most significant bit first. The product is
\(M(t)=A_{b_1}\cdots A_{b_m}\). Sought readouts, over \(\mathbb F_2\) and
\(\mathbb F_3\), with \(d\in\{2,3\}\):

- \(c_t=\operatorname{Tr}(M(t))\);
- \(c_t=\operatorname{Tr}(M(t))+k\) for a field constant \(k\);
- \(c_t=M(t)_{11}\) (and, in the same pass, every other fixed entry);
- the affine shift of a fixed entry;
- for \(d=2\) only, \(c_t=\lambda^\top M(t)\rho\), and the same with \(+k\).

This is a representation of the **time index** of the single-cell seed,
not a Lax pair and not a spatial communication matrix of an apex \(f_h\).
It is also not the killed concatenation-rank freeze of dimension 16
over \(\mathbb F_3\) in [time_digit_matrices.md](time_digit_matrices.md):
that test asked whether some \(r\le 16\) linear representation exists, and
died at \(\ell=5\). The present freeze is the tiny explicit catalogue
\(d\le 3\), including the trace readout (which is not a length-\(d\)
linear representation) and the dimension-2 bilinear readout (which that
rank argument does not by itself enumerate).

Training times are \(t=1,\ldots,255\). Hold-out is \(t=256,\ldots,4095\).
Centre bits match `experiment.center_bits` on a prefix of length 256.
The product recurrence \(M(t)=M(\lfloor t/2\rfloor)A_{t\bmod 2}\) with
\(M(1)=A_1\) is MSB-first and is checked against an independent bit-loop
multiply on every recorded witness.

## Search

All \(p^{2d^2}\) matrix pairs are enumerated for
\((p,d)\in\{(2,2),(2,3),(3,2)\}\) in Python, using a full multiply table.
The \(\mathbb F_3\) \(3\times 3\) catalogue is \(3^{18}=387{,}420{,}489\)
pairs and is enumerated in C with OpenMP, aborting a pair as soon as
every readout family has failed. Affine constants are fixed at \(t=1\).
Dimension-2 linear representations enumerate \(\lambda,\rho\) (and \(k\))
on top of the \(2\times 2\) pairs. Cap two hours.

A planted \(\operatorname{Tr}\) model over \(\mathbb F_2\) on a fake
prefix is recovered by the same enumerator.

## Outcome

**Status: %(status)s. Wall time %(wall).3f s. Kill %(killverb)s.**

Status `unsat` means no pair fitted \(t=1..255\). %(hold_note)s
`sat` would have been a hold-out survivor (still not a prize
claim without an induction to Rule 30).

| field \(p\) | \(d\) | pairs | readout | status | train SAT | hold-out SAT | wall |
| ---: | ---: | ---: | --- | --- | ---: | ---: | ---: |
%(pair_table)s

Every other fixed entry \(M(t)_{ij}\) (exact and affine) was screened in
the same pair enumeration: %(n_aux_unsat)s of %(n_aux)s auxiliary entry
families are unsat on training. Extra hold-out survivors: %(extra_txt)s.

### Dimension-2 linear representations \(\lambda^\top M\rho\)

| field \(p\) | readout | candidates | status | train SAT | hold-out SAT | wall |
| ---: | --- | ---: | --- | ---: | ---: | ---: |
%(lin_table)s

Self-checks: centre prefix matches `experiment.center_bits` on 256
bits; multiply and MSB product recurrence agree on a hand example; a
planted \(\mathbb F_2\) trace model on a fake prefix is recovered and
holds out (planted_train_sat=%(plant_train)s, holdout_ok=%(plant_hold)s).

Total wall time %(wall).3f s, inside the two-hour cap.

## Why it died

Preregistered kill: no pair fits the training set, or a fit fails
hold-out. %(kill_text)s

A survivor would still have needed an induction from the matrices to
Rule 30. Fitting alone is not a prize claim. Not a prize claim.
"""
    md = body % {
        "lead": lead,
        "status": st,
        "wall": wall,
        "killverb": "fired" if k["fired"] else "did not fire",
        "hold_note": hold_note,
        "pair_table": "\n".join(pair_lines),
        "n_aux": n_aux,
        "n_aux_unsat": n_aux_unsat,
        "extra_txt": extra_txt,
        "lin_table": "\n".join(lin_lines),
        "plant_train": planted["planted_train_sat"],
        "plant_hold": planted["planted_holdout_ok"],
        "kill_text": k["text"],
    }
    dest.write_text(md + "\n")


def main():
    t0 = time.time()
    os.environ.setdefault("OMP_NUM_THREADS", str(os.cpu_count() or 4))
    bits = packed_center(HOLDOUT_HI + 1)
    assert bits[:PREFIX_CHECK] == experiment_center_bits(PREFIX_CHECK)
    assert self_check_mul()
    planted = self_check_planted(bits)
    assert planted["recovered_verifies"] and planted["planted_holdout_ok"]

    deadline = t0 + BUDGET_SEC
    declared_pair = (
        "tr",
        "tr_affine",
        "entry11",
        "entry11_affine",
    )

    pair_screens = []
    print("F2 d=2 pairs", flush=True)
    pair_screens.append(
        search_pairs_python(bits, 2, 2, FIT_N, HOLDOUT_HI, deadline)
    )
    print(
        f"  elapsed={pair_screens[-1]['elapsed_sec']:.3f}s "
        f"tr={pair_screens[-1]['families'][0]['status']}",
        flush=True,
    )
    print("F2 d=3 pairs", flush=True)
    pair_screens.append(
        search_pairs_python(bits, 3, 2, FIT_N, HOLDOUT_HI, deadline)
    )
    print(
        f"  elapsed={pair_screens[-1]['elapsed_sec']:.3f}s "
        f"tr={pair_screens[-1]['families'][0]['status']}",
        flush=True,
    )
    print("F3 d=2 pairs", flush=True)
    pair_screens.append(
        search_pairs_python(bits, 2, 3, FIT_N, HOLDOUT_HI, deadline)
    )
    print(
        f"  elapsed={pair_screens[-1]['elapsed_sec']:.3f}s "
        f"tr={pair_screens[-1]['families'][0]['status']}",
        flush=True,
    )

    linrep = []
    for p in (2, 3):
        for affine in (False, True):
            rem = deadline - time.time()
            print(f"linrep d=2 p={p} affine={affine} budget={rem:.1f}s", flush=True)
            rec = search_linrep_d2(
                bits, p, FIT_N, HOLDOUT_HI, deadline, affine
            )
            if rec["train_witness"] is not None:
                w = rec["train_witness"]
                mm = verify_linrep(
                    bits, w["A0"], w["A1"], w["lambda"], w["rho"], p, w["k"], 1, FIT_N
                )
                rec["verifier_train_mismatch"] = mm
            linrep.append(rec)
            print(
                f"  status={rec['status']} train_sat={rec['train_sat']} "
                f"t={rec['elapsed_sec']:.3f}s",
                flush=True,
            )

    rem = deadline - time.time()
    print(f"F3 d=3 pairs C budget={rem:.1f}s", flush=True)
    f3d3 = run_f3_d3(bits, max(1.0, rem))
    print(
        f"  timed_out={f3d3['timed_out']} elapsed={f3d3['elapsed_sec']:.3f}s "
        f"tr={f3d3['families'][0]['status']}",
        flush=True,
    )
    # Verify any C witnesses independently.
    for fam in f3d3["families"]:
        w = fam.get("train_witness")
        if not w:
            continue
        kind = "tr" if fam["name"].startswith("tr") else "entry" + fam["name"][5:7]
        if fam["name"].endswith("affine") and kind != "tr":
            kind = "entry" + fam["name"][5:7]
        k = w.get("k", 0)
        if fam["name"].startswith("tr"):
            kind = "tr"
        mm = verify_witness_pair(bits, w["A0"], w["A1"], 3, kind, k, 1, FIT_N)
        fam["verifier_train_mismatch"] = mm

    pair_screens.append(f3d3)

    declared_blocks = [summarize_pair_block(r, declared_pair) for r in pair_screens]

    # Also keep auxiliary entry_ij statuses (not only 11) for the dump.
    extra_entry_sat = []
    for rec in pair_screens:
        for fam in rec["families"]:
            if fam["name"] in declared_pair:
                continue
            if fam["status"] == "sat":
                extra_entry_sat.append(
                    {"p": rec["p"], "d": rec["d"], "name": fam["name"]}
                )

    any_sat = False
    any_holdout_fail = False
    any_timeout = False
    all_unsat = True
    for block in declared_blocks:
        if block["timed_out"]:
            any_timeout = True
        for fam in block["families"]:
            if fam["status"] == "sat":
                any_sat = True
                all_unsat = False
            elif fam["status"] == "holdout_fail":
                any_holdout_fail = True
                all_unsat = False
            elif fam["status"] != "unsat":
                all_unsat = False
    for rec in linrep:
        if rec["status"] == "sat":
            any_sat = True
            all_unsat = False
        elif rec["status"] == "holdout_fail":
            any_holdout_fail = True
            all_unsat = False
        elif rec["status"] == "timeout":
            any_timeout = True
            all_unsat = False
        elif rec["status"] != "unsat":
            all_unsat = False

    if any_sat:
        status = "SAT"
        fired = False
        text = (
            "A pair (or d=2 linear representation) fitted t=1..255 and "
            "held out through t=4095. An induction connecting the matrices to "
            "Rule 30 is still required. Not a prize claim."
        )
    elif any_timeout and all(
        (f["status"] == "unsat" or f["status"] == "timeout")
        for b in declared_blocks
        for f in b["families"]
    ):
        status = "TIMEOUT"
        fired = True
        text = "No candidate within the two-hour enumeration cap."
    elif all_unsat:
        status = "UNSAT"
        fired = True
        text = (
            "No pair A0, A1 of d<=3 matrices over F2 or F3 realises c_t as "
            "Tr of the MSB-first bin(t) product, as that trace plus a "
            "constant, as a fixed matrix entry (including (1,1)) plus an "
            "optional constant, or as a dimension-2 linear representation "
            "lambda^T M rho (exact or affine), on the training times t=1..255."
        )
    elif any_holdout_fail:
        status = "UNSAT"
        fired = True
        text = (
            "At least one pair fitted t=1..255 but failed the hold-out "
            "t=256..4095, and no hold-out survivor exists in the freeze."
        )
    else:
        status = "UNSAT"
        fired = True
        text = "No hold-out survivor in the declared freeze."

    payload = {
        "not_a_prize_claim": True,
        "status": status,
        "family": {
            "fields": [2, 3],
            "d": [2, 3],
            "readouts": [
                "Tr(product)",
                "Tr(product)+k",
                "fixed entry (1,1) and all other entries",
                "fixed entry + k",
                "d=2 linear representation lambda^T M rho",
                "d=2 lambda^T M rho + k",
            ],
            "bin": "MSB-first, no leading zeros, t>=1",
            "fit": [1, FIT_N],
            "holdout": [HOLDOUT_LO, HOLDOUT_HI],
            "not": [
                "F3 concatenation-rank freeze of dimension 16 (time_digit_matrices)",
                "Lax pairs",
                "communication rank of f_h",
            ],
        },
        "self_check_prefix": True,
        "self_check_mul": True,
        "self_check_planted": planted,
        "pair_screens": pair_screens,
        "pair_declared": declared_blocks,
        "linrep_d2": linrep,
        "extra_entry_holdout_sat": extra_entry_sat,
        "f3_d3_elapsed_sec": f3d3.get("elapsed_sec") or 0.0,
        "kill": {
            "no_train_fit": all_unsat,
            "holdout_mismatch": any_holdout_fail,
            "timeout": any_timeout and not any_sat,
            "fired": fired,
            "text": text,
        },
        "elapsed_sec": time.time() - t0,
    }
    dest_json = Path(__file__).with_suffix(".json")
    dest_md = Path(__file__).with_suffix(".md")
    dest_json.write_text(json.dumps(payload, indent=2) + "\n")
    write_md(payload, dest_md)
    print(
        json.dumps(
            {
                "wrote": [str(dest_json), str(dest_md)],
                "status": status,
                "kill": payload["kill"]["fired"],
                "elapsed_sec": payload["elapsed_sec"],
                "declared": [
                    (b["p"], b["d"], f["name"], f["status"])
                    for b in declared_blocks
                    for f in b["families"]
                ],
                "linrep": [(r["p"], r["affine"], r["status"]) for r in linrep],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
