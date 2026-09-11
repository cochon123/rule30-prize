# Cycle CE: \(d=Da\) iff \(c\) implies \(a\); \(c\) implies \(b\) forbids \(11\)s

Packed update \(a'=d\oplus(c\lor a)\) makes \(d=a\oplus a'\) iff
\(a=c\lor a\) iff \(c\) implies \(a\), pointwise. Identically AND
therefore requires \(c\to a\) (hence \(d=Da\)) and \(c\to b\). If
\(c_t=b_t=1\) then \(b'=0\), so \(c\to b\) at the next time forces
\(c_{t+1}=0\): no consecutive \(11\)s in \(c\). On the \(k=4\) and
\(k=8\) odd lifts both implications hold together only at the
ident-\(0\)/ident-\(1\) scar triple, where \(011\) kills AND
(prefix). Not a prize claim: the Fermat covering remains a prefix.

Helper: `python3 research/cycle_ce.py --certify` (~0.02s). Dump:
`research/cycle_ce.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (\(d=Da\) iff \(c\to a\))

From \(a'=d\oplus(c\lor a)\) one has \(a\oplus a'=d\oplus(c\lor a)\).
Then \(d=Da\) iff \(0=a\oplus(c\lor a)\) iff \(a=c\lor a\) iff
\(c\to a\). This is a three-bit identity, independent of AND.
Certified on all eight triples \((d,c,a)\). On the odd lifts the two
lists \(d=Da\) and \(c\to a\) agree (zero mismatches).

## Lemma (\(c\to b\) forbids consecutive \(11\)s in \(c\))

If \(c_t=b_t=1\) then \(b'=c\oplus(a\lor b)=0\). Identically
\(c\to b\) at time \(t+1\) then requires \(c_{t+1}=0\). Hence \(c\)
has no cyclic factor \(11\). Certified: \(c=b=1\) forces \(b'=0\) for
both values of \(a\); on the odd lifts every \(c\to b\) string has no
\(11\).

## Lemma (AND is three implications)

Identically AND iff \(c\to a\), \(c\to b\), and \((a\land b)\to c\).
The first is \(d=Da\). The second forbids \(11\)s in \(c\). The third
is the absence of \(011\).

## Prefix (both implications only at the scar \(c\equiv 0\))

On the \(k=4\) lift, \(c\to a\) at bits \(29,31,32\) and \(c\to b\)
only at \(31\) (\(c\equiv 0\), \(b\equiv 1\)). On the \(k=8\) lift,
\(c\to a\) at \(400,402,403,410\) and \(c\to b\) at \(402,406,436\);
both only at \(402\) (\(c\equiv 0\), \(b\equiv 1\), eight \(011\)s).
**PREFIX**, not a theorem for every odd lift. The scar pair with
\(c\equiv 0\) cannot be AND unless \(a\equiv 0\), and \(a=T\not\equiv 0\).

## \(c\to a\) never after the scar — killed

Four later triples at \(k=8\) have \(c\to a\), including \(q=410\)
which is neither ident-\(0\) nor ident-\(1\). **Killed.**

## No \(11\) in \(c\) after the scar — killed

Four later triples at \(k=8\) have no \(11\) in \(c\). **Killed** as a
blanket obstruction.

## Verdict

`LEMMA` (\(d=Da\) iff \(c\to a\); \(c\to b\) forbids \(11\)s in \(c\);
AND is three implications).
`PREFIX` (both implications only at the scar \(c\equiv 0\); no
AND-triple after the scar; at most one odd toggle for all \(k\);
seed for all \(k\); Fermat covering).
`KILLED` (\(c\to a\) never after the scar; no \(11\) in \(c\) after
the scar).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_ce.md` (this note)
- `research/cycle_ce.py`
- `research/cycle_ce.json`
