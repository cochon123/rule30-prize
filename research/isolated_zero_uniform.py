"""Uniform isolated-zero certificate at radius 6.

Machine-checks the cruise/gadget dumps, the q=8 obstruction, the induction
step that extra cruise layers cannot un-force the phase-0 left bit, and
independent analyze() runs for q=7 and large q.
"""
from collections import defaultdict
from pathlib import Path
import json
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from strip_graph import graph, components, analyze

RADIUS = 6
WIDTH = 13
ROWS = 1 << WIDTH
INTERIOR = ((1 << (WIDTH - 1)) - 1) ^ 1


def bits(row, n=WIDTH):
    return ''.join(str((row >> j) & 1) for j in range(n))


def parse_bits(s):
    v = 0
    for j, ch in enumerate(s):
        if ch == '1':
            v |= 1 << j
    return v


def middle_of(row):
    return ((row << 1) ^ (row | (row >> 1))) & INTERIOR


def successors(row, next_center):
    mid = middle_of(row)
    if (mid >> RADIUS) & 1 != next_center:
        return []
    return [mid | left | (right << (WIDTH - 1)) for left in range(2) for right in range(2)]


OMIT_CRUISE = {parse_bits('1100'), parse_bits('1101')}


def layer(prefix, omit=OMIT_CRUISE):
    p = parse_bits(prefix) if isinstance(prefix, str) else prefix
    rows = []
    for suf in range(16):
        if suf in omit:
            continue
        rows.append(p | (suf << 9))
    return frozenset(rows)


# Frozen 14-state cruise (repeating 1-to-1 layer for every extra 1 once q>=17).
CRUISE_PREFIX = '101010101'
C = layer(CRUISE_PREFIX)

# Wrap-through-zero gadget, listed as (center_bit, prefix, omitted suffixes, n).
# Post-zero / bump (phases 0..10), stable for q>=16; phase 0 stable for q>=10.
# Pre-wrap (relative phases q-5..q), stable for q>=16.
POSTZERO_SPEC = [
    (0, '101011001', OMIT_CRUISE, 14),   # phase 0, left neighbor 1
    (1, '101010111', OMIT_CRUISE, 14),   # 1
    (1, '101010100', OMIT_CRUISE, 14),   # 2
]

# Bump layers that are not a single prefix; dumped from q=18 SCC.
# Filled at runtime from a base q, then frozen by equality checks.


def scc_layers(q):
    word = [0] + [1] * q
    out, rev, rows = graph(RADIUS, word)
    labels, groups = components(out, rev)
    rec = [g for g in groups if not (len(g) == 1 and g[0] not in out[g[0]])]
    by = defaultdict(set)
    if not rec:
        return by, out, labels, rec
    label = labels[rec[0][0]]
    for v in rec[0]:
        phase, row = divmod(v, rows)
        by[phase].add(row)
    return by, out, labels, rec


def left_bits(rows):
    return sorted({(r >> 5) & 1 for r in rows})


def prefix_set(rows):
    return sorted({bits(r & 0x1FF, 9) for r in rows})


def dump_rows(rows):
    return [bits(r) for r in sorted(rows)]


def induced_successors(q, by, out, labels, rec):
    if len(rec) != 1:
        return None
    label = labels[rec[0][0]]
    succ = defaultdict(lambda: defaultdict(set))
    for v in rec[0]:
        phase, row = divmod(v, ROWS)
        for w in out[v]:
            if labels[w] == label:
                np, nr = divmod(w, ROWS)
                succ[phase][row].add(nr)
    return succ


def verify_degree_two_cover(by, succ, q):
    for p in range(q + 1):
        nxt = (p + 1) % (q + 1)
        im = set()
        for r in by[p]:
            deg = len(succ[p][r])
            if deg != 2:
                return False, f'phase {p} row {bits(r)} deg {deg}'
            im.update(succ[p][r])
        if im != by[nxt]:
            return False, f'phase {p} image mismatch {len(im)} vs {len(by[nxt])}'
    return True, 'ok'


def suffix_map(rows_from, succ_from):
    m = {}
    for r in sorted(rows_from):
        m[bits((r >> 9) & 0xF, 4)] = sorted(bits((x >> 9) & 0xF, 4) for x in succ_from[r])
    return m


CRUISE_SUFFIX_MAP = {
    '0000': ['1000', '1001'],
    '1000': ['0100', '0101'],
    '0100': ['0110', '0111'],
    '0010': ['1110', '1111'],
    '1010': ['0010', '0011'],
    '0110': ['0100', '0101'],
    '1110': ['0000', '0001'],
    '0001': ['1010', '1011'],
    '1001': ['0110', '0111'],
    '0101': ['0100', '0101'],
    '0011': ['1110', '1111'],
    '1011': ['0010', '0011'],
    '0111': ['0100', '0101'],
    '1111': ['0000', '0001'],
}


def predicted_V(q, frozen):
    """Candidate recurrent vertices by phase for q>=17, from frozen q=18 slices."""
    assert q >= 17
    by = {}
    for p in range(11):
        by[p] = set(frozen[p])
    # phases 11 .. q-6 : cruise C
    for p in range(11, q - 5):
        by[p] = set(C)
    # last 6 phases: frozen pre-wrap of q=18 phases 13..18
    prewrap = [frozen[18 - k] for k in range(5, -1, -1)]  # phases 13,14,15,16,17,18
    # q=18: last 6 = phases 13..18
    for i, p in enumerate(range(q - 5, q + 1)):
        by[p] = set(prewrap[i])
    return by


def next_prefixes(pref9):
    p = parse_bits(pref9)
    if ((p >> 5) & 1) != 0:
        return set()
    out = set()
    for suf in range(16):
        row = p | (suf << 9)
        mid = middle_of(row)
        if (mid >> RADIUS) & 1 != 1:
            continue
        interior = mid & 0x1FE
        for left in range(2):
            out.add(bits(interior | left, 9))
    return out


def image_rows(rows, next_center):
    out = set()
    for r in rows:
        out.update(successors(r, next_center))
    return out


def prove_unique_self_loop_and_living_wrap():
    """q-independent lemmas used for every q>=17."""
    selfloops = []
    for i in range(512):
        pref = bits(i, 9)
        if pref in next_prefixes(pref):
            selfloops.append(pref)
    assert selfloops == [CRUISE_PREFIX], selfloops

    wrap_prefs = [bits(head, 5) + '1101' for head in range(32)]
    living = []
    for wp in wrap_prefs:
        W = [parse_bits(wp) | (s << 9) for s in range(16)]
        p0 = image_rows(W, 0)
        s = image_rows(p0, 1)
        for _ in range(10):
            s = image_rows(s, 1)
        if s & C:
            living.append(wp)
    assert living == ['110001101'], living
    L = layer('110001101')
    assert {(r >> 4) & 1 for r in L} == {0}
    p0 = image_rows(L, 0)
    assert left_bits(p0) == [1]
    print('unique 9-bit 1-to-1 self-loop', selfloops)
    print('unique living wrap prefix from the C-tree', living, 'phase0 left', left_bits(p0))


def main():
    report = {}

    print('===== freeze gadget from q=18 =====')
    by18, out18, lab18, rec18 = scc_layers(18)
    assert len(rec18) == 1
    frozen = {p: frozenset(by18[p]) for p in range(19)}
    succ18 = induced_successors(18, by18, out18, lab18, rec18)
    ok, msg = verify_degree_two_cover(by18, succ18, 18)
    print('q=18 degree-2 cover', ok, msg)
    assert ok

    print('phase dumps:')
    gadget_dump = {}
    for p in range(19):
        info = {
            'n': len(frozen[p]),
            'left': left_bits(frozen[p]),
            'prefixes': prefix_set(frozen[p]),
            'rows': dump_rows(frozen[p]),
        }
        gadget_dump[p] = info
        print(f'  ph {p:2d} n={info["n"]:3d} left={info["left"]} pref={info["prefixes"]}')

    # Cruise identity
    print('\n===== cruise C =====')
    print('C n', len(C), 'rows', dump_rows(C))
    print('q18 phase11 == C', frozen[11] == C)
    print('q18 phase12 == C', frozen[12] == C)
    sm = suffix_map(frozen[11], succ18[11])
    print('suffix map matches frozen', sm == CRUISE_SUFFIX_MAP)
    assert sm == CRUISE_SUFFIX_MAP
    assert frozen[11] == C == frozen[12]

    # Unconstrained successors of C split by left outer bit
    stay, exit_ = set(), set()
    for r in C:
        for w in successors(r, 1):
            if (w & 0x1FF) == parse_bits(CRUISE_PREFIX):
                stay.add(w)
            else:
                exit_.add(w)
    print('unconstrained R(C) stay n', len(stay), 'exit n', len(exit_),
          'exit prefs', prefix_set(exit_), 'stay==C', stay == C)
    print('exit == q18 phase13?', exit_ <= frozen[13] or exit_ == frozen[13])
    print('exit prefixes', prefix_set(exit_), 'phase13', prefix_set(frozen[13]))
    # SCC keeps stay at cruise phases and exit at the countdown phase.
    print('stay intersect C suffixes omit', prefix_set(stay))

    # q=8 obstruction
    print('\n===== q=8 obstruction =====')
    by8, _, _, rec8 = scc_layers(8)
    assert len(rec8) == 1
    left0 = {r for r in by8[0] if ((r >> 5) & 1) == 0}
    left1 = {r for r in by8[0] if ((r >> 5) & 1) == 1}
    extra_last = {r for r in by8[8] if bits(r).startswith('000111100')}
    print('q8 phase0 left0 n', len(left0), 'pref', prefix_set(left0))
    print('q8 phase0 left1 n', len(left1), 'pref', prefix_set(left1))
    print('q8 extra last-1 n', len(extra_last), dump_rows(extra_last))
    # Algebra: phase0 left = NOT bit4 of last-1
    for r in by8[8]:
        nxt_left = [((w >> 5) & 1) for w in successors(r, 0)]
        pred = 1 - ((r >> 4) & 1)
        assert all(x == pred for x in nxt_left)
    bit4_one = {r for r in by8[8] if (r >> 4) & 1}
    print('q8 last-1 with bit4=1 n', len(bit4_one), 'prefs', prefix_set(bit4_one))
    assert bit4_one == extra_last

    # For q>=9 last-1 has bit4=0
    print('\n===== last-1 bit4 for q=7,9..18 =====')
    last_bit4 = {}
    for q in [7] + list(range(9, 19)):
        by, _, _, rec = scc_layers(q)
        assert len(rec) == 1
        b4 = {(r >> 4) & 1 for r in by[q]}
        last_bit4[q] = sorted(b4)
        print(f'  q={q:2d} last n={len(by[q]):3d} bit4={sorted(b4)} left0={left_bits(by[0])} pref={prefix_set(by[q])}')
        if q >= 11:
            assert b4 == {0}
            assert left_bits(by[0]) == [1]
            assert by[q] == frozen[18]

    # Predicted V_q vs actual for q=17,18
    print('\n===== predicted V_q vs SCC q=17,18 =====')
    by17, _, _, rec17 = scc_layers(17)
    assert len(rec17) == 1
    pred17 = predicted_V(17, frozen)
    pred18 = predicted_V(18, frozen)
    eq17 = all(pred17[p] == by17[p] for p in range(18))
    eq18 = all(pred18[p] == by18[p] for p in range(19))
    print('V_17 matches', eq17, 'V_18 matches', eq18)
    assert eq17 and eq18

    # Induction invariant: phase 0 and last-1 freeze
    print('\n===== freeze of Z and L =====')
    Z, L = frozen[0], frozen[18]
    print('Z n', len(Z), 'left', left_bits(Z), dump_rows(Z))
    print('L n', len(L), 'left', left_bits(L), 'bit4', {(r >> 4) & 1 for r in L}, dump_rows(L))
    assert left_bits(Z) == [1]
    assert {(r >> 4) & 1 for r in L} == {0}

    # Unconstrained B(L) both prefixes have left=1
    BL = set()
    for r in L:
        BL.update(successors(r, 0))
    print('B(L) n', len(BL), 'left', left_bits(BL), 'pref', prefix_set(BL))
    assert left_bits(BL) == [1]
    assert Z < BL

    prewrap_prefs = [prefix_set(frozen[p]) for p in range(13, 19)]
    print('prewrap prefs', prewrap_prefs)
    print('\n===== q-independent lemmas =====')
    prove_unique_self_loop_and_living_wrap()

    # Independent analyze checks
    print('\n===== independent analyze() =====')
    checks = {}
    for q in (7, 9, 10, 11, 17, 18):
        t0 = time.monotonic()
        a = analyze(6, [0] + [1] * q)
        dt = time.monotonic() - t0
        checks[q] = a
        print(f'  q={q} rec={a["recurrent_components"]} residual={a["components_without_forced_periodic_neighbor"]} ({dt:.2f}s)')
        if q != 8:
            assert a['components_without_forced_periodic_neighbor'] == 0
            assert a['recurrent_components'] == 1

    large = {}
    for q in (31, 40):
        t0 = time.monotonic()
        a = analyze(6, [0] + [1] * q)
        dt = time.monotonic() - t0
        large[q] = {k: a[k] for k in a if k != 'all_components'}
        print(f'  q={q} rec={a["recurrent_components"]} residual={a["components_without_forced_periodic_neighbor"]} ({dt:.2f}s)')
        assert a['components_without_forced_periodic_neighbor'] == 0
        assert a['recurrent_components'] == 1
        by, _, _, rec = scc_layers(q)
        assert len(rec) == 1
        pred = predicted_V(q, frozen)
        match = all(pred[p] == by[p] for p in range(q + 1))
        print(f'  q={q} V_q matches predicted {match} size {sum(len(by[p]) for p in by)} expected {14*q + 74}')
        assert match
        assert left_bits(by[0]) == [1]
        assert by[0] == Z and by[q] == L

    # Size formula
    print('\n===== size formula 14q+74 for q>=9 =====')
    for q in range(9, 19):
        by, _, _, rec = scc_layers(q)
        size = sum(len(by[p]) for p in by)
        print(f'  q={q} size={size} formula={14*q+74}')
        assert size == 14 * q + 74

    report.update({
        'cruise_prefix': CRUISE_PREFIX,
        'cruise_rows': dump_rows(C),
        'cruise_omitted_suffixes': ['1100', '1101'],
        'cruise_suffix_map': CRUISE_SUFFIX_MAP,
        'zero_layer_Z': dump_rows(Z),
        'last_one_layer_L': dump_rows(L),
        'q18_layers': {str(p): gadget_dump[p] for p in gadget_dump},
        'q8_phase0_left0': dump_rows(left0),
        'q8_extra_last1': dump_rows(extra_last),
        'large_q': large,
        'formula_size': '14q+74 for q>=9',
    })
    path = Path(__file__).resolve().parent / 'isolated_zero_uniform.json'
    path.write_text(json.dumps(report, indent=2) + '\n')
    print('wrote', path)


if __name__ == '__main__':
    main()
