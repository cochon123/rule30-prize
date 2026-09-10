"""Wreath-section arithmetic for the Rule 30 row map as a 3-state automaton.

Does not overwrite strip_graph.py, strip_extend.py, or experiment.py.
Does not claim a prize result.

The row map A = f, with
    f(z) = z XOR ((2z) OR (4z)),
is the binary-tree automorphism (LSB first)
    A = (A, C),     B = (A, C)σ,     C = (B, C)σ,
where σ flips the current bit. States remember whether the previous two
input bits are 00, 01, or 1*. Composition is (gh)(x) = g(h(x)), so
    (gh)|_x = g|_{x XOR ε(h)} · h|_x,     ε(gh) = ε(g) XOR ε(h).

The prize bit is c_n = ε(A^n | 10^{n-1}) = ε(C^n | 0^{n-1}) for n ≥ 1.

Run: python3 research/automaton_sections.py
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from itertools import product
# ---------------------------------------------------------------------------
# Generators and wreath tables
# ---------------------------------------------------------------------------

A, B, C = "A", "B", "C"
GENS = (A, B, C)
SIGMA = 1  # activity; identity root permutation is 0

# g = (g|_0, g|_1) σ^{ε(g)}
SECTIONS = {
    A: (A, C),
    B: (A, C),
    C: (B, C),
}
ACTIVITY = {A: 0, B: 1, C: 1}


def f_int(z: int) -> int:
    return z ^ ((z << 1) | (z << 2))


def apply_gen(g: str, z: int, nbits: int) -> int:
    """Apply one generator to the low nbits of z (higher bits ignored)."""
    out = 0
    s = g
    for i in range(nbits):
        bit = (z >> i) & 1
        if s == A:
            out_bit = bit
            s = A if bit == 0 else C
        elif s == B:
            out_bit = bit ^ 1
            s = A if bit == 0 else C
        else:
            out_bit = bit ^ 1
            s = B if bit == 0 else C
        out |= out_bit << i
    return out


def apply_word(word: str, z: int, nbits: int) -> int:
    """Left-to-right word: apply the rightmost generator first."""
    for g in reversed(word):
        z = apply_gen(g, z, nbits)
    return z


def packed_row(n: int) -> int:
    """f^n(1) as an integer."""
    z = 1
    for _ in range(n):
        z = f_int(z)
    return z


def center_bit(n: int) -> int:
    return (packed_row(n) >> n) & 1


# ---------------------------------------------------------------------------
# Algebraic words: strings over {A,B,C}
# ---------------------------------------------------------------------------

def eps_word(word: str) -> int:
    return sum(ACTIVITY[g] for g in word) & 1


def section_word(word: str, x: int) -> str:
    """(g0...g_{L-1})|_x with rightmost applied first."""
    if not word:
        return ""
    bit = x
    out = []
    for g in reversed(word):
        out.append(SECTIONS[g][bit])
        bit ^= ACTIVITY[g]
    return "".join(reversed(out))


def first_letter_image(word: str, x: int) -> int:
    return x ^ eps_word(word)


# ---------------------------------------------------------------------------
# Power-section identities (closed forms)
# ---------------------------------------------------------------------------

def alt_pair(even_start: str, end: str, m: int) -> str:
    """Alternating word of length m over {even_start, end} ending in `end`.

    For m even the word is (even_start + end)^{m/2}.
    For m odd it is end + (even_start + end)^{(m-1)/2} if even_start≠end...
    Standard: pair {X,Y} with Y = end, X = the other.
    """
    if m == 0:
        return ""
    X, Y = even_start, end
    if m % 2 == 0:
        return (X + Y) * (m // 2)
    return Y + (X + Y) * (m // 2)


def power_C_section(m: int, x: int) -> str:
    """C^m |_x as an expanded word. Identity:
    C^m |_0 = Alt ending B;  C^m |_1 = Alt ending C.
    """
    if x == 0:
        return alt_pair(C, B, m)  # (CB)^{m/2} or B(CB)^{(m-1)/2}
    return alt_pair(B, C, m)


def power_B_section(m: int, x: int) -> str:
    if x == 0:
        return alt_pair(C, A, m)
    return alt_pair(A, C, m)


def power_A_section(m: int, x: int) -> str:
    if x == 0:
        return A * m
    return C * m


def power_BC_section(m: int, x: int) -> str:
    if x == 0:
        return (C + B) * m
    return (A + C) * m


def power_CB_section(m: int, x: int) -> str:
    if x == 0:
        return (C + A) * m
    return (B + C) * m


# ---------------------------------------------------------------------------
# Compressed periodic elements
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Periodic:
    """Element prefix * block^exp * suffix in the semigroup {A,B,C}*.

    All three strings are ordinary generator words. The expanded length is
    |prefix| + exp*|block| + |suffix|.
    """

    prefix: str
    block: str
    exp: int
    suffix: str = ""

    def expanded(self) -> str:
        if self.exp < 0:
            raise ValueError("exp")
        return self.prefix + self.block * self.exp + self.suffix

    def desc_size(self) -> int:
        """Letters stored in the compressed description (not expanded)."""
        return len(self.prefix) + len(self.block) + len(self.suffix)

    def expanded_len(self) -> int:
        return len(self.prefix) + self.exp * len(self.block) + len(self.suffix)

    def eps(self) -> int:
        e = eps_word(self.prefix) ^ eps_word(self.suffix)
        if self.exp & 1:
            e ^= eps_word(self.block)
        return e


def section_periodic(p: Periodic, x: int) -> Periodic:
    """Section of a compressed periodic element at a first letter.

    Uses the wreath product rule and the power-of-a-word formula:
      if ε(w)=0: w^e |_x = (w|_x)^e
      if ε(w)=1: w^e |_x = (w|_{x⊕1} w|_x)^{e/2}   (e even)
                 w^e |_x = w|_x · (w|_{x⊕1} w|_x)^{(e-1)/2} wait:
        product_{j=e-1..0} w|_{x ⊕ (j mod 2)}
    Does not expand block^exp except by forming a new block of size
    O(|block|) from w|_0 and w|_1.
    """
    # g = prefix * block^exp * suffix
    # g|_x = prefix|_{image} * (block^exp)|_{suf-image} * suffix|_x
    suf_sec = section_word(p.suffix, x)
    x_mid = first_letter_image(p.suffix, x)
    mid = _section_pure_power(p.block, p.exp, x_mid)
    x_pre = _power_image(p.block, p.exp, x_mid)
    pre_sec = section_word(p.prefix, x_pre)
    return Periodic(pre_sec + mid.prefix, mid.block, mid.exp, mid.suffix + suf_sec)


def _power_image(block: str, exp: int, x: int) -> int:
    return x ^ ((exp & 1) * eps_word(block) if block else 0)


def _section_pure_power(w: str, e: int, x: int) -> Periodic:
    """w^e |_x as a Periodic, without expanding to e copies."""
    if e == 0 or w == "":
        return Periodic("", "", 0, "")
    if len(w) == 1:
        return Periodic(*_from_alt_power(w, e, x))

    ew = eps_word(w)
    w0 = section_word(w, 0)
    w1 = section_word(w, 1)
    if ew == 0:
        # w^e |_x = (w|_x)^e
        return Periodic("", section_word(w, x), e, "")
    # ε(w)=1: product_{j=e-1 down to 0} w|_{x XOR (j mod 2)}
    # e even: (w|_{x⊕1} · w|_x)^{e/2}
    # e odd:  w|_x · (w|_{x⊕1} · w|_x)^{(e-1)/2}  is WRONG for left-to-right
    # written product (leftmost is applied last = j=e-1).
    #
    # Written left-to-right with rightmost applied first:
    # leftmost factor is w|_{x XOR ((e-1) mod 2)}, rightmost is w|_x.
    if e % 2 == 0:
        # leftmost j=e-1 is odd, so w|_{x⊕1}, then w|_x, repeating.
        new_block = section_word(w, x ^ 1) + section_word(w, x)
        return Periodic("", new_block, e // 2, "")
    # e odd: leftmost j=e-1 even, w|_x, then (w|_{x⊕1} w|_x)^{(e-1)/2}
    # so prefix = w|_x, block = w|_{x⊕1} w|_x, exp = (e-1)/2.
    # Check e=1: prefix = w|_x, exp=0. Yes, w|_x.
    # e=3: w|_x · (w|_{x⊕1} w|_x). Leftmost j=2 even: w|_x; j=1: w|_{x⊕1}; j=0: w|_x.
    # Written: w|_x  w|_{x⊕1}  w|_x. That is prefix=w|_x, block=w|_{x⊕1} w|_x, exp=1.
    # YES.
    return Periodic(section_word(w, x), section_word(w, x ^ 1) + section_word(w, x), (e - 1) // 2, "")


def _from_alt_power(g: str, e: int, x: int) -> tuple[str, str, int, str]:
    """Special-case A^e, B^e, C^e via the proved identities, as Periodic fields."""
    if g == A:
        return ("", A if x == 0 else C, e, "")
    if g == C:
        if x == 0:
            # (CB)^{e/2} or B(CB)^{(e-1)/2}
            if e % 2 == 0:
                return ("", C + B, e // 2, "")
            return (B, C + B, (e - 1) // 2, "")
        if e % 2 == 0:
            return ("", B + C, e // 2, "")
        return (C, B + C, (e - 1) // 2, "")
    if g == B:
        if x == 0:
            if e % 2 == 0:
                return ("", C + A, e // 2, "")
            return (A, C + A, (e - 1) // 2, "")
        if e % 2 == 0:
            return ("", A + C, e // 2, "")
        return (C, A + C, (e - 1) // 2, "")
    raise ValueError(g)


# ---------------------------------------------------------------------------
# Equality tests via action
# ---------------------------------------------------------------------------

def equal_on_level(w1: str, w2: str, level: int) -> bool:
    nbits = level
    cap = 1 << nbits
    if nbits <= 12:
        return all(apply_word(w1, z, nbits) == apply_word(w2, z, nbits) for z in range(cap))
    # random + structured probes
    probes = list(range(min(64, cap)))
    probes += [cap - 1, cap // 2, cap // 3, (cap * 2) // 3]
    for k in range(nbits):
        probes.append(1 << k)
        probes.append((1 << nbits) - 1 - (1 << k if k < nbits else 0))
    for z in probes:
        z &= cap - 1
        if apply_word(w1, z, nbits) != apply_word(w2, z, nbits):
            return False
    return True


# ---------------------------------------------------------------------------
# Query-ray walk with the proved rewrite rules
# ---------------------------------------------------------------------------

def walk_query_ray(n: int) -> dict:
    """Walk C^n along 0^{n-1} using Periodic rewrite; record expansion.

    Returns activities (should be bits 1..n of f^n(1)) and cost measures.
    """
    # Start at C^n
    cur = Periodic("", C, n, "")
    activities = [cur.eps()]
    desc_sizes = [cur.desc_size()]
    exp_lens = [cur.expanded_len()]
    # total expansion charged as sum of expanded lengths after each rewrite
    # (each section of an expanded word of length L costs Θ(L) generator
    # rewrites if the Periodic block is written out, and Θ(desc_size) if
    # only the compressed form is rewritten).
    for _ in range(n - 1):
        cur = section_periodic(cur, 0)
        # flatten prefix/suffix into a single periodic form when possible
        cur = _normalize(cur)
        activities.append(cur.eps())
        desc_sizes.append(cur.desc_size())
        exp_lens.append(cur.expanded_len())
    return {
        "n": n,
        "activities": activities,
        "desc_sizes": desc_sizes,
        "exp_lens": exp_lens,
        "sum_desc": sum(desc_sizes),
        "sum_exp": sum(exp_lens),
        "final_eps": activities[-1] if activities else 0,
        "max_desc": max(desc_sizes) if desc_sizes else 0,
        "max_exp_len": max(exp_lens) if exp_lens else 0,
        "final": cur,
    }


def _normalize(p: Periodic) -> Periodic:
    """Keep prefix/suffix from growing without bound by absorbing length-0 exp."""
    if p.exp == 0:
        w = p.prefix + p.suffix
        return Periodic("", w, 1, "") if w else Periodic("", "", 0, "")
    # If prefix+suffix small relative to block, leave it.
    # Absorb a full extra block copy from prefix/suffix if they match.
    return p


def bits_of_row_from_bit1(n: int) -> list[int]:
    """Bits 1..n of f^n(1), i.e. the zero-ray activities of C^n including ε(C^n)."""
    row = packed_row(n)
    return [(row >> k) & 1 for k in range(1, n + 1)]


# ---------------------------------------------------------------------------
# Relation search
# ---------------------------------------------------------------------------

def all_words_upto(L: int) -> list[str]:
    out = [""]
    for n in range(1, L + 1):
        for tup in product(GENS, repeat=n):
            out.append("".join(tup))
    return out


def relation_search(max_len: int = 4, level: int = 10) -> list[tuple[str, str]]:
    """Pairs of distinct words of length ≤ max_len that agree on level `level`."""
    words = all_words_upto(max_len)
    # bucket by (activity, action fingerprint)
    buckets: dict[tuple, list[str]] = defaultdict(list)
    nbits = level
    cap = 1 << nbits
    sample = list(range(cap)) if nbits <= 10 else list(range(256))
    for w in words:
        fp = tuple(apply_word(w, z, nbits) for z in sample)
        buckets[(eps_word(w), fp)].append(w)
    rels = []
    for group in buckets.values():
        if len(group) < 2:
            continue
        # verify full equality on the level
        w0 = group[0]
        for w in group[1:]:
            if equal_on_level(w0, w, level):
                rels.append((w0, w))
    return rels


def short_equal_to(target: str, max_len: int, level: int = 10) -> list[str]:
    hits = []
    for w in all_words_upto(max_len):
        if w == target:
            continue
        if eps_word(w) != eps_word(target):
            continue
        if equal_on_level(w, target, level):
            hits.append(w)
    return hits


# ---------------------------------------------------------------------------
# Morphic block doubling along n = 2^m
# ---------------------------------------------------------------------------

def iterate_block_under_zero(n: int, steps: int | None = None) -> list[dict]:
    """Start from C^n and iterate the pure Periodic |_0, recording blocks."""
    cur = Periodic("", C, n, "")
    hist = []
    steps = n - 1 if steps is None else steps
    for i in range(steps + 1):
        hist.append({
            "k": i,
            "prefix": cur.prefix,
            "block": cur.block,
            "exp": cur.exp,
            "suffix": cur.suffix,
            "eps": cur.eps(),
            "desc": cur.desc_size(),
            "explen": cur.expanded_len(),
            "block_eps": eps_word(cur.block) if cur.block else 0,
        })
        if i == steps:
            break
        cur = _normalize(section_periodic(cur, 0))
    return hist


def substitution_trace(seed: str, max_rounds: int = 8) -> list[str]:
    """If we only had exponent-halving when ε=1: w |-> w|_1 w|_0 or w|_0."""
    w = seed
    out = [w]
    for _ in range(max_rounds):
        if eps_word(w) == 0:
            w = section_word(w, 0)
        else:
            w = section_word(w, 1) + section_word(w, 0)
        out.append(w)
    return out


# ---------------------------------------------------------------------------
# Cost model for the proved rewrite along n = 2^m
# ---------------------------------------------------------------------------

def expansion_family_pow2(max_m: int = 8) -> list[dict]:
    rows = []
    for m in range(1, max_m + 1):
        n = 1 << m
        walk = walk_query_ray(n)
        row_bits = bits_of_row_from_bit1(n)
        ok = walk["activities"] == row_bits
        rows.append({
            "n": n,
            "ok": ok,
            "sum_desc": walk["sum_desc"],
            "sum_exp": walk["sum_exp"],
            "max_desc": walk["max_desc"],
            "c_n_rewrite": walk["final_eps"],
            "c_n_true": center_bit(n),
            "sum_exp_over_n2": walk["sum_exp"] / (n * n),
            "sum_desc_over_n2": walk["sum_desc"] / (n * n),
        })
    return rows


def expansion_family_allones(max_m: int = 7) -> list[dict]:
    rows = []
    for m in range(2, max_m + 1):
        n = (1 << m) - 1
        walk = walk_query_ray(n)
        row_bits = bits_of_row_from_bit1(n)
        ok = walk["activities"] == row_bits
        rows.append({
            "n": n,
            "ok": ok,
            "sum_desc": walk["sum_desc"],
            "sum_exp": walk["sum_exp"],
            "max_desc": walk["max_desc"],
            "c_n_rewrite": walk["final_eps"],
            "c_n_true": center_bit(n),
            "sum_exp_over_n2": walk["sum_exp"] / (n * n),
        })
    return rows


# ---------------------------------------------------------------------------
# Direct verification of identities against the wreath product
# ---------------------------------------------------------------------------

def verify_power_identities(mmax: int = 12, level: int = 10) -> None:
    for m in range(0, mmax + 1):
        for x in (0, 1):
            # C^m |_x via expanding C*C*...*C vs closed form
            w = C * m
            got = section_word(w, x)
            want = power_C_section(m, x)
            assert got == want, (m, x, got, want)
            assert equal_on_level(got, want, level)
            wB = B * m
            gotB = section_word(wB, x)
            wantB = power_B_section(m, x)
            assert gotB == wantB, (m, x, gotB, wantB)
            wA = A * m
            gotA = section_word(wA, x)
            wantA = power_A_section(m, x)
            assert gotA == wantA
            wBC = (B + C) * m
            gotBC = section_word(wBC, x)
            wantBC = power_BC_section(m, x)
            assert gotBC == wantBC, (m, x, gotBC, wantBC)
            wCB = (C + B) * m
            gotCB = section_word(wCB, x)
            wantCB = power_CB_section(m, x)
            assert gotCB == wantCB, (m, x, gotCB, wantCB)
    # A^m |_1 = C^m
    for m in range(0, mmax + 1):
        assert section_word(A * m, 1) == C * m
        assert equal_on_level(section_word(A * m, 1), C * m, level)


def verify_center_formula(nmax: int = 40) -> None:
    for n in range(1, nmax + 1):
        # ε(A^n | 10^{n-1}) = ε(C^n | 0^{n-1})
        # A^n |_1 = C^n, then n-1 zeros.
        walk = walk_query_ray(n)
        cn = center_bit(n)
        assert walk["final_eps"] == cn, (n, walk["final_eps"], cn)
        # activities along the ray equal bits 1..n of f^n(1)
        assert walk["activities"] == bits_of_row_from_bit1(n), n


def verify_periodic_section_matches_expand(nmax: int = 20) -> None:
    for n in range(1, nmax + 1):
        cur = Periodic("", C, n, "")
        expanded = C * n
        for k in range(n - 1):
            cur = _normalize(section_periodic(cur, 0))
            expanded = section_word(expanded, 0)
            assert cur.expanded() == expanded, (n, k, cur, expanded)
            assert cur.eps() == eps_word(expanded)


def verify_wreath_on_integers(nbits: int = 12) -> None:
    """A,B,C integer action matches the wreath recursion bit-wise."""
    cap = 1 << nbits
    for z in range(cap):
        z0, rest = z & 1, z >> 1
        # A
        a = apply_gen(A, z, nbits)
        assert (a & 1) == z0
        sec = A if z0 == 0 else C
        assert (a >> 1) == apply_gen(sec, rest, nbits - 1)
        # B
        b = apply_gen(B, z, nbits)
        assert (b & 1) == (z0 ^ 1)
        sec = A if z0 == 0 else C
        assert (b >> 1) == apply_gen(sec, rest, nbits - 1)
        # C
        c = apply_gen(C, z, nbits)
        assert (c & 1) == (z0 ^ 1)
        sec = B if z0 == 0 else C
        assert (c >> 1) == apply_gen(sec, rest, nbits - 1)
    # A agrees with f on nbits (f may set bits above nbits-1 from low bits)
    for z in range(cap):
        assert apply_gen(A, z, nbits) == (f_int(z) & (cap - 1) if nbits >= z.bit_length() + 2 or True else 0)
        # f(z) can use bits z_{nbits-1}, z_{nbits-2} to produce out_{nbits-1}
        # so on nbits of input, output low nbits of f(z) is exact if we
        # treat missing high input bits as 0, which apply_gen does.
        assert apply_gen(A, z, nbits) == (f_int(z) & ((1 << nbits) - 1))


# ---------------------------------------------------------------------------
# SLP size under iterated section: product construction with 2 states
# ---------------------------------------------------------------------------

@dataclass
class SLP:
    """Straight-line program over {A,B,C} with concat and power nodes.

    nodes[i] is ('G', letter) or ('CAT', i, j) or ('POW', i, e).
    The last node is the root.
    """

    nodes: list[tuple]

    def size(self) -> int:
        return len(self.nodes)

    def add(self, node: tuple) -> int:
        self.nodes.append(node)
        return len(self.nodes) - 1


def slp_power(g: str, n: int) -> SLP:
    """Binary exponentiation SLP for g^n. Size Θ(log n)."""
    slp = SLP([])
    idx = slp.add(("G", g))
    if n == 0:
        slp.add(("POW", idx, 0))
        return slp
    # binary method: build g, g^2, g^4, ...
    pows = [idx]
    k = 1
    while (k << 1) <= n:
        idx = slp.add(("POW", idx, 2))
        pows.append(idx)
        k <<= 1
    # multiply bits
    acc = None
    bit = 0
    nn = n
    while nn:
        if nn & 1:
            if acc is None:
                acc = pows[bit]
            else:
                acc = slp.add(("CAT", pows[bit], acc))
        nn >>= 1
        bit += 1
    if acc is None:
        slp.add(("POW", pows[0], 0))
    elif acc != len(slp.nodes) - 1:
        # root is already acc if it was the last add; else the last CAT is root
        pass
    return slp


def slp_eps(slp: SLP) -> int:
    eps = [0] * len(slp.nodes)
    for i, node in enumerate(slp.nodes):
        if node[0] == "G":
            eps[i] = ACTIVITY[node[1]]
        elif node[0] == "CAT":
            eps[i] = eps[node[1]] ^ eps[node[2]]
        else:
            _, j, e = node
            eps[i] = eps[j] if (e & 1) else 0
    return eps[-1]


def slp_section(slp: SLP, x: int) -> SLP:
    """Section of every node at a given first letter, producing a new SLP.

    For CAT: (XY)|_x = X|_{x⊕ε(Y)} Y|_x.
    For POW: uses _section_pure_power at the node level by expanding the
    power into CAT of two sectioned copies when ε=1 — this is exactly the
    rewrite that doubles description size.

    Cached per (node, letter). Worst-case size O(2 * old size) per call
    because each node has two possible letters.
    """
    # We implement the full (node, letter) product, which is the tight
    # closed-form size bound for one section of an SLP under a 2-bit twist.
    eps = [0] * len(slp.nodes)
    for i, node in enumerate(slp.nodes):
        if node[0] == "G":
            eps[i] = ACTIVITY[node[1]]
        elif node[0] == "CAT":
            eps[i] = eps[node[1]] ^ eps[node[2]]
        else:
            _, j, e = node
            eps[i] = eps[j] if (e & 1) else 0

    new = SLP([])
    # map (old_index, letter) -> new_index
    memo: dict[tuple[int, int], int] = {}

    def rec(i: int, letter: int) -> int:
        key = (i, letter)
        if key in memo:
            return memo[key]
        node = slp.nodes[i]
        if node[0] == "G":
            g = node[1]
            out = SECTIONS[g][letter]
            idx = new.add(("G", out))
            memo[key] = idx
            return idx
        if node[0] == "CAT":
            left, right = node[1], node[2]
            r = rec(right, letter)
            l = rec(left, letter ^ eps[right])
            idx = new.add(("CAT", l, r))
            memo[key] = idx
            return idx
        # POW
        _, j, e = node
        if e == 0:
            idx = new.add(("POW", rec(j, 0), 0))
            memo[key] = idx
            return idx
        ew = eps[j]
        if ew == 0:
            idx = new.add(("POW", rec(j, letter), e))
            memo[key] = idx
            return idx
        # ε=1: e even => (w|_{ℓ⊕1} w|_ℓ)^{e/2}
        # e odd  => w|_ℓ · (w|_{ℓ⊕1} w|_ℓ)^{(e-1)/2}
        a = rec(j, letter ^ 1)
        b = rec(j, letter)
        blk = new.add(("CAT", a, b))
        if e % 2 == 0:
            idx = new.add(("POW", blk, e // 2))
        else:
            half = new.add(("POW", blk, (e - 1) // 2))
            idx = new.add(("CAT", b, half))
        memo[key] = idx
        return idx

    rec(len(slp.nodes) - 1, x)
    return new


def slp_walk_sizes(n: int) -> list[int]:
    slp = slp_power(C, n)
    sizes = [slp.size()]
    for _ in range(n - 1):
        slp = slp_section(slp, 0)
        sizes.append(slp.size())
    return sizes


# ---------------------------------------------------------------------------
# Block-doubling lemma along n = 2^m: explicit family
# ---------------------------------------------------------------------------

def doubling_trace_pow2(m: int) -> list[dict]:
    """Unroll the first m section steps of C^{2^m} symbolically."""
    n = 1 << m
    return iterate_block_under_zero(n, steps=min(n - 1, m + 4))


# ---------------------------------------------------------------------------
# Self-test / main
# ---------------------------------------------------------------------------

def main() -> None:
    print("=== wreath recursion on integers ===")
    verify_wreath_on_integers(12)
    print("ok  nbits=12")

    print("=== power-section identities (expanded words) ===")
    verify_power_identities(16, 10)
    print("ok  m<=16")

    print("=== Periodic section matches expand ===")
    verify_periodic_section_matches_expand(24)
    print("ok  n<=24")

    print("=== center formula c_n = ε(C^n | 0^{n-1}) ===")
    verify_center_formula(48)
    print("ok  n<=48")

    print("=== A^n|_1 = C^n and query identity vs packed f ===")
    for n in range(1, 33):
        assert section_word(A * n, 1) == C * n
        assert center_bit(n) == walk_query_ray(n)["final_eps"]
    print("ok  n<=32")

    print("=== A^n acts as f^n on integers ===")
    for n in range(1, 20):
        nbits = 2 * n + 4
        assert apply_word(A * n, 1, nbits) == (packed_row(n) & ((1 << nbits) - 1))
    print("ok  n<=19")

    print("=== (AC)^m and (CA)^m sections vs wreath expand ===")
    for m in range(0, 12):
        for x in (0, 1):
            assert section_word((A + C) * m, x) == _section_pure_power(A + C, m, x).expanded()
            assert section_word((C + A) * m, x) == _section_pure_power(C + A, m, x).expanded()
            assert section_word((B + A) * m, x) == _section_pure_power(B + A, m, x).expanded()
            assert section_word((A + B) * m, x) == _section_pure_power(A + B, m, x).expanded()
    print("ok  m<=11")

    print("=== short relations (words of length ≤ 4, level 10) ===")
    rels = relation_search(4, 10)
    nontrivial = [(a, b) for a, b in rels if a != b]
    print(f"  equal pairs: {len(nontrivial)}")
    assert not nontrivial

    print("=== CCBA vs shorter words ===")
    hits = short_equal_to("CCBA", 3, 10)
    print(f"  CCBA equals a word of length ≤3: {hits}")
    hits4 = [w for w in all_words_upto(4) if w != "CCBA" and eps_word(w) == eps_word("CCBA") and equal_on_level(w, "CCBA", 10)]
    print(f"  CCBA equals a different length-≤4 word: {hits4[:20]} (count {len(hits4)})")

    print("=== substitution / block doubling from C ===")
    trace = substitution_trace(C, 8)
    for i, w in enumerate(trace):
        print(f"  round {i}: |w|={len(w)}  ε={eps_word(w)}  {w if len(w)<=32 else w[:32]+'...'}")

    print("=== expansion along n=2^m ===")
    rows = expansion_family_pow2(7)
    print("  n  ok  sum_exp  sum_desc  max_desc  sum_exp/n^2  c_n")
    for r in rows:
        print(
            f"  {r['n']:4d}  {int(r['ok'])}  {r['sum_exp']:8d}  {r['sum_desc']:8d}  "
            f"{r['max_desc']:4d}  {r['sum_exp_over_n2']:.4f}  {r['c_n_rewrite']}/{r['c_n_true']}"
        )

    print("=== expansion along n=2^m-1 ===")
    rows1 = expansion_family_allones(6)
    print("  n  ok  sum_exp  max_desc  sum_exp/n^2  c_n")
    for r in rows1:
        print(
            f"  {r['n']:4d}  {int(r['ok'])}  {r['sum_exp']:8d}  {r['max_desc']:4d}  "
            f"{r['sum_exp_over_n2']:.4f}  {r['c_n_rewrite']}/{r['c_n_true']}"
        )

    print("=== first steps of C^{2^m} compressed form ===")
    for m in (1, 2, 3, 4, 5, 6):
        hist = doubling_trace_pow2(m)
        print(f"  n={1<<m}")
        for h in hist[: m + 3]:
            blk = h["block"] if len(h["block"]) <= 24 else h["block"][:24] + "..."
            print(
                f"    k={h['k']:2d}  pre={h['prefix']!r:8s} blk={blk!r:26s} "
                f"e={h['exp']:4d}  desc={h['desc']:4d}  explen={h['explen']:4d}  ε={h['eps']}"
            )

    print("=== relations up to length 6 ===")
    for L in (5, 6):
        relsL = relation_search(L, 8)
        nontrivialL = [(a, b) for a, b in relsL if a != b]
        print(f"  length ≤{L}: {len(nontrivialL)} equal pairs")
        assert not nontrivialL, nontrivialL[:5]

    print("=== ray words are not equal to any strictly shorter word ===")
    for n in (4, 5, 6, 7, 8):
        cur = C * n
        for k in range(n):
            assert len(cur) == n
            hits = short_equal_to(cur, n - 1, 8)
            assert not hits, (n, k, cur, hits[:3])
            if k < n - 1:
                cur = section_word(cur, 0)
    print("ok  n<=8, every C^n|_{0^k} has no representative of length < n")

    print("=== first three zero-sections of C^{2^m} ===")
    for m in range(2, 8):
        n = 1 << m
        w = C * n
        s0 = section_word(w, 0)
        assert s0 == (C + B) * (n // 2)
        s1 = section_word(s0, 0)
        assert s1 == (C + A) * (n // 2)
        s2 = section_word(s1, 0)
        assert s2 == (C + C + B + A) * (n // 4)
    print("ok  C^{2^m}|_0=(CB)^{n/2}, then (CA)^{n/2}, then (CCBA)^{n/4}")

    print("=== sum_exp = n² on the two infinite families (exact) ===")
    for n in [1 << m for m in range(1, 8)] + [(1 << m) - 1 for m in range(2, 7)]:
        walk = walk_query_ray(n)
        assert walk["sum_exp"] == n * n, (n, walk["sum_exp"])
        assert all(L == n for L in walk["exp_lens"])
    print("ok  expanded length is constantly n; n snapshots give n²")

    print("=== SLP size under iterated section (n=8,16) ===")
    for n in (8, 16):
        sizes = slp_walk_sizes(n)
        print(f"  n={n}  slp sizes (first 12): {sizes[:12]}  ... last={sizes[-1]}  sum={sum(sizes)}")

    print("=== all checks passed ===")


if __name__ == "__main__":
    main()
