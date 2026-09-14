# Cycle ST: pal-center packed AND is next-row center AND right neighbor

Covering pal-center \(j=n\) has packed \(p=s+2\) on even snapshot
\(s=10U-2n-2\). Cycle HH packed AND is odd-\(s\) bits \(p\) and
\(p-1\), so AND \(= c_{s+1}\land x(s+1,1)\). For \(k\ge 3\) the
min pal-center \(p=2U+2\ge 18\), never forced, so the pal-center
rest bit equals that AND. Time residues for \(k\ge 1\): even \(n\)
at \(s\equiv 2\pmod{4}\) in \([2U+2,10U-2]\); odd \(n\) at
\(s\equiv 0\pmod{4}\) in \([2U,10U-4]\). Do **not** claim
pal-center tot equals \(S\oplus T\). Do **not** claim pal-center
AND identically \(0\). Do **not** claim pal-center AND equals
\(c_{s+1}\) alone. This is **not** rest \(=S\oplus T\). **Not**
\(E_k=0\) for all \(k\). Do **not** catalogue leftover \(p\)
one-by-one. Do **not** catalogue further \(S\)/\(T\) subregions
unless the experiment answers why \(E_k=0\). Do **not** claim
pal-left leftover xor vanishes for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\). Do **not** walk \(k=11\) covering packed. Do
**not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_st.py --certify` (~0.17s).
Dump: `research/cycle_st.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/PB/QV/SO/SR/SS (pal-center packed AND is
next-row center AND right neighbor; no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (pal-center packed AND \(= c_{s+1}\land x(s+1,1)\))

On \(q=10\), covering pal-center \(j=n\) has packed \(p=10U-2n\)
and even snapshot \(s=10U-2n-2\), so \(p=s+2\). Cycle HH packed
AND is the odd-row bits \(p\) and \(p-1\). Two-sided coords give
\(x(s+1,0)=\) packed bit \(s+1\) and \(x(s+1,1)=\) packed bit
\(s+2\). Hence pal-center packed AND \(= c_{s+1}\land x(s+1,1)\).
Status: **lemma**. Pal-center-only covering walk through
\(k\le 10\) (match Cycle SR pal-center tots); algebra through
\(k\le 64\). **Killed:** pal-center AND identically \(0\).
**Killed:** pal-center AND equals \(c_{s+1}\) alone (\(t=0\):
\(c_0=1\), \(x(0,1)=0\)).

## Lemma (pal-centers never forced for \(k\ge 3\))

Largest covering \(n=4U-1\) has pal-center \(p=2U+2\). For
\(k\ge 3\) that min sits past \(\{4,6,14\}\), so pal-center rest
equals the AND bit. Forced pal-centers only at \(k=0\) (\(n=3\),
\(p=4\) and \(n=2\), \(p=6\)), \(k=1\) (\(n=7\), \(p=6\) and
\(n=3\), \(p=14\)), \(k=2\) (\(n=13\), \(p=14\)). Status:
**lemma**. **Killed:** pal-center tot equals \(S\oplus T\).

## Lemma (pal-center time residues, \(k\ge 1\))

Even \(n\): \(s\equiv 2\pmod{4}\) in \([2U+2,10U-2]\). Odd \(n\):
\(s\equiv 0\pmod{4}\) in \([2U,10U-4]\). Status: **lemma**.

## Verdict

`LEMMA` (pal-center packed AND \(= c_{s+1}\land x(s+1,1)\);
pal-center \(p=s+2\); pal-centers never forced for \(k\ge 3\);
time residues for \(k\ge 1\)).
`CERTIFIED` (pal-center-only covering walk through \(k\le 10\);
\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (pal-center tot equals \(S\oplus T\); pal-center AND
identically \(0\); pal-center AND equals \(c_{s+1}\) alone;
cellwise 2-fold packed AND).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_st.md` (this note)
- `research/cycle_st.py`
- `research/cycle_st.json`
