import subprocess
import json
from pathlib import Path

download_dir = Path("neo_graph_download")

# Find the nodes file (filename ends with '_nodes.tsv' and _egdes.tsv)
nodes_files = list(download_dir.glob("*_nodes.tsv"))
if not nodes_files:
    raise FileNotFoundError("No *_nodes.tsv file found in neo_graph_download/")
nodes_file = nodes_files[0]

edges_files = list(download_dir.glob("*_edges.tsv"))
if not edges_files:
    raise FileNotFoundError("No *_edges.tsv file found in neo_graph_download/")
edges_file = edges_files[0]

print(f"[INFO] Using nodes file: {nodes_file}")
print(f"[INFO] Using edges file: {edges_file}")

# Define report output path
report_file = Path("reports/validation_report.json")
report_file.parent.mkdir(exist_ok=True)

# Prepare the command
cmd = [
    "kgx", "validate",
    "--input-format", "tsv",
    str(nodes_file),
    str(edges_file),
]

print("[INFO] Running KGX validation...")
result = subprocess.run(cmd, capture_output=True, text=True)

# Try to parse JSON output and save to a file
try:
    json_data = json.loads(result.stderr)
    with open(report_file, "w") as f:
        json.dump(json_data, f, indent=2)
    print(f"[✅] Validation complete. Report saved to {report_file}")
except json.JSONDecodeError:
    print("[❌] Validation output was not JSON or validation failed.")
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
