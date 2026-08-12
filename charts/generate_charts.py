#!/usr/bin/env python3
"""Generate the dataset charts used across the documentation.

Reads every JSONL file, computes reasoning depth (words inside think blocks) and
final-answer length per record, and renders PNG charts into charts/.

Run from the repository root:

    python charts/generate_charts.py
"""
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "charts"

T_OPEN, T_CLOSE = "<think>", "</think>"

TIERS = ["easy", "medium", "hard"]
MODES = ["wrong_then_fix", "right_and_confirm", "right_doubt_reaffirm"]
DOMAINS = ["math", "code", "general"]

MODE_LABEL = {
    "wrong_then_fix": "wrong → catch → fix",
    "right_and_confirm": "right → scrutinize → verify",
    "right_doubt_reaffirm": "right → doubt → reaffirm",
}

# palette: calm, readable on white; used consistently across all charts
TIER_COLOR = {"easy": "#7fb07f", "medium": "#e0a458", "hard": "#b45252"}
DOMAIN_COLOR = {"math": "#4a6fa5", "code": "#3d7d7d", "general": "#a06b9e"}
MODE_COLOR = {
    "wrong_then_fix": "#b45252",
    "right_and_confirm": "#4a8059",
    "right_doubt_reaffirm": "#5d5d94",
}


def load_records():
    """Return list of dicts: domain, tier, mode, think_words, final_words."""
    recs = []
    for path in sorted(ROOT.glob("*/*/*.jsonl")):
        rel = path.relative_to(ROOT).parts
        domain, tier, mode = rel[0], rel[1], rel[2].replace(".jsonl", "")
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                content = rec["messages"][-1]["content"]
                parts = content.split(T_CLOSE)
                thinking = " ".join(p.strip() for p in parts[:-1]).replace(T_OPEN, "")
                final = parts[-1].strip()
                recs.append({
                    "domain": domain,
                    "tier": tier,
                    "mode": mode,
                    "think": len(thinking.split()),
                    "final": len(final.split()),
                })
    return recs


def style(ax, title, xlab=None, ylab=None):
    ax.set_title(title, fontsize=14, fontweight="bold", pad=14)
    if xlab:
        ax.set_xlabel(xlab)
    if ylab:
        ax.set_ylabel(ylab)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis="both", labelsize=11)


def chart_structure_grid(recs):
    """3x3 dot grid: domains by tiers, marker size = records per cell."""
    fig, ax = plt.subplots(figsize=(8.5, 6))
    counts = defaultdict(int)
    for r in recs:
        counts[(r["domain"], r["tier"])] += 1
    for i, dom in enumerate(DOMAINS):
        for j, tier in enumerate(TIERS):
            n = counts[(dom, tier)]
            ax.scatter(j, -i, s=n * 14, color=DOMAIN_COLOR[dom], alpha=0.85,
                       edgecolors="white", linewidths=2, zorder=3)
            ax.text(j, -i, str(n), ha="center", va="center", fontsize=13,
                    fontweight="bold", color="white", zorder=4)
    ax.set_xlim(-0.55, 2.55)
    ax.set_ylim(-2.55, 0.55)
    ax.set_xticks(range(3))
    ax.set_xticklabels([t.capitalize() for t in TIERS], fontsize=12)
    ax.set_yticks(range(-3, 0))
    ax.set_yticklabels([d.upper() for d in DOMAINS], fontsize=12, fontweight="bold")
    ax.set_xlabel("Difficulty tier", fontsize=12)
    ax.set_ylabel("Domain", fontsize=12)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(length=0)
    style(ax, "A 3 × 3 × 3 library — 100 records in every cell")
    fig.tight_layout()
    fig.savefig(OUT / "structure_grid.png", dpi=160)


def chart_depth_by_tier(recs):
    """Box plot: reasoning words per record by tier. The central design proof."""
    data = [[r["think"] for r in recs if r["tier"] == t] for t in TIERS]
    fig, ax = plt.subplots(figsize=(8.5, 5.8))
    bp = ax.boxplot(data, tick_labels=[t.capitalize() for t in TIERS],
                    patch_artist=True, widths=0.55, showfliers=False,
                    medianprops=dict(color="#222222", linewidth=2),
                    whiskerprops=dict(color="#555555"),
                    capprops=dict(color="#555555"))
    for patch, tier in zip(bp["boxes"], TIERS):
        patch.set_facecolor(TIER_COLOR[tier])
        patch.set_alpha(0.9)
    for i, t in enumerate(TIERS):
        d = data[i]
        ax.text(i + 1, np.percentile(d, 50) + max(d) * 0.02,
                f"median {int(np.median(d))}w", ha="center", fontsize=10,
                color="#333333", fontstyle="italic")
    style(ax, "Reasoning depth scales with difficulty (2,700 records)",
          ylab="words of reasoning per record")
    fig.tight_layout()
    fig.savefig(OUT / "think_depth_by_tier.png", dpi=160)


def chart_modes(recs):
    """Side-by-side bars: records per mode, mean reasoning words per mode."""
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))
    counts = [sum(1 for r in recs if r["mode"] == m) for m in MODES]
    means = [np.mean([r["think"] for r in recs if r["mode"] == m]) for m in MODES]
    labels = [MODE_LABEL[m] for m in MODES]

    ax = axes[0]
    bars = ax.bar(labels, counts, color=[MODE_COLOR[m] for m in MODES], alpha=0.9)
    for b, n in zip(bars, counts):
        ax.text(b.get_x() + b.get_width() / 2, n + 8, str(n), ha="center",
                fontweight="bold", fontsize=11)
    style(ax, "Records per mode", ylab="records")
    ax.set_ylim(0, max(counts) * 1.18)
    ax.tick_params(axis="x", labelsize=9)

    ax = axes[1]
    bars = ax.bar(labels, means, color=[MODE_COLOR[m] for m in MODES], alpha=0.9)
    for b, v in zip(bars, means):
        ax.text(b.get_x() + b.get_width() / 2, v + 8, f"{v:.0f}w", ha="center",
                fontweight="bold", fontsize=11)
    style(ax, "Mean reasoning length per mode", ylab="words of reasoning")
    ax.set_ylim(0, max(means) * 1.18)
    ax.tick_params(axis="x", labelsize=9)

    fig.suptitle("All three modes are evenly represented", fontsize=14,
                 fontweight="bold", y=1.0)
    fig.tight_layout()
    fig.savefig(OUT / "mode_comparison.png", dpi=160)


def chart_think_histogram(recs):
    """Stacked histogram of reasoning length, colored by tier."""
    fig, ax = plt.subplots(figsize=(9, 5))
    bins = np.arange(0, 1101, 25)
    data = [[r["think"] for r in recs if r["tier"] == t] for t in TIERS]
    ax.hist(data, bins=bins, stacked=True,
            color=[TIER_COLOR[t] for t in TIERS],
            label=[t.capitalize() for t in TIERS], alpha=0.92)
    style(ax, "Reasoning length distribution across 2,700 records",
          xlab="words of reasoning", ylab="records")
    ax.legend(frameon=False, fontsize=11)
    fig.tight_layout()
    fig.savefig(OUT / "think_length_distribution.png", dpi=160)


def chart_final_by_tier(recs):
    """Box plot of final-answer length by tier."""
    data = [[r["final"] for r in recs if r["tier"] == t] for t in TIERS]
    fig, ax = plt.subplots(figsize=(8.5, 5))
    bp = ax.boxplot(data, tick_labels=[t.capitalize() for t in TIERS],
                    patch_artist=True, widths=0.55, showfliers=False,
                    medianprops=dict(color="#222222", linewidth=2),
                    whiskerprops=dict(color="#555555"),
                    capprops=dict(color="#555555"))
    for patch, tier in zip(bp["boxes"], TIERS):
        patch.set_facecolor(TIER_COLOR[tier])
        patch.set_alpha(0.9)
    for i, t in enumerate(TIERS):
        d = data[i]
        ax.text(i + 1, np.percentile(d, 50) + max(d) * 0.03,
                f"median {int(np.median(d))}w", ha="center", fontsize=10,
                color="#333333", fontstyle="italic")
    style(ax, "Final answers carry their reasoning — scaled to tier",
          ylab="words in final answer")
    fig.tight_layout()
    fig.savefig(OUT / "final_answer_by_tier.png", dpi=160)


def chart_domain_depth(domain):
    """One chart per domain: reasoning length by tier within that domain."""
    recs = [r for r in load_records() if r["domain"] == domain]
    data = [[r["think"] for r in recs if r["tier"] == t] for t in TIERS]
    fig, ax = plt.subplots(figsize=(8.5, 5))
    bp = ax.boxplot(data, tick_labels=[t.capitalize() for t in TIERS],
                    patch_artist=True, widths=0.55, showfliers=False,
                    medianprops=dict(color="#222222", linewidth=2),
                    whiskerprops=dict(color="#555555"),
                    capprops=dict(color="#555555"))
    for patch, tier in zip(bp["boxes"], TIERS):
        patch.set_facecolor(DOMAIN_COLOR[domain])
        patch.set_alpha(0.9)
    for i, t in enumerate(TIERS):
        d = data[i]
        ax.text(i + 1, np.percentile(d, 50) + max(d) * 0.03,
                f"median {int(np.median(d))}w", ha="center", fontsize=10,
                color="#333333", fontstyle="italic")
    style(ax, f"{domain.capitalize()} — reasoning depth by tier (900 records)",
          ylab="words of reasoning per record")
    fig.tight_layout()
    fig.savefig(OUT / f"{domain}_depth.png", dpi=160)
    plt.close(fig)


def chart_records_per_file(recs):
    """Horizontal bar: one bar per file, all exactly 100."""
    files = defaultdict(int)
    for r in recs:
        files[(r["domain"], r["tier"])] += 0
    # group by domain+tier file set is uniform; instead show records per file
    per_file = defaultdict(int)
    for r in recs:
        per_file[(r["domain"], r["tier"], r["mode"])] += 1
    labels = [f"{d}/{t}/{m.replace('_', ' ')}" for (d, t, m) in sorted(per_file)]
    vals = [per_file[k] for k in sorted(per_file)]
    fig, ax = plt.subplots(figsize=(8.5, 8))
    colors = [DOMAIN_COLOR[k[0]] for k in sorted(per_file)]
    ax.barh(range(len(vals)), vals, color=colors, alpha=0.9)
    ax.set_yticks(range(len(vals)))
    ax.set_yticklabels(labels, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlim(0, 115)
    ax.axvline(100, color="#333333", linestyle="--", linewidth=1)
    ax.text(100, -0.7, "100 = complete", fontsize=10, color="#333333")
    style(ax, "All 27 files hold exactly 100 records", xlab="records")
    fig.tight_layout()
    fig.savefig(OUT / "records_per_file.png", dpi=160)


def main():
    OUT.mkdir(exist_ok=True)
    plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white"})
    recs = load_records()
    print(f"loaded {len(recs)} records")
    chart_structure_grid(recs)
    chart_depth_by_tier(recs)
    chart_modes(recs)
    chart_think_histogram(recs)
    chart_final_by_tier(recs)
    chart_records_per_file(recs)
    for dom in DOMAINS:
        chart_domain_depth(dom)
    print("charts written to charts/:")
    for p in sorted(OUT.glob("*.png")):
        print(f"  {p.name}")


if __name__ == "__main__":
    main()
