from __future__ import annotations
import os, json, hashlib
from pathlib import Path
from typing import List, Dict, Any
from mega_common.config import CONFIG
from mega_common.logging import get_logger

log = get_logger("pdf.ingest")

try:
    import PyPDF2  # type: ignore
except ImportError:  # pragma: no cover
    PyPDF2 = None

INDEX_PATH = Path(CONFIG.pdf.index_path)


def _hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def extract_text(pdf_path: Path) -> Dict[str, Any]:
    if not PyPDF2:
        raise RuntimeError("PyPDF2 não instalado. pip install PyPDF2")
    meta: Dict[str, Any] = {"pages": 0, "chars": 0, "preview": "", "hash": ""}
    text_parts: List[str] = []
    with open(pdf_path, "rb") as f:
        raw = f.read()
        meta["hash"] = _hash_bytes(raw)
        f.seek(0)
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            meta["pages"] += 1
            try:
                t = page.extract_text() or ""
            except Exception:
                t = ""
            text_parts.append(t)
    full = "\n".join(text_parts)
    meta["chars"] = len(full)
    meta["preview"] = full[: CONFIG.pdf.preview_chars]
    return meta


def load_index() -> Dict[str, Any]:
    if INDEX_PATH.exists():
        try:
            return json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        except Exception as e:
            log.warning("Falha ao carregar índice PDF: %s", e)
    return {}


def save_index(idx: Dict[str, Any]):
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = INDEX_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(idx, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(INDEX_PATH)


def index_pdf(path: Path):
    log.info("Indexando PDF: %s", path)
    meta = extract_text(path)
    idx = load_index()
    idx[str(path)] = meta
    save_index(idx)
    return meta


def batch_index(target: str):
    p = Path(target)
    results = []
    if p.is_file() and p.suffix.lower() in CONFIG.pdf.allowed_extensions:
        results.append(index_pdf(p))
    else:
        for root, _, files in os.walk(p):
            for f in files:
                fp = Path(root) / f
                if fp.suffix.lower() in CONFIG.pdf.allowed_extensions:
                    try:
                        results.append(index_pdf(fp))
                    except Exception as e:  # pragma: no cover
                        log.error("Falha indexando %s: %s", fp, e)
    return results
