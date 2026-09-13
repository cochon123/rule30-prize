# Cycle OI: palindrome-right \(T\)-xor is \(1\) iff \(n\) is odd

Palindrome-right xor of \(G(n,j-1)\) on \(G=1\) splits by the parity
of \(n\).

If \(n\) is even and \(G(n,j)=1\), then \(j\) is even (Green
even-\(n\) / odd-\(d\): \(G(n,d)=0\) whenever \(n\) is even and
\(d\) is odd). Hence \(j-1\) is odd, so \(G(n,j-1)=0\). Palindrome-right
\(T\)-xor and \(T\)-fire therefore vanish on every even \(n\). This
is a **lemma** from the definition of \(G\), not a finite
certificate.

If \(n\) is odd and \(n<2048\), the same palindrome-right xor is
identically \(1\) (**certified**, not claimed for all odd \(n\)).
Stay at \(n<2048\) so this is the union of Cycle OH's dyadic bands
\(k\le 11\); do **not** walk \(k=12\) \(T\)-bands.

Each odd \(n\) contributes \(1\) and even \(n\) contribute \(0\), so
the dyadic band
\[
B_k=\bigoplus\{\text{pal-right \(T\)-xor of \(n\)}\,:\,n\in[2^{k-1},2^k)\}
\]
equals the number of odd \(n\) in that interval, mod \(2\). That
count is \(1\) at \(k=1,2\) and \(2^{k-2}\) (even) for \(k\ge 3\).
For \(k\le 11\) this **proves** Cycle OH's vanish from the per-\(n\)
identity, not a re-walk of bands. Do **not** claim the odd-\(n\) xor
is \(1\) for all odd \(n\). Do **not** claim palindrome-right
\(T\)-xor vanishes on odd \(n\). Do **not** claim \(T\) is \(1\) iff
\(k=2\) for all \(k\) (that lift needs the odd-\(n\) identity for
all odd \(n\)). Do **not** catalogue further \(S\)/\(T\) subregions
unless the experiment answers why \(E_k=0\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\). Do **not** walk \(k=11\) covering packed.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\). Do
**not** record unique-slot XOR vs \(J\).

Certify: `python3 research/cycle_oi.py --certify`.
Dump: `research/cycle_oi.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OH/OG (Green even-\(n\) / odd-\(d\) and palindrome-right
\(T\)-xor on \(n<2048\); reconstructs OH bands \(k\le 11\); prefix
OH \(T\)-band and OG \(E_k\); no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (even \(n\): pal-right \(T\) vanishes)

Let \(n\) be even and \(G(n,j)=1\). The even-\(n\) clause of \(G\)
forces \(G(n,d)=0\) for every odd \(d\), so \(j\) is even. Then
\(j-1\) is odd, hence \(G(n,j-1)=0\). Every palindrome-right
\(G=1\) cell on even \(n\) is silent for \(T\). Status: **lemma**
for all even \(n\). Checked on \(n<2048\).

## Certificate (odd \(n<2048\): pal-right \(T\)-xor \(=1\))

Every odd \(n<2048\) has palindrome-right xor of \(G(n,j-1)\) on
\(G=1\) equal to \(1\). Odd \(n=1,3,\ldots,63\) each xor \(=1\);
\(n=1\) has \(n_T=1\) and one fire. Status: **certified** on this
range, not a lemma for all odd \(n\).

## Killed

Pal-right \(T\)-xor vanishes on odd \(n\): \(n=1\) has xor \(=1\).
Even \(n\) fire \(G(j-1)\) on pal-right \(G=1\): \(n_{\mathrm{fire}}=0\)
on even \(n<2048\) while those rows still have \(G=1\) cells.
Odd \(n\) empty: \(n=1\) has \(n_T=1\). Odd-\(n\) xor \(=1\) for
all odd \(n\). \(T=1\) iff \(k=2\) for all \(k\).

## Verdict

`LEMMA` (even-\(n\) pal-right \(T\)-xor vanishes for all even \(n\)).
`CERTIFIED` (odd-\(n\) pal-right \(T\)-xor is \(1\) for \(n<2048\);
dyadic \(T\)-band xor vanishes for \(3\le k\le 11\); \(E_k=0\) on
odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (odd-\(n\) xor \(=0\); even-\(n\) fire; odd \(n\) empty).
`PREFIX` (odd-\(n\) xor \(=1\) for all odd \(n\); \(T=1\) iff
\(k=2\) for all \(k\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all
\(k\); 11-bit gap; formula for extra 414990; at-most-one-odd for
all \(k\); seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_oi.md` (this note)
- `research/cycle_oi.py`
- `research/cycle_oi.json`
