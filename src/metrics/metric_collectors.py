import csv
from collections import Counter
from pathlib import Path
from typing import Any

def artifact_exists(path:Path)->bool:
    return Path(path).exists()

def count_vcf_records(vcf_path:Path)->int:
    path=Path(vcf_path)
    if not path.exists():
        raise FileNotFoundError(f"VCF not found: {path}")
    count=0
    with path.open("r",encoding="utf-8",errors="replace") as handle:
        for line in handle:
            if line.startswith("#"):
                continue
            if line.strip():
                count+=1
    return count

def count_tsv_rows(tsv_path:Path)->int:
    path=Path(tsv_path)
    if not path.exists():
        raise FileNotFoundError(f"TSV not found: {path}")
    with path.open("r",encoding="utf-8",errors="replace",newline="") as handle:
        reader=csv.reader(handle,delimiter="\t")
        try:
            next(reader)
        except StopIteration:
            return 0
        return sum(1 for row in reader if row)

def get_tsv_header(tsv_path:Path)->list[str]:
    path=Path(tsv_path)
    if not path.exists():
        raise FileNotFoundError(f"TSV not found: {path}")
    with path.open("r",encoding="utf-8",errors="replace",newline="") as handle:
        reader=csv.reader(handle,delimiter="\t")
        try:
            return next(reader)
        except StopIteration:
            return []

def count_column_values(tsv_path:Path,column:str)->dict[str,int]:
    path=Path(tsv_path)
    if not path.exists():
        raise FileNotFoundError(f"TSV not found: {path}")
    counts=Counter()
    with path.open("r",encoding="utf-8",errors="replace",newline="") as handle:
        reader=csv.DictReader(handle,delimiter="\t")
        if column not in (reader.fieldnames or []):
            raise ValueError(f"Column not found in {path}: {column}")
        for row in reader:
            value=row.get(column,"")
            if value is None or value=="":
                value="missing"
            counts[str(value)]+=1
    return dict(sorted(counts.items()))

def count_unique_values(tsv_path:Path,column:str)->int:
    path=Path(tsv_path)
    if not path.exists():
        raise FileNotFoundError(f"TSV not found: {path}")
    values=set()
    with path.open("r",encoding="utf-8",errors="replace",newline="") as handle:
        reader=csv.DictReader(handle,delimiter="\t")
        if column not in (reader.fieldnames or []):
            raise ValueError(f"Column not found in {path}: {column}")
        for row in reader:
            value=row.get(column,"")
            if value not in ("",None):
                values.add(value)
    return len(values)

def count_exact_string_distribution(tsv_path:Path,column:str)->dict[str,int]:
    path=Path(tsv_path)
    if not path.exists():
        raise FileNotFoundError(f"TSV not found: {path}")

    counts=Counter()

    with path.open("r",encoding="utf-8",errors="replace",newline="") as handle:
        reader=csv.DictReader(handle,delimiter="\t")

        if column not in (reader.fieldnames or []):
            raise ValueError(f"Column not found in {path}: {column}")

        for row in reader:
            value=row.get(column,"")

            if value is None:
                value="missing"

            value=str(value).strip()

            if value=="":
                value="missing"

            counts[value]+=1

    return dict(sorted(counts.items()))

def count_binned_population_frequency(tsv_path:Path,column:str)->dict[str,int]:
    path=Path(tsv_path)

    if not path.exists():
        raise FileNotFoundError(f"TSV not found: {path}")

    counts=Counter()

    with path.open("r",encoding="utf-8",errors="replace",newline="") as handle:
        reader=csv.DictReader(handle,delimiter="\t")

        if column not in (reader.fieldnames or []):
            raise ValueError(f"Column not found in {path}: {column}")

        for row in reader:
            raw=row.get(column,"")

            if raw is None:
                counts["missing"]+=1
                continue

            raw=str(raw).strip()

            if raw=="" or raw.upper()=="NA":
                counts["missing"]+=1
                continue

            try:
                af=float(raw)
            except ValueError:
                counts["missing"]+=1
                continue

            if af < 0.01:
                counts["rare"]+=1
            elif af < 0.05:
                counts["low_frequency"]+=1
            else:
                counts["common"]+=1

    return dict(sorted(counts.items()))

def safe_exact_string_distribution(tsv_path:Path,column:str)->tuple[str,Any]:
    path=Path(tsv_path)

    if not path.exists():
        return "source_missing","not_available"

    header=get_tsv_header(path)

    if column not in header:
        return "not_available","not_available"

    return "available",count_exact_string_distribution(path,column)

def safe_binned_population_frequency(tsv_path:Path,column:str)->tuple[str,Any]:
    path=Path(tsv_path)

    if not path.exists():
        return "source_missing","not_available"

    header=get_tsv_header(path)

    if column not in header:
        return "not_available","not_available"

    return "available",count_binned_population_frequency(path,column)

def safe_count_vcf_records(vcf_path:Path)->tuple[str,Any]:
    path=Path(vcf_path)
    if not path.exists():
        return "source_missing","not_available"
    return "available",count_vcf_records(path)

def safe_count_tsv_rows(tsv_path:Path)->tuple[str,Any]:
    path=Path(tsv_path)
    if not path.exists():
        return "source_missing","not_available"
    return "available",count_tsv_rows(path)

def safe_count_column_values(tsv_path:Path,column:str)->tuple[str,Any]:
    path=Path(tsv_path)
    if not path.exists():
        return "source_missing","not_available"
    header=get_tsv_header(path)
    if column not in header:
        return "not_available","not_available"
    return "available",count_column_values(path,column)

