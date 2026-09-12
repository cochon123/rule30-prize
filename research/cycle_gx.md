# Cycle GX: at odd \(s\), the \(j\)-th even column has Green \(G(n,j)\)

Cycle GU gives \(G=G(n,W/2-r/2)\) with \(n=UQ-t-1\). Palindrome and
\(r=\mathrm{lo}+2j\) send that to \(G(n,j)\), so Cycle GP’s \(j\)-index
holds at every odd \(s\), not only hits. Off-hit this is **not**
\(\mathrm{mer\_one}(j)\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: a \(j\)-index for odd-\(s\) Green does not prove
covering never-fail (AND still mixes; even \(s\) still contribute).

Helper: `odd_clock` from `research/cycle_gu.py`. Certify:
`python3 research/cycle_gx.py --certify` (~0.02s). Dump:
`research/cycle_gx.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/GN/GP/GU/GW (Green \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (\(G(m,W-r)=G(n,j)\) on even \(r=\mathrm{lo}+2j\))

Certified \(k\le 6\), all covering \(W\), every odd \(s\). Hits
recover Cycle GP / GO when \(n=U(Q-q)-1\).

## Killed

Off-hit equals \(\mathrm{mer\_one}(j)\): at \(k=2\), \(W=8U\),
\(\delta=3\), \(n=6\), \(j=1\), \(G=0\) but \(\mathrm{mer\_one}=1\).
Reversed \(G(n,U-1-j)\): at \(j=0\), \(1\neq 0\). Identically 1: same
\(j=1\), \(G=0\).

## Verdict

`LEMMA` (odd-\(s\) \(j\)-th even column has \(G(n,j)\)).
`KILLED` (off-hit \(\mathrm{mer\_one}\); reversed index; identically
1).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_gx.md` (this note)
- `research/cycle_gx.py`
- `research/cycle_gx.json`
