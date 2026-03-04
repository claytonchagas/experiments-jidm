import csv
import re
import sys
from pathlib import Path

import networkx as nx

WORKSPACE = Path(__file__).parent.parent
FOLDERS_FILE = WORKSPACE / "folders.txt"
OUTPUT_CSV = Path(__file__).parent / "graph_metrics_pypo.csv"
OUTPUT_TSV = Path(__file__).parent / "graph_metrics_pypo.tsv"
OUTPUT_MD  = Path(__file__).parent / "graph_metrics_pypo.md"

FIELDS = ["folder", "file", "Nodes", "Edges", "Longest Path", "Components"]


def read_folders() -> list[Path]:
    folders = []
    for line in FOLDERS_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip().rstrip("/\\")
        if line:
            folders.append(WORKSPACE / line)
    return folders


def collect_dot_files(folders: list[Path]) -> list[tuple[str, Path]]:
    result = []
    for folder in folders:
        dataflows = folder / "dataflows"
        if dataflows.is_dir():
            for dot_file in sorted(dataflows.rglob("*.dot")):
                result.append((folder.name, dot_file))
    return result


def parse_dot(path: Path) -> nx.DiGraph:
    G = nx.DiGraph()
    text = path.read_text(encoding="utf-8", errors="replace")
    for line in text.splitlines():
        # Node declarations: e_123 [...]
        node_match = re.match(r'^\s+(e_\w+)\s*\[', line)
        if node_match:
            G.add_node(node_match.group(1))
            continue
        # Edge declarations: e_123 -> e_456
        edge_matches = re.findall(r'(e_\w+)\s*->\s*(e_\w+)', line)
        for src, dst in edge_matches:
            G.add_edge(src, dst)
    return G


def compute_graph_metrics(G: nx.DiGraph) -> dict:
    nodes = G.number_of_nodes()
    edges = G.number_of_edges()

    if nx.is_directed_acyclic_graph(G):
        longest_path = nx.dag_longest_path_length(G)
    else:
        longest_path = "N/A (cycle)"

    components = nx.number_weakly_connected_components(G)

    return {
        "Nodes": nodes,
        "Edges": edges,
        "Longest Path": longest_path,
        "Components": components,
    }


def print_table(rows: list[dict]) -> None:
    headers = FIELDS[:]
    col_widths = [len(h) for h in headers]

    for row in rows:
        values = [str(row[k]) for k in FIELDS]
        for i, v in enumerate(values):
            col_widths[i] = max(col_widths[i], len(v))

    sep = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"
    header_line = "| " + " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers)) + " |"

    print(sep)
    print(header_line)
    print(sep)
    for row in rows:
        values = [str(row[k]) for k in FIELDS]
        line = "| " + " | ".join(v.ljust(col_widths[i]) for i, v in enumerate(values)) + " |"
        print(line)
    print(sep)


def write_csv(rows: list[dict]) -> None:
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"CSV saved to:      {OUTPUT_CSV}")


def write_tsv(rows: list[dict]) -> None:
    OUTPUT_TSV.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_TSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(FIELDS)
        for row in rows:
            writer.writerow([row[k] for k in FIELDS])
    print(f"TSV saved to:      {OUTPUT_TSV}")


def write_markdown(rows: list[dict]) -> None:
    headers = FIELDS[:]
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, key in enumerate(FIELDS):
            col_widths[i] = max(col_widths[i], len(str(row[key])))

    def fmt_row(values):
        return "| " + " | ".join(str(v).ljust(col_widths[i]) for i, v in enumerate(values)) + " |"

    separator = "| " + " | ".join("-" * w for w in col_widths) + " |"

    lines = [fmt_row(headers), separator]
    prev_folder = None
    for row in rows:
        if prev_folder and row["folder"] != prev_folder:
            lines.append(fmt_row([""] * len(FIELDS)))
        lines.append(fmt_row([str(row[k]) for k in FIELDS]))
        prev_folder = row["folder"]

    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Markdown saved to: {OUTPUT_MD}")


def main():
    folders = read_folders()
    files = collect_dot_files(folders)

    if not files:
        print("No .dot files found.", file=sys.stderr)
        sys.exit(1)

    rows = []
    for folder_name, dot_file in files:
        G = parse_dot(dot_file)
        metrics = compute_graph_metrics(G)
        rows.append({"folder": folder_name, "file": dot_file.name, **metrics})

    print_table(rows)
    write_csv(rows)
    write_tsv(rows)
    write_markdown(rows)


if __name__ == "__main__":
    main()
