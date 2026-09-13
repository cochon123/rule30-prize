# Cycle MB: covering rest through \(k\le 9\) is a rest8 form

On covering \(J_6,J_{10}\), packed AND xor off
\(\{p=4,p=6,p=14\}\) is \(1\) iff \(q=10\) and
(\(k\equiv 2\pmod{4}\) or (\(k>0\) and \(k\equiv 0\pmod{8}\)))
for \(k\le 9\). That fits Cycle MA's \(k=8\), \(q=10\) kill
(\(8\equiv 0\pmod{8}\)) and restores
\(J=\mathrm{want}_{\mathrm{forced}}\oplus\mathrm{rest}_8\) at
\(k=9\). This is **not** rest \(=1\) once \(k\ge 8\) (\(k=9\),
\(q=10\) is \(0\)), **not** the form dead for all \(k\ge 8\),
**not** rest8 for all \(k\), and **not**
\(\mathrm{want}_{\mathrm{forced}}\) dying at \(k=9\). Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do
**not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: covering never-fail stays open. Do **not**
claim rest8 for all \(k\) without a new probe.

Certify: `python3 research/cycle_mb.py --certify` (~6.49s).
Dump: `research/cycle_mb.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/LZ (k=9 covering walks; prefix LZ for \(k\le 6\) and MA
for \(k=7,8\); no Fermat table, no extra window, no \(n_0=16\)
window).

## Lemma (rest8 XOR on \(k\le 9\))

AND xor off \(\{4,6,14\}\) is \(1\) iff \(q=10\) and
(\(k\equiv 2\pmod{4}\) or (\(k>0\) and \(k\equiv 0\pmod{8}\))).
Equals Cycle LZ's rest formula on \(k\le 7\); at \(k=8\),
\(q=10\) it is \(1\) while LZ rest is \(0\).

## Lemma (LZ form with rest8 holds at \(k=9\))

Both covering \(q\) have rest \(=0\) and
\(J=\mathrm{want}_{\mathrm{forced}}=1\).

## Lemma (\(\mathrm{want}_{\mathrm{forced}}\) still holds at \(k=9\))

Both covering \(q\). Forced XOR is \(1\).

## Killed

Rest \(=1\) once \(k\ge 8\): \(k=9\), \(q=10\) has rest \(=0\).
Form dead for all \(k\ge 8\): \(k=9\) both \(q\) match
\(\mathrm{want}_{J8}\). Rest8 fails at \(k=9\): it holds.
\(\mathrm{want}_{\mathrm{forced}}\) dies at \(k=9\): it holds.

## Verdict

`LEMMA` (rest8 on \(k\le 9\); LZ form with rest8 at \(k=9\);
\(\mathrm{want}_{\mathrm{forced}}\) at \(k=9\); LZ form holds at
\(k=7\); \(\mathrm{want}_{\mathrm{forced}}\) at \(k=8\); \(J\)
closed form on \(k\le 6\); rest XOR is
\(1_{q=10,\,k\equiv 2\pmod{4}}\) on \(k\le 6\)).
`KILLED` (rest \(=1\) once \(k\ge 8\); form dead for all
\(k\ge 8\); rest8 fails at \(k=9\);
\(\mathrm{want}_{\mathrm{forced}}\) dies at \(k=9\); LZ form for
all \(k\); LZ rest for all \(k\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_mb.md` (this note)
- `research/cycle_mb.py`
- `research/cycle_mb.json`
