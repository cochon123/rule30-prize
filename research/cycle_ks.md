# Cycle KS: family clip counts are Jacobsthal \(J_{k+1}-1\) and \(2^{k+1}-1\)

Covering \(k\le 6\): the \(q=6\) max-Mersenne clip and the \(q=10\)
\(3\cdot 2^k-1\) clip equal \(\operatorname{jacobsthal}(k+1)-1\)
(and \(g_{\mathrm{wt}}(2^{k-1}-1)-1\)), vanishing for \(k<2\); the
\(q=10\) max-Mersenne clip is \(2^{k+1}-1\). This is **not**
Jacobsthal without the \(-1\), **not** \(q=6\) max equal to \(q=10\)
max, **not** \(q=10\) tri equal to \(q=10\) mer, and **not** \(q=6\)
max equal to \(2^{k+1}-1\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: this is a closed form for Cycle KR's clip table,
not packed AND XOR \(J\), so covering never-fail stays open.

Certify: `python3 research/cycle_ks.py --certify` (~0.14s).
Dump: `research/cycle_ks.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AT/CA/KH/KJ/KR (covering \(k\le 6\); no Fermat table, no extra
window, no \(n_0=16\) window).

## Lemma (family clip counts)

Certified \(k\le 6\). Palindrome sends clipped \(G=1\) to a low
prefix of \(f(d)=[d\not\equiv 2\pmod{3}]\). Covering \(J_6,J_{10}\)
still have \(G=1\) columns \(22659\); odd-\(s\) \(J\) XOR matches
Cycles HF/HG.

## Lemma (family clippers)

Cycle KR. \(q=6\) none if \(k<2\) else \(n=2^{k+1}-1\); \(q=10\)
always \(n=2^{k+2}-1\), and also \(n=3\cdot 2^k-1\) when \(k\ge 2\).

## Killed

Clip is Jacobsthal without \(-1\): \(k=2\), \(q=6\) is \(2\) vs \(3\).
\(q=6\) max equals \(q=10\) max: \(k=2\) is \(2\) vs \(7\). \(q=10\)
tri equals mer: \(k=2\) is \(2\) vs \(7\). \(q=6\) max is
\(2^{k+1}-1\): \(k=2\) is \(2\) vs \(7\).

## Verdict

`LEMMA` (family clip counts; family clippers; family weight odd;
covering family parity is \(q\)).
`KILLED` (no minus one; \(q=6\) equals \(q=10\) mer; \(q=10\) tri
equals mer; \(q=6\) is \(2^{k+1}-1\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ks.md` (this note)
- `research/cycle_ks.py`
- `research/cycle_ks.json`
