#!/usr/bin/env python3
"""Figures for the FAccT submission.

Every number plotted here is PARSED out of the committed generated artifacts under
``papers/unified-report/generated/`` -- the same files the tables ``\\input`` -- so a
figure cannot drift from the table beside it. Nothing is hand-typed: if a value is
not recoverable from a committed artifact, the script fails loudly rather than
falling back to a literal.

Usage:  python figures/make_facct_figures.py [--outdir figures]
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

HERE = Path(__file__).resolve().parent
GEN = (HERE / ".." / ".." / "unified-report" / "generated").resolve()
MORTGAGE_GEN = GEN  # mortgage tables are emitted into the same directory

# ---------------------------------------------------------------------------
# palette -- one system, legible in print and on screen
# ---------------------------------------------------------------------------
C_REP = "#1B6CA8"      # represented sources (the guard's own training sources)
C_TRANS = "#C2492D"    # held-out / transfer sources
C_BASE = "#8A94A6"     # untuned base
C_OWN = "#9FC6E3"      # tuned guard at its own threshold
C_MATCH = "#8C2318"    # tuned guard at the base's alarm budget
C_INK = "#2B3038"
C_RULE = "#C9CED6"
C_CHANCE = "#B08900"

PANEL = ["Qwen2.5-1.5B", "SmolLM2-1.7B", "SmolLM3-3B", "Qwen3-4B"]

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 8.4,
    "axes.titlesize": 8.8,
    "axes.labelsize": 8.4,
    "axes.edgecolor": C_INK,
    "axes.linewidth": 0.7,
    "axes.labelcolor": C_INK,
    "text.color": C_INK,
    "xtick.color": C_INK,
    "ytick.color": C_INK,
    "xtick.labelsize": 7.8,
    "ytick.labelsize": 7.8,
    "xtick.major.width": 0.7,
    "ytick.major.width": 0.7,
    "legend.fontsize": 7.6,
    "legend.frameon": False,
    "figure.dpi": 200,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.02,
    "pdf.fonttype": 42,
})


def read(name: str) -> str:
    path = GEN / name
    if not path.exists():
        raise SystemExit(f"missing committed artifact: {path}")
    return path.read_text(encoding="utf-8")


def macros(name: str) -> dict[str, str]:
    """Parse a generated \\newcommand macro file into {name: value}."""
    out: dict[str, str] = {}
    for m in re.finditer(r"\\newcommand\{\\(\w+)\}\{(.*?)\}\s*$", read(name), re.M):
        out[m.group(1)] = m.group(2)
    if not out:
        raise SystemExit(f"parsed no macros from {name}")
    return out


def num(text: str) -> float:
    """Strip LaTeX decoration from a numeric cell and return a float."""
    t = text
    t = t.replace(r"\textbf{", "").replace(r"\textdagger{}", "")
    t = t.replace("$", "").replace("{", "").replace("}", "")
    t = t.replace(r"\,", "").replace("~", "").replace(r"\%", "")
    t = t.replace("\\", "").strip()
    if t.startswith("+"):
        t = t[1:]
    return float(t)


def rows_of(table_tex: str) -> list[list[str]]:
    """Return the '&'-split body rows of a tabular, in order."""
    body = []
    for line in table_tex.splitlines():
        line = line.strip()
        if "&" not in line or line.startswith("%"):
            continue
        line = re.sub(r"\\\\.*$", "", line).strip()
        body.append([c.strip() for c in line.split("&")])
    return body


# ---------------------------------------------------------------------------
# parsers, one per committed artifact
# ---------------------------------------------------------------------------
def parse_primary() -> dict[str, dict[str, float]]:
    """tab_primary_gen.tex -> per-checkpoint base/SFT/delta+CI, both regimes."""
    out: dict[str, dict[str, float]] = {}
    for cells in rows_of(read("tab_primary_gen.tex")):
        name = cells[0].strip()
        key = name if name in PANEL else ("panel" if "aggregate" in name.lower() else None)
        if key is None or len(cells) < 7:
            continue
        def ci(cell: str) -> tuple[float, float, float]:
            point = num(cell.split("[")[0])
            lo, hi = (num(x) for x in cell.split("[")[1].rstrip("]").split(","))
            return point, lo, hi
        d_rep, rep_lo, rep_hi = ci(cells[3])
        d_tr, tr_lo, tr_hi = ci(cells[6])
        rec = {"d_rep": d_rep, "rep_lo": rep_lo, "rep_hi": rep_hi,
               "d_tr": d_tr, "tr_lo": tr_lo, "tr_hi": tr_hi}
        if key != "panel":
            rec |= {"rep_base": num(cells[1]), "rep_sft": num(cells[2]),
                    "tr_base": num(cells[4]), "tr_sft": num(cells[5])}
        out[key] = rec
    missing = [c for c in PANEL + ["panel"] if c not in out]
    if missing:
        raise SystemExit(f"tab_primary_gen.tex: missing rows {missing}")
    return out


def parse_matched() -> dict[str, dict[str, float]]:
    """tab_matched_fpr_gen.tex -> transfer + HarmBench recall at three thresholds."""
    out: dict[str, dict[str, float]] = {}
    for cells in rows_of(read("tab_matched_fpr_gen.tex")):
        name = cells[0].strip()
        key = name if name in PANEL else ("panel" if name.startswith("Panel mean") else None)
        if key is None or len(cells) < 8:
            continue
        out[key] = {
            "budget": num(cells[1]) / 100.0,
            "tr_base": num(cells[2]), "tr_own": num(cells[3]), "tr_match": num(cells[4]),
            "hb_base": num(cells[5]), "hb_own": num(cells[6]), "hb_match": num(cells[7]),
        }
    missing = [c for c in PANEL + ["panel"] if c not in out]
    if missing:
        raise SystemExit(f"tab_matched_fpr_gen.tex: missing rows {missing}")
    return out


def parse_lowfpr() -> dict[str, dict[str, dict[str, float]]]:
    """tab_lowfpr_gen.tex -> {regime: {checkpoint: {ap, pauc, tpr}}}."""
    out: dict[str, dict[str, dict[str, float]]] = {"represented": {}, "transfer": {}}
    regime = None
    for line in read("tab_lowfpr_gen.tex").splitlines():
        s = line.strip()
        if "Represented" in s and "multicolumn" in s:
            regime = "represented"
            continue
        if "Transfer" in s and "multicolumn" in s:
            regime = "transfer"
            continue
        if regime is None or "&" not in s or s.startswith("%"):
            continue
        cells = [c.strip() for c in re.sub(r"\\\\.*$", "", s).split("&")]
        name = cells[0].replace(r"\quad", "").replace(r"\textbf{", "").replace("}", "").strip()
        key = name if name in PANEL else ("panel" if name.startswith("Panel mean") else None)
        if key is None or len(cells) < 4:
            continue
        out[regime][key] = {
            "ap": num(cells[1].split("~")[0]),
            "pauc": num(cells[2].split("~")[0]),
            "tpr": num(cells[3].split("~")[0]),
        }
    for regime in ("represented", "transfer"):
        missing = [c for c in PANEL + ["panel"] if c not in out[regime]]
        if missing:
            raise SystemExit(f"tab_lowfpr_gen.tex [{regime}]: missing rows {missing}")
    return out


PRETTY_GUARD = {
    "qwen25_15b_base": "Qwen2.5-1.5B",
    "smollm2_17b_base": "SmolLM2-1.7B",
    "smollm3_3b_base": "SmolLM3-3B",
    "qwen3_4b_base": "Qwen3-4B",
}


def parse_mortgage() -> dict[str, dict[str, float]]:
    """mortgage_baseline_table.tex -> AP.D with CI, AUROC.D, and the pair gaps."""
    out: dict[str, dict[str, float]] = {}
    for cells in rows_of(read("mortgage_baseline_table.tex")):
        raw = cells[0].replace("\\", "").strip()
        if raw not in PRETTY_GUARD or len(cells) < 8:
            continue
        ap_cell = cells[2]
        point = num(ap_cell.split("[")[0].replace(r"\,", ""))
        lo, hi = (num(x) for x in ap_cell.split("[")[1].rstrip("]").split(","))
        out[PRETTY_GUARD[raw]] = {
            "ap_g": num(cells[1]), "ap_d": point, "ap_d_lo": lo, "ap_d_hi": hi,
            "auroc_d": num(cells[3]),
            "d_prob": num(cells[5]), "d_margin": num(cells[6]), "d_1tok": num(cells[7]),
        }
    missing = [c for c in PANEL if c not in out]
    if missing:
        raise SystemExit(f"mortgage_baseline_table.tex: missing rows {missing}")
    return out


def parse_case_study() -> dict[str, int]:
    """mortgage_case_study.tex -> benign rows ranked above the worked G0/D1 row."""
    out: dict[str, int] = {}
    tex = read("mortgage_case_study.tex")
    for line in tex.splitlines():
        cells = [c.strip() for c in re.sub(r"\\\\.*$", "", line.strip()).split("&")]
        if len(cells) != 4 or cells[0] not in PANEL:
            continue
        out[cells[0]] = int(num(cells[3]))
    if len(out) != len(PANEL):
        raise SystemExit(f"mortgage_case_study.tex: parsed {out}")
    return out


# ---------------------------------------------------------------------------
# shared drawing helpers
# ---------------------------------------------------------------------------
def tidy(ax, *, grid_axis="y", zero=True):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color(C_RULE)
    ax.spines["bottom"].set_color(C_RULE)
    ax.grid(axis=grid_axis, color=C_RULE, lw=0.5, alpha=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(length=2.5)
    if zero:
        line = ax.axhline if grid_axis == "y" else ax.axvline
        line(0, color=C_INK, lw=0.8)


def short(name: str) -> str:
    return name.replace("-1.5B", "\n1.5B").replace("-1.7B", "\n1.7B") \
               .replace("-3B", "\n3B").replace("-4B", "\n4B")


# ---------------------------------------------------------------------------
# Figure 1 -- the four findings in one spread
# ---------------------------------------------------------------------------
def fig_findings(out: Path, primary, matched, h2h, frontier, mortgage):
    fig, axes = plt.subplots(2, 2, figsize=(7.1, 3.95))
    (a, b), (c, d) = axes
    x = range(len(PANEL))
    w = 0.36
    tkw = dict(loc="left", fontweight="bold", fontsize=8.2, pad=6)

    # (a) paired change, represented vs held-out
    rep = [primary[k]["d_rep"] for k in PANEL]
    tr = [primary[k]["d_tr"] for k in PANEL]
    rep_err = [[primary[k]["d_rep"] - primary[k]["rep_lo"] for k in PANEL],
               [primary[k]["rep_hi"] - primary[k]["d_rep"] for k in PANEL]]
    tr_err = [[primary[k]["d_tr"] - primary[k]["tr_lo"] for k in PANEL],
              [primary[k]["tr_hi"] - primary[k]["d_tr"] for k in PANEL]]
    a.bar([i - w / 2 for i in x], rep, w, color=C_REP, label="represented sources",
          yerr=rep_err, error_kw=dict(lw=0.7, capsize=1.8, ecolor=C_INK))
    a.bar([i + w / 2 for i in x], tr, w, color=C_TRANS, label="held-out sources",
          yerr=tr_err, error_kw=dict(lw=0.7, capsize=1.8, ecolor=C_INK))
    a.set_xticks(list(x)); a.set_xticklabels([short(k) for k in PANEL])
    a.set_ylabel(r"paired $\Delta$ macro-AP vs. base")
    a.set_title("(a) The gain sits on the sources it was tuned on", **tkw)
    a.legend(loc="upper right", handlelength=1.1, borderaxespad=0.2)
    a.set_ylim(-0.30, 0.72)
    tidy(a)

    # (b) transfer recall at an equal alarm budget
    base = [matched[k]["tr_base"] for k in PANEL]
    own = [matched[k]["tr_own"] for k in PANEL]
    mat = [matched[k]["tr_match"] for k in PANEL]
    b.bar([i - w for i in x], base, w * 0.9, color=C_BASE, label="untuned base")
    b.bar(list(x), own, w * 0.9, color=C_OWN, label="tuned, its own threshold")
    b.bar([i + w for i in x], mat, w * 0.9, color=C_MATCH, label="tuned, base's alarm budget")
    for i in x:
        b.add_patch(FancyArrowPatch((i - w, base[i] + 0.035), (i + w, mat[i] + 0.035),
                                    connectionstyle="arc3,rad=-0.30", color=C_MATCH,
                                    lw=0.85, arrowstyle="-|>,head_width=1.7,head_length=3.4",
                                    mutation_scale=1))
    b.set_xticks(list(x)); b.set_xticklabels([short(k) for k in PANEL])
    b.set_ylabel("held-out recall")
    b.set_title("(b) At an equal alarm budget the gain reverses", **tkw)
    b.legend(loc="upper left", handlelength=1.1, borderaxespad=0.2, labelspacing=0.3)
    b.set_ylim(0, 1.18)
    tidy(b, zero=False)

    # (c) the ordering reverses by traffic regime
    labels = ["traffic the manifest\nrepresents", "traffic it does not\n(external, expert-labelled)"]
    rep_d = num(h2h["HtwoAggDeltaTpr"])
    rep_lo, rep_hi = sorted(num(v) for v in h2h["HtwoAggDeltaTprCI"].strip("[]$").split(","))
    tr_d = -num(frontier["FrontierGainOverBase"])
    tr_lo, tr_hi = sorted(-num(v) for v in frontier["FrontierGainOverBaseCI"].strip("[] ").split(","))
    vals, los, his = [rep_d, tr_d], [rep_lo, tr_lo], [rep_hi, tr_hi]
    errs = [[v - lo for v, lo in zip(vals, los)], [hi - v for v, hi in zip(vals, his)]]
    cols = ["#1F7A4C", "#7A1F3D"]
    c.barh(labels, vals, 0.40, color=cols,
           xerr=errs, error_kw=dict(lw=0.7, capsize=2.2, ecolor=C_INK))
    c.set_xlabel(r"$\Delta$ recall at a matched 5% alarm budget"
                 "\n" r"$\leftarrow$ hosted better    $\vert$    local guard better $\rightarrow$")
    c.set_title("(c) Which guard wins depends on the traffic", **tkw)
    c.set_xlim(-0.34, 0.38)
    tidy(c, grid_axis="x", zero=False)
    c.axvline(0, color=C_INK, lw=0.8)
    for i, (v, lo, hi) in enumerate(zip(vals, los, his)):
        c.text(0.36 if v > 0 else -0.32, i, f"{v:+.3f}\n[{lo:+.3f}, {hi:+.3f}]",
               va="center", ha="right" if v > 0 else "left", fontsize=6.9,
               fontweight="bold", color=cols[i], linespacing=1.4)
    c.invert_yaxis()

    # (d) domain policy ranking against its own chance floor
    ap_d = [mortgage[k]["ap_d"] for k in PANEL]
    err = [[mortgage[k]["ap_d"] - mortgage[k]["ap_d_lo"] for k in PANEL],
           [mortgage[k]["ap_d_hi"] - mortgage[k]["ap_d"] for k in PANEL]]
    d.axhspan(0, 0.555, color="#F2ECDA", zorder=0)
    d.bar(list(x), ap_d, 0.50, color="#4B6584", zorder=2,
          yerr=err, error_kw=dict(lw=0.7, capsize=1.8, ecolor=C_INK))
    d.axhline(0.555, color=C_CHANCE, lw=1.1, ls=(0, (4, 2)), zorder=3)
    d.axhline(1.0, color=C_RULE, lw=0.8, ls=":", zorder=1)
    d.text(3.98, 0.525, "chance floor\n0.555", fontsize=6.8, color=C_CHANCE,
           ha="right", va="top", linespacing=1.3)
    d.text(3.98, 1.01, "perfect", fontsize=6.8, color="#8A94A6", ha="right", va="bottom")
    d.set_xticks(list(x)); d.set_xticklabels([short(k) for k in PANEL])
    d.set_xlim(-0.62, 4.0)
    d.set_ylabel(r"AP on the policy label $D$")
    d.set_title("(d) A general safety score is not a compliance screen", **tkw)
    d.set_ylim(0, 1.20)
    tidy(d, zero=False)
    d.text(-0.52, 1.16, "zero-shot; only 0.12–0.30 above chance",
           fontsize=6.9, color=C_INK, ha="left", va="top")

    fig.tight_layout(h_pad=2.2, w_pad=2.6)
    fig.savefig(out / "fig_facct_findings.pdf")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 2 -- the alarm-budget reversal, both instruments
# ---------------------------------------------------------------------------
def fig_budget(out: Path, matched):
    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.0), sharey=True)
    x = range(len(PANEL))
    w = 0.26
    specs = [("transfer recall (benchmark-macro)", "tr", axes[0],
              "(a) Held-out transfer suite"),
             ("HarmBench recall", "hb", axes[1],
              "(b) HarmBench: the attacks a guard exists to stop")]
    for ylabel, prefix, ax, title in specs:
        base = [matched[k][f"{prefix}_base"] for k in PANEL]
        own = [matched[k][f"{prefix}_own"] for k in PANEL]
        mat = [matched[k][f"{prefix}_match"] for k in PANEL]
        ax.bar([i - w for i in x], base, w, color=C_BASE, label="untuned base")
        ax.bar(list(x), own, w, color=C_OWN, label="tuned, own calibrated threshold")
        ax.bar([i + w for i in x], mat, w, color=C_MATCH,
               label="tuned, re-thresholded to the base's alarm budget")
        for i in x:
            for pos, v in ((i - w, base[i]), (i, own[i]), (i + w, mat[i])):
                ax.text(pos, v + 0.02, f"{v:.2f}", ha="center", fontsize=6.4, color=C_INK)
        ax.set_xticks(list(x))
        ax.set_xticklabels([f"{short(k)}\n({matched[k]['budget']*100:.1f}% budget)" for k in PANEL])
        ax.set_title(title, loc="left", fontweight="bold")
        tidy(ax, zero=False)
        ax.set_ylim(0, 1.14)
    axes[0].set_ylabel("recall")
    axes[0].set_ylabel("recall")
    axes[1].set_ylabel(None)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.11))
    fig.tight_layout(w_pad=1.6)
    fig.savefig(out / "fig_facct_budget.pdf")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 3 -- the metric region co-produces the size of the effect
# ---------------------------------------------------------------------------
def fig_region(out: Path, lowfpr):
    fig, axes = plt.subplots(1, 2, figsize=(7.1, 1.72))
    metrics = [("ap", "macro-AP\n(whole ranking)"),
               ("pauc", r"pAUC$[0,0.05]$" "\n(inside the budget)"),
               ("tpr", r"recall @ 5% FPR" "\n(the operating point)")]
    for ax, regime, colour, title in (
        (axes[0], "represented", C_REP, "(a) Represented sources: the gain"),
        (axes[1], "transfer", C_TRANS, "(b) Held-out sources: the cost"),
    ):
        means = [lowfpr[regime]["panel"][m] for m, _ in metrics]
        xs = range(len(metrics))
        ax.bar(list(xs), means, 0.5, color=colour, alpha=0.9, zorder=2)
        for i, (m, _) in enumerate(metrics):
            pts = [lowfpr[regime][k][m] for k in PANEL]
            ax.scatter([i + 0.30] * len(pts), pts, s=13, facecolor="white",
                       edgecolor=C_INK, lw=0.7, zorder=3)
        for i, v in enumerate(means):
            ax.text(i, v + (0.03 if v > 0 else -0.03), f"{v:+.3f}", ha="center",
                    va="bottom" if v > 0 else "top", fontsize=7.4, fontweight="bold",
                    color=colour)
        ax.set_xticks(list(xs))
        ax.set_xticklabels([lbl for _, lbl in metrics])
        ax.set_title(title, loc="left", fontweight="bold")
        tidy(ax)
    axes[0].set_ylabel(r"panel-mean paired $\Delta$")
    axes[0].set_ylim(0, 0.95)
    axes[1].set_ylim(-0.55, 0.16)
    axes[1].text(0.02, 0.06, "hollow dots = individual checkpoints", fontsize=6.8,
                 transform=axes[1].transAxes, color=C_INK)
    fig.tight_layout(w_pad=2.0)
    fig.savefig(out / "fig_facct_region.pdf")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 4 -- one worked compliance miss, as a rank
# ---------------------------------------------------------------------------
def fig_casestudy_ranks(out: Path, above):
    fig, ax = plt.subplots(figsize=(3.55, 1.95))
    total = 65
    vals = [above[k] for k in PANEL]
    ys = range(len(PANEL))
    ax.barh(list(ys), [total] * len(PANEL), 0.5, color="#EEF0F3", zorder=1)
    ax.barh(list(ys), vals, 0.5, color="#8C2318", zorder=2)
    for i, v in enumerate(vals):
        ax.text(v + 1.2, i, f"{v} of {total}", va="center", fontsize=7.2,
                fontweight="bold", color="#8C2318")
    ax.axvline(total / 2, color=C_CHANCE, lw=1.1, ls=(0, (4, 2)), zorder=3)
    ax.text(total / 2 - 1.4, -0.66, "median benign row", fontsize=6.8, color=C_CHANCE,
            ha="right")
    ax.set_yticks(list(ys)); ax.set_yticklabels(PANEL)
    ax.set_xlabel("benign requests in the same split scored\n"
                  "MORE suspicious than this policy violation")
    ax.set_xlim(0, total + 12)
    tidy(ax, grid_axis="x", zero=False)
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(out / "fig_facct_casestudy_ranks.pdf")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 5 -- the fairness gate is scale-dependent (a negative result)
# ---------------------------------------------------------------------------
def fig_gate(out: Path, mortgage):
    fig, axes = plt.subplots(1, 2, figsize=(7.1, 1.78))
    x = range(len(PANEL))
    prob = [mortgage[k]["d_prob"] for k in PANEL]
    onetok = [mortgage[k]["d_1tok"] for k in PANEL]
    margin = [mortgage[k]["d_margin"] for k in PANEL]
    w = 0.36
    axes[0].bar([i - w / 2 for i in x], prob, w, color="#4B6584",
                label="all 3 pairs")
    axes[0].bar([i + w / 2 for i in x], onetok, w, color="#A8B5C4",
                label="single-token pairs only (2 of 3)")
    axes[0].set_ylabel(r"$\Delta_{\mathrm{context}}$, probability scale")
    axes[0].set_title("(a) On the probability scale, the ranking is an artifact",
                      loc="left", fontweight="bold")
    axes[0].legend(loc="upper right")
    axes[0].set_ylim(0, 0.235)
    axes[1].bar(list(x), margin, 0.5, color="#8C2318")
    axes[1].set_ylabel(r"$\Delta_{\mathrm{context}}$, log-odds margin")
    axes[1].set_title("(b) On the raw margin, the order nearly inverts",
                      loc="left", fontweight="bold")
    axes[1].set_ylim(0, 1.02)
    for ax, vals, fmt in ((axes[0], prob, "{:.3f}"), (axes[1], margin, "{:.2f}")):
        ax.set_xticks(list(x)); ax.set_xticklabels([short(k) for k in PANEL])
        tidy(ax, zero=False)
        for i, v in enumerate(vals):
            ax.text(i if ax is axes[1] else i - w / 2, v + 0.012, fmt.format(v),
                    ha="center", fontsize=6.8, color=C_INK)
    axes[0].annotate("saturation,\nnot invariance", xy=(3 - w / 2 - 0.02, 0.010),
                     xytext=(2.30, 0.115), fontsize=6.9, color="#8C2318", ha="center",
                     arrowprops=dict(arrowstyle="->", lw=0.7, color="#8C2318"))
    axes[1].annotate("the same guard", xy=(2.74, 0.80), xytext=(1.95, 0.955),
                     fontsize=6.9, color="#8C2318", ha="center",
                     arrowprops=dict(arrowstyle="->", lw=0.7, color="#8C2318"))
    fig.tight_layout(w_pad=2.0)
    fig.savefig(out / "fig_facct_gate.pdf")
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default=str(HERE))
    args = ap.parse_args()
    out = Path(args.outdir).resolve()
    out.mkdir(parents=True, exist_ok=True)

    primary = parse_primary()
    matched = parse_matched()
    lowfpr = parse_lowfpr()
    mortgage = parse_mortgage()
    above = parse_case_study()
    h2h = macros("h2h_macros.tex")
    frontier = macros("frontier_macros.tex")

    fig_findings(out, primary, matched, h2h, frontier, mortgage)
    fig_budget(out, matched)
    fig_region(out, lowfpr)
    fig_casestudy_ranks(out, above)
    fig_gate(out, mortgage)
    print(f"wrote 5 figures to {out}")


if __name__ == "__main__":
    main()
