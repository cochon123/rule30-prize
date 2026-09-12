# Cycle GQ: hit endpoints are Green ones; \(k\le 3\) AND extras are only lo

\(\mathrm{mer\_one}(0)=\mathrm{mer\_one}(U-1)=1\) for every \(k\). Packed
AND at cone-hi \(j=U-1\) is live on all Cycle GG hits (\(k\le 6\)).
For \(k\le 3\) the only possible extra AND among \(\mathrm{mer\_one}\)
columns is \(j=0\). AND at lo is **not** always live; extras are
**not** only lo at \(k=4\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: endpoint Green-ones plus a \(k\le 3\) extra-AND
restriction do not prove covering never-fail (AND still mixes at
\(k\ge 4\); the cone-hi XOR is not \(J\)).

Helper: `python3 research/cycle_gq.py --certify` (~0.01s). Dump:
`research/cycle_gq.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles CA/GG/GN/GP (Mersenne endpoints \(k\le 16\);
packed \(k\le 6\); no Fermat table, no extra window, no \(n_0=16\)
window).

## Lemma (endpoints \(j=0,U-1\) are Green ones)

Certified \(k\le 16\). So both cone edges at a hit have \(G=1\).

## Lemma (AND at \(j=U-1\) live; \(k\le 3\) extras \(\subseteq\{0\}\))

Packed \(k\le 6\), all covering \(W\). For \(k\le 3\) the live
\(\mathrm{mer\_one}\) AND set is \(\{U-1\}\) or \(\{0,U-1\}\).

## Killed

\(\mathrm{mer\_one}(0)=0\): it is 1. AND at lo always live: at
\(k=1\), \(W=4U\), dead. Extras only lo at \(k=4\): \(W=8U\), \(q=0\),
\(\{6,7\}\).

## Verdict

`LEMMA` (endpoints Green; cone-hi AND live; \(k\le 3\) extras only lo).
`KILLED` (\(\mathrm{mer\_one}(0)=0\); lo AND always; extras only lo at
\(k=4\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_gq.md` (this note)
- `research/cycle_gq.py`
- `research/cycle_gq.json`
