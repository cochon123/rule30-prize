# Cycle LZ: covering \(J\) on \(k\le 6\) is a closed \((k,q)\) form

On covering \(J_6,J_{10}\) for \(k\le 6\), packed AND xor off
\(\{p=4,p=6,p=14\}\) is \(1\) iff \(q=10\) and \(k\equiv 2\pmod{4}\).
The \(\{4,6,14\}\) XOR is \(1_{k=0}\oplus\mathrm{want}_{p=14}^{\mathrm{xor}}\),
so odd-\(s\) \(J\) equals a closed \((k,q)\) form. This is **not**
rest always \(0\), **not** Cycle LB's \(1001\) remainder (that is
\(q=6\) and \(k\equiv 2\pmod{4}\)), **not** \(J\) identically \(1\),
and **not** the formula for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: the form is certified only for \(k\le 6\), so
covering never-fail stays open.

Certify: `python3 research/cycle_lz.py --certify`.
Dump: `research/cycle_lz.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HG/HH/HU/KH/LB/LD/LF (covering \(k\le 6\); no Fermat table,
no extra window, no \(n_0=16\) window).

## Lemma (rest XOR is \(1_{q=10,\,k\equiv 2\pmod{4}}\))

Certified \(k\le 6\). AND xor off \(\{4,6,14\}\) is \(1\) only at
\((k,q)=(2,10)\) and \((6,10)\). Covering \(J_6,J_{10}\) still have
\(G=1\) columns \(22659\); odd-\(s\) \(J\) XOR matches Cycles
HF/HG.

## Lemma (\(J=\mathrm{want}_J(k,q)\) on \(k\le 6\))

\(J=1_{k=0}\oplus\mathrm{want}_{p=14}^{\mathrm{xor}}\oplus\mathrm{rest}\).
At \(k=2\) both \(q\) give \(J=0\), matching covering fail in this
range.

## Lemma (\(G=1\) at \(p=14\) has AND except two \(t=0\) cells)

Cycle LY.

## Killed

Rest always \(0\): \(k=2\), \(q=10\) is \(1\). Equal to LB \(1001\)
rem: \(k=2\), \(q=6\) has rem \(1\), rest \(0\). \(J\) identically
\(1\): \(k=1\), \(q=6\) is \(0\). Rest equals \(J\): \(k=0\),
\(q=6\) has rest \(0\) and \(J=1\).

## Verdict

`LEMMA` (rest XOR is \(1_{q=10,\,k\equiv 2\pmod{4}}\); \(J\) closed
form on \(k\le 6\); \(G=1\) at \(p=14\) has AND except two \(t=0\)
cells; only \(p=4\) and \(p=6\) are silent-free; \(1001\) AND xor
remainder).
`KILLED` (rest always \(0\); equal to LB rem; \(J\) identically
\(1\); rest equals \(J\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_lz.md` (this note)
- `research/cycle_lz.py`
- `research/cycle_lz.json`
