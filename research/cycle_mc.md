# Cycle MC: rest8 dies at \(k=10\), \(q=10\)

On covering \(J_6,J_{10}\), Cycle MB's rest8 holds at \(k=10\),
\(q=6\) but dies at \(k=10\), \(q=10\): rest \(=0\) while
\(\mathrm{want}_{\mathrm{rest}8}=1\) (\(10\equiv 2\pmod{4}\)), so
odd-\(s\) \(J=1\) while \(\mathrm{want}_{J8}=0\).
\(\mathrm{want}_{\mathrm{forced}}\) still holds at \(k=10\). This
is **not** rest8 for all \(k\), **not** \(\mathrm{want}_{J8}\) for
all \(k\), **not** a fail at \(k=10\), \(q=6\), and **not**
\(\mathrm{want}_{\mathrm{forced}}\) dying at \(k=10\). Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do
**not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: covering never-fail stays open. Do **not**
guess a replacement rest formula for all \(k\) without a new
probe. The \(k\equiv 2\pmod{4}\) rest pattern itself fails at
\(k=10\), \(q=10\).

Certify: `python3 research/cycle_mc.py --certify` (~31.36s).
Dump: `research/cycle_mc.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/LZ/MB (k=10 covering walks; prefix MB for \(k\le 9\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (\(q=6\) rest is \(0\) at \(k=10\))

AND xor off \(\{4,6,14\}\) is \(0\); \(J=\mathrm{want}_{J8}=1\).

## Lemma (\(\mathrm{want}_{\mathrm{forced}}\) still holds at \(k=10\))

Both covering \(q\) have forced XOR \(1\). Only rest breaks, and
only on \(q=10\).

## Lemma (rest8 on \(k\le 9\))

Cycle MB.

## Killed

Rest8 for all \(k\): \(k=10\), \(q=10\) has rest \(=0\neq 1\).
\(\mathrm{want}_{J8}\) for all \(k\): \(J=1\neq 0\). Rest8 fails
at \(k=10\), \(q=6\): it holds. \(\mathrm{want}_{\mathrm{forced}}\)
dies at \(k=10\): it holds.

## Verdict

`LEMMA` (\(q=6\) rest \(=0\) at \(k=10\);
\(\mathrm{want}_{\mathrm{forced}}\) at \(k=10\); rest8 on
\(k\le 9\); LZ form with rest8 at \(k=9\);
\(\mathrm{want}_{\mathrm{forced}}\) at \(k=8,9\); \(J\) closed
form on \(k\le 6\)).
`KILLED` (rest8 for all \(k\); \(\mathrm{want}_{J8}\) for all
\(k\); rest8 fails at \(k=10\), \(q=6\);
\(\mathrm{want}_{\mathrm{forced}}\) dies at \(k=10\); rest \(=1\)
once \(k\ge 8\); form dead for all \(k\ge 8\); LZ form for all
\(k\); LZ rest for all \(k\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_mc.md` (this note)
- `research/cycle_mc.py`
- `research/cycle_mc.json`
