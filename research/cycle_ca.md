# Cycle CA: unique continuation equals \(B\) iff \(A\) is the cyclic derivative

Packed update \(U_{t+1}=A_t\oplus(B_t\lor U_t)\). If \(U=B\) then
\(A_t=B_t\oplus B_{t+1}\), the cyclic derivative \(DB\). Conversely,
\(A=DB\) with \(B\not\equiv 0\) makes \(U=B\) the unique period-\(\pi\)
continuation. A later ident-\(0\) is exactly a later consecutive pair
with \(U=B\), hence \(A=DB\). After an odd doubling
\(T=T_0\|\lnot T_0\), the scar pairs \((0,T)\), \((T,1)\),
\((1,\lnot T)\) (or a rotation of \(\lnot T\)) are not derivative
pairs when the pre-toggle period is a \(2\)-power at least \(2\).
The rest of the \(k=4\) and \(k=8\) high halves also avoid \(A=DB\)
(prefix). No linear functional of \(B\oplus U\) is constant after
the scar. Not a prize claim: the Fermat covering remains a prefix.

Helper: `python3 research/cycle_ca.py --certify` (~0.02s). Dump:
`research/cycle_ca.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (\(U=B\) iff \(A=DB\))

On a period-\(\pi\) drive with \(B\not\equiv 0\), the unique
continuation satisfies \(U=B\) if and only if \(A_t=B_t\oplus B_{t+1}\)
for every \(t\). If \(U=B\) then
\(B_{t+1}=A_t\oplus(B_t\lor B_t)=A_t\oplus B_t\). Conversely, \(A=DB\)
gives \(u'=a\oplus(b\lor u)=b\oplus Db\oplus(b\lor u)\); the string
\(u=b\) is a solution, and uniqueness of the reset continuation
forces it. Certified: \(877\) random drives at lengths \(4,8,16\)
(the two sides agree), and \(884\) constructed \(A=DB\) recover
\(U=B\).

## Lemma (later ident-\(0\) iff \(A=DB\))

Ident-\(0\) at packed bit \(q+1\) iff \(\lambda_{q-1}=\lambda_q\)
(Cycle BZ). For \(B=\lambda_{q-1}\not\equiv 0\) that equality is
\(U=B\) at bit \(q\), hence \(A=DB\). Consecutive ident-\(0\) is
already impossible, so the \(B\equiv 0\) branch does not occur.
A second odd toggle in the same lift therefore requires a later
derivative pair with odd driver XOR.

## Lemma (scar pairs are not derivatives)

After an odd doubling, \(T=T_0\|\lnot T_0\) with \(|T_0|=\pi\ge 2\) a
\(2\)-power. Then \(T\not\equiv 0\), so \(0\not=DT\). Next,
\(D(1)\equiv 0\), so \(T\not=D(1)\). Next, \(D(\lnot T)=DT\), and
\(DT\equiv 1\) iff \(T\) is alternating. A string \(T_0\|\lnot T_0\)
of even block length \(\pi\ge 2\) has a repeated bit at the junction,
so it is not alternating. Certified on random non-constant \(T_0\) of
lengths \(2,4,8,16\). (The \(\pi=1\) case \(T\in\{01,10\}\) is
alternating, but the first odd high toggle on the prize orbit has
\(\pi\ge 4\).)

## Prefix (no later derivative on \(k=4,8\))

After the scar, the remaining high-half pairs have \(A\not=DB\)
(\(k=4\): bit \(29\), \(3\) later pairs; \(k=8\): bit \(400\),
\(112\) later pairs; zero hits). **PREFIX**, not a theorem for all
\(k\). Combined with Cycle BY this keeps \(r\le 1\), the period-\(H\)
seed, and \(J_B^{\to 2U}=0\) as prefixes.

## Linear syndrome of \(B\oplus U\) — killed

Post-scar consecutive differences of reconstructed bits at \(k=8\)
span all of \(\mathbb{F}_2^{16}\) (GF(2) rank \(16\)). No nonzero
linear functional of \(B\oplus U\) is constantly \(0\) or \(1\).
**Killed** as a route to \(A\not=DB\).

## Verdict

`LEMMA` (\(U=B\) iff \(A=DB\); later ident-\(0\) iff \(A=DB\); scar
pairs are not derivatives).
`PREFIX` (no later derivative on \(k=4,8\); at most one odd toggle
for all \(k\); seed for all \(k\); Fermat covering).
`KILLED` (linear syndrome of \(B\oplus U\)).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_ca.md` (this note)
- `research/cycle_ca.py`
- `research/cycle_ca.json`
