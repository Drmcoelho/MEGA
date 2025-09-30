"""
Prepara dataset educacional para fine-tuning (formato JSONL).
Entrada:
  data/raw/  -> arquivos .json ou .csv simples (Pergunta,Resposta[,Raciocinio])
Saída:
  data/processed/train.jsonl
  data/processed/val.jsonl
"""

import json, os, random, csv
from pathlib import Path
from typing import List, Dict

RAW_DIR = Path("data/raw")
OUT_DIR = Path("data/processed")
TRAIN_FILE = OUT_DIR / "train.jsonl"
VAL_FILE = OUT_DIR / "val.jsonl"


def load_raw_items() -> List[Dict]:
    items = []
    if RAW_DIR.exists():
        for file in RAW_DIR.iterdir():
            if file.suffix == ".json":
                with open(file, "r", encoding="utf-8") as f:
                    chunk = json.load(f)
                    if isinstance(chunk, list):
                        items.extend(chunk)
            elif file.suffix == ".csv":
                with open(file, newline="", encoding="utf-8") as cf:
                    reader = csv.DictReader(cf)
                    for row in reader:
                        items.append(
                            {
                                "question": row.get("question") or row.get("pergunta"),
                                "answer": row.get("answer") or row.get("resposta"),
                                "reasoning": row.get("reasoning")
                                or row.get("raciocinio"),
                            }
                        )
    return items


def normalize(items: List[Dict]) -> List[Dict]:
    norm = []
    for it in items:
        q = (it.get("question") or "").strip()
        a = (it.get("answer") or "").strip()
        r = (it.get("reasoning") or "").strip()
        if not q or not a:
            continue
        prompt = f"Pergunta: {q}\n"
        if r:
            prompt += f"Raciocínio sugerido: {r}\n"
        prompt += "Responda de maneira objetiva."
        norm.append({"input": prompt, "output": a, "meta": {"has_reasoning": bool(r)}})
    return norm


def split(items: List[Dict], val_ratio=0.1):
    random.shuffle(items)
    n_val = max(1, int(len(items) * val_ratio)) if len(items) > 5 else 1
    return items[n_val:], items[:n_val]


def write_jsonl(path: Path, rows: List[Dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def main():
    items = load_raw_items()
    norm = normalize(items)
    train, val = split(norm)
    write_jsonl(TRAIN_FILE, train)
    write_jsonl(VAL_FILE, val)
    print(f"Gerado: {TRAIN_FILE} ({len(train)})")
    print(f"Gerado: {VAL_FILE} ({len(val)})")


if __name__ == "__main__":
    main()
