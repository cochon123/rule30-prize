# Cycle OW: covering even-parent rem is a partial \(R_2\) tail; xor \(=1\) iff \(k\ge 6\) and \(k\bmod 4=2\)

Covering \(n=4p+1\) runs \(p<2^k\). Clip-active even-parent \(p\)
starts at \(5\cdot 2^{k-3}\) for \(k\ge 3\). Full \(R_2\)
(\(d_{\min}=1\)) would need \(p\ge 5\cdot 2^{k-2}+1\), which is
past \(p\le 2^k-1\). So every covering even-parent rem is
\(r_2\mathrm{-tail}(p,5\cdot 2^{k-2}-p+1)\). The left endpoint
\(p=5\cdot 2^{k-3}\) has \(d_{\min}=p+1\), hence an empty tail.
There are \(3\cdot 2^{k-3}\) such \(p\).

On \(k\le 10\) that xor is \(1\) iff \(k\ge 6\) and \(k\bmod 4=2\)
(so \(k=6,10\); \(k=2\) is \(2\bmod 4\) but ep \(=0\)). Covering
\(n=8t+3\) rem xor is \(1\) iff \(k\ge 2\) is even. With Cycle OV,
covering rem recurses \(\mathrm{rem}(k)=n_3(k)\oplus\mathrm{rem}(k-2)\oplus\mathrm{ep}(k)\).

This is **not** ep xor for all \(k\). **Not** n3 xor for all \(k\).
**Not** covering \(S\) for all \(k\). **Not** \(E_k=0\) for all
\(k\). Do **not** catalogue further \(S\)/\(T\) subregions unless
the experiment answers why \(E_k=0\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).

Certify: `python3 research/cycle_ow.py --certify`.
Dump: `research/cycle_ow.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/OS/OV/OU/OG (even-parent covering shape; prefix OV n7
recurrence, OU \(n=8t+3\) image, OG \(E_k\); no Fermat table, no
extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (covering even-parent rem is a partial \(R_2\) tail)

For \(k\ge 3\), clip-active covering \(p\) is
\(\{5\cdot 2^{k-3},\ldots,2^k-1\}\), count \(3\cdot 2^{k-3}\),
with \(d_{\min}=5\cdot 2^{k-2}-p+1>1\). The left endpoint has
an empty tail. Status: **lemma**. Checked on \(3\le k\le 10\).

## Certified (covering rem recurrence bits)

On \(k\le 10\), covering ep xor \(=1\) iff \(k\ge 6\) and
\(k\bmod 4=2\); covering n3 xor \(=1\) iff \(k\ge 2\) even;
covering rem equals \(n_3\oplus\mathrm{rem}(k-2)\oplus\mathrm{ep}\).
Status: **certified**. Not all \(k\).

## Killed

\(k=2\) is \(2\bmod 4\) but covering ep xor is \(0\), so the ep
form is not \(k\bmod 4=2\) alone.

## Verdict

`LEMMA` (covering even-parent partial \(R_2\) tail; OV n7
recurrence; OU \(n=8t+3\) rem).
`CERTIFIED` (ep xor and n3 xor on \(k\le 10\); rem recurrence
on \(k\le 10\); \(E_k=0\) on odd-\(s\) rest for \(q=10\),
\(k\le 10\)).
`KILLED` (ep xor \(=1\) iff \(k\bmod 4=2\) including \(k=2\)).
`PREFIX` (ep xor for all \(k\); n3 xor for all \(k\); covering
\(S\) for all \(k\); \(E_k=0\) for all \(k\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ow.md` (this note)
- `research/cycle_ow.py`
- `research/cycle_ow.json`
