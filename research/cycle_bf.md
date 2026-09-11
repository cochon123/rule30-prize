# Cycle BF: Fermat \(p=1\) times; Mersenne centre-right unique bits

Cycle AR lifts \(G\bigl(m,(2^a+1)2^k-1\bigr)\) to \(G(s,2^a)\). On the
\(q\)-fold annulus that lift is a complete list of leftmost-11 times
for every Fermat-odd spine \(\varphi^{(q)}_k\), including the covering
triple \(q=3,5,9\). The Mersenne-target law makes two centre-right
ANDs unique-Green on every such annulus. Extra unique bits take both
firing values (or vanish on the scanned prefix), so they are not
identically-1 productions. Doubling relates \(\varphi^{(q)}_{k+1}\) to
the even spine \(\varphi^{(2q)}_k\). Not a prize claim: the Fermat
covering remains a prefix, and some \(\varphi^{(q)}_k=1\) infinitely
often is unproved.

Helper: `python3 research/cycle_bf.py --certify` (~0.06s). Dump:
`research/cycle_bf.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (Fermat leftmost-11 times)

Let \(q=2^a+1\), \(U=2^k\), and \(a\ge 1\). Packed bit 1 Green-hits
the target \(qU\) on \([U,qU)\) iff \(t=\lambda U\) with
\(G(2^a-\lambda,2^a)=1\). Equivalently
\(t=(2^a-s)U\) for those \(s\in[2^{a-1},2^a)\) with \(G(s,2^a)=1\).

Proof. Cycle AR: \(G\bigl(m,(2^a+1)2^k-1\bigr)=1\) iff \(2^k\mid(m+1)\)
and \(G\bigl((m+1)/2^k-1,\,2^a\bigr)=1\). Here \(m=qU-t-1\), so
\(2^k\mid(m+1)\) iff \(U\mid t\), i.e. \(t=\lambda U\) with
\(\lambda\in\{1,\ldots,2^a\}\). Then \(s=2^a-\lambda\), and
\(G(s,2^a)=0\) automatically for \(s<2^{a-1}\). Cycle AQ evaluates
\(G(\,\cdot\,,2^a)\) on that finite window. Certified against a direct
Green scan for \(1\le a\le 4\) and \(1\le k\le 8\).

In particular the covering spines have

| \(q\) | \(a\) | \(N(q)\) | times |
|------:|------:|:--------:|:------|
| 3 | 1 | 1 | \(U\) |
| 5 | 2 | 1 | \(2U\) |
| 9 | 3 | 3 | \(U,\,3U,\,4U\) |
| 17 | 4 | 5 | \(2U,\,5U,\,6U,\,7U,\,8U\) |

Cycle AO already had the \(q=3,5\) times and the counts \(N(q)\). The
\(q=9\) times are new as an explicit list. XOR of the three \(q=9\)
hits is 1, recovering \(P(9)=1\).

## Lemma (Mersenne centre-right unique bits)

Let \(q=2^a+1\) and \(k\ge 1\). Write \(\alpha_k:=c_U\land r_U\).

1. Packed bit \(p=U+1\) has Mersenne target \(2^{k+a}-1\). Cycle AP:
   \(G(m,2^{k+a}-1)=1\) iff \(2^{k+a}\mid(m+1)\). On the \(q\)-fold
   annulus \(m+1\le 2^{k+a}\), so the only candidate is \(m+1=2^{k+a}\),
   i.e. time \(t=U\). The cone \(p\le 2t\) holds. Hence \(p=U+1\) is
   unique-Green at \(t=U\) and fires iff \(\alpha_k=1\).
2. Packed bit \(p=(2^{a-1}+1)U+1\) has Mersenne target \(2^{k+a-1}-1\).
   The two candidates are \(t=(2^{a-1}+1)U\) and \(t=U\); the latter
   fails the cone because \(p\ge 2U+1\). The survivor is the
   centre-right AND at time \((2^{a-1}+1)U\).

So every Fermat-odd spine has a unique contribution of \(\alpha_k\)
in \(S^{(q)}\), and a second unique centre-right AND at time
\((2^{a-1}+1)U\). For the covering triple that second bit is
\(p=2U+1\) on the 3-fold annulus (Cycle AP), \(p=3U+1\) on the 5-fold
(fires iff \(c_{3U}\land r_{3U}\)), and \(p=5U+1\) on the 9-fold
(fires iff \(c_{5U}\land r_{5U}\)). Certified: Green-count 1 with
those times for \(q\in\{3,5,9\}\) and \(3\le k\le 7\).

## Lemma (doubling)

For every integer \(q\ge 1\) and \(k\ge 0\),

\[
\varphi^{(q)}_{k+1}
=\varphi^{(2q)}_k\oplus I_{k+1}.
\]

Both sides equal \(c_{q\cdot 2^{k+1}}\oplus c_{2^{k+1}}\). Certified
for \(q=1,\ldots,12\) and \(k\le 8\). In particular a covering
failure at \(k+1\) forces
\(\varphi^{(6)}_k=\varphi^{(10)}_k=\varphi^{(18)}_k=I_{k+1}\).

## Prefix (exactly three / two unique-Green bits)

On \(3\le k\le 7\) the unique-Green packed bits are exactly

- 5-fold: \(\{1,\,U+1,\,3U+1\}\);
- 9-fold: \(\{U+1,\,5U+1\}\), with packed bit 1 triple at
  \(t=U,3U,4U\).

Exhaustiveness is a prefix, not a theorem for all \(k\). The \(r=1\)
Mersenne analysis above already produces those bits for every \(k\).

## Extra unique bits — killed as forced 1s

\(\alpha_k\) takes both values on \(3\le k\le 7\). So does
\(c_{3U}\land r_{3U}\). The bit \(p=5U+1\) is 0 on that range (and on
an extra check through \(k=12\)); that vanishing is a prefix, not a
theorem. None of these unique bits is an identically-1 production for
a Fermat spine. **Killed.** The covering still has no closed form that
forces a 1.

The common unique term \(\alpha_k\) does couple the three remainders:
writing \(\varphi^{(q)}=1\oplus\alpha_k\oplus S^{(q)}_{\mathrm{rest}}\)
for each covering \(q\), a covering failure is equivalent to
\(S^{(3)}_{\mathrm{rest}}=S^{(5)}_{\mathrm{rest}}=S^{(9)}_{\mathrm{rest}}=1\oplus\alpha_k\).
That rest still includes even-multiplicity hits, and is not controlled.

## Verdict

`LEMMA` (Fermat \(p=1\) times; Mersenne centre-right unique bits on
every Fermat-odd annulus; doubling \(\varphi^{(q)}_{k+1}=\varphi^{(2q)}_k\oplus I_{k+1}\)).
`PREFIX` (exactly those unique-Green bits on the 5-fold and 9-fold;
\(p=5U+1\) never fires).
`KILLED` (extra unique bits as identically-1 productions).
`OPEN` (Fermat covering for all \(k\ge 2\); some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_bf.md` (this note)
- `research/cycle_bf.py`
- `research/cycle_bf.json`
