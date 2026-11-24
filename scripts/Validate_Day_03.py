"""Read-only checks for the small Northstar Day 3 datasets and Delta tables."""
from pathlib import Path
from datetime import date, datetime
from decimal import Decimal
import hashlib
import json
import re

def canonical_hash(records, columns):
    def value(x):
        if x is None or x == "":
            return None
        if isinstance(x, (date, datetime)):
            return x.isoformat()
        return str(x)
    rows = [[value(r[c]) for c in columns] for r in records]
    rows.sort(key=lambda r: json.dumps(r, ensure_ascii=False, separators=(",", ":")))
    payload = json.dumps(rows, ensure_ascii=False, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()

def check_records(name, records, schema, expected):
    expected_schema = expected["schemas"][name]
    assert schema == expected_schema, f"{name}: schema differs: {schema}"
    count_key = {"sales_bronze": "sales_bronze_rows",
                 "sales_silver": "sales_silver_rows",
                 "sales_by_store": "gold_store_count"}[name]
    assert len(records) == expected[count_key], f"{name}: wrong row count"
    columns = [x[0] for x in expected_schema]
    assert canonical_hash(records, columns) == expected["content_sha256"][name], (
        f"{name}: row values or duplicate multiplicities differ")
    if name == "sales_by_store":
        assert sum(r["TransactionCount"] for r in records) == expected["transaction_count"]
        assert sum(r["TotalQuantity"] for r in records) == expected["total_quantity"]
        assert sum(r["TotalRevenue"] for r in records) == Decimal(expected["total_revenue"])
        for r in records:
            target = expected["store_results"][r["StoreID"]]
            assert r["TransactionCount"] == target["TransactionCount"]
            assert r["TotalRevenue"] == Decimal(target["TotalRevenue"])

def validate_day03(spark, catalog, schema, source_root):
    for name in (catalog, schema):
        assert re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name), "Invalid identifier"
    assert schema.startswith("northstar_"), "Use the personal schema"
    root = Path(source_root)
    expected = json.loads((root / "expected_results.json").read_text(encoding="utf-8"))
    for filename, digest in expected["source_sha256"].items():
        assert hashlib.sha256((root / filename).read_bytes()).hexdigest() == digest, (
            f"Source file differs: {filename}")
    for name, count_key in [("sales_bronze", "sales_bronze_rows"),
                            ("sales_silver", "sales_silver_rows"),
                            ("sales_by_store", "gold_store_count")]:
        full_name = f"`{catalog}`.`{schema}`.`{name}`"
        frame = spark.table(full_name)
        detail = spark.sql(f"DESCRIBE DETAIL {full_name}").first()
        assert detail["format"].lower() == "delta", f"{name}: expected Delta"
        actual_schema = [[f.name, f.dataType.simpleString()] for f in frame.schema.fields]
        # Bounded collection is deliberate: this exercise has at most 112 rows.
        records = [r.asDict() for r in frame.limit(expected[count_key] + 1).collect()]
        check_records(name, records, actual_schema, expected)
        print(f"PASS {name}: schema, rows and values match")
    print("PASS Day 3: Bronze 112; Silver 96; Gold 4; revenue 2680.90")
