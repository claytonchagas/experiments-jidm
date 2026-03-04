import ast
import csv
import sys
from pathlib import Path

WORKSPACE = Path(__file__).parent.parent
FOLDERS_FILE = WORKSPACE / "folders.txt"
OUTPUT_CSV = Path(__file__).parent / "metrics_pypo.csv"
OUTPUT_MD = Path(__file__).parent / "metrics_pypo.md"
OUTPUT_TSV = Path(__file__).parent / "metrics_pypo.tsv"

EXCLUDE_FILES = {"fatoracao_lu.py", "heat_map.py", "model.py", "solver.py"}


def count_functions(source: str) -> int:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return 0
    return sum(
        1 for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    )


def count_loc(source: str) -> int:
    count = 0
    for line in source.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            count += 1
    return count


def compute_metrics(py_file: Path) -> dict:
    source = py_file.read_text(encoding="utf-8", errors="replace")
    nfuncs = count_functions(source)
    loc = count_loc(source)
    nfuncs_per_loc = round(nfuncs / loc, 4) if loc > 0 else 0
    loc_per_f = round(loc / nfuncs, 4) if nfuncs > 0 else "N/A"
    return {
        "NFuncs": nfuncs,
        "LOC": loc,
        "NFuncs/LOC": nfuncs_per_loc,
        "LOC/F": loc_per_f,
    }


def read_folders() -> list[Path]:
    folders = []
    for line in FOLDERS_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip().rstrip("/\\")
        if line:
            folders.append(WORKSPACE / line)
    return folders


def collect_files(folders: list[Path]) -> list[tuple[str, Path]]:
    result = []
    for folder in folders:
        for py_file in sorted(folder.glob("*.py")):
            if py_file.name not in EXCLUDE_FILES:
                result.append((folder.name, py_file))
    return result


def print_table(rows: list[dict]) -> None:
    headers = ["Folder", "File", "NFuncs", "LOC", "NFuncs/LOC", "LOC/F"]
    col_widths = [len(h) for h in headers]

    for row in rows:
        values = [
            row["folder"], row["file"],
            str(row["NFuncs"]), str(row["LOC"]),
            str(row["NFuncs/LOC"]), str(row["LOC/F"]),
        ]
        for i, v in enumerate(values):
            col_widths[i] = max(col_widths[i], len(v))

    sep = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"
    header_line = "| " + " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers)) + " |"

    print(sep)
    print(header_line)
    print(sep)
    for row in rows:
        values = [
            row["folder"], row["file"],
            str(row["NFuncs"]), str(row["LOC"]),
            str(row["NFuncs/LOC"]), str(row["LOC/F"]),
        ]
        line = "| " + " | ".join(v.ljust(col_widths[i]) for i, v in enumerate(values)) + " |"
        print(line)
    print(sep)


def write_csv(rows: list[dict]) -> None:
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["folder", "file", "NFuncs", "LOC", "NFuncs/LOC", "LOC/F"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"CSV saved to: {OUTPUT_CSV}")


def write_markdown(rows: list[dict]) -> None:
    headers = ["Folder", "File", "NFuncs", "LOC", "NFuncs/LOC", "LOC/F"]
    keys = ["folder", "file", "NFuncs", "LOC", "NFuncs/LOC", "LOC/F"]

    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, key in enumerate(keys):
            col_widths[i] = max(col_widths[i], len(str(row[key])))

    def fmt_row(values):
        return "| " + " | ".join(str(v).ljust(col_widths[i]) for i, v in enumerate(values)) + " |"

    separator = "| " + " | ".join("-" * w for w in col_widths) + " |"

    lines = [
        fmt_row(headers),
        separator,
    ]

    prev_folder = None
    for row in rows:
        if prev_folder and row["folder"] != prev_folder:
            lines.append(fmt_row([""] * len(keys)))
        lines.append(fmt_row([str(row[k]) for k in keys]))
        prev_folder = row["folder"]

    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Markdown saved to: {OUTPUT_MD}")


def write_tsv(rows: list[dict]) -> None:
    OUTPUT_TSV.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_TSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["Folder", "File", "NFuncs", "LOC", "NFuncs/LOC", "LOC/F"])
        for row in rows:
            writer.writerow([row[k] for k in ["folder", "file", "NFuncs", "LOC", "NFuncs/LOC", "LOC/F"]])
    print(f"TSV saved to:      {OUTPUT_TSV}")


def main():
    folders = read_folders()
    files = collect_files(folders)

    if not files:
        print("No Python files found.", file=sys.stderr)
        sys.exit(1)

    rows = []
    for folder_name, py_file in files:
        metrics = compute_metrics(py_file)
        rows.append({
            "folder": folder_name,
            "file": py_file.name,
            **metrics,
        })

    print_table(rows)
    write_csv(rows)
    write_markdown(rows)
    write_tsv(rows)


if __name__ == "__main__":
    main()
