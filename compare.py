import csv
import sys
from collections import deque

# Constants
EXPECTED_HEADERS = ['PC'] + [f'r{i}' for i in range(16)]
PRE_CONTEXT = 10
OUTPUT_FILE = 'full_diff_report.txt'

def stream_trace(filename):
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield {k: row[k] for k in EXPECTED_HEADERS if k in row}

def format_row(label, row):
    fields = [f"{k}={row.get(k, '')}" for k in EXPECTED_HEADERS]
    return f"{label}: " + ", ".join(fields) + "\n"

def compare_traces_streamed(fileA, fileB):
    genA = stream_trace(fileA)
    genB = stream_trace(fileB)

    prevA = deque(maxlen=PRE_CONTEXT)
    prevB = deque(maxlen=PRE_CONTEXT)

    differences = []
    line_num = 0

    for rowA, rowB in zip(genA, genB):
        line_num += 1

        diff_regs = [r for r in EXPECTED_HEADERS if rowA.get(r) != rowB.get(r)]
        if diff_regs:
            differences.append(f"== Difference at line {line_num} ==\n\n")

            differences.append("== Previous 10 instructions from Simulator A ==\n")
            for i, prev_row in enumerate(prevA):
                differences.append(format_row(f"Line {line_num - PRE_CONTEXT + i}", prev_row))
            differences.append("\n")

            differences.append("== Previous 10 instructions from Simulator B ==\n")
            for i, prev_row in enumerate(prevB):
                differences.append(format_row(f"Line {line_num - PRE_CONTEXT + i}", prev_row))
            differences.append("\n")

            differences.append("== Differing instruction Simulator A ==\n")
            differences.append(format_row(f"Line {line_num}", rowA))
            differences.append("\n")

            differences.append("== Differing instruction Simulator B ==\n")
            differences.append(format_row(f"Line {line_num}", rowB))
            differences.append("-" * 60 + "\n")
            break

        prevA.append(rowA)
        prevB.append(rowB)

    if not differences:
        differences.append("No differences found.\n")

    with open(OUTPUT_FILE, 'w') as f:
        f.writelines(differences)

    print(f"{'1 difference' if differences[0].startswith('==') else 'No differences'} written to {OUTPUT_FILE}.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python trace_compare_stream.py simA.csv simB.csv")
        sys.exit(1)

    fileA, fileB = sys.argv[1], sys.argv[2]
    compare_traces_streamed(fileA, fileB)

