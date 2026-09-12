# Cycle KM: odd Green rows have no \(00\) iff Mersenne or \(3\cdot 2^k-1\)

Odd \(n\) has no consecutive Green zeros iff
\(g_{\mathrm{wt}}(n/2)+g_{\mathrm{wt}}(n/4)=2(n/2+1)\). For \(n<256\)
those \(n\) are \(2^k-1\) or \(3\cdot 2^k-1\). Even \(n\) without
\(00\) are only \(0\) and \(2\). This is **not** all odd \(n\), **not**
all fibbinary \(n\), **not** only Mersenne, and **not** all even \(n\)
having \(00\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\)
for all \(k\). Do **not** push the even-spine scan past \(k=18\). Do
**not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: this is Green-row shape, not the packed AND XOR
\(J\), so covering never-fail stays open.

Certify: `python3 research/cycle_km.py --certify`.
Dump: `research/cycle_km.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/KH/KJ/KK/KL (\(n<256\); covering \(k\le 6\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (odd no-\(00\) characterization)

For odd \(n<256\), no consecutive Green zeros iff
\(g_{\mathrm{wt}}(m)+g_{\mathrm{wt}}(m/2)=2(m+1)\) for \(m=n/2\).
That holds exactly on \(2^k-1\) (\(k=1..8\)) and
\(3\cdot 2^k-1\) (\(k=1..6\)): fourteen rows. Even \(n<256\) without
\(00\) are \(\{0,2\}\).

## Lemma (Jacobsthal product)

Cycle KL: \(a_L=|S_{L+2}|\). Covering \(J_6,J_{10}\) for \(k\le 6\)
still has \(G=1\) columns \(22659\); odd-\(s\) \(J\) XOR matches
Cycles HF/HG.

## Killed

Every odd \(n\) has no \(00\): \(n=9\) has \(00\). Every fibbinary
\(n\) has no \(00\): \(n=9=1001_2\) has no adjacent binary \(11\) but
has Green \(00\). Every even \(n\) has \(00\): \(n=2\) is \(10101\).
Only Mersenne odd \(n\) lack \(00\): \(n=5=3\cdot 2-1\) is not
Mersenne.

## Verdict

`LEMMA` (odd no-\(00\) characterization; odd no-\(00\) family;
\(a_L=|S_{L+2}|\); Jacobsthal product).
`KILLED` (all odd no \(00\); all fibbinary no \(00\); all even have
\(00\); only Mersenne lack \(00\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_km.md` (this note)
- `research/cycle_km.py`
- `research/cycle_km.json`
