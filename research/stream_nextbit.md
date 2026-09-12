# Streaming the next centre bit from the packed row

Attack on prize problem 3, as specified in [_astra_ideas10.md](_astra_ideas10.md) item 1 (leftover [_astra_ideas9.md](_astra_ideas9.md) item 5). Finite evidence only. **Not a prize claim.**

Certifier: `research/stream_nextbit.py`. Dump: `research/stream_nextbit.json`.
Does not modify `experiment.py`, `strip_graph.py`, or `strip_extend.py`.

## Local rule and packing

Rule 30 is

\[
x(t+1,j)=x(t,j-1)\oplus\bigl(x(t,j)\lor x(t,j+1)\bigr).
\]

The next centre bit is therefore three bits of row \(t\):

\[
c_{t+1}=x(t,-1)\oplus\bigl(x(t,0)\lor x(t,1)\bigr).
\]

Packing is `experiment.py`: \(z_0=1\), `z=(z<<2)^((z<<1)|z)`, and \(x(t,j)=(z>>(j+t))\&1\). The centre is bit \(t\); the triple sits at indices \(t-1,t,t+1\). Centre bits match `experiment.center_bits` through 4097, including the known 20-bit word `11011100110001011001`. \(N_t=\operatorname{popcount}(z\land(z{\ll}1))\) agrees with [packed_valuation.md](packed_valuation.md) on the published sample times.

## Word-RAM baseline (allowed only as a control)

Given \(z\) and the index \(t\), three bit tests plus a few Boolean operations return \(c_{t+1}\). That is \(O(1)\) in the word-RAM / Python-bigint model (bit \(k\) of an integer is a constant-time word operation). It still *uses the growing index* \(t\). The three-bit formula is therefore not a streaming shortcut: Problem 3 is producing \(z_t\) or those three bits without \(\Theta(t^2)\) bit operations (each of the \(t\) packed updates XORs a \(\Theta(t)\)-bit word). This freeze only kills cheap *summaries* of an already-known \(z\).

The length-3 window at offset \(t-1\) is exactly the packed triple. On \(t=8\ldots 4096\) it witnessed-determines both the triple and \(c_{t+1}\) (8 values, every value reused, no ambiguity). Exact integer equality with the single next bit fails, as expected for a 3-bit word.

## Freeze

Candidate \(o(t)\) statistics of \(z\) at time \(t\le 4096\):

- \(\operatorname{popcount}(z)\), and \(\operatorname{popcount}(z\land((1{\ll}k)-1))\) for \(k=8,16,32\)
- \(v_2(z)\), \(v_2(z+1)\), \(v_2(z\oplus(z{\ll}1))\), \(v_2(z\oplus(1{\ll}t))\)
- \(\operatorname{popcount}(z\land(z{\ll}1))=N_t\)
- every length-\(\le 8\) bit window, but only at a *fixed* set of at most 16 bit positions (offsets \(0..31\)), or at offsets that depend on \(t\) only through \(\operatorname{popcount}\) and \(v_2\) (16 frozen arithmetic combinations); extracting a window at an arbitrary index still costs reading those bits
- the same scalars on \(z\oplus(z{\ll}1)\) and \(z\land(z{\ll}1)\)

A statistic *equals* the next centre bit if its raw value (or, separately, its parity) equals \(c_{t+1}\) for every \(t=8\ldots 4096\). It *determines the triple* if every reused value is compatible with a single triple (witnessed: some value appears at least twice). Injectivity on this finite prefix is not an evaluator: a 32-bit left-edge key is expected to be unique by the birthday paradox and does not extend.

Costs: \(v_2\) and any window / popcount of \(O(1)\) low bits are \(O(1)\) bit operations. Full \(\operatorname{popcount}(z)\), \(N_t\), and a histogram of all sliding windows read \(\Theta(t)\) bits of a \((2t+1)\)-bit word. Those last are killed even if they accidentally determined the triple.

Primary range \(t=8..4096\). Clean range \(t=32..4096\) makes the
32 LSBs disjoint from the triple (so small-\(t\) overlap cannot
fake a determination).

## Scalar statistics

| statistic | cost | eq \(c_{t+1}\) | parity eq | det triple | det next | values | reuse | amb triple | first eq fail |
|---|---|---|---|---|---|---:|---:|---:|---|
| `popcount(z)` | Theta(t) | no | no | no | no | 2619 | 1069 | 985 | t=8 |
| `popcount_low8` | O(1) | no | no | no | no | 2 | 2 | 2 | t=8 |
| `popcount_low16` | O(1) | no | no | no | no | 6 | 5 | 5 | t=8 |
| `popcount_low32` | O(1) | no | no | no | no | 12 | 8 | 8 | t=8 |
| `v2(z)` | O(1) | no | no | no | no | 1 | 1 | 1 | t=8 |
| `v2(z+1)` | O(1) | no | no | no | no | 1 | 1 | 1 | t=8 |
| `v2(z XOR (z<<1))` | O(1) | no | no | no | no | 1 | 1 | 1 | t=8 |
| `v2(z XOR (1<<t))` | O(1) | no | no | no | no | 1 | 1 | 1 | t=8 |
| `N_t` | Theta(t) | no | no | no | no | 1795 | 1199 | 1127 | t=8 |
| `low16` | O(1) | no | no | no | no | 9 | 4 | 4 | t=8 |
| `low8` | O(1) | no | no | no | no | 2 | 2 | 2 | t=8 |
| `tdep16` | O(1) | no | no | no | no | 120 | 93 | 92 | t=8 |
| `popcount(z XOR (z<<1))` | Theta(t) | no | no | no | no | 1781 | 1228 | 1140 | t=8 |
| `v2(z AND (z<<1))` | O(1) | no | no | no | no | 1 | 1 | 1 | t=9 |
| `popcount_low8(z XOR (z<<1))` | O(1) | no | no | no | no | 1 | 1 | 1 | t=8 |
| `popcount_low8(z AND (z<<1))` | O(1) | no | no | no | no | 2 | 2 | 2 | t=9 |
| `popcount_low16(z XOR (z<<1))` | O(1) | no | no | no | no | 4 | 3 | 3 | t=8 |
| `popcount_low16(z AND (z<<1))` | O(1) | no | no | no | no | 4 | 4 | 4 | t=8 |
| `popcount_low32(z XOR (z<<1))` | O(1) | no | no | no | no | 11 | 9 | 9 | t=8 |
| `popcount_low32(z AND (z<<1))` | O(1) | no | no | no | no | 9 | 7 | 7 | t=8 |
| `baseline_window(t-1,3)` | O(1) word-RAM, index t | no | no | yes | yes | 8 | 8 | 0 | t=8 |
| `baseline_next_bit` | O(1) word-RAM, index t | yes | yes | no | yes | 2 | 2 | 2 | — |

On this orbit \(z\) is always odd, so \(v_2(z)=0\). For the experiment packing, \(v_2(z+1)=2\) at every \(t\ge 2\) ([packed_valuation.md](packed_valuation.md)). \(v_2(z\oplus(z{\ll}1))=0\) and \(v_2(z\oplus(1{\ll}t))=0\) for \(t>0\) (XOR with bit \(t\) does not touch the LSB). These valuations are constants and cannot separate eight triples.

Full \(\operatorname{popcount}(z)\) and \(N_t\) have many reused values and many ambiguous triples; their parities agree with \(c_{t+1}\) on about half the times (popcount parity frac 0.497, \(N_t\) parity frac 0.497). They also read \(\Theta(t)\) bits.

## Length-\(\le 8\) windows

Fixed offsets \(0\ldots 31\), lengths \(1\ldots 8\): 256 windows. T-dependent offsets through popcount/\(v_2\) (16 frozen functions), same lengths: 128 windows. The second row of each family is the clean range \(t=32..4096\).

| family | tested | eq next | parity eq | det triple | det next | injective |
|---|---:|---:|---:|---:|---:|---:|
| fixed offset 0..31, t=8..4096 | 256 | 0 | 0 | 0 | 0 | 0 |
| fixed offset 0..31, t=32..4096 | 256 | 0 | 0 | 0 | 0 | 0 |
| popcount/v2-of-t offset, t=8..4096 | 128 | 0 | 0 | 0 | 0 | 0 |
| popcount/v2-of-t offset, t=32..4096 | 128 | 0 | 0 | 0 | 0 | 0 |

No fixed window and no popcount/\(v_2\)-of-\(t\) window equals the next bit, equals it in parity, or witnessed-determines the triple or the next bit, on either range. First ambiguities occur early (typical \(t<64\)); JSON `windows_fixed` / `windows_tdep` store the first equality-fail and first triple-ambiguity time of each window.

The 16 frozen t-dependent positions are all \(O(\log t)\) and, for \(t\ge 32\), lie strictly left of index \(t-1\). They never secretly read the triple. The packed 16-bit word at those positions is an \(O(1)\) statistic in the scalar table (`tdep16`); it collides with distinct triples. The 16 LSBs (`low16`) likewise fail on the clean range, where they are disjoint from the centre.

## Joint freeze and \(\Theta(t)\) histograms

| joint | cost | det triple | det next | values | reuse | amb triple | injective |
|---|---|---|---|---:|---:|---:|---|
| `joint_O(1)_scalars` | O(1) | no | no | 152 | 102 | 102 | no |
| `joint_low_popcounts` | O(1) | no | no | 20 | 10 | 10 | no |
| `joint_v2` | O(1) | no | no | 1 | 1 | 1 | no |
| `joint_Theta(t)_popcount_N` | Theta(t) | no | no | 4065 | 24 | 20 | no |
| `joint_O(1)_plus_tdep_windows` | O(1) | no | no | 161 | 106 | 106 | no |
| `histogram_all_windows_L1` | Theta(t) | no | no | 4089 | 0 | 0 | yes |
| `histogram_all_windows_L3` | Theta(t) | no | no | 4089 | 0 | 0 | yes |
| `histogram_all_windows_L8` | Theta(t) | no | no | 4089 | 0 | 0 | yes |

The joint of every \(O(1)\) scalar in the freeze (low popcounts, valuations, 16 LSBs, t-dep 16-bit gather, length-8 windows at popcount(\(t\)) and \(v_2(t+1)\)) remains ambiguous for the triple: distinct triples share the same cheap summary. Histograms of all length-1/3/8 windows read \(\Theta(t)\) bits and are injective fingerprints of the scanned rows (no reuse), which is not an \(o(t)\) formula.

## Why it died

Killed. Every statistic in the freeze fails to equal the next centre bit, and fails to witnessed-determine the triple (or the next bit), on t=8..4096; the same holds on the clean range t=32..4096 where fixed low bits are disjoint from the triple. Full popcount, N_t, XOR-popcount, and all-window histograms secretly read Theta(t) bits. The three centre-adjacent bits (length-3 window at offset t-1) work as a baseline: O(1) word-RAM given z, but they use the growing index t. The three-bit formula is already O(1) in word RAM given z, so Problem 3 is really about producing z or those bits without Theta(t^2) work. This freeze only kills cheap summaries of z.

A cheap exact formula for \(c_{t+1}\) given \(z_t\) would not by itself have been a prize claim: the three-bit local rule already is that formula. The missing piece is still an algorithm that produces \(z_n\) (or bit \(n\) of it) in \(o(n^2)\) bit operations. Not a prize claim.

Wall time: `10.488` seconds.

Self-check: packed centre agrees with `experiment.center_bits` on 256 bits and on \(0..4097\); three-bit formula matches \(c_{t+1}\) for \(t=1..4096\); \(N_t\) sample matches `packed_valuation.json`; \(v_2(z)=0\), \(v_2(z+1)=2\) (\(t\ge 2\)).

