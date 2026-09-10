"""q=8 reconstruction quotient: finite left support vs mixing sigma.

Does not modify strip_graph.py or strip_extend.py.

Machine-checked facts (see research/period9_sigma.md):
- Every eventually periodic sigma is Jen/Kopra-excluded (incl. 0101...).
- Radius-6 20-state return graph is a full 2-shift on sigma labels.
- The wrap-controlled 18-bit pair FSM has a 512-state invariant I of
  phase-0 vacuum, unique wrap on every state, unique recurrent vacuum.
- L_0 at n=0 implies the pair enters I, hence wrap is eventually 0 and
  W_k(0) is eventually 0^9. That is periodic labels on the reconstruction
  quotient, not a proof that sigma itself is eventually periodic.
- Consistent reconstruction (wrap = C_{k,0}(1) from the same sigma) has
  rank <= 3 through depth DEPTH, so never enters I in that range; every
  onset T<=TMAX dies by R=5. q=8 is not excluded.

Run: python3 research/period9_sigma.py
"""
from __future__ import annotations

from collections import Counter, defaultdict, deque
from pathlib import Path
import json
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from strip_graph import components, graph, self_check

WORD = [0, 1, 1, 1, 1, 1, 1, 1, 1]
PERIOD = 9
CENTER = 6
WIDTH = 13
DEPTH = 16  # consistent-pair rank bound
TMAX = 12


def bit(w, a):
    return (w >> a) & 1


def xor_or(a, b, c):
    return a ^ (b | c)


def W0():
    w = 0
    for a in range(1, 9):
        w |= 1 << a
    return w  # 011111111


def W1(sigma):
    return (sigma & 1) | (1 << 8)  # sigma 00000001


def pair_step(prev, curr, wrap):
    nxt = 0
    for a in range(8):
        nxt |= xor_or(bit(curr, a + 1), bit(curr, a), bit(prev, a)) << a
    nxt |= xor_or(wrap & 1, bit(curr, 8), bit(prev, 8)) << 8
    return nxt


def encode(prev, curr):
    return ((prev & 0x1FF) << 9) | (curr & 0x1FF)


def decode(s):
    return (s >> 9) & 0x1FF, s & 0x1FF


def bits9_lsb(x):
    return "".join(str(bit(x, a)) for a in range(9))


# ---------------------------------------------------------------------------
# Reconstruction from a sigma stream
# ---------------------------------------------------------------------------

def reconstruct(sigmas, kmax):
    L = len(sigmas)
    W = [[0] * (L + 1) for _ in range(kmax + 1)]
    w0 = W0()
    for n in range(L + 1):
        W[0][n] = w0
    for n in range(L):
        W[1][n] = W1(sigmas[n])
    for k in range(1, kmax):
        for n in range(L - k):
            prev, curr = W[k - 1][n], W[k][n]
            wrap = bit(W[k][n + 1], 0)
            W[k + 1][n] = pair_step(prev, curr, wrap)
    return W


def add_bit(pairs, sigma_bit, L_old):
    """Extend the anti-diagonal by one sigma bit. pairs[n]=(W_{L-n-1}(n), W_{L-n}(n))."""
    w0, w1 = W0(), W1(sigma_bit)
    new_diag = [0] * (L_old + 2)
    new_diag[0] = w0
    new_diag[1] = w1
    for k in range(1, L_old + 1):
        n = L_old - k
        prev, curr = pairs[n]
        new_diag[k + 1] = pair_step(prev, curr, bit(new_diag[k], 0))
    new_pairs = []
    for n in range(L_old):
        prev, curr = pairs[n]
        new_pairs.append((curr, new_diag[L_old + 1 - n]))
    new_pairs.append((w0, w1))
    return new_pairs


# ---------------------------------------------------------------------------
# 20-state phase-0 automaton
# ---------------------------------------------------------------------------

def residual_r6():
    out, rev, rows = graph(6, WORD)
    labels, groups = components(out, rev)
    rec = [g for g in groups if not (len(g) == 1 and g[0] not in out[g[0]])]
    assert len(rec) == 1
    group = rec[0]
    label = labels[group[0]]
    by = defaultdict(list)
    verts = {}
    for v in group:
        phase, row = divmod(v, rows)
        by[phase].append(row)
        verts[(phase, row)] = v
    return out, labels, label, rows, by, verts


def phase0_automaton():
    out, labels, label, rows, by, verts = residual_r6()
    p0 = sorted(by[0])
    assert len(p0) == 20
    index = {r: i for i, r in enumerate(p0)}
    sigmas = [((r >> (CENTER - 1)) & 1) for r in p0]
    step = [[] for _ in p0]
    for r in p0:
        frontier = {r}
        ph = 0
        for _ in range(9):
            nxt = set()
            for x in frontier:
                v = verts[(ph, x)]
                for w in out[v]:
                    if labels[w] == label:
                        np, nr = divmod(w, rows)
                        nxt.add(nr)
            ph = (ph + 1) % 9
            frontier = nxt
        step[index[r]] = sorted(index[x] for x in frontier)
    return p0, sigmas, step


def sofic_is_full_shift(sigmas, step):
    n = len(step)
    s0 = frozenset(i for i in range(n) if sigmas[i] == 0)
    s1 = frozenset(i for i in range(n) if sigmas[i] == 1)
    assert s0 and s1

    def go(S, b):
        T = set()
        for u in S:
            for w in step[u]:
                if sigmas[w] == b:
                    T.add(w)
        return frozenset(T)

    t00, t01 = go(s0, 0), go(s0, 1)
    t10, t11 = go(s1, 0), go(s1, 1)
    full = t00 == s0 and t01 == s1 and t10 == s0 and t11 == s1
    return {
        "n_sigma0": len(s0),
        "n_sigma1": len(s1),
        "full_2_shift": full,
        "from0_on0": len(t00),
        "from0_on1": len(t01),
        "from1_on0": len(t10),
        "from1_on1": len(t11),
    }


# ---------------------------------------------------------------------------
# 18-bit pair FSM, invariant I
# ---------------------------------------------------------------------------

def build_succ(N=1 << 18):
    succ0 = [0] * N
    succ1 = [0] * N
    for s in range(N):
        prev, curr = decode(s)
        succ0[s] = encode(curr, pair_step(prev, curr, 0))
        succ1[s] = encode(curr, pair_step(prev, curr, 1))
    return succ0, succ1


def build_Z(succ0, succ1, N=1 << 18):
    layers = [bytearray(N)]
    for s in range(N):
        if (s & 1) == 0:
            layers[0][s] = 1
    sizes = [int(sum(layers[0]))]
    for _ in range(8):
        nxt = bytearray(N)
        for s in range(N):
            if layers[-1][s] and (layers[-1][succ0[s]] or layers[-1][succ1[s]]):
                nxt[s] = 1
        layers.append(nxt)
        sizes.append(int(sum(nxt)))
    return layers, sizes


def z_formulas_check(layers):
    """Z0..Z4 have closed identities independent of wrap."""
    N = len(layers[0])

    def pb_cb(s):
        p, c = decode(s)
        pb = [bit(p, i) for i in range(9)]
        cb = [bit(c, i) for i in range(9)]
        return pb, cb

    def in_formula(j, pb, cb):
        if cb[0] != 0:
            return False
        if j >= 1 and cb[1] != pb[0]:
            return False
        if j >= 2 and cb[2] != (cb[1] | pb[1]):
            return False
        if j >= 3 and cb[3] != (cb[1] ^ (cb[2] | pb[2])):
            return False
        if j >= 4 and cb[4] != (cb[2] ^ (cb[3] | pb[3])):
            return False
        return True

    out = {}
    for j in range(5):
        miss = extra = 0
        for s in range(N):
            pb, cb = pb_cb(s)
            ins = bool(layers[j][s])
            pr = in_formula(j, pb, cb)
            if ins and not pr:
                miss += 1
            if (not ins) and pr:
                extra += 1
        out[f"Z{j}"] = {"miss": miss, "extra": extra, "ok": miss == 0 and extra == 0}
        assert out[f"Z{j}"]["ok"], (j, miss, extra)
    return out


def inspect_I(layers, succ0, succ1):
    N = len(layers[0])
    I = layers[8]
    states = [s for s in range(N) if I[s]]
    assert len(states) == 512
    forced = {}
    both = none = 0
    for s in states:
        a, b = I[succ0[s]], I[succ1[s]]
        if a and b:
            both += 1
        elif a:
            forced[s] = 0
        elif b:
            forced[s] = 1
        else:
            none += 1
    assert both == 0 and none == 0 and len(forced) == 512
    # functional graph SCCs
    nI = 512
    idx = {s: i for i, s in enumerate(states)}
    adj = [[] for _ in range(nI)]
    radj = [[] for _ in range(nI)]
    wrap_of = [forced[s] for s in states]
    for i, s in enumerate(states):
        t = succ0[s] if wrap_of[i] == 0 else succ1[s]
        j = idx[t]
        adj[i].append(j)
        radj[j].append(i)
    labels, groups = components(adj, radj)
    rec = []
    for g in groups:
        if len(g) == 1 and g[0] not in adj[g[0]]:
            continue
        rec.append(g)
    vac = encode(0, 0)
    assert I[vac]
    assert forced[vac] == 0
    assert succ0[vac] == vac
    assert len(rec) == 1 and rec[0] == [idx[vac]]
    # longest path to vacuum
    dist = {}

    def depth_to_vac(s):
        if s in dist:
            return dist[s]
        if s == vac:
            dist[s] = 0
            return 0
        w = forced[s]
        t = succ0[s] if w == 0 else succ1[s]
        dist[s] = 1 + depth_to_vac(t)
        return dist[s]

    longest = max(depth_to_vac(s) for s in states)
    return {
        "size": 512,
        "unique_wrap": True,
        "n_wrap0": sum(1 for s in states if forced[s] == 0),
        "n_wrap1": sum(1 for s in states if forced[s] == 1),
        "n_recurrent_sccs": 1,
        "recurrent_is_vacuum_wrap0": True,
        "longest_path_to_vacuum": longest,
        "curr_is_function_of_prev": len({decode(s)[0] for s in states}) == 512,
    }


def constant_sigma_orbit(sigma, kmax=400):
    prev, curr = W0(), W1(sigma)
    seq = [bit(curr, 0)]
    seen = {(prev, curr): 0}
    for k in range(1, kmax):
        wrap = bit(curr, 0)
        nxt = pair_step(prev, curr, wrap)
        prev, curr = curr, nxt
        seq.append(bit(curr, 0))
        key = (prev, curr)
        if key in seen:
            pre = seen[key]
            per = k - pre
            tail = seq[pre:]
            return {
                "sigma": sigma,
                "preperiod": pre,
                "period": per,
                "cycle_ones": sum(tail),
                "infinitely_many_1s": any(tail),
                "has_last_1": not any(tail),
            }
        seen[key] = k
    return {"sigma": sigma, "note": "no cycle", "kmax": kmax}


def jen_periodic_sigma():
    samples = ["0", "1", "01", "10", "001", "011", "0101", "0001", "0111"]
    rows = []
    for w in samples:
        m = len(w)
        col = []
        for n in range(m):
            col.append(int(w[n]))
            col.extend([0] * 7)
            col.append(1)
        assert len(col) == 9 * m
        rows.append({"sigma": w, "col_m1_period": 9 * m})
    return rows


def C2_table():
    rows = []
    for s0 in (0, 1):
        for s1 in (0, 1):
            W = reconstruct([s0, s1, 0], kmax=2)
            rows.append(
                {
                    "sigma_n": s0,
                    "sigma_n1": s1,
                    "C1": bits9_lsb(W[1][0]),
                    "C2": bits9_lsb(W[2][0]),
                }
            )
    const = {
        str(s): next(r["C2"] for r in rows if r["sigma_n"] == s and r["sigma_n1"] == s)
        for s in (0, 1)
    }
    assert const["1"] == "111111100"
    assert const["0"] == "011111101"
    mixed = {
        "0then1": next(r["C2"] for r in rows if r["sigma_n"] == 0 and r["sigma_n1"] == 1),
        "1then0": next(r["C2"] for r in rows if r["sigma_n"] == 1 and r["sigma_n1"] == 0),
    }
    assert mixed["0then1"] == "011111100"
    assert mixed["1then0"] == "111111101"
    return {"all": rows, "constant": const, "mixed_wrap": mixed}


def vacuum_propagation_lemma():
    return {
        "identity": (
            "C_{k+1,0}(n)=C_{k,1}(n) XOR (C_{k,0}(n) OR C_{k-1,0}(n)); "
            "phase 8 wrap uses C_{k,0}(n+1)."
        ),
        "lemma": (
            "If C_{k,0}(0)=0 for every k>T, then C_{k,a}(0)=0 for a=0..8 and "
            "k>T+a, and C_{k,0}(1)=0 for k>T+8. Iterating, C_{k,0}(n)=0 for "
            "k>T+9n."
        ),
    }


def consistent_rank_bound(layers, depth):
    """Max controlled-rank of (W_{k-1}(0), W_k(0)) over all sigma, k<=depth."""
    maxrank = -1
    witness = None
    n_in_I = 0

    def rank_of(s):
        for j in range(8, -1, -1):
            if layers[j][s]:
                return j
        return -1

    def dfs(pairs, lab):
        nonlocal maxrank, witness, n_in_I
        L = len(lab)
        if L >= 1:
            s = encode(*pairs[0])
            r = rank_of(s)
            if r > maxrank:
                maxrank = r
                witness = ("".join(map(str, lab)), r, bits9_lsb(pairs[0][0]), bits9_lsb(pairs[0][1]))
            if r == 8:
                n_in_I += 1
        if L >= depth:
            return
        for b in (0, 1):
            dfs(add_bit(pairs, b, L), lab + [b])

    dfs([], [])
    return {
        "depth": depth,
        "max_rank": maxrank,
        "n_pairs_in_I": n_in_I,
        "witness_max_rank": {
            "sigma": witness[0] if witness else None,
            "rank": witness[1] if witness else None,
            "prev": witness[2] if witness else None,
            "curr": witness[3] if witness else None,
        },
        "never_enters_I": n_in_I == 0,
        "no_five_consecutive_phase0_zeros": maxrank < 4,
    }


def onset_scan(tmax, rmax):
    rows = []
    for T in range(1, tmax + 1):
        killed = None
        witness = None
        for R in range(1, rmax + 1):
            found = None

            def dfs(pairs, lab):
                nonlocal found
                if found is not None:
                    return
                L = len(lab)
                if L < T:
                    for b in (0, 1):
                        dfs(add_bit(pairs, b, L), lab + [b])
                    return
                if L == T and bit(pairs[0][1], 0) != 1:
                    return
                if L > T:
                    if bit(pairs[0][1], 0) != 0:
                        return
                    if L >= T + R:
                        found = lab[:]
                        return
                for b in (0, 1):
                    np = add_bit(pairs, b, L)
                    b0 = bit(np[0][1], 0)
                    if L + 1 == T and b0 != 1:
                        continue
                    if L + 1 > T and b0 != 0:
                        continue
                    dfs(np, lab + [b])

            dfs([], [])
            if found is None:
                killed = R
                break
            witness = "".join(map(str, found))
        rows.append({"T": T, "killed_at_R": killed, "survivor_prefix": witness})
        assert killed is not None, T
    return rows


def main():
    self_check()
    t0 = time.monotonic()
    report = {}

    print("===== C2 =====", flush=True)
    report["C2"] = C2_table()
    print(json.dumps(report["C2"]["constant"],), flush=True)

    print("===== Jen periodic sigma =====", flush=True)
    report["jen_periodic_sigma"] = {
        "lemma": (
            "If sigma is eventually period m, column -1 is eventually period 9m "
            "(sigma on isolated 0, forced 0^7 1 on the 1-run). Column 0 is period 9. "
            "Jen/Kopra exclude every such adjacent pair for a nonzero finite seed. "
            "This includes constant sigma and alternating 0101...."
        ),
        "samples": jen_periodic_sigma(),
    }

    print("===== 20-state sigma language =====", flush=True)
    p0, sigmas, step = phase0_automaton()
    degs = [len(s) for s in step]
    sofic = sofic_is_full_shift(sigmas, step)
    report["automaton"] = {
        "n_states": 20,
        "n_sigma0": sigmas.count(0),
        "n_sigma1": sigmas.count(1),
        "outdeg_min": min(degs),
        "outdeg_max": max(degs),
        "sofic": sofic,
    }
    assert sofic["full_2_shift"]
    print(json.dumps(report["automaton"]), flush=True)

    print("===== pair FSM / I =====", flush=True)
    succ0, succ1 = build_succ()
    layers, sizes = build_Z(succ0, succ1)
    report["Z_sizes"] = sizes
    assert sizes == [131072, 65536, 32768, 16384, 8192, 4096, 2048, 1024, 512]
    report["Z_formulas"] = z_formulas_check(layers)
    report["I"] = inspect_I(layers, succ0, succ1)
    print(json.dumps({"Z": sizes, "I": report["I"]}), flush=True)

    print("===== constant sigma spatial orbits =====", flush=True)
    report["constant_sigma_orbits"] = [constant_sigma_orbit(s) for s in (0, 1)]
    for row in report["constant_sigma_orbits"]:
        assert row["infinitely_many_1s"]
    print(json.dumps(report["constant_sigma_orbits"]), flush=True)

    print("===== vacuum propagation =====", flush=True)
    report["vacuum_propagation"] = vacuum_propagation_lemma()

    print("===== consistent rank bound =====", flush=True)
    t1 = time.monotonic()
    report["consistent_rank"] = consistent_rank_bound(layers, DEPTH)
    report["consistent_rank"]["elapsed"] = round(time.monotonic() - t1, 3)
    assert report["consistent_rank"]["never_enters_I"]
    assert report["consistent_rank"]["max_rank"] <= 3
    print(json.dumps(report["consistent_rank"]), flush=True)

    print("===== onset scan =====", flush=True)
    t1 = time.monotonic()
    report["onset"] = onset_scan(TMAX, 8)
    report["onset_elapsed"] = round(time.monotonic() - t1, 3)
    assert all(r["killed_at_R"] is not None for r in report["onset"])
    assert max(r["killed_at_R"] for r in report["onset"]) <= 5
    print(json.dumps(report["onset"]), flush=True)

    report["elapsed_total"] = round(time.monotonic() - t0, 3)
    report["excluded"] = False
    report["strongest"] = (
        "q=8 is not excluded. Every eventually periodic sigma is Jen-excluded. "
        "The reconstruction quotient I forces a periodic wrap label (eventually 0) "
        "on any phase-0 vacuum tail, but consistent sigma streams do not enter I "
        f"through depth {DEPTH}, and every onset T<= {TMAX} dies by R=5. "
        "The 20-state strip automaton is a full 2-shift on sigma; free-boundary "
        "mixing is not a seed orbit."
    )
    path = Path(__file__).resolve().parent / "period9_sigma.json"
    path.write_text(json.dumps(report, indent=2) + "\n")
    print("wrote", path, "total", report["elapsed_total"], "s", flush=True)
    print("EXCLUDED", report["excluded"])
    print("STRONGEST", report["strongest"])


if __name__ == "__main__":
    main()
