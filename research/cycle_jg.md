# Cycle JG: on \(n\equiv 2\pmod{4}\), `iso_half3` is the core-slot end formula

For \(n=2m\) with \(m\) odd, the isolated-one 3-window is \(001\) at
core-slot offset \(0\), \(100\) at offset \(2r\), and \(010\) on
every interior offset. There is no \(111\) on \(n\equiv 2\pmod{4}\).
Offset \(0\) is **not** \(010\). Offset \(2r\) is **not** \(001\).
\(n\equiv 0\pmod{4}\) interiors are **not** all \(010\) (\(G(4,4)\)
is \(111\)). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\)
for all \(k\). Do **not** push the even-spine scan past \(k=18\).
Do **not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: the slot-end 3-window still leaves packed AND on
those columns (and on pairs), so covering never-fail stays open.

Helper: `iso3_from_slot`. Certify:
`python3 research/cycle_jg.py --certify` (~0.15s).
Dump: `research/cycle_jg.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IR/IT/JF (\(n<64\); covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (`iso_half3` is `iso3_from_slot` on \(n\equiv 2\pmod{4}\))

For \(n<64\), every isolated one with \(n\equiv 2\pmod{4}\) has
`iso_half3==iso3_from_slot`. Census \(n_{\mathrm{iso}}=461\): seed
\(1\), odd \(45\), \(n\equiv 2\) \(288\) split \(001\) \(80\),
\(010\) \(128\), \(100\) \(80\), \(111\) \(0\); \(n\equiv 0\)
\(127\) of which \(111\) is \(44\).

## Lemma (no \(111\) on \(n\equiv 2\pmod{4}\))

All even-\(n\) \(111\) 3-windows in Cycle JF sit on
\(n\equiv 0\pmod{4}\).

## Lemma (covering slot-end 3-windows)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): isolated ones
\(7785\) (seed \(14\), odd \(741\), \(n\equiv 2\) \(4846\),
\(n\equiv 0\) \(2184\)). On \(n\equiv 2\): \(001\) \(1376\),
\(010\) \(2146\), \(100\) \(1324\), \(111\) \(0\). On
\(n\equiv 0\): \(111\) \(734\). Clipped ends need not match.
Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

Offset \(0\) is \(010\): at \(k=0\), \(s=5\), \(n=2\), \(j=0\),
slot \((0,1,0)\), three \(001\), \(p=10\). Offset \(2r\) is
\(001\): at \(k=1\), \(s=7\), \(n=2\), \(j=4\), slot \((0,1,2)\),
three \(100\), \(p=4\). \(n\equiv 0\) interiors are \(010\): at
\(k=1\), \(s=11\), \(n=4\), \(j=4\), slot \((0,1,1)\), three
\(111\), \(p=12\).

## Verdict

`LEMMA` (`iso_half3` is `iso3_from_slot` on \(n\equiv 2\pmod{4}\);
no \(111\) on \(n\equiv 2\pmod{4}\); covering slot-end 3-windows).
`KILLED` (offset \(0\) is \(010\); offset \(2r\) is \(001\);
\(n\equiv 0\) interiors are \(010\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_jg.md` (this note)
- `research/cycle_jg.py`
- `research/cycle_jg.json`
