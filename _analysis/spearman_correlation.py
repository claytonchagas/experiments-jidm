import csv
import sys
from pathlib import Path

import pandas as pd
from scipy.stats import spearmanr

ANALYSIS_DIR = Path(__file__).parent
METRICS_TSV = ANALYSIS_DIR / "metrics_pypo.tsv"
GRAPH_METRICS_TSV = ANALYSIS_DIR / "graph_metrics_pypo.tsv"

OUTPUT_CSV = ANALYSIS_DIR / "spearman_correlation_pypo.csv"
OUTPUT_TSV = ANALYSIS_DIR / "spearman_correlation_pypo.tsv"
OUTPUT_MD  = ANALYSIS_DIR / "spearman_correlation_pypo.md"

# Code metrics (modularity indicators) vs Graph metrics
CODE_METRICS = ["NFuncs", "LOC", "NFuncs/LOC", "LOC/F"]
GRAPH_METRICS = ["Nodes", "Edges", "Longest Path", "Components"]


def load_data() -> pd.DataFrame:
    code = pd.read_csv(METRICS_TSV, sep="\t")
    graph = pd.read_csv(GRAPH_METRICS_TSV, sep="\t")

    # Normalize file names for merge: .py -> .dot
    code["merge_key"] = code["Folder"] + "/" + code["File"].str.replace(".py", "", regex=False)
    graph["merge_key"] = graph["folder"] + "/" + graph["file"].str.replace(".dot", "", regex=False)

    df = code.merge(graph, on="merge_key", how="inner")
    return df


def compute_spearman(df: pd.DataFrame) -> list[dict]:
    rows = []
    for code_col in CODE_METRICS:
        for graph_col in GRAPH_METRICS:
            subset = df[[code_col, graph_col]].copy()

            # Convert to numeric, coercing N/A values
            subset[code_col] = pd.to_numeric(subset[code_col], errors="coerce")
            subset[graph_col] = pd.to_numeric(subset[graph_col], errors="coerce")

            # Drop rows with NaN (N/A entries)
            subset = subset.dropna()

            if len(subset) < 3:
                rho, p_val = "N/A", "N/A"
                n = len(subset)
            else:
                rho_val, p_raw = spearmanr(subset[code_col], subset[graph_col])
                rho = round(rho_val, 4)
                p_val = round(p_raw, 4)
                n = len(subset)

            rows.append({
                "Code Metric": code_col,
                "Graph Metric": graph_col,
                "Spearman rho": rho,
                "p-value": p_val,
                "N": n,
                "Significant": "Yes" if isinstance(p_val, float) and p_val < 0.05 else ("N/A" if p_val == "N/A" else "No"),
            })
    return rows


FIELDS = ["Code Metric", "Graph Metric", "Spearman rho", "p-value", "N", "Significant"]


def print_table(rows: list[dict]) -> None:
    col_widths = [len(h) for h in FIELDS]
    for row in rows:
        for i, key in enumerate(FIELDS):
            col_widths[i] = max(col_widths[i], len(str(row[key])))

    sep = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"
    header_line = "| " + " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(FIELDS)) + " |"

    print(sep)
    print(header_line)
    print(sep)
    prev_code = None
    for row in rows:
        if prev_code and row["Code Metric"] != prev_code:
            print(sep)
        values = [str(row[k]) for k in FIELDS]
        line = "| " + " | ".join(v.ljust(col_widths[i]) for i, v in enumerate(values)) + " |"
        print(line)
        prev_code = row["Code Metric"]
    print(sep)


def write_csv(rows: list[dict]) -> None:
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"CSV saved to:      {OUTPUT_CSV}")


def write_tsv(rows: list[dict]) -> None:
    with OUTPUT_TSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(FIELDS)
        for row in rows:
            writer.writerow([row[k] for k in FIELDS])
    print(f"TSV saved to:      {OUTPUT_TSV}")


def write_markdown(rows: list[dict]) -> None:
    col_widths = [len(h) for h in FIELDS]
    for row in rows:
        for i, key in enumerate(FIELDS):
            col_widths[i] = max(col_widths[i], len(str(row[key])))

    def fmt_row(values):
        return "| " + " | ".join(str(v).ljust(col_widths[i]) for i, v in enumerate(values)) + " |"

    separator = "| " + " | ".join("-" * w for w in col_widths) + " |"

    lines = [fmt_row(FIELDS), separator]
    prev_code = None
    for row in rows:
        if prev_code and row["Code Metric"] != prev_code:
            lines.append(fmt_row([""] * len(FIELDS)))
        lines.append(fmt_row([str(row[k]) for k in FIELDS]))
        prev_code = row["Code Metric"]

    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Markdown saved to: {OUTPUT_MD}")


def main():
    df = load_data()
    print(f"Merged data: {len(df)} rows\n")

    if len(df) == 0:
        print("No matching rows between metrics and graph_metrics.", file=sys.stderr)
        sys.exit(1)

    rows = compute_spearman(df)

    print_table(rows)
    print()
    write_csv(rows)
    write_tsv(rows)
    write_markdown(rows)


if __name__ == "__main__":
    main()
