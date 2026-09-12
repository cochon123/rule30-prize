# Cycle KK: Green weight is the product of binary 1-run weights

\(g_{\mathrm{wt}}(n)\) equals the product over binary ones-runs of
length \(L\) of \(a_L=g_{\mathrm{wt}}(2^L-1)=(2^{L+2}-(-1)^L)/3\).
If \(n\) has no adjacent binary \(1\)s then
\(g_{\mathrm{wt}}(n)=3^{\mathrm{popcount}(n)}\). Weight is **not**
\(3^{\mathrm{popcount}}\) for every \(n\). It is **not** the sum of
run weights. \(a_L\) is **not** \(2^{L+1}-1\). Odd stretch is **not**
always \(3 g_{\mathrm{wt}}(m)\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: this is Green-only arithmetic, not the packed
AND XOR \(J\), so covering never-fail stays open.

Certify: `python3 research/cycle_kk.py --certify`.
Dump: `research/cycle_kk.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/KH/KJ (\(n<256\); covering \(k\le 6\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (weight is a 1-run product)

For \(n<256\), \(g_{\mathrm{wt}}(n)=\prod a_L\) over the binary
ones-runs of \(n\), where \(a_L=g_{\mathrm{wt}}(2^L-1)\). The
Mersenne weights have closed form
\(a_L=(2^{L+2}-(-1)^L)/3\) and recurrence
\(a_L=a_{L-1}+2 a_{L-2}\) with \(a_0=1\), \(a_1=3\). Empty product
is \(1\) at \(n=0\).

## Lemma (no adjacent \(11\) is \(3^{\mathrm{popcount}}\))

The \(55\) integers \(n<256\) with \(n\land (n\ll 1)=0\) have
\(g_{\mathrm{wt}}(n)=3^{\mathrm{popcount}(n)}\). The other \(201\)
have strictly smaller weight. Covering \(J_6,J_{10}\) for \(k\le 6\)
still has \(G=1\) columns \(22659\); odd-\(s\) \(J\) XOR matches
Cycles HF/HG.

## Killed

\(g_{\mathrm{wt}}=3^{\mathrm{popcount}}\) for all \(n\): \(n=3\) has
weight \(5\), not \(9\). Weight is the sum of run weights: \(n=11\)
(\(1011_2\)) is \(5\cdot 3=15\), not \(5+3=8\). \(a_L=2^{L+1}-1\):
\(L=3\) gives \(15\), but \(g_{\mathrm{wt}}(7)=11\). Odd stretch is
always \(3 g_{\mathrm{wt}}(m)\): \(n=3\) is \(5\), not \(9\).

## Verdict

`LEMMA` (weight is a binary 1-run product; Mersenne \(a_L\) closed
form; no-adjacent-\(11\) is \(3^{\mathrm{popcount}}\); child runs
equal parent weight).
`KILLED` (all \(n\) have \(3^{\mathrm{popcount}}\); sum of run
weights; \(a_L=2^{L+1}-1\); odd stretch always \(3\) times parent).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_kk.md` (this note)
- `research/cycle_kk.py`
- `research/cycle_kk.json`
