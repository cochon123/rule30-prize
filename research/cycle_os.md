# Cycle OS: even-parent clip-removed pal-right \(S\) is the \(R_2\) tail of \(p\)

Cycle OP gives \(S(2m+1)=R_2(p)\) for even \(m=2p\). The even-first
clause of \(G\) is \(G(2p,2e)=G(p,e)\) with odd offsets zero, so
pal-right bits of \(m\) are pal-right bits of \(p\) stretched by two.
Clip-removed pal-right \(S\) of \(n=2m+1\) counts parent \(01\)-flips
at even offsets \(r\equiv 4\pmod{6}\) with \(j=2k>j_{\max}\), and
parent \(11\)-flips cannot fire on even \(m\). Those \(01\)-flips are
exactly \(G(p,p+d)\) for \(d\equiv 2\pmod{3}\) and
\(2(p+d)>j_{\max}/2\).

On covering \(q=10\), \(j_{\max}=5U\), so even-parent \(n=4p+1\) in
the clip window has \(d_{\min}=5U/4-p+1\). This is **not** the
odd-parent clip-removed xor (\(n=51\), \(j_{\max}=80\): rem \(=1\),
the same tail on \(\lfloor(n-1)/4\rfloor\) is \(0\)). **Not**
covering \(S\) for all \(k\). **Not** \(E_k=0\) for all \(k\). Do
**not** catalogue further \(S\)/\(T\) subregions unless the
experiment answers why \(E_k=0\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\). Do **not** walk \(k=11\) covering packed. Do
**not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).

Certify: `python3 research/cycle_os.py --certify`.
Dump: `research/cycle_os.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/OP/OQ/OR/OG (\(G(2p,2e)=G(p,e)\); even-parent \(R_2\)
tail; prefix OR unclipped covering window, OP \(S=R_2(p)\), OQ
popcount \(S\), OG \(E_k\); no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (\(G(2p,2e)=G(p,e)\))

Even first argument of \(G\) halves the second; odd second argument
vanishes. Status: **lemma** for every \(p,e\ge 0\). Checked on
\(p<40\).

## Lemma (even-parent clip-removed \(S\) is the \(R_2\) tail)

For every even \(m=2p\) and every \(j_{\max}\), the clip-removed
pal-right \(S\)-xor of \(n=2m+1\) equals \(R_2(p)\) restricted to
\(d\ge d_{\min}\), where \(d_{\min}\) is the first offset with
\(2(p+d)>j_{\max}/2\) (or \(1\) if the tail is the whole row).
Status: **lemma**. Checked on \(p<40\) and several \(j_{\max}\),
and on covering \(q=10\) even-parent \(n\) for \(k\le 8\).

## Killed

Odd-parent clip-removed equals the same \(R_2\) tail:
\(n=51\), \(j_{\max}=80\) has rem \(=1\) and tail \(=0\). Covering
even-parent rem is the full \(R_2(p)\): the first clip-window
even-parent at \(k=6\) has an empty tail.

## Verdict

`LEMMA` (\(G(2p,2e)=G(p,e)\); even-parent clip-removed \(R_2\) tail;
\(P(2^k)\); unclipped covering-window \(S\); clip-window unclipped
xor \(0\); unclipped pal-right \(S\)).
`CERTIFIED` (covering even-parent rem on \(q=10\), \(k\le 8\);
\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (odd-parent rem is the \(R_2\) tail; covering even-parent
rem is full \(R_2\)).
`PREFIX` (covering \(S\) for all \(k\); \(E_k=0\) for all \(k\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_os.md` (this note)
- `research/cycle_os.py`
- `research/cycle_os.json`
