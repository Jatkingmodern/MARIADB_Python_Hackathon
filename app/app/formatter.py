from typing import List, Dict, Any
import math

def human_format_number(n):
    try:
        n = float(n)
    except Exception:
        return str(n)
    if abs(n) >= 1e9:
        return f"{n/1e9:.1f}B"
    if abs(n) >= 1e6:
        return f"{n/1e6:.1f}M"
    if abs(n) >= 1e3:
        return f"{int(n):,}"
    # show two decimals for small numbers
    if abs(n) < 1 and n != 0:
        return f"{n:.2f}"
    if n == int(n):
        return str(int(n))
    return f"{n:.2f}"

def format_result_set(rows: List[Dict[str, Any]], sql: str, max_items: int = 50) -> str:
    """
    Given rows (list of dicts) produce a natural-language summary.
    - If rows are aggregates with 'group_col' and 'metric_sum', produce "Top ... were A with X, B with Y"
    - If rows are single-row count, produce "There are N ..."
    - Otherwise produce a short table summary.
    """
    if not rows:
        return "No matching records found."

    # Detect common patterns
    keys = list(rows[0].keys())
    # Aggregate top-N pattern
    if len(keys) == 2 and "group_col" in keys and ("metric_sum" in keys or "metric" in keys):
        metric_key = "metric_sum" if "metric_sum" in keys else "metric"
        items = []
        for r in rows[:max_items]:
            items.append(f"{r['group_col']} with {human_format_number(r[metric_key])}")
        return "The top results are: " + ", ".join(items) + "."

    # Count-only
    if len(keys) == 1 and keys[0] in ("cnt", "COUNT", "count"):
        v = rows[0][keys[0]]
        return f"Count: {human_format_number(v)}."

    # Generic: produce up to 5-row summary with columns
    limit = min(len(rows), 5)
    header = " | ".join(keys)
    lines = [header]
    for r in rows[:limit]:
        lines.append(" | ".join([human_format_number(r[k]) if isinstance(r[k], (int, float)) else str(r[k]) for k in keys]))
    note = ""
    if len(rows) > limit:
        note = f"\n(Showing {limit} of {len(rows)} rows.)"
    return "Here is a short summary:\n" + "\n".join(lines) + note
