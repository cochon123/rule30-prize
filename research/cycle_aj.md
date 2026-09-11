# Cycle AJ: \(\theta_k=c_{3\cdot 2^k}\oplus c_{2^k}\); leftmost 11 hits

Cycle AI’s dyadic step from time \(2^k\) by \(2^{k+1}\) has both
spatial extras outside the light cone. The 3-spine and the 1-spine
therefore differ by a Green remainder on the 3-fold interval
\([2^k,3\cdot 2^k)\). Eventual period \(2^m\) forces that difference
to vanish. The leftmost 11, which never hits \(I_k\) (Cycle AA),
always hits \(\theta_k\). Not a prize claim: \(\theta_k=1\)
infinitely often is unproved, and periods with an odd factor remain.

Helper: `python3 research/cycle_aj.py --certify`. Dump:
`research/cycle_aj.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (\(\theta_k\) is a 3-fold remainder)

Let \(U=2^k\) and \(\theta_k:=c_{3U}\oplus c_U\). Cycle AI with
\(t=U\) and step \(2U\) gives extras \(x(U,\pm 2U)=0\), so

\[
c_{3U}=c_U\oplus J^{(3)}_k,
\qquad
\theta_k=J^{(3)}_k,
\]

where \(J^{(3)}_k\) is the Green parity of AND injections on
\([U,3U)\) that hit packed bit \(3U\). Certified against packed
Rule 30 for \(k\le 8\).

As in Cycle AA, \(G(m,m)=1\), so every centre-right AND on that
interval hits: if \(p=s+1\) then \(3U-p=3U-s-1=m\). The coboundary
of Cycle AB on the same interval is

\[
\theta_k
=\bigoplus_{s=U}^{3U-1}(c_s\oplus c_{s+1})
=\bigoplus_{s=U}^{3U-1}\bigl(d_s\oplus(c_s\land r_s)\bigr).
\]

Certified: Green \(J\), centre-right hit count, and coboundary match
for \(k\le 8\).

## Lemma (period \(2^m\) forces \(\theta_k=0\))

If \(c\) is eventually period \(2^m\) with onset \(T\), then for
\(k\ge\max(m,\min\{j:2^j\ge T\})\) both \(U\) and \(3U\) are
multiples of \(2^m\) and at least \(T\), hence
\(c_U=c_{3U}\) and \(\theta_k=0\). In particular the 3-spine and the
1-spine eventually agree (both equal to the periodic value at residue
0), which is stronger than Cycle AH’s eventual constancy of
\((b_k)\). Certified on synthetic periods \(2^m\) for \(m\le 4\) with
onset 5.

Thus **infinitely many \(\theta_k=1\) would kill every eventual
period \(2^m\)**, including period 2 and isolated-zero \(q=3\), even
if \(I_k\) vanished. Periods 3, 5, 6, 7 and \(q=8\) would remain.

## Lemma (leftmost 11 hits \(\theta_k\))

Packed bit 1 is identically 1 for \(t\ge 1\) and the leftmost 11
always fires (Cycle AA). At time \(s=U=2^k\) it contributes to
\(\theta_k\) iff \(G(2U-1,3U-1)=1\). Write \(n=k+1\), so this is
\(G(2^n-1,2^n+2^{n-1}-1)\). Base \(n=1\): \(G(1,2)=1\). For \(n\ge 2\)
the first argument is odd and the second is odd, and

\[
G(2m+1,2j+1)=G(m,j),\qquad m=2^{n-1}-1,\quad j=2^{n-1}+2^{n-2}-1,
\]

which is the same claim at \(n-1\). Hence the leftmost 11 at time
\(2^k\) always hits, and

\[
\theta_k=1\oplus S_k,
\]

where \(S_k\) is the Green parity of all other AND hits on
\([U,3U)\) targeting \(3U\). Certified: \(G(2^{k+1}-1,3\cdot 2^k-1)=1\)
for \(k\le 16\), and at least one packed-bit-1 hit for \(k\le 8\).

Cycle AA: the same 11 never hits \(I_k\) (\(2m\le 2T-2<2T-1\)). The
3-fold target \(3U\) is just far enough for the Mersenne degree
\(2U-1\) to carry it.

## \(S_k\equiv 0\) and local formulas — killed

If \(S_k\) vanished, then \(\theta_k\equiv 1\), which would already
kill every period \(2^m\). On \(k\le 8\),
\(\theta=(0,0,1,0,0,1,0,1,1)\), so \(S\) cancels the forced 1 at
\(k=0,1,3,4,6\). **Killed.** Off-centre hits are not a singleton
(\(n_{\mathrm{other}}>1\) already at \(k=1\)). \(\theta_k\) equals
neither \(I_k\), nor \(\bigoplus d\), nor \(\bigoplus(c\land r)\) on
the 3-fold interval (first failures at \(k=0\) or \(k=1\)).

## Verdict

`LEMMA` (\(\theta_k=J^{(3)}_k\); period \(2^m\) forces \(\theta=0\);
leftmost 11 hits \(\theta_k\), so \(\theta_k=1\oplus S_k\)).
`KILLED` (\(S\equiv 0\); \(\theta\) equals \(I_k\), \(\bigoplus d\),
or \(\bigoplus(c\land r)\)). `OPEN` (\(\theta_k=1\) infinitely often;
eventual vanishing of \(I_k\)). Prize unsolved.

## Files

- `research/cycle_aj.md` (this note)
- `research/cycle_aj.py`
- `research/cycle_aj.json`
