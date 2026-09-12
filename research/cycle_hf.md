# Cycle HF: \(J_6\) is the in-support \(j\)-index on \([2U,6U)\) with \(Q=2\)

Cycle HC’s j6slice \([4U,6U)\) is only the \(n\in[0,U)\) half of
\(J_6\). The full remainder uses \(T=6U\), \(t_0=2U\), \(Q=2\): Green
is GX/GY from \(n=2U-t-1\), left-clipped for \(s<3U-1\) (packed
\(p\ge 0\)), and the \(G\cdot\mathrm{AND}\) XOR equals FR \(J_6\).
The slice XOR is **not** \(J_6\) (\(k=3\): \(1\) vs \(0\)). Width is
**not** the unclipped \(2m+1\) on the whole window. AND at \(p=T\)
XOR is **not** \(J_6\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: putting \(J_6\) in the \(j\)-index does not give
a closed form for packed AND, so covering never-fail stays open.

Helper: `J6_WINDOW` / `WINDOWS` / `odd_clock` from Cycles HF/HC/GU.
Certify: `python3 research/cycle_hf.py --certify` (~0.05s). Dump:
`research/cycle_hf.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FR/GU/HC/HE (packed \(k\le 6\);
algebra \(k\le 12\); no Fermat table, no extra window, no \(n_0=16\)
window).

## Lemma (\(J_6=\) in-support \(j\)-index, \(Q=2\); pre \(\oplus\) j6slice \(=J_6\))

Certified \(k\le 6\). Dual of Cycle HC’s tail / mid10, now on the
missing \([2U,6U)\) window. Odd \(s\) enumerates \(n\in[0,2U)\).

## Lemma (left clip \(s<3U-1\); first unclipped \(s=3U-1\) has \(\mathrm{lo}=0\))

Certified \(k\le 12\). Clip length \(U-1\). After that, \(T-\mathrm{lo}=2m\).

## Killed

j6slice XOR \(=J_6\): at \(k=3\), \(1\neq 0\). Unclipped full Green
on the whole \(J_6\) window: at \(k=2\), \(s=t_0\), width \(25\neq 31\).
AND at \(p=T\) XOR \(=J_6\): at \(k=3\), \(1\neq 0\).

## Verdict

`LEMMA` (\(J_6=\) in-support \(j\)-index \(Q=2\); left clip
\(s<3U-1\); odd-\(s\) \(n\in[0,2U)\); pre \(\oplus\) j6slice \(=J_6\)).
`KILLED` (j6slice \(=J_6\); unclipped full Green; AND at \(p=T\)
\(=\ J_6\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_hf.md` (this note)
- `research/cycle_hf.py`
- `research/cycle_hf.json`
