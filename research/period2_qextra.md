# Period-2 \(L_0\): clip index to sound \(R\), and \(T=37\) attains \(17\)

Checked lemma: a ugap onset prefix of length `nvars(T)` has a unique
attempted \(L_0\) tail \(u_n=Q_n\) until a `11`-clip, `00000`-clip, or
even \(F_{2n}>T\). The clip index \(n\) is a sound extra-zero count,
\[
R=2n-T\quad(11/00000),\qquad R=2n-1-T\quad(\text{even }F),
\]
so extra \(\le E\) implies \(R\le 2E+1\). Through \(T=40\) every ugap
onset prefix has extra \(\le 8\), hence \(R\le 17\), and \(T=37\)
attains \(17\) (three bump words, 11-clip at \(n=27\)). \(T=20\),
\(R=16\) is no longer uniquely worst. Not a prize claim: extra \(\le 8\)
is not proved for all \(T\).

Helper: `python3 research/period2_qextra.py --certify`. Dump:
`research/period2_qextra.json`. Uses `force_from` from
`research/period2_qshift.md` and ugap strings from
`research/period2_ugap_sat.md`. Vacuum padding of a short prefix is
*not* used for \(R\).

## Lemma (sound \(R\) from a clip)

Let \(u_0,\ldots,u_{n_0-1}\) be ugap with \(n_0=\mathrm{nvars}(T)\) and
\(F_T=1\). For \(n\ge n_0\), \(F_{2n}\) does not contain \(u_n\)
(`research/period2_lead.md`), and \(F_{2n+1}=u_n\oplus Q_n\). The
unique bit that keeps \(F_{2n+1}=0\) is \(u_n=Q_n\). This bit is
illegal in ugap precisely on a `11`-clip (\(Q_n=1\) and \(u_{n-1}=1\))
or a `00000`-clip (\(Q_n=0\) and four trailing zeros). An even fire
\(F_{2n}=1\) with \(2n>T\) is decided by the prefix of length \(n\)
alone.

If the first obstruction is even \(F\) at index \(n\), then
\(F_{T+1}=\cdots=F_{2n-1}=0\) and \(F_{2n}=1\), so \(R=2n-1-T\). If it
is a ugap clip at \(n\), then even \(F_{2n}\) did not fire, hence
\(F_{2n}=0\), and no ugap value of \(u_n\) makes \(F_{2n+1}=0\), so
\(R=2n-T\).

## Corollary (extra cap)

Write extra \(e=n-n_0\). Then \(n_0=\lfloor(T-1)/2\rfloor+1\), and a
`11`-clip (the larger case) gives \(R=2e+1\) for odd \(T\) and
\(R=2e\) for even \(T\). In particular extra \(\le 8\) implies
\(R\le 17\). Combined with compactness in the ugap SFT, a uniform
extra \(\le 8\) would exclude every \(L_0\) onset, hence every period-2
centre. That uniform extra is **not** proved.

## Census through \(T=40\)

Every ugap word of length `nvars(T)` with \(F_T=1\) Q-clips with extra
\(\le 8\). Global \(\max R=17\), uniquely at \(T=37\):

| \(T\) | max \(R\) | extra | stop | kind | \(n\) |
| ---: | ---: | ---: | --- | --- | ---: |
| 20 | 16 | 8 | `11` | bump | 3 |
| 22 | 12 | 6 | `11` | bump | 5 |
| 33 | 14 | 7 | even \(F\) | iso | 3 |
| 35 | 14 | 7 | even \(F\) | iso | 6 |
| 37 | 17 | 8 | `11` | bump | 3 |
| 38 | 13 | 7 | even \(F\) | iso | 4 |
| 40 | 13 | 7 | even \(F\) | iso | 19 |

The three \(T=37\) last-sat words, length 27, share the tail
`01010101010100100100101` and 11-clip at \(n=27\). Each has
\(F_{37}=1\), \(F_{36}=1\), then 17 zeros. The clip lemma makes
\(R=18\) unsat without a further SAT.

A probe through \(T=48\) still has extra \(\le 8\) and \(\max R=17\)
only at \(T=37\); \(T=43,44,47\) hit \(R=16\). That probe is not in
the certificate.

## What this does not do

Extra \(\le 8\) at large \(T\) would finish period 2 of the prize
centre (every even-right \(u\) is ugap). The census through \(T=40\)
is not that bound, and \(T=37\) shows the implied \(R\le 17\) is sharp.
Other periods of \(c_t\) are untouched.

Periodic \(u\) is already infinite on the left
(`research/period2_periodic.md`). Aperiodic \(u\) remains the
obstruction to period 2 only if extra is unbounded; if extra is
bounded, aperiodic \(u\) dies too.

## Verdict

`LEMMA`, wall time ~8s.

- Kill of period 2: no.
- Sound \(R\) from Q-clip: yes.
- Extra \(\le 8\Rightarrow R\le 17\): yes.
- Uniform extra \(\le 8\): no; \(T=37\) attains the cap \(R=17\).

## Files

- `research/period2_qextra.md` (this note)
- `research/period2_qextra.py` (`--certify`)
- `research/period2_qextra.json` (dump)
