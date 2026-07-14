"""Run every solver on a fixed set of levels and export report-ready CSV data."""

import argparse
import csv
import re
from pathlib import Path
from statistics import mean

from algorithms.solver import solve
from block import Block
from board import Board


ALGORITHMS = ("BFS", "IDS", "UCS", "ASTAR")


def level_number(path):
    match = re.search(r"\d+", path.stem)
    return int(match.group()) if match else 999999


def run_level(level_path, algorithm, repeats):
    results = []
    for _ in range(repeats):
        board = Board(level_path)
        results.append(solve(board, Block(*board.start), algorithm))

    first = results[0]
    return {
        "level": level_path.stem,
        "algorithm": algorithm,
        "found": first.found,
        "solution_length": first.steps,
        "solution_cost": f"{first.solution_cost:.2f}",
        "expanded_nodes": round(mean(item.expanded_nodes for item in results), 2),
        "generated_nodes": round(mean(item.generated_nodes for item in results), 2),
        "peak_frontier": round(mean(item.peak_frontier for item in results), 2),
        "search_time_ms": round(mean(item.search_time for item in results) * 1000, 6),
        "peak_memory_mb": round(mean(item.memory_usage_mb for item in results), 6),
        "path": " ".join(first.path),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maps", default="maps", help="Thư mục chứa level JSON")
    parser.add_argument("--repeats", type=int, default=5, help="Số lần đo mỗi cấu hình")
    parser.add_argument(
        "--output",
        default="output/experiments.csv",
        help="File CSV kết quả",
    )
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error("--repeats phải lớn hơn 0")

    level_paths = sorted(Path(args.maps).glob("*.json"), key=level_number)
    if not level_paths:
        parser.error(f"Không tìm thấy level trong {args.maps}")

    rows = [
        run_level(level_path, algorithm, args.repeats)
        for level_path in level_paths
        for algorithm in ALGORITHMS
    ]
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8-sig") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Đã ghi {len(rows)} dòng vào {output_path}")


if __name__ == "__main__":
    main()
