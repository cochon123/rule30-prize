# Cycle OG: \(E_k=R_k\oplus S_k\oplus T_k\) vanishes on \(q=10\) through \(k\le 10\); this is odd-\(s\) rest, not FR \(J\)

Write
\[
E_k=R_k\oplus S_k\oplus T_k,
\]
where \(R_k\) is the odd-\(s\) packed AND xor on covering \(G=1\)
cells with \(p\notin\{4,6,14\}\) (Cycle MD rest), and \(S_k\),
\(T_k\) are Cycle NA's Green-only pieces. On covering \(q=10\)
through \(k\le 10\), a packed walk gives \(E_k=0\) and
\(R_k=\) rest10. This is **odd-\(s\) rest**, equal to HF/HG
\(\mathrm{xor}_{\mathrm{odd}}\oplus\) forced, **not** the FR full
remainder \(J_{\mathrm{full}}=\mathrm{xor}_{\mathrm{odd}}\oplus\mathrm{xor}_{\mathrm{even}}\).

The identity is **certified on eleven scales**, not an all-\(k\)
theorem: \(n_E=392048\) error cells cancel in the global XOR; that
is not 392048 independent predictions. This is **not** pointwise
(\(k=0\): \(n_E=2\)), **not** palindrome pairing of all errors
(\(k=0\): \(n_{\mathrm{pal}}=0\)), **not** \(R\) on \(S\)/\(T\)
with \(R\) off those cells vanishing (\(k=8\): \(R_T=1\),
\(T=0\)), **not** \(E_k=0\) on \(q=6\) (\(k=2\): \(E=1\); also
\(k=3,9\)), **not** \(E_k=0\) on \(q=18\) (\(k=1\): \(E=1\)),
**not** \(E_k=0\Rightarrow J_{\mathrm{full}}=0\) (\(k=2\),
\(q=10\): \(E=0\), \(J_{10}=1\)), **not** \(S\oplus T\) equal to
odd-\(s\) \(J\) or FR \(J\), and **not** the form for all \(k\).
Do **not** catalogue further \(S\)/\(T\) subregions unless the
experiment answers why \(E_k=0\). Do **not** claim \(T\) is \(1\)
iff \(k=2\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Even-time
\(\mathrm{xor}_{\mathrm{even}}\) is still required for
\(J_{\mathrm{full}}\). Do **not** claim Green-only rest for all
\(k\). Do **not** record unique-slot XOR vs \(J\).

Certify: `python3 research/cycle_og.py --certify` (~32.31s).
Dump: `research/cycle_og.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/NB/MD/HF/HG/MJ (packed odd-\(s\) \(R\) with Green \(S,T\)
on \(q=10\) through \(k\le 10\); HF/HG odd vs full remainder;
\(q=6\) \(k=2,3,9\) and \(q=18\) \(k=1\) kills; no Fermat table,
no extra window, no \(n_0=16\) window).

## Glossary

- \(R_k\): odd-\(s\) packed AND xor, \(G=1\), \(p\notin\{4,6,14\}\).
- \(S_k\): xor of \(G(n,j+1)\) on palindrome-right \(d\bmod 3=1\)
  cells with \(G(n,j-1)=0\).
- \(T_k\): xor of \(G(n,j-1)\) on palindrome-right \(G=1\) with
  \(n<U/2\).
- \(J_{\mathrm{odd}}\): HF/HG \(\mathrm{xor}_{\mathrm{odd}}\) \(=\)
  forced \(\oplus R_k\).
- \(J_{\mathrm{full}}\): FR covering remainder \(=\)
  \(J_{\mathrm{odd}}\oplus J_{\mathrm{even}}\).

## Lemma (\(E_k=0\) on \(q=10\) through \(k\le 10\); odd-\(s\) rest)

Covering \(q=10\), \(k\le 10\). The walk reads the packed row for
\(R_k\) and Green for \(S_k,T_k\). At \(k=2\), \(R=1\), \(S=0\),
\(T=1\), \(J_{\mathrm{odd}}=0\), \(J_{10}=1\). At \(k=9\),
\(n_E=83722\) and \(E=0\). At \(k=10\), \(n_E=271350\) and
\(E=0\). Status: **certified** on this range, not a lemma for all
\(k\).

## Killed

Pointwise \(e_{n,j}=0\): \(k=0\) has \(n_E=2\). Palindrome pairs
all errors: \(k=0\) has \(n_{\mathrm{pal}}=0\). Region-wise
\(R|_S=S\), \(R|_T=T\), \(R_{\mathrm{off}}=0\): \(k=8\) has
\(R_T=1\) and \(T=0\). \(E_k=0\) on \(q=6\): \(k=2\) is \(1\)
(also \(k=3,9\)). \(E_k=0\) on \(q=18\): \(k=1\) is \(1\).
\(E_k=0\Rightarrow J_{\mathrm{full}}=0\): \(k=2\), \(q=10\) has
\(J_{10}=1\). Odd-\(s\) \(J\) equals FR \(J\): \(k=0\) both
covering \(q\) have \(\mathrm{xor}_{\mathrm{odd}}=1\) and
\(\mathrm{tot}=0\). \(S\oplus T\) equals odd-\(s\) \(J\):
\(k=2\), \(q=10\) is \(1\) vs \(0\). The form for all \(k\).

## Verdict

`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\);
odd-\(s\) \(J\neq\) FR \(J\)).
`LEMMA` (NB Green-only \(S\oplus T\) equals rest on \(q=10\) for
\(k\le 10\); rest10 census; HF/HG full remainder dumps).
`KILLED` (pointwise; palindrome pairing; region-wise \(R\);
\(E_k=0\) on \(q=6\); \(E_k=0\) on \(q=18\);
\(E_k=0\Rightarrow J_{\mathrm{full}}=0\); \(S\oplus T\) equals
odd-\(s\) \(J\); the form for all \(k\); unique-rest xor equals
\(J\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_og.md` (this note)
- `research/cycle_og.py`
- `research/cycle_og.json`
