#!/usr/bin/env python3
"""CFG parse-parity of canonical bin(n) for the Rule 30 centre
(Astra ideas7 item 4).

Seek a Chomsky grammar with 4 nonterminals (start = 0), at most eight
binary productions, and terminal productions X -> 0 and/or X -> 1,
such that c_n = (# parses of bin(n) without leading zeros) mod 2.
No ε or unit productions. n=0 is omitted (bin(0) is "0" or ε).

Kill: unsatisfiable bounded grammar, held-out mismatch through 2^16-1,
or no candidate in two hours. Not a prize claim.

Does not modify experiment.py, strip_graph.py, or strip_extend.py.

Run: python3 research/cfg_parse_parity.py
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

START = 0
FIT_N = 1023
HOLDOUT_N = (1 << 16) - 1
BUDGET_SEC = 7200
PREFIX_CHECK = 256

# Nested freezes; the declared kill family is the last row.
RANKS = (
    {"n_nt": 2, "max_bin": 8},
    {"n_nt": 3, "max_bin": 6},
    {"n_nt": 3, "max_bin": 8},
    {"n_nt": 4, "max_bin": 6},
    {"n_nt": 4, "max_bin": 8},
)

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

typedef struct { uint64_t w[4]; } bits256;

static inline bits256 z256(void) { bits256 r = {{0,0,0,0}}; return r; }
static inline bits256 and256(bits256 a, bits256 b) {
    bits256 r;
    r.w[0] = a.w[0] & b.w[0]; r.w[1] = a.w[1] & b.w[1];
    r.w[2] = a.w[2] & b.w[2]; r.w[3] = a.w[3] & b.w[3];
    return r;
}
static inline bits256 xor256(bits256 a, bits256 b) {
    bits256 r;
    r.w[0] = a.w[0] ^ b.w[0]; r.w[1] = a.w[1] ^ b.w[1];
    r.w[2] = a.w[2] ^ b.w[2]; r.w[3] = a.w[3] ^ b.w[3];
    return r;
}
static inline bits256 not256(bits256 a) {
    bits256 r;
    r.w[0] = ~a.w[0]; r.w[1] = ~a.w[1]; r.w[2] = ~a.w[2]; r.w[3] = ~a.w[3];
    return r;
}
static inline int nz256(bits256 a) {
    return (a.w[0] | a.w[1] | a.w[2] | a.w[3]) != 0;
}
static inline void setbit256(bits256 *a, int t) {
    a->w[t >> 6] |= 1ULL << (t & 63);
}
static inline int ctz256(bits256 a) {
    for (int i = 0; i < 4; i++)
        if (a.w[i]) return (i << 6) + __builtin_ctzll(a.w[i]);
    return -1;
}

#define MAXNT 4
#define MAXL 16
#define MAXFIT 1024
#define MAXBIN 8

static int n_nt, max_bin, fit_n, nslots, n_assign;
static double t_end;
static uint8_t cbit[MAXFIT];
static uint8_t W[MAXFIT][MAXL];
static uint8_t WL[MAXFIT];
static bits256 Tvec[MAXNT][2];
static bits256 live0;
static bits256 assign_mask;

static volatile int g_found = 0;
static volatile int g_stop = 0;
static double g_t0 = 0;
static int g_k = -1;
static int g_idx[MAXBIN];
static int g_tmask = -1;
static uint64_t g_checked = 0;

static double wall_now(void) {
#ifdef _OPENMP
    return omp_get_wtime();
#else
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
#endif
}

static void init_tvec(void) {
    memset(Tvec, 0, sizeof(Tvec));
    assign_mask = z256();
    for (int t = 0; t < n_assign; t++) {
        setbit256(&assign_mask, t);
        for (int x = 0; x < n_nt; x++) {
            for (int a = 0; a < 2; a++) {
                if ((t >> (2 * x + a)) & 1) setbit256(&Tvec[x][a], t);
            }
        }
    }
    live0 = Tvec[0][1]; /* n=1, c_1=1, Start -> 1 */
}

/* Bit-sliced CYK over all terminal assignments. Returns 1 if some assignment
   matches c_n for every n in 1..fit_n. */
static int check_subset(const int *idx, int k, int *out_tmask) {
    int xs[MAXBIN], ys[MAXBIN], zs[MAXBIN];
    for (int p = 0; p < k; p++) {
        int id = idx[p];
        xs[p] = id / (n_nt * n_nt);
        ys[p] = (id / n_nt) % n_nt;
        zs[p] = id % n_nt;
    }
    bits256 live = live0;
    bits256 dp[MAXL][MAXL + 1][MAXNT];
    for (int n = 2; n <= fit_n; n++) {
        int L = WL[n];
        for (int i = 0; i < L; i++) {
            int a = W[n][i];
            for (int x = 0; x < n_nt; x++) dp[i][1][x] = Tvec[x][a];
        }
        for (int len = 2; len <= L; len++) {
            for (int i = 0; i <= L - len; i++) {
                bits256 acc[MAXNT];
                for (int x = 0; x < n_nt; x++) acc[x] = z256();
                for (int split = 1; split < len; split++) {
                    for (int p = 0; p < k; p++) {
                        int x = xs[p], y = ys[p], z = zs[p];
                        acc[x] = xor256(acc[x],
                            and256(dp[i][split][y], dp[i + split][len - split][z]));
                    }
                }
                for (int x = 0; x < n_nt; x++) dp[i][len][x] = acc[x];
            }
        }
        bits256 st = dp[0][L][0];
        if (cbit[n]) live = and256(live, st);
        else live = and256(live, not256(st));
        live = and256(live, assign_mask);
        if (!nz256(live)) return 0;
        if (n == 7) {
            /* cheap progress counter; not exact under OpenMP */
        }
    }
    *out_tmask = ctz256(live);
    return 1;
}

static void rec(int filled, int k, int start, int *idx, uint64_t *local_checked) {
    if (g_stop) return;
    if (filled == k) {
        (*local_checked)++;
        if (((*local_checked) & 0x3fff) == 0) {
            if (wall_now() >= t_end) {
                g_stop = 1;
                return;
            }
        }
        int tmask = -1;
        if (check_subset(idx, k, &tmask)) {
#pragma omp critical
            {
                if (!g_found) {
                    g_found = 1;
                    g_stop = 1;
                    g_k = k;
                    g_tmask = tmask;
                    for (int i = 0; i < k; i++) g_idx[i] = idx[i];
                }
            }
        }
        return;
    }
    int last = nslots - (k - filled);
    for (int i = start; i <= last; i++) {
        idx[filled] = i;
        rec(filled + 1, k, i + 1, idx, local_checked);
        if (g_stop) return;
    }
}

static int search(void) {
    /* k=0: only terminals. n>=2 have 0 parses. */
    {
        int dummy[1] = {0};
        int tmask = -1;
        uint64_t one = 0;
        (void)dummy;
        g_checked++;
        if (check_subset(dummy, 0, &tmask)) {
            g_found = 1;
            g_k = 0;
            g_tmask = tmask;
            return 1;
        }
        if (wall_now() >= t_end) {
            g_stop = 1;
            return 0;
        }
    }
    for (int k = 1; k <= max_bin; k++) {
        if (g_stop) break;
#ifdef _OPENMP
#pragma omp parallel
        {
            uint64_t local = 0;
            int idx[MAXBIN];
#pragma omp for schedule(dynamic, 1)
            for (int i0 = 0; i0 <= nslots - k; i0++) {
                if (g_stop) continue;
                idx[0] = i0;
                rec(1, k, i0 + 1, idx, &local);
            }
#pragma omp atomic
            g_checked += local;
        }
#else
        uint64_t local = 0;
        int idx[MAXBIN];
        for (int i0 = 0; i0 <= nslots - k; i0++) {
            if (g_stop) break;
            idx[0] = i0;
            rec(1, k, i0 + 1, idx, &local);
        }
        g_checked += local;
#endif
        fprintf(stderr, "finished k=%d found=%d checked=%llu t=%.1f\n",
                k, g_found, (unsigned long long)g_checked, wall_now() - g_t0);
        fflush(stderr);
        if (g_found) return 1;
        if (wall_now() >= t_end) {
            g_stop = 1;
            return 0;
        }
    }
    return g_found;
}

int main(int argc, char **argv) {
    if (argc < 6) {
        fprintf(stderr, "usage: cfg_enum n_nt max_bin fit_n bits.bin timeout_sec\n");
        return 2;
    }
    n_nt = atoi(argv[1]);
    max_bin = atoi(argv[2]);
    fit_n = atoi(argv[3]);
    double timeout = atof(argv[5]);
    if (n_nt < 1 || n_nt > MAXNT || max_bin < 0 || max_bin > MAXBIN) return 2;
    if (fit_n < 1 || fit_n >= MAXFIT) return 2;
    nslots = n_nt * n_nt * n_nt;
    n_assign = 1 << (2 * n_nt);

    FILE *f = fopen(argv[4], "rb");
    if (!f) return 2;
    if (fread(cbit, 1, (size_t)fit_n + 1, f) != (size_t)fit_n + 1) {
        fclose(f);
        return 2;
    }
    fclose(f);

    for (int n = 1; n <= fit_n; n++) {
        int tmp[MAXL];
        int L = 0;
        int v = n;
        while (v) {
            tmp[L++] = v & 1;
            v >>= 1;
        }
        WL[n] = (uint8_t)L;
        for (int i = 0; i < L; i++) W[n][i] = (uint8_t)tmp[L - 1 - i];
    }
    init_tvec();
    g_t0 = wall_now();
    t_end = g_t0 + timeout;
    int sat = search();
    double elapsed = wall_now() - g_t0;
    if (sat) {
        printf("{\"status\":\"sat\",\"n_nt\":%d,\"max_bin\":%d,\"k\":%d,\"tmask\":%d,\"prods\":[",
               n_nt, max_bin, g_k, g_tmask);
        for (int i = 0; i < g_k; i++) {
            int id = g_idx[i];
            int x = id / (n_nt * n_nt);
            int y = (id / n_nt) % n_nt;
            int z = id % n_nt;
            printf("%s[%d,%d,%d]", i ? "," : "", x, y, z);
        }
        printf("],\"checked\":%llu,\"elapsed_sec\":%.6f,\"fit_n\":%d}\n",
               (unsigned long long)g_checked, elapsed, fit_n);
    } else if (g_stop && wall_now() >= t_end && !g_found) {
        printf("{\"status\":\"timeout\",\"n_nt\":%d,\"max_bin\":%d,\"checked\":%llu,\"elapsed_sec\":%.6f,\"fit_n\":%d}\n",
               n_nt, max_bin, (unsigned long long)g_checked, elapsed, fit_n);
    } else {
        printf("{\"status\":\"unsat\",\"n_nt\":%d,\"max_bin\":%d,\"checked\":%llu,\"elapsed_sec\":%.6f,\"fit_n\":%d}\n",
               n_nt, max_bin, (unsigned long long)g_checked, elapsed, fit_n);
    }
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


def bin_word(n: int) -> tuple[int, ...]:
    L = n.bit_length()
    return tuple((n >> i) & 1 for i in range(L - 1, -1, -1))


def parse_parity(word, binary, term, n_nt: int, start: int = START) -> int:
    """CYK parse count of `word` as `start`, modulo 2."""
    L = len(word)
    dp = [[0] * (L + 1) for _ in range(L)]
    for i, a in enumerate(word):
        m = 0
        for x in range(n_nt):
            if term[x][a]:
                m |= 1 << x
        dp[i][1] = m
    for j in range(2, L + 1):
        for i in range(L - j + 1):
            acc = 0
            for k in range(1, j):
                left = dp[i][k]
                right = dp[i + k][j - k]
                for x, y, z in binary:
                    if ((left >> y) & 1) and ((right >> z) & 1):
                        acc ^= 1 << x
            dp[i][j] = acc
    return (dp[0][L] >> start) & 1


def count_parses_naive(word, x, binary, term) -> int:
    if len(word) == 1:
        return 1 if term[x][word[0]] else 0
    total = 0
    for X, y, z in binary:
        if X != x:
            continue
        for k in range(1, len(word)):
            total += count_parses_naive(word[:k], y, binary, term) * count_parses_naive(
                word[k:], z, binary, term
            )
    return total


def self_check_cyk() -> bool:
    binary = [(0, 0, 1), (0, 1, 0), (1, 0, 0), (1, 1, 1)]
    term = [[0, 1], [1, 1]]
    n_nt = 2
    for n in range(1, 16):
        w = bin_word(n)
        p = parse_parity(w, binary, term, n_nt)
        q = count_parses_naive(w, 0, binary, term) & 1
        if p != q:
            return False
    return True


def python_exists_2nt(bits, fit_n: int, max_bin: int = 8) -> bool:
    """Exhaustive 2-NT screen (8 binary slots, 4 terminal bits)."""
    from itertools import combinations

    n_nt = 2
    nslots = 8
    for k in range(max_bin + 1):
        for idxs in combinations(range(nslots), k):
            binary = []
            for idx in idxs:
                binary.append((idx // 4, (idx // 2) % 2, idx % 2))
            for tmask in range(1 << 4):
                if ((tmask >> 1) & 1) != bits[1]:
                    continue
                term = [[(tmask >> (2 * x + a)) & 1 for a in (0, 1)] for x in range(n_nt)]
                ok = True
                for n in range(1, fit_n + 1):
                    if parse_parity(bin_word(n), binary, term, n_nt) != bits[n]:
                        ok = False
                        break
                if ok:
                    return True
    return False


def first_mismatch(binary, term, bits, n_nt, n0: int, n1: int):
    for n in range(n0, n1 + 1):
        if parse_parity(bin_word(n), binary, term, n_nt) != bits[n]:
            return n
    return None


def term_from_tmask(tmask: int, n_nt: int):
    term = [[0, 0] for _ in range(n_nt)]
    for x in range(n_nt):
        for a in (0, 1):
            term[x][a] = (tmask >> (2 * x + a)) & 1
    return term


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
        raise RuntimeError(f"gcc failed:\n{proc.stderr}")


def run_enum(
    binary: Path,
    bits_path: Path,
    n_nt: int,
    max_bin: int,
    fit_n: int,
    timeout: float,
) -> dict:
    cmd = [
        str(binary),
        str(n_nt),
        str(max_bin),
        str(fit_n),
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
    return rec


def main():
    t0 = time.time()
    os.environ.setdefault("OMP_NUM_THREADS", str(os.cpu_count() or 4))
    bits = packed_center(HOLDOUT_N + 1)
    assert bits[:PREFIX_CHECK] == experiment_center_bits(PREFIX_CHECK)
    assert self_check_cyk()
    python_2nt = python_exists_2nt(bits, 31, 8)

    z3_version = None
    try:
        import z3

        z3_version = z3.get_version_string()
    except Exception:
        z3_version = None

    tmp = Path(tempfile.mkdtemp(prefix="cfg_parse_"))
    c_path = tmp / "cfg_enum.c"
    bin_path = tmp / "cfg_enum"
    bits_path = tmp / "center.bin"
    c_path.write_text(C_SRC)
    bits_path.write_bytes(bytes(bits[: FIT_N + 1]))
    compile_enum(c_path, bin_path)

    ranks = []
    kill_family = None
    deadline = t0 + BUDGET_SEC
    for spec in RANKS:
        remaining = deadline - time.time()
        rec = {
            "n_nt": spec["n_nt"],
            "max_bin": spec["max_bin"],
            "fit_n": FIT_N,
            "start": START,
        }
        if remaining <= 1:
            rec["status"] = "timeout"
            rec["elapsed_sec"] = 0.0
            ranks.append(rec)
            continue
        print(
            f"rank n_nt={spec['n_nt']} max_bin={spec['max_bin']} "
            f"budget={remaining:.1f}s",
            flush=True,
        )
        status = None
        inner = []
        grammar = None
        rem = deadline - time.time()
        if rem <= 1:
            status = "timeout"
            raw = None
        else:
            raw = run_enum(
                bin_path, bits_path, spec["n_nt"], spec["max_bin"], FIT_N, rem
            )
        if raw is not None:
            inner.append(
                {
                    "fit_n": FIT_N,
                    "status": raw["status"],
                    "checked": raw.get("checked"),
                    "elapsed_sec": raw.get("elapsed_sec"),
                    "k": raw.get("k"),
                    "prods": raw.get("prods"),
                    "tmask": raw.get("tmask"),
                }
            )
            print(
                f"  fit 1..{FIT_N} -> {raw['status']} "
                f"checked={raw.get('checked')} t={raw.get('elapsed_sec'):.3f}s",
                flush=True,
            )
            status = raw["status"]
            if status == "sat":
                binary = [tuple(p) for p in raw["prods"]]
                term = term_from_tmask(raw["tmask"], spec["n_nt"])
                mm_fit = first_mismatch(binary, term, bits, spec["n_nt"], 1, FIT_N)
                if mm_fit is not None:
                    rec["verifier_mismatch"] = mm_fit
                    status = "verifier_fail"
                else:
                    grammar = {
                        "binary": [list(p) for p in binary],
                        "terminals": term,
                        "tmask": raw["tmask"],
                        "k": raw["k"],
                    }
        rec["status"] = status
        rec["phases"] = inner
        rec["elapsed_sec"] = time.time() - t0
        if grammar is not None:
            mm = first_mismatch(
                [tuple(p) for p in grammar["binary"]],
                grammar["terminals"],
                bits,
                spec["n_nt"],
                1,
                HOLDOUT_N,
            )
            rec["grammar"] = grammar
            rec["holdout_first_mismatch"] = mm
            rec["holdout_ok"] = mm is None
        ranks.append(rec)
        if spec["n_nt"] == 4 and spec["max_bin"] == 8:
            kill_family = rec

    kill_unsat = False
    holdout_mm = None
    no_candidate = False
    fired = False
    text = ""
    if kill_family is None:
        no_candidate = True
        fired = True
        text = "Declared 4-NT/8-prod family was not run."
    else:
        st = kill_family.get("status")
        if st == "unsat":
            kill_unsat = True
            fired = True
            text = (
                "No Chomsky grammar with 4 nonterminals, at most 8 binary "
                "productions, and no ε/unit productions realises c_n as "
                "parse parity of canonical bin(n) on n=1..1023."
            )
        elif st == "sat" and kill_family.get("holdout_ok"):
            fired = False
            text = (
                "A grammar fitted n=1..1023 and held out through 2^16-1; "
                "a structural Rule 30 explanation of the productions is still "
                "required. Not a prize claim."
            )
        elif st == "sat":
            holdout_mm = kill_family.get("holdout_first_mismatch")
            fired = True
            text = (
                f"A 4-NT/8-prod grammar fitted n=1..1023 but mismatched "
                f"held-out n={holdout_mm}."
            )
        elif st == "timeout":
            no_candidate = True
            fired = True
            text = (
                "No 4-NT/8-prod candidate within the two-hour synthesis cap."
            )
        else:
            no_candidate = True
            fired = True
            text = f"Declared family ended with status {st}."

    payload = {
        "not_a_prize_claim": True,
        "family": {
            "n_nonterminals": 4,
            "start": START,
            "max_binary_productions": 8,
            "terminals": [0, 1],
            "no_epsilon": True,
            "no_unit": True,
            "omit_n0": True,
            "omit_n0_reason": (
                "bin(0) is special (ε is forbidden; '0' would be a "
                "leading-zero-free encoding of zero). Constraints start at n=1."
            ),
            "fit": [1, FIT_N],
            "holdout": [1, HOLDOUT_N],
        },
        "self_check_prefix": True,
        "self_check_cyk": True,
        "python_2nt_exists_n1_31": python_2nt,
        "z3_version": z3_version,
        "solver": "bit-sliced CYK over all terminal assignments; OpenMP subset enum",
        "ranks": ranks,
        "kill": {
            "unsat_bounded": kill_unsat,
            "holdout_mismatch": holdout_mm,
            "no_candidate_in_cap": no_candidate,
            "fired": fired,
            "text": text,
        },
        "elapsed_sec": time.time() - t0,
    }
    dest = Path(__file__).with_suffix(".json")
    dest.write_text(json.dumps(payload, indent=2) + "\n")
    print(
        json.dumps(
            {
                "wrote": str(dest),
                "ranks": [(r["n_nt"], r["max_bin"], r.get("status")) for r in ranks],
                "kill": payload["kill"]["fired"],
                "elapsed_sec": payload["elapsed_sec"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
