# Cycle KQ: no-\(00\) family weight is odd; covering parity is \(q\)

Every no-\(00\) family Green weight is odd (Jacobsthal
\(a_L=a_{L-1}+2a_{L-2}\) stays odd; \(3\cdot 2^a-1\) is
\(3a_{a}\)). Covering in-support \(G=1\) XOR on those clocks is
\(0\) for \(q=6\) and \(1\) for \(q=10\), \(k\le 6\). This is
**not** even weight, **not** \(J\), **not** independent of \(q\),
and **not** the unclipped \(g_{\mathrm{wt}}\) XOR on \(q=10\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\).
Do **not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: this is family covering parity, not packed AND
XOR \(J\), so covering never-fail stays open.

Certify: `python3 research/cycle_kq.py --certify` (~0.14s).
Dump: `research/cycle_kq.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/AT/CA/HG/KH/KJ/KM/KP (\(n<256\); covering \(k\le 6\); no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (family weight odd)

Certified \(n<256\) no-\(00\) family and \(3\cdot 2^a-1\) for
\(a\le 8\). Jacobsthal \(|S_{L+2}|\) odd for \(L\le 10\).

## Lemma (covering family parity is \(q\))

In-support \(G=1\) XOR on family clocks is \(0\) for \(J_6\) and
\(1\) for \(J_{10}\), \(k\le 6\). Covering \(J_6,J_{10}\) still have
\(G=1\) columns \(22659\); odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

Family weight even: \(n=1\) has \(g_{\mathrm{wt}}=3\). Family
parity equals \(J\): \(k=0\), \(q=6\) is \(0\) vs \(J=1\).
Independent of \(q\): \(q=6\) is \(0\), \(q=10\) is \(1\). Unclipped
equals in-support: \(k=0\), \(q=10\), \(n=3\) clips one \(1\).

## Verdict

`LEMMA` (family weight odd; covering family parity is \(q\);
Mersenne prefix; piecewise residues).
`KILLED` (even weight; equals \(J\); independent of \(q\);
unclipped).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_kq.md` (this note)
- `research/cycle_kq.py`
- `research/cycle_kq.json`
