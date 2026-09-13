# Cycle MA: covering \(J\) form holds at \(k=7\), killed at \(k=8\) \(q=10\)

On covering \(J_6,J_{10}\), Cycle LZ's \(\mathrm{want}_J\) holds at
\(k=7\) (both \(q\)) and at \(k=8\), \(q=6\), but dies at
\(k=8\), \(q=10\): odd-\(s\) \(J=0\) while \(\mathrm{want}_J=1\)
because rest \(=1\) while \(\mathrm{want}_{\mathrm{rest}}=0\)
(\(8\not\equiv 2\pmod{4}\)). \(\mathrm{want}_{\mathrm{forced}}\)
still holds at \(k=8\). This is **not** the form for all \(k\),
**not** the rest formula for all \(k\), **not** a fail at \(k=7\),
and **not** \(\mathrm{want}_{\mathrm{forced}}\) dying at \(k=8\).
Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all
\(k\). Do **not** push the even-spine scan past \(k=18\). Do
**not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: covering never-fail stays open. Do **not**
guess a replacement rest formula for all \(k\) without a new
probe.

Certify: `python3 research/cycle_ma.py --certify`.
Dump: `research/cycle_ma.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/LZ (k=7 and k=8 covering walks; prefix LZ for \(k\le 6\);
no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (LZ form holds at \(k=7\))

Both covering \(q\). Rest is \(0\); \(\{4,6,14\}\) XOR matches
\(\mathrm{want}_{\mathrm{forced}}\); \(J=\mathrm{want}_J\).

## Lemma (\(\mathrm{want}_{\mathrm{forced}}\) still holds at \(k=8\))

Both covering \(q\) have forced XOR \(1\). Only rest breaks.

## Killed

Form for all \(k\): \(k=8\), \(q=10\) has \(J=0\neq 1\). Rest
formula for all \(k\): rest \(=1\), \(\mathrm{want}_{\mathrm{rest}}=0\).
Form fails at \(k=7\): it holds. \(\mathrm{want}_{\mathrm{forced}}\)
dies at \(k=8\): it holds. Covering fail is not both-zero at
\(k=8\) (\(J_6=1\), \(J_{10}=0\)).

## Verdict

`LEMMA` (LZ form holds at \(k=7\); \(\mathrm{want}_{\mathrm{forced}}\)
at \(k=8\); \(J\) closed form on \(k\le 6\); rest XOR is
\(1_{q=10,\,k\equiv 2\pmod{4}}\) on \(k\le 6\); \(G=1\) at
\(p=14\) has AND except two \(t=0\) cells; only \(p=4\) and
\(p=6\) are silent-free; \(1001\) AND xor remainder).
`KILLED` (form for all \(k\); rest formula for all \(k\); form
fails at \(k=7\); \(\mathrm{want}_{\mathrm{forced}}\) dies at
\(k=8\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ma.md` (this note)
- `research/cycle_ma.py`
- `research/cycle_ma.json`
