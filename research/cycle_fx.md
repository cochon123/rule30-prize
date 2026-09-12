# Cycle FX: unclipped cone-hi is 1 iff \(((-s-1)\bmod 2U)\) is a one-zero residue

On the unified \(T=2U+W\) band, \(W\in\{4U,8U,16U\}\) is \(0\bmod 2U\),
so \(m=T-s-1\equiv -s-1\pmod{2U}\). Cycle FS says the unclipped
cone-hi Green is \(G(m,2U-2)\); Cycle FW evaluates that by the
one-zero pattern at scale \(k+1\) on \(r=m\bmod 2U\). Hence \(G=1\)
iff \(\mathrm{want\_one}((-s-1)\bmod 2U,\,k+1)=1\). The hi AND does
**not** fire whenever \(G=1\), and \(G\) is **not** identically 1.
Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\).
Do **not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: a time-index criterion for the unclipped hi Green
does not prove covering never-fail.

Helper: `python3 research/cycle_fx.py --certify` (~0.01s). Dump:
`research/cycle_fx.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FQ/FS/FW (endpoint samples \(k\le 7\);
packed AND check at \(k=2\), \(W=8U\); no Fermat table, no extra
window, no \(n_0=16\) window).

## Lemma (\(W\equiv 0\pmod{2U}\))

Certified \(k\le 20\), \(W\in\{4U,8U,16U\}\).

## Lemma (unclipped hi iff one-zero residue of \(-s-1\))

Certified on endpoint samples \(k\le 7\).

## Killed

Unclipped hi identically 1: at \(k=2\), \(W=8U\), \(s=9U-1\), \(G=0\).
Hi AND whenever \(G=1\): at \(k=2\), \(W=8U\), 2 live and 5 dead.

## Verdict

`LEMMA` (\(W\equiv 0\pmod{2U}\); unclipped hi iff one-zero residue of
\(-s-1\)).
`KILLED` (hi identically 1; AND whenever \(G=1\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_fx.md` (this note)
- `research/cycle_fx.py`
- `research/cycle_fx.json`
