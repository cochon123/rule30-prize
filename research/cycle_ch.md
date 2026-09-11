# Cycle CH: next scar bit is shifted-not \(T\); Hamming gap \(2\) on \(|T_0|=8\)

After ident-\(0\), \(T=T_0\|\lnot T_0\), ident-\(1\), packed update at the
identically-\(1\) bit forces the next packed bit to be the cyclic
shift-and-flip of \(T\): \(\lambda_{I+1,t}=\lnot T_{t-1}\). That sequence
equals the ident-\(1\) continuation iff \(T\) is alternating. For even
\(|T_0|\ge 2\), \(T_0\|\lnot T_0\) is never alternating (the junction
repeats), so the first tail pair is never equal. Consecutive Hamming
along the unique-continuation tail is at least \(2\) for every
nonconstant \(T_0\) of length \(8\) on \(130\) bits. Length \(4\)
reaches Hamming \(1\) at \(q=43\) on an \(80\)-bit window; the prize
\(k=4\) lift is only four high bits and stays at Hamming \(\ge 2\).
A blanket gap of \(3\) does not hold, nor is Hamming always even.
Not a prize claim: longer \(T_0\) and the Fermat covering remain
prefixes.

Helper: `python3 research/cycle_ch.py --certify` (~0.7s). Dump:
`research/cycle_ch.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (next bit is shifted-not \(T\))

Ident-\(1\) at packed bit \(I\) has driver \(T=\lambda_{I-1}\). The
update of bit \(I+1\) is
\(\lambda_{I+1,t+1}=T_t\oplus(1\lor\lambda_{I+1,t})=T_t\oplus 1\),
independent of the current bit. Hence
\(\lambda_{I+1,t}=\lnot T_{t-1}\). Exhaustive on even
\(|T_0|\in\{2,4,6,8,10,12,16\}\).

## Lemma (even \(T_0\|\lnot T_0\) is never alternating)

Let \(n_0=|T_0|\) be even and at least \(2\), and set
\(T=T_0\|\lnot T_0\). If \(T\) were alternating then the junction would
force \(T_0[0]=T_0[-1]\), while an even-length alternating block has
first \(\ne\) last. Contradiction. Exhaustive through \(n_0=16\).

## Lemma (first tail pair never equal)

Write \(S=\lambda_{I+1}\) and \(U\) the unique continuation of
\((1,S)\). Then \(S=U\) iff \(1=DS\) iff \(S\) is alternating iff \(T\)
is alternating. The previous lemma kills that for every even
\(|T_0|\ge 2\). On lengths \(4\) and \(8\) the Hamming distance is at
least \(3\).

## Lemma (\(|T_0|=8\): tail Hamming \(\ge 2\))

All \(254\) nonconstant blocks of length \(8\), \(130\) extra bits:
every consecutive pair has Hamming at least \(2\), so \(A\ne B\) and
there is no later ident-\(0\). Exhaustive. The prize \(k=8\) odd lift
has \(\pi=8\) and \(112\) post-toggle pairs, all Hamming at least
\(3\).

## Gap \(\ge 2\) on long length-\(4\) tails — killed

All \(14\) nonconstant blocks of length \(4\), \(80\) extra bits: six
of them hit Hamming \(1\), first at \(q=43\) for \(T_0=1000\).
**Killed** as a statement about long length-\(4\) windows. The prize
\(k=4\) odd lift has only three post-toggle pairs, all Hamming at
least \(3\).

## Gap \(\ge 3\), always-even Hamming — killed

Length \(8\) already has Hamming \(2\). Both lengths have odd
Hamming. **Killed.**

## Prefix (every \(2\)-power \(|T_0|\))

Hamming \(\ge 2\) (even Hamming \(\ge 1\)) is not proved for
\(|T_0|\ge 16\) on a window as long as the next high half. **PREFIX**.
Combined with Cycle BY this keeps \(r\le 1\) and the period-\(H\) seed
as prefixes for all \(k\).

## Verdict

`LEMMA` (next bit is shifted-not \(T\); even \(T_0\|\lnot T_0\) never
alternating; first tail pair never equal; Hamming \(\ge 3\) on that
pair for \(|T_0|\in\{4,8\}\); Hamming \(\ge 2\) on the length-\(8\)
tail).
`PREFIX` (every \(2\)-power \(|T_0|\); at most one odd toggle for
all \(k\); seed for all \(k\); Fermat covering).
`KILLED` (Hamming \(\ge 2\) on long length-\(4\) tails; Hamming
\(\ge 3\) on the whole tail; Hamming always even).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_ch.md` (this note)
- `research/cycle_ch.py`
- `research/cycle_ch.json`
