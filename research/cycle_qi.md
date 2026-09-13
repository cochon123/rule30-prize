# Cycle QI: covering even-\(j\) and odd-\(j\) clipped \(G=1\) xor via clip-edge \(p=0\)

Cycle QH's covering clipped \(G=1\) xor \(A(k)\) splits by \(j\)
parity. Even \(n\) have \(G(\mathrm{even},\mathrm{odd})=0\), so
even-\(n\) odd-\(j\) tot is \(0\), and even-\(n\) even-\(j\) tot is
\(A(k-1)\). Odd \(n=2m+1\) telescopes even \(j=2l\) to
\(G(m,5U')\) on the parent covering window, which is Green xor at
packed \(p=0\) (clip edge \(j=5U'\)). Odd-\(n\) odd-\(j\) tot is
\(A(k-1)\) xor that clip-edge xor. Packed \(p=0\) has even \(j\),
so tot equals parent \(p=2\) at \(k-1\) (Cycle QG even-\(j\)
doubling; live windows match for \(k\ge 1\)). Packed \(p=2\) is
Cycle PA's unique column \(G(t,5\cdot 2^k-1)\), which fires only
at \(t=3U-1\) on the covering live window, xor \(1\) for every
\(k\). Hence clip-edge Green \(p=0\) xor is \(1\) for every \(k\),
even-\(j\) tot is \(1\) except \(k=1\), and odd-\(j\) tot is \(1\)
iff \(k\ge 2\). This is **not** rest \(=S\oplus T\) (even-\(j\) is
\(1\) for every \(k\ge 2\)). **Not** even-\(j\) tot equals \(A\)
(\(k=2\): even-\(j\) \(=1\), \(A=0\)). **Not** \(E_k=0\) for all
\(k\). Do **not** catalogue leftover \(p\) one-by-one. Do **not**
catalogue further \(S\)/\(T\) subregions unless the experiment
answers why \(E_k=0\). Do **not** claim pal-left leftover xor
vanishes for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim even-\(j\) tot equals leftover or unique Green tot.

Certify: `python3 research/cycle_qi.py --certify` (~0.51s).
Dump: `research/cycle_qi.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/PA/PB/PC/QG/QH (clip-edge \(p=0\); unique column
\(p=2\); prefix QH clipped \(A(k)\), PA unique \(G(t,5\cdot 2^a-1)\);
no Fermat table, no extra window, no \(n_0=16\) window, no packed
covering \(k=11\)).

## Lemma (covering Green xor at packed \(p=2\) is \(1\) for every \(k\))

Cycle PA: for \(a\ge 1\) and \(t\in[5\cdot 2^{a-1},2^{a+2})\),
\(G(t,5\cdot 2^a-1)=1\) iff \(t=3\cdot 2^a-1\). That window is the
covering live window for packed \(p=2\). At \(k=0\) the unique one
is \(n=2\). Status: **lemma**. Checked on \(k\le 12\).

## Lemma (covering Green xor at clip-edge \(p=0\) is \(1\) for every \(k\))

Packed \(p=0\) has even \(j=5U\). Cycle QG even-\(j\) doubling
gives tot equal to parent \(p=2\) at \(k-1\); live \(m\)-windows
match for \(k\ge 1\). Status: **lemma**. Checked on \(k\le 12\).

## Lemma (even-\(j\) tot is \(1\) except \(k=1\); odd-\(j\) tot is \(1\) iff \(k\ge 2\))

Even-\(n\) even-\(j\) tot \(=A(k-1)\); even-\(n\) odd-\(j\) tot
\(=0\); odd-\(n\) even-\(j\) tot is clip-edge \(p=0\) at \(k-1\);
odd-\(n\) odd-\(j\) tot is \(A(k-1)\) xor that bit. Status:
**lemma**. Checked on \(k\le 8\). **Killed:** even-\(j\) tot equals
\(S\oplus T\) / packed rest (\(k=7\): even-\(j\) \(=1\), rest
\(=0\)); even-\(j\) tot equals \(A\) (\(k=2\)).

## Verdict

`LEMMA` (Green xor at \(p=2\) and clip-edge \(p=0\) are \(1\) for
every \(k\); even-\(j\) tot is \(1\) except \(k=1\); odd-\(j\) tot
is \(1\) iff \(k\ge 2\); QH clipped \(A(k)=0\) for \(k\ge 1\); PA
unique column).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (even-\(j\) tot equals \(S\oplus T\) / packed rest;
even-\(j\) tot equals \(A\)).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_qi.md` (this note)
- `research/cycle_qi.py`
- `research/cycle_qi.json`
