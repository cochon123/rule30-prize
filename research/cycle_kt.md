# Cycle KT: clipped \(G=1\) of family clippers is the palindrome dual of \(f\bmod 3\)

Covering \(k\le 6\): on each no-\(00\) family clipper, the clipped
\(G=1\) columns are \(j=2n-d\) for \(d\) in a low prefix with
\(d\not\equiv 2\pmod{3}\) (\(q=6\) max Mersenne and \(q=10\)
\(3U-1\): \(d<U-2\); \(q=10\) max Mersenne: \(d<3U-2\)). This is
**not** every \(j>T/2\), **not** a suffix of the row, **not** the
\(q=6\) dual \(4U-2\) on \(q=10\) max Mersenne, and **not** a single
residue mod \(3\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: this is the column set behind Cycle KS's clip
counts, not packed AND XOR \(J\), so covering never-fail stays open.

Certify: `python3 research/cycle_kt.py --certify`.
Dump: `research/cycle_kt.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/AN/CA/HG/KH/KR/KS (covering \(k\le 6\); no Fermat table, no extra
window, no \(n_0=16\) window).

## Lemma (family clip columns)

Certified \(k\le 6\) (17 clipper clocks). Palindrome plus Cycle AN/KO
low-band \(f(d)\). Covering \(J_6,J_{10}\) still have \(G=1\) columns
\(22659\); odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Lemma (family clip counts)

Cycle KS. \(\operatorname{jacobsthal}(k+1)-1\) on \(q=6\) max
Mersenne and \(q=10\) \(3\cdot 2^k-1\); \(2^{k+1}-1\) on \(q=10\)
max Mersenne.

## Killed

Every \(j>T/2\) on a clipper is \(G=1\): \(k=3\), \(q=6\), \(n=15\)
has zeros at \(25,28\). Clipped ones are a suffix: \(k=2\), \(q=10\),
\(n=15\) last 7 is \(24..30\). \(q=10\) max Mersenne uses the \(q=6\)
dual: \(k=2\), \(n=15\) would be \(13,14\). Single residue mod \(3\):
\(k=2\), \(q=6\) is \(13,14\).

## Verdict

`LEMMA` (family clip columns; family clip counts; family clippers).
`KILLED` (all high; suffix; \(q=10\) uses \(q=6\) dual; one residue).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_kt.md` (this note)
- `research/cycle_kt.py`
- `research/cycle_kt.json`
