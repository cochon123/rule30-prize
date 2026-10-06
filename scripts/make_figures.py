"""Draw the README figures from the Rule 30 experiment.

Run from anywhere:

    python3 scripts/make_figures.py

Every number is computed by experiment.py. The script refuses to write
figures unless those numbers match the checkpoints in REPORT.md and
results.json. Output is docs/figures/.
"""

import hashlib
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from experiment import (  # noqa: E402
    center_bits,
    check_recurrence,
    dyadic_annuli,
    linear_complexity,
    period_witnesses,
    right_edge_periods,
)

OUT = ROOT / "docs" / "figures"
BITS = 100_000
INK = "#1c2833"
BLUE = "#1f4e79"
RED = "#b42318"
GRAY = "#5c6b7a"
MARK = "#8a4b08"

# Checkpoints printed in REPORT.md. Signed discrepancy is 2 * ones - N.
REPORT_COUNTS = {
    100: (52, 4),
    1_000: (481, -38),
    10_000: (5_032, 64),
    100_000: (50_098, 196),
}
REPORT_COMPLEXITY = {
    100: (48, 100),
    1_000: (500, 1_000),
    10_000: (5_001, 10_001),
    20_000: (10_000, 20_002),
}
REPORT_ANNULI = [
    (1, 1.0),
    (2, 0.5),
    (4, 0.5),
    (8, 0.25),
    (16, 0.1875),
    (32, 0.09375),
    (64, 0.125),
    (128, 0.125),
    (256, 0.046875),
    (512, 0.1015625),
    (1024, 0.03515625),
    (2048, 0.01220703125),
    (4096, 0.015869140625),
    (8192, 0.0223388671875),
    (16384, 0.01519775390625),
    (32768, 0.0054931640625),
]
REPORT_EDGE_PERIODS = [1, 2, 2, 4, 8, 8, 16, 32, 32, 64, 64, 64, 64]
REPORT_SHA256 = "1070424af717c627d55c57fae20fc9a0baf3b3c327d19a10f8fb397c7ad0dc38"
REPORT_MIN_LAST_MISMATCH = 95_902
SELF_CHECK_PREFIX = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1]
# Standard Rule 30 rows inside the light cone, left edge first.
KNOWN_ROWS = [
    "1",
    "111",
    "11001",
    "1101111",
    "110010001",
    "11011110111",
    "1100100001001",
    "110111100111111",
]


def style():
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.titlesize": 12,
            "axes.labelsize": 11,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.linewidth": 0.8,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
            "text.color": INK,
            "axes.labelcolor": INK,
            "xtick.color": INK,
            "ytick.color": INK,
            "axes.titlecolor": INK,
        }
    )


def spacetime(steps):
    """Rows of x(t, j) for j from -t to t. Same rule as experiment.reference_bits."""
    row = {0: 1}
    rows = []
    for t in range(steps):
        rows.append([row.get(j, 0) for j in range(-t, t + 1)])
        row = {
            j: row.get(j - 1, 0) ^ (row.get(j, 0) | row.get(j + 1, 0))
            for j in range(-t - 1, t + 2)
        }
    return rows


def assert_matches_report(bits):
    if list(bits[:20]) != SELF_CHECK_PREFIX:
        raise SystemExit("center prefix disagrees with experiment.py self-check")
    digest = hashlib.sha256(bits).hexdigest()
    if digest != REPORT_SHA256:
        raise SystemExit(f"sha256 {digest} disagrees with results.json")
    for n, (ones, imbalance) in REPORT_COUNTS.items():
        got_ones = sum(bits[:n])
        got_imbalance = 2 * got_ones - n
        if (got_ones, got_imbalance) != (ones, imbalance):
            raise SystemExit(f"checkpoint {n}: {(got_ones, got_imbalance)}")
    for n, (length, failure) in REPORT_COMPLEXITY.items():
        got_length, connection = linear_complexity(bits[:n])
        got_failure = check_recurrence(bits[: min(2 * n, len(bits))], got_length, connection)
        if (got_length, got_failure) != (length, failure):
            raise SystemExit(f"complexity {n}: {(got_length, got_failure)}")
    annuli = dyadic_annuli(bits)
    got = [(item["start"], item["normalized_maximum"]) for item in annuli]
    if got != REPORT_ANNULI:
        raise SystemExit("dyadic annuli disagree with results.json")
    if right_edge_periods(12) != REPORT_EDGE_PERIODS:
        raise SystemExit("right-edge periods disagree with results.json")
    for k, period in enumerate(REPORT_EDGE_PERIODS):
        if (2**k) % period != 0:
            raise SystemExit(f"period at offset {k} does not divide 2^{k}")
    witnesses = period_witnesses(bits, 4096)
    last = [item["last_mismatch"] for item in witnesses]
    if min(last) != REPORT_MIN_LAST_MISMATCH or len(witnesses) != 4096:
        raise SystemExit(f"period witnesses min={min(last)} count={len(witnesses)}")
    rows = spacetime(8)
    for row, text in zip(rows, KNOWN_ROWS):
        if "".join(map(str, row)) != text:
            raise SystemExit(f"spacetime row {text} came out {row}")
    if [row[t] for t, row in enumerate(rows)] != list(bits[:8]):
        raise SystemExit("spacetime center column disagrees with center_bits")
    # Both light-cone edges stay live: x(t, -t) = x(t, t) = 1.
    if any(row[0] != 1 or row[-1] != 1 for row in rows):
        raise SystemExit("light-cone edge is not the constant-1 boundary")
    return witnesses, annuli


def save(fig, name):
    path = OUT / name
    fig.savefig(path, dpi=160, bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)
    return path


def running(bits):
    values = np.asarray(bits, dtype=np.int8)
    ones = np.cumsum(values)
    n = np.arange(1, len(values) + 1)
    discrepancy = 2 * ones - n
    return n, ones / n, discrepancy


def mark_checkpoints(ax, xs, ys, labels, offsets):
    ax.scatter(xs, ys, s=28, color=MARK, zorder=4, label="checkpoints in REPORT.md")
    for x, y, text, offset in zip(xs, ys, labels, offsets):
        ax.annotate(
            text,
            (x, y),
            textcoords="offset points",
            xytext=offset,
            fontsize=8,
            color=MARK,
        )


def _font(size):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)


def figure_spacetime(bits):
    """Crisp cells. A side panel enlarges the center so the column stays visible."""
    steps = 192
    rows = spacetime(steps)
    if [row[t] for t, row in enumerate(rows)] != list(bits[:steps]):
        raise SystemExit("plotted center column disagrees with center_bits")
    scale = 3
    tri_w = (2 * steps - 1) * scale
    tri_h = steps * scale
    j_lo, j_hi = -16, 16
    t_zoom = 32
    cell = 18
    zoom_w = (j_hi - j_lo + 1) * cell
    zoom_h = t_zoom * cell

    left_gutter = 46
    zoom_gutter = 44
    gap = 36
    margin = 16
    header = 62
    footer = 44
    width = margin + left_gutter + tri_w + gap + zoom_gutter + zoom_w + margin
    height = margin + header + max(tri_h, zoom_h) + footer
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    title_font = _font(18)
    label_font = _font(13)
    small_font = _font(12)

    draw.text((margin, 12), "Rule 30 from one live cell, through time 191", fill=INK, font=title_font)
    legend_y = 40
    swatch = 12
    legend = [("0", (255, 255, 255), INK), ("1", (22, 22, 22), None), ("center column", (196, 28, 28), None)]
    lx = margin
    for text, fill, outline in legend:
        draw.rectangle([lx, legend_y, lx + swatch, legend_y + swatch], fill=fill, outline=outline or fill)
        draw.text((lx + swatch + 6, legend_y - 2), text, fill=INK, font=small_font)
        lx += swatch + 8 + int(draw.textlength(text, font=small_font)) + 16

    origin_x = margin + left_gutter
    origin_y = margin + header
    center = steps - 1
    for t, row in enumerate(rows):
        offset = center - t
        for i, bit in enumerate(row):
            x = origin_x + (offset + i) * scale
            y = origin_y + t * scale
            if i == t:
                color = (255, 214, 214) if bit == 0 else (196, 28, 28)
            else:
                color = (22, 22, 22) if bit else (255, 255, 255)
            draw.rectangle([x, y, x + scale - 1, y + scale - 1], fill=color)
    for t, text in [(0, "0"), (64, "64"), (128, "128"), (191, "191")]:
        y = origin_y + t * scale - 6
        draw.text((margin, y), "t=" + text, fill=INK, font=small_font)
    for j, text in [(-(steps - 1), str(-(steps - 1))), (0, "0"), (steps - 1, str(steps - 1))]:
        x = origin_x + (center + j) * scale + scale // 2
        tw = draw.textlength(text, font=small_font)
        draw.text((x - tw / 2, origin_y + tri_h + 8), text, fill=INK, font=small_font)

    zx = origin_x + tri_w + gap + zoom_gutter
    zy = origin_y
    outside = (236, 236, 234)
    grid = (214, 214, 212)
    for t in range(t_zoom):
        for j in range(j_lo, j_hi + 1):
            x = zx + (j - j_lo) * cell
            y = zy + t * cell
            if abs(j) > t:
                color = outside
                outline = grid
            else:
                bit = rows[t][j + t]
                if j == 0:
                    color = (255, 214, 214) if bit == 0 else (196, 28, 28)
                    outline = color
                else:
                    color = (22, 22, 22) if bit else (255, 255, 255)
                    outline = grid
            draw.rectangle([x, y, x + cell - 1, y + cell - 1], fill=color, outline=outline)
    draw.rectangle([zx, zy, zx + zoom_w - 1, zy + zoom_h - 1], outline=INK)
    for t, text in [(0, "0"), (16, "16"), (31, "31")]:
        y = zy + t * cell + 2
        draw.text((zx - zoom_gutter + 6, y), text, fill=INK, font=small_font)
    for j, text in [(j_lo, str(j_lo)), (0, "0"), (j_hi, str(j_hi))]:
        x = zx + (j - j_lo) * cell + cell / 2
        tw = draw.textlength(text, font=small_font)
        draw.text((x - tw / 2, zy + zoom_h + 8), text, fill=INK, font=small_font)
    draw.text((zx, zy - 22), "center, enlarged", fill=INK, font=label_font)

    # Interior of the enlarged center column uses only the two center colors.
    center_colors = {(255, 214, 214), (196, 28, 28)}
    cx0 = zx + (0 - j_lo) * cell
    interior = image.crop((cx0 + 2, zy + 2, cx0 + cell - 2, zy + zoom_h - 2))
    if set(interior.get_flattened_data()) - center_colors:
        raise SystemExit("enlarged center column is not colored as the center")
    path = OUT / "spacetime.png"
    image.save(path, optimize=True)
    return path


def figure_center_statistics(bits):
    n, freq, discrepancy = running(bits)
    fig = plt.figure(figsize=(9.2, 8.6))
    grid = fig.add_gridspec(3, 1, height_ratios=[1.05, 1.05, 1.15], hspace=0.42)
    ax0 = fig.add_subplot(grid[0])
    ax1 = fig.add_subplot(grid[1])
    ax2 = fig.add_subplot(grid[2])

    cols = 20
    shown = 100
    grid_bits = np.asarray(bits[:shown], dtype=np.int8).reshape(shown // cols, cols)
    ax0.imshow(
        grid_bits,
        cmap=ListedColormap(["#f7f7f5", "#161616"]),
        interpolation="nearest",
        aspect="equal",
        vmin=0,
        vmax=1,
    )
    for r in range(grid_bits.shape[0]):
        for c in range(cols):
            bit = int(grid_bits[r, c])
            ax0.text(
                c,
                r,
                str(bit),
                ha="center",
                va="center",
                fontsize=7.5,
                color="white" if bit else INK,
            )
    ax0.set_title(f"First {shown} center bits  ({int(grid_bits.sum())} ones)")
    ax0.set_xticks([0, 4, 9, 14, 19])
    ax0.set_xlabel("bit inside the row")
    ax0.set_yticks(range(grid_bits.shape[0]))
    ax0.set_yticklabels([f"t = {r * cols}" for r in range(grid_bits.shape[0])])
    ax0.tick_params(length=0)
    for spine in ax0.spines.values():
        spine.set_visible(True)
        spine.set_color("#d5d5d2")

    view = n >= 20
    ax1.plot(n[view], freq[view], color=BLUE, linewidth=1.15, label="fraction of ones")
    ax1.axhline(0.5, color=GRAY, linewidth=0.8, linestyle="--", label="1/2")
    xs = [100, 1_000, 10_000, 100_000]
    mark_checkpoints(
        ax1,
        xs,
        [freq[x - 1] for x in xs],
        ["0.520", "0.481", "0.503", "0.501"],
        [(6, 8), (6, -12), (6, 8), (-32, 8)],
    )
    ax1.set_xscale("log")
    ax1.set_xlim(20, 100_000)
    ax1.set_ylim(0.46, 0.60)
    ax1.set_xlabel("prefix length N")
    ax1.set_ylabel("ones in the first N bits")
    ax1.set_title("Running frequency of the center column")
    ax1.legend(frameon=False, fontsize=8.5, loc="upper right")
    ax1.grid(True, axis="y", color="#ececec", linewidth=0.7)

    ax2.plot(n, discrepancy, color=BLUE, linewidth=0.9, label="D(N)")
    ax2.axhline(0, color=GRAY, linewidth=0.8, linestyle="--")
    mark_checkpoints(
        ax2,
        xs,
        [discrepancy[x - 1] for x in xs],
        ["+4", "-38", "+64", "+196"],
        [(8, 10), (8, -14), (8, 10), (-34, 12)],
    )
    ax2.set_xscale("log")
    ax2.set_xlim(1, 100_000)
    ax2.set_xlabel("prefix length N")
    ax2.set_ylabel("D(N) = ones - zeros")
    ax2.set_title("Signed discrepancy of the same prefix")
    ax2.legend(frameon=False, fontsize=8.5, loc="upper left")
    ax2.grid(True, axis="y", color="#ececec", linewidth=0.7)
    return save(fig, "center_statistics.png")


def figure_finite_checks(bits, witnesses, annuli):
    fig, axes = plt.subplots(2, 2, figsize=(9.6, 7.4))
    fig.subplots_adjust(hspace=0.38, wspace=0.32)

    lengths = sorted(
        set(REPORT_COMPLEXITY) | set(range(500, 20_001, 500))
    )
    measured = []
    for n in lengths:
        measured.append(linear_complexity(bits[:n])[0])
    ax = axes[0, 0]
    ax.plot(lengths, measured, color=BLUE, linewidth=1.3, label="L(N)")
    ax.plot([0, 20_000], [0, 10_000], color=GRAY, linewidth=0.8, linestyle="--", label="N/2")
    report_n = list(REPORT_COMPLEXITY)
    report_L = [REPORT_COMPLEXITY[n][0] for n in report_n]
    ax.scatter(report_n, report_L, s=32, facecolors="white", edgecolors=MARK, linewidths=1.4, zorder=4, label="REPORT.md")
    for n, length, offset in zip(report_n, report_L, [(8, 8), (6, 8), (6, 8), (-28, 8)]):
        ax.annotate(
            str(length),
            (n, length),
            textcoords="offset points",
            xytext=offset,
            fontsize=8,
            color=MARK,
        )
    ax.set_xlim(0, 21_000)
    ax.set_ylim(0, 12_500)
    ax.set_xlabel("training length N")
    ax.set_ylabel("linear complexity L(N)")
    ax.set_title("Shortest GF(2) recurrence")
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax.grid(True, axis="y", color="#ececec", linewidth=0.7)

    ax = axes[0, 1]
    starts = [item["start"] for item in annuli]
    normalized = [item["normalized_maximum"] for item in annuli]
    ax.plot(starts, normalized, color=BLUE, linewidth=1.2, marker="o", markersize=3.5)
    ax.set_xscale("log", base=2)
    ax.set_xlabel("annulus start  2^m")
    ax.set_ylabel("max |partial imbalance| / length")
    ax.set_title("Dyadic annuli inside 100,000 bits")
    ax.set_ylim(0, 1.05)
    ax.grid(True, axis="y", color="#ececec", linewidth=0.7)

    ax = axes[1, 0]
    periods = np.array([item["period"] for item in witnesses])
    last = np.array([item["last_mismatch"] for item in witnesses])
    envelope = BITS - periods - 1
    ax.plot(periods, last, color=BLUE, linewidth=0.9, label="last mismatch")
    ax.plot(periods, envelope, color=GRAY, linewidth=0.8, linestyle="--", label="last comparable time")
    ax.axhline(
        REPORT_MIN_LAST_MISMATCH,
        color=RED,
        linewidth=0.9,
        label=f"earliest: {REPORT_MIN_LAST_MISMATCH:,}",
    )
    gap = int((envelope - last).max())
    if gap != 15:
        raise SystemExit(f"period gap changed: {gap}")
    ax.set_xlim(1, 4096)
    ax.set_ylim(95_400, 100_400)
    ax.set_xlabel("period p")
    ax.set_ylabel("time of last mismatch")
    ax.set_title("Periods 1..4096 (axis from 95,400)")
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    ax.text(
        0.03,
        0.20,
        f"largest gap between the curves: {gap} steps",
        transform=ax.transAxes,
        fontsize=8,
        color=GRAY,
    )
    ax.grid(True, axis="y", color="#ececec", linewidth=0.7)

    ax = axes[1, 1]
    ks = np.arange(len(REPORT_EDGE_PERIODS))
    ax.bar(ks, REPORT_EDGE_PERIODS, color=BLUE, width=0.72, label="measured period")
    ax.plot(ks, 2**ks, color=RED, marker="o", markersize=3.5, linewidth=1.1, label="2^k")
    ax.set_yscale("log", base=2)
    ax.set_xticks(ks)
    ax.set_xlabel("right-edge offset k")
    ax.set_ylabel("period")
    ax.set_title("Period of fixed offset k")
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax.set_ylim(0.8, 2**13)
    ax.grid(True, axis="y", color="#ececec", linewidth=0.7)
    return save(fig, "finite_checks.png")


def box(ax, x, y, w, h, face, edge, title, lines, title_color, body_color):
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.18,rounding_size=0.4",
        facecolor=face,
        edgecolor=edge,
        linewidth=1.15,
    )
    ax.add_patch(patch)
    cx = x + w / 2
    ax.text(cx, y + h - 1.15, title, ha="center", va="top", fontsize=11.5, color=title_color)
    ax.text(
        cx,
        y + h - 3.5,
        "\n".join(lines),
        ha="center",
        va="top",
        fontsize=9,
        color=body_color,
        linespacing=1.35,
    )


def arrow(ax, start, end):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=11,
            linewidth=1.0,
            color=GRAY,
            shrinkA=2,
            shrinkB=2,
        )
    )


def figure_swarm():
    fig, ax = plt.subplots(figsize=(10.2, 6.7))
    fig.suptitle(
        "Swarm recorded in REPORT.md and research/LOG.md",
        fontsize=13,
        color=INK,
        y=0.98,
    )
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    box(
        ax, 22, 78, 56, 14,
        "#1c3d5a", "#1c3d5a",
        "Coordinating agent",
        ["Checks the mathematics.", "Runs the experiments. Writes REPORT.md."],
        "white", "#e6eef5",
    )
    agents = [
        (2, "Nonperiodicity", ["Problem 1", "Is the center column", "eventually periodic?"]),
        (35, "Balance", ["Problem 2", "Limiting frequency", "of ones in that column"]),
        (68, "Complexity", ["Problem 3", "Cost of computing", "one center bit"]),
    ]
    fills = ["#e7f0f8", "#e6f3ec", "#f8f1e6"]
    for (x, title, lines), fill in zip(agents, fills):
        box(ax, x, 46, 30, 22, fill, "#1c3d5a", title, lines, INK, "#243140")
        arrow(ax, (50, 78), (x + 15, 68.2))

    box(
        ax, 2, 22, 96, 16,
        "#f4f6f8", "#1c3d5a",
        "Cycles A-H",
        [
            "Follow-up attacks on the same three problems.",
            "Each met a kill criterion in research/LOG.md.",
        ],
        INK, "#243140",
    )
    arrow(ax, (17, 46), (28, 38.2))
    arrow(ax, (50, 46), (50, 38.2))
    arrow(ax, (83, 46), (72, 38.2))

    box(
        ax, 20, 2, 60, 12,
        "#f7f7f6", "#1c2833",
        "Recorded outcome",
        ["No prize problem solved."],
        INK, "#243140",
    )
    arrow(ax, (50, 22), (50, 14.2))
    fig.subplots_adjust(top=0.90, bottom=0.02, left=0.02, right=0.98)
    return save(fig, "swarm.png")


def main():
    style()
    OUT.mkdir(parents=True, exist_ok=True)
    bits = center_bits(BITS)
    witnesses, annuli = assert_matches_report(bits)
    written = [
        figure_spacetime(bits),
        figure_center_statistics(bits),
        figure_finite_checks(bits, witnesses, annuli),
        figure_swarm(),
    ]
    for path in written:
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
