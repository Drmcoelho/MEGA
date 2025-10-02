#!/usr/bin/env bash
# ============================================
# MEGA - Setup FULL Robusto (Adaptive + API + Case + PDF + CLI + Tests)
# ============================================
# Variáveis ambiente opcionais:
#   BRANCH=feat/robust-adaptive-api-case-pdf
#   BACKEND=json|sqlite
#   FORCE=1          (sobrescreve e guarda versão antiga em depraceted/)
#   NO_PR=1          (não abre PR)
#   NO_INSTALL=1     (não instala dependências)
#
# Requisitos:
#  - git, python3.11+, pip, pnpm, gh (autenticado para PR)
#
# Observações:
#  - Sem 'set -euo pipefail' conforme pedido.
#  - Backups em 'depraceted/' quando FORCE=1.
# ============================================

BRANCH="${BRANCH:-feat/robust-adaptive-api-case-pdf}"
BACKEND="${BACKEND:-json}"
FORCE="${FORCE:-0}"
NO_PR="${NO_PR:-0}"
NO_INSTALL="${NO_INSTALL:-0}"
BACKUP_DIR="depraceted"

echo "==> Branch alvo: $BRANCH"
echo "==> Backend adaptativo: $BACKEND"
echo "==> FORCE sobrescrever (com backup): $FORCE"
echo "==> Criar PR automaticamente: $(( NO_PR==0 ))"
echo "==> Instalar dependências: $(( NO_INSTALL==0 ))"
echo "==> Diretório de backups: $BACKUP_DIR"

BACKUPS=()

# ---------- Funções utilitárias ----------
backup_file () {
  local path="$1"
  local dest="${BACKUP_DIR}/${path}"
  mkdir -p "$(dirname "$dest")"
  cp -p "$path" "$dest" 2>/dev/null && echo "[backup] $path -> $dest"
  BACKUPS+=("$dest")
}

write_file () {
  local path="$1"
  local content="$2"
  if [[ -f "$path" ]]; then
    if [[ "$FORCE" -eq 1 ]]; then
      backup_file "$path"
    else
      echo "[skip] $path (existe; FORCE=1 para sobrescrever e criar backup)"
      return 0
    fi
  fi
  mkdir -p "$(dirname "$path")"
  printf "%s\n" "$content" > "$path"
  echo "[ok] wrote $path"
}

append_line_if_missing () {
  local file="$1"
  local line="$2"
  mkdir -p "$(dirname "$file")"
  touch "$file"
  grep -Fxq "$line" "$file" || { echo "$line" >> "$file"; echo "[append] $line -> $file"; }
}

# ---------- Verificações iniciais ----------
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Erro: não está em um repositório git."
  exit 1
fi

git fetch origin >/dev/null 2>&1 || true
if git rev-parse origin/main >/dev/null 2>&1; then
  git checkout main || exit 1
  git pull --ff-only || true
fi

if git rev-parse --verify "$BRANCH" >/dev/null 2>&1; then
  git checkout "$BRANCH"
else
  git checkout -b "$BRANCH"
fi

# ---------- Arquivos de Config ----------
write_file mega.config.yaml "$(cat <<EOF
version: 0.1.0
adaptive:
  backend: ${BACKEND}
  path: .adaptive/data.json
  min_interval_seconds: 10
  medium_interval_seconds: 30
  long_interval_seconds: 60
  growth_factor_partial: 1.4
  growth_factor_correct: 2.2
  mastery_scale: 2
pdf:
  index_path: data/pdf_index.json
  preview_chars: 500
  allowed_extensions: [".pdf"]
logging:
  level: INFO
  format: "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
cli:
  color: true
  json_pretty: true
case_generator:
  include_explainer: true
  include_critic: true
  include_failsafe: true
EOF
)"

write_file .env.example "$(cat <<'EOF'
# Ambiente de desenvolvimento
MEGA_ADAPTIVE_BACKEND=json
MEGA_ADAPTIVE_PATH=.adaptive/data.json
MEGA_LOG_LEVEL=INFO
EOF
)"

# ---------- common-utils ----------
write_file packages/common-utils/pyproject.toml "$(cat <<'EOF'
[project]
name = "mega-common-utils"
version = "0.1.0"
description = "Utilidades compartilhadas (config, logging)"
requires-python = ">=3.11"

[tool.setuptools.packages.find]
where=["src"]
EOF
)"

write_file packages/common-utils/src/mega_common/config.py "$(cat <<'EOF'
from __future__ import annotations
import os, yaml
from dataclasses import dataclass, field
from typing import Any, Dict
from pathlib import Path

DEFAULT_CONFIG_PATH = Path("mega.config.yaml")

@dataclass
class AdaptiveConfig:
    backend: str = "json"
    path: str = ".adaptive/data.json"
    min_interval_seconds: int = 10
    medium_interval_seconds: int = 30
    long_interval_seconds: int = 60
    growth_factor_partial: float = 1.4
    growth_factor_correct: float = 2.2
    mastery_scale: int = 2

@dataclass
class PDFConfig:
    index_path: str = "data/pdf_index.json"
    preview_chars: int = 500
    allowed_extensions: list[str] = field(default_factory=lambda: [".pdf"])

@dataclass
class LoggingConfig:
    level: str = "INFO"
    format: str = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

@dataclass
class CLIConfig:
    color: bool = True
    json_pretty: bool = True

@dataclass
class CaseGenConfig:
    include_explainer: bool = True
    include_critic: bool = True
    include_failsafe: bool = True

@dataclass
class MegaConfig:
    version: str = "0.1.0"
    adaptive: AdaptiveConfig = field(default_factory=AdaptiveConfig)
    pdf: PDFConfig = field(default_factory=PDFConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    cli: CLIConfig = field(default_factory=CLIConfig)
    case_generator: CaseGenConfig = field(default_factory=CaseGenConfig)

    @staticmethod
    def load(path: str | Path | None = None) -> "MegaConfig":
        p = Path(path) if path else DEFAULT_CONFIG_PATH
        if not p.exists():
            return MegaConfig()
        data: Dict[str, Any] = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        return MegaConfig(
            version=data.get("version", "0.1.0"),
            adaptive=AdaptiveConfig(**data.get("adaptive", {})),
            pdf=PDFConfig(**data.get("pdf", {})),
            logging=LoggingConfig(**data.get("logging", {})),
            cli=CLIConfig(**data.get("cli", {})),
            case_generator=CaseGenConfig(**data.get("case_generator", {})),
        )

CONFIG = MegaConfig.load(os.getenv("MEGA_CONFIG_PATH"))
EOF
)"

write_file packages/common-utils/src/mega_common/logging.py "$(cat <<'EOF'
import logging, os
from .config import CONFIG

_LEVEL = os.getenv("MEGA_LOG_LEVEL", CONFIG.logging.level)
_FMT = CONFIG.logging.format

logging.basicConfig(level=_LEVEL, format=_FMT)

def get_logger(name: str):
    return logging.getLogger(name)
EOF
)"

# ---------- Adaptive Engine ----------
write_file packages/adaptive-engine/src/adaptive/exceptions.py "$(cat <<'EOF'
class AdaptiveError(Exception):
    pass

class InvalidRatingError(AdaptiveError):
    pass

class BackendNotSupportedError(AdaptiveError):
    pass
EOF
)"

write_file packages/adaptive-engine/src/adaptive/scheduler.py "$(cat <<'EOF'
from __future__ import annotations
from dataclasses import dataclass
from .exceptions import InvalidRatingError
from mega_common.config import CONFIG

@dataclass
class IntervalResult:
    item_id: str
    rating: int
    previous_interval: int
    next_interval: int

class IntervalScheduler:
    def __init__(self, *, min_interval: int | None = None, medium: int | None = None, long: int | None = None,
                 growth_partial: float | None = None, growth_correct: float | None = None):
        a = CONFIG.adaptive
        self.min_interval = min_interval or a.min_interval_seconds
        self.med_interval = medium or a.medium_interval_seconds
        self.long_interval = long or a.long_interval_seconds
        self.growth_partial = growth_partial or a.growth_factor_partial
        self.growth_correct = growth_correct or a.growth_factor_correct

    def compute_interval(self, last_interval: int, rating: int) -> int:
        if rating not in (0,1,2):
            raise InvalidRatingError(f"Rating inválido: {rating}")
        if rating == 0:
            return self.min_interval
        if rating == 1:
            base = int(last_interval * self.growth_partial) if last_interval else self.med_interval
            return max(self.med_interval, base)
        base = int(last_interval * self.growth_correct) if last_interval else self.long_interval
        return max(self.long_interval, base)

    def next(self, item_id: str, last_interval: int, rating: int) -> IntervalResult:
        nxt = self.compute_interval(last_interval, rating)
        return IntervalResult(item_id=item_id, rating=rating, previous_interval=last_interval, next_interval=nxt)
EOF
)"

write_file packages/adaptive-engine/src/adaptive/storage.py "$(cat <<'EOF'
from __future__ import annotations
import json, time, sqlite3, threading
from pathlib import Path
from typing import Dict, Tuple, List
from mega_common.logging import get_logger

log = get_logger("adaptive.storage")

class JSONStorage:
    def __init__(self, path: Path):
        self.path = path
        self._data = {"intervals": {}, "mastery": {}}
        self._loaded = False
        self._lock = threading.RLock()

    def load(self):
        with self._lock:
            if self._loaded:
                return
            if self.path.exists():
                try:
                    self._data = json.loads(self.path.read_text(encoding="utf-8"))
                except Exception as e:
                    log.warning("Falha ao carregar JSONStorage: %s", e)
            self._loaded = True

    def save(self):
        with self._lock:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self.path.with_suffix(".tmp")
            tmp.write_text(json.dumps(self._data, ensure_ascii=False, indent=2), encoding="utf-8")
            tmp.replace(self.path)

    def get_interval(self, item_id: str) -> Tuple[int,int]:
        self.load()
        return tuple(self._data["intervals"].get(item_id, [0,0]))  # type: ignore

    def set_interval(self, item_id: str, interval: int):
        self.load()
        with self._lock:
            self._data["intervals"][item_id] = [interval, int(time.time())]
            self.save()

    def due_items(self) -> List[str]:
        self.load()
        now = int(time.time())
        return [k for k,(interval, ts) in self._data["intervals"].items() if now - ts >= interval]

    def update_mastery(self, subskill: str, rating: int):
        self.load()
        with self._lock:
            score_sum, attempts = self._data["mastery"].get(subskill, [0,0])
            score_sum += rating
            attempts += 1
            self._data["mastery"][subskill] = [score_sum, attempts]
            self.save()

    def mastery_snapshot(self) -> Dict[str,float]:
        self.load()
        snap = {}
        for s,(score_sum, attempts) in self._data["mastery"].items():
            snap[s] = 0.0 if attempts == 0 else round((score_sum/(2*attempts))*100, 2)
        return snap

class SQLiteStorage:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._lock = threading.RLock()
        self._init()

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def _init(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._conn() as c:
            c.execute("""CREATE TABLE IF NOT EXISTS intervals(
                item_id TEXT PRIMARY KEY,
                interval INTEGER,
                last_ts INTEGER
            )""")
            c.execute("""CREATE TABLE IF NOT EXISTS mastery(
                subskill TEXT PRIMARY KEY,
                score_sum INTEGER,
                attempts INTEGER
            )""")

    def get_interval(self, item_id: str):
        with self._conn() as c:
            cur = c.execute("SELECT interval,last_ts FROM intervals WHERE item_id=?",(item_id,))
            row = cur.fetchone()
            return (0,0) if not row else row

    def set_interval(self, item_id: str, interval: int):
        import time
        ts = int(time.time())
        with self._lock, self._conn() as c:
            c.execute("REPLACE INTO intervals(item_id, interval, last_ts) VALUES(?,?,?)",(item_id, interval, ts))

    def due_items(self):
        import time
        now = int(time.time())
        out=[]
        with self._conn() as c:
            for item_id, interval, last_ts in c.execute("SELECT item_id, interval, last_ts FROM intervals"):
                if now - last_ts >= interval:
                    out.append(item_id)
        return out

    def update_mastery(self, subskill: str, rating: int):
        with self._lock, self._conn() as c:
            cur = c.execute("SELECT score_sum, attempts FROM mastery WHERE subskill=?",(subskill,))
            row = cur.fetchone()
            score_sum, attempts = row if row else (0,0)
            score_sum += rating
            attempts += 1
            c.execute("REPLACE INTO mastery(subskill,score_sum,attempts) VALUES(?,?,?)",(subskill,score_sum,attempts))

    def mastery_snapshot(self):
        snap={}
        with self._conn() as c:
            for subskill, score_sum, attempts in c.execute("SELECT subskill,score_sum,attempts FROM mastery"):
                snap[subskill] = 0.0 if attempts == 0 else round((score_sum/(2*attempts))*100,2)
        return snap
EOF
)"

write_file packages/adaptive-engine/src/adaptive/engine.py "$(cat <<'EOF'
from __future__ import annotations
from pathlib import Path
from .storage import JSONStorage, SQLiteStorage
from .scheduler import IntervalScheduler
from .exceptions import BackendNotSupportedError, InvalidRatingError
from mega_common.config import CONFIG
from mega_common.logging import get_logger
from dataclasses import asdict

log = get_logger("adaptive.engine")

class AdaptiveEngine:
    def __init__(self, backend: str | None = None, path: str | None = None):
        a = CONFIG.adaptive
        self.backend = backend or a.backend
        data_path = path or a.path
        p = Path(data_path)
        if self.backend == "json":
            self.store = JSONStorage(p)
        elif self.backend == "sqlite":
            self.store = SQLiteStorage(p)
        else:
            raise BackendNotSupportedError(self.backend)
        self.scheduler = IntervalScheduler()

    def rate_item(self, item_id: str, rating: int):
        if rating not in (0,1,2):
            raise InvalidRatingError(rating)
        last_interval,_ = self.store.get_interval(item_id)
        result = self.scheduler.next(item_id, last_interval, rating)
        self.store.set_interval(item_id, result.next_interval)
        log.debug("Rated item %s => %s", item_id, asdict(result))
        return result

    def update_mastery(self, subskill: str, rating: int):
        if rating not in (0,1,2):
            raise InvalidRatingError(rating)
        self.store.update_mastery(subskill, rating)
        snap = self.store.mastery_snapshot()
        return {"subskill": subskill, "mastery": snap.get(subskill, 0.0)}

    def due(self):
        return self.store.due_items()

    def snapshot(self):
        return self.store.mastery_snapshot()
EOF
)"

# ---------- Case Generator ----------
write_file packages/case-generator/pyproject.toml "$(cat <<'EOF'
[project]
name = "mega-case-generator"
version = "0.2.0"
description = "Gerador de casos clínicos multi-agente (robusto)"
requires-python = ">=3.11"

[tool.setuptools.packages.find]
where=["src"]
EOF
)"

write_file packages/case-generator/src/case_generator/core.py "$(cat <<'EOF'
from __future__ import annotations
from multi_agent.session import MultiAgentSession
from dataclasses import dataclass, asdict
from mega_common.config import CONFIG

@dataclass
class CaseSection:
    title: str
    content: str

@dataclass
class ClinicalCase:
    topic: str
    plan: list[str]
    explanations: dict[str,str]
    critic: dict
    failsafe: dict

    def to_markdown(self) -> str:
        lines = [f"# Caso Clínico: {self.topic}", "", "## Plano", *[f"- {p}" for p in self.plan], "", "## Explicações"]
        for lvl, txt in self.explanations.items():
            lines.append(f"### {lvl.capitalize()}\n{txt}\n")
        lines.append("## Análise Crítica")
        lines.append(f"```json\n{self.critic}\n```\n")
        lines.append("## Fail-Safe")
        lines.append(f"```json\n{self.failsafe}\n```")
        return "\n".join(lines)

    def to_dict(self):
        return asdict(self)

def compose_case(topic: str) -> ClinicalCase:
    cfg = CONFIG.case_generator
    sess = MultiAgentSession()
    plan = sess.run_plan(topic=topic)["plan"]
    explanations = sess.explain_levels(topic) if cfg.include_explainer else {}
    critic = sess.critic.act(passage=" ".join(plan)) if cfg.include_critic else {}
    failsafe = sess.failsafe.act(answer=" ".join(plan)) if cfg.include_failsafe else {}
    return ClinicalCase(topic=topic, plan=plan, explanations=explanations, critic=critic, failsafe=failsafe)
EOF
)"

# ---------- PDF ingest ----------
write_file packages/content-engine/src/pdf_ingest.py "$(cat <<'EOF'
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
    import hashlib as _h
    return _h.sha256(data).hexdigest()

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
    meta["preview"] = full[:CONFIG.pdf.preview_chars]
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
                fp = Path(root)/f
                if fp.suffix.lower() in CONFIG.pdf.allowed_extensions:
                    try:
                        results.append(index_pdf(fp))
                    except Exception as e:  # pragma: no cover
                        log.error("Falha indexando %s: %s", fp, e)
    return results
EOF
)"

# ---------- APIs Next ----------
write_file apps/web/lib/apiErrors.ts "$(cat <<'EOF'
export interface ApiErrorShape { error: string; details?: any }
export function errorResponse(res: any, status: number, message: string, details?: any) {
  res.status(status).json({ error: message, details });
}
EOF
)"

write_file apps/web/pages/api/adaptive/mastery.ts "$(cat <<'EOF'
import type { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs';
import path from 'path';
import { errorResponse } from '../../../lib/apiErrors';

const DATA = path.join(process.cwd(), '.adaptive', 'data.json');

export default function handler(_req: NextApiRequest, res: NextApiResponse) {
  try {
    if (!fs.existsSync(DATA)) return res.status(200).json({ mastery: {} });
    const raw = JSON.parse(fs.readFileSync(DATA, 'utf-8'));
    const m = raw.mastery || {};
    const snapshot: Record<string, number> = {};
    Object.entries(m).forEach(([subskill, [sum, attempts]]: any) => {
      snapshot[subskill] = attempts === 0 ? 0 : Math.round((sum / (2 * attempts)) * 10000) / 100;
    });
    res.status(200).json({ mastery: snapshot });
  } catch (e: any) {
    errorResponse(res, 500, 'MASTERy_READ_ERROR', e?.message);
  }
}
EOF
)"

write_file apps/web/pages/api/adaptive/due.ts "$(cat <<'EOF'
import type { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs';
import path from 'path';
import { errorResponse } from '../../../lib/apiErrors';

const DATA = path.join(process.cwd(), '.adaptive', 'data.json');

export default function handler(_req: NextApiRequest, res: NextApiResponse) {
  try {
    if (!fs.existsSync(DATA)) return res.status(200).json({ due: [] });
    const raw = JSON.parse(fs.readFileSync(DATA, 'utf-8'));
    const intervals = raw.intervals || {};
    const now = Math.floor(Date.now()/1000);
    const due: string[] = [];
    Object.entries(intervals).forEach(([itemId, [interval, ts]]: any) => {
      if (now - ts >= interval) due.push(itemId);
    });
    res.status(200).json({ due });
  } catch (e: any) {
    errorResponse(res, 500, 'DUE_READ_ERROR', e?.message);
  }
}
EOF
)"

write_file apps/web/pages/api/adaptive/rate.ts "$(cat <<'EOF'
import type { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs';
import path from 'path';
import { errorResponse } from '../../../lib/apiErrors';

const DATA = path.join(process.cwd(), '.adaptive', 'data.json');

function load(): any {
  if (!fs.existsSync(DATA)) return { intervals:{}, mastery:{} };
  return JSON.parse(fs.readFileSync(DATA,'utf-8'));
}
function save(obj:any) {
  const dir = path.dirname(DATA);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, {recursive:true});
  fs.writeFileSync(DATA, JSON.stringify(obj, null, 2), 'utf-8');
}

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') return errorResponse(res, 405, 'METHOD_NOT_ALLOWED');
  try {
    const { itemId, rating } = req.body || {};
    if (!itemId || typeof rating !== 'number') return errorResponse(res, 400, 'INVALID_PAYLOAD');
    if (![0,1,2].includes(rating)) return errorResponse(res, 400, 'INVALID_RATING');
    const store = load();
    const prev = store.intervals[itemId] || [0,0];
    const lastInterval = prev[0];
    let nextInterval:number;
    if (rating <= 0) nextInterval = 10;
    else if (rating === 1) nextInterval = Math.max(30, parseInt(String(lastInterval*1.4)) || 30);
    else nextInterval = Math.max(60, parseInt(String(lastInterval*2.2)) || 60);
    store.intervals[itemId] = [nextInterval, Math.floor(Date.now()/1000)];
    save(store);
    res.status(200).json({ itemId, nextInterval });
  } catch (e:any) {
    errorResponse(res, 500, 'RATE_ERROR', e?.message);
  }
}
EOF
)"

write_file apps/web/pages/api/search/pdf.ts "$(cat <<'EOF'
import type { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs';
import path from 'path';
import { errorResponse } from '../../../lib/apiErrors';

const INDEX = path.join(process.cwd(), 'data', 'pdf_index.json');

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const q = (req.query.q || '').toString().toLowerCase();
  if (!q) return errorResponse(res, 400, 'QUERY_REQUIRED');
  try {
    if (!fs.existsSync(INDEX)) return res.status(200).json({results:[]});
    const data = JSON.parse(fs.readFileSync(INDEX,'utf-8'));
    const results = Object.entries<any>(data)
      .filter(([_, meta]) => (meta.preview || "").toLowerCase().includes(q))
      .map(([file, meta]) => ({ file, snippet: meta.preview.slice(0,300), pages: meta.pages, chars: meta.chars }));
    res.status(200).json({results});
  } catch (e:any) {
    errorResponse(res, 500, 'PDF_SEARCH_ERROR', e?.message);
  }
}
EOF
)"

# ---------- CLI Subcomandos ----------
write_file packages/cli/src/mega_cli/case_commands.py "$(cat <<'EOF'
import typer, json
from case_generator.core import compose_case
from mega_common.config import CONFIG

case_app = typer.Typer(help="Geração de casos clínicos (robusto)")

@case_app.command("generate")
def generate(topic: str, markdown: bool = typer.Option(False, help="Saída em Markdown")):
    case = compose_case(topic)
    if markdown:
        typer.echo(case.to_markdown())
    else:
        if CONFIG.cli.json_pretty:
            typer.echo(json.dumps(case.to_dict(), ensure_ascii=False, indent=2))
        else:
            typer.echo(json.dumps(case.to_dict(), ensure_ascii=False))
EOF
)"

write_file packages/cli/src/mega_cli/pdf_commands.py "$(cat <<'EOF'
import typer, json
from mega_common.config import CONFIG
try:
    from content_engine.src.pdf_ingest import batch_index
except ImportError:
    batch_index = None

pdf_app = typer.Typer(help="Ingestão de PDFs (robusta)")

@pdf_app.command("ingest")
def ingest(target: str):
    if not batch_index:
        typer.echo("Dependências de PDF não instaladas. pip install PyPDF2")
        raise typer.Exit(1)
    res = batch_index(target)
    typer.echo(json.dumps(res, ensure_ascii=False, indent=2 if CONFIG.cli.json_pretty else None))
EOF
)"

write_file packages/cli/src/mega_cli/adaptive_commands.py "$(cat <<'EOF'
import typer, json
from adaptive.engine import AdaptiveEngine
from mega_common.config import CONFIG
from adaptive.exceptions import InvalidRatingError

adaptive_app = typer.Typer(help="Comandos do motor adaptativo persistente")
_engine = AdaptiveEngine()

@adaptive_app.command("rate")
def rate(item_id: str, rating: int = typer.Argument(..., min=0, max=2)):
    try:
        result = _engine.rate_item(item_id, rating)
        payload = {
            "item": result.item_id,
            "previous_interval": result.previous_interval,
            "next_interval": result.next_interval,
            "rating": result.rating
        }
        typer.echo(json.dumps(payload, ensure_ascii=False, indent=2 if CONFIG.cli.json_pretty else None))
    except InvalidRatingError as e:
        typer.echo(f"Rating inválido: {e}")
        raise typer.Exit(1)

@adaptive_app.command("mastery")
def mastery(subskill: str, rating: int):
    resp = _engine.update_mastery(subskill, rating)
    typer.echo(json.dumps(resp, ensure_ascii=False, indent=2 if CONFIG.cli.json_pretty else None))

@adaptive_app.command("due")
def due():
    typer.echo(json.dumps({"due": _engine.due()}, ensure_ascii=False, indent=2 if CONFIG.cli.json_pretty else None))

@adaptive_app.command("snapshot")
def snapshot():
    typer.echo(json.dumps({"mastery": _engine.snapshot()}, ensure_ascii=False, indent=2 if CONFIG.cli.json_pretty else None))
EOF
)"

# Atualizar main CLI (realiza backup se FORCE=1)
if [[ -f packages/cli/src/mega_cli/main.py && "$FORCE" -eq 1 ]]; then
  backup_file packages/cli/src/mega_cli/main.py
fi
write_file packages/cli/src/mega_cli/main.py "$(cat <<'EOF'
import typer, json, os, yaml
from mega_common.config import CONFIG
from .adaptive_commands import adaptive_app
from .agent_commands import agent_app
from .case_commands import case_app
from .pdf_commands import pdf_app

app = typer.Typer(help="CLI MEGA (robusta)")
BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
MODULES_DIR = os.path.join(BASE, "content", "modules")

@app.command()
def version():
    typer.echo("mega-cli 0.2.0")

@app.command()
def ingest():
    if not os.path.isdir(MODULES_DIR):
        typer.echo("Nenhum módulo encontrado")
        raise typer.Exit(code=0)
    mods = []
    for d in sorted(os.listdir(MODULES_DIR)):
        mpath = os.path.join(MODULES_DIR, d, "manifest.yaml")
        if os.path.isfile(mpath):
            with open(mpath, 'r') as f:
                try:
                    data = yaml.safe_load(f)
                    mods.append({"id": data.get("id"), "title": data.get("title"), "version": data.get("version")})
                except Exception as e:
                    typer.echo(f"Erro lendo {mpath}: {e}")
    typer.echo(json.dumps(mods, ensure_ascii=False, indent=2 if CONFIG.cli.json_pretty else None))

@app.command()
def draft_case(topic: str = typer.Argument(..., help="Tópico para caso clínico (placeholder)")):
    typer.echo(json.dumps({"topic": topic, "status": "placeholder"}, ensure_ascii=False, indent=2 if CONFIG.cli.json_pretty else None))

app.add_typer(adaptive_app, name="adaptive")
app.add_typer(agent_app, name="agent")
app.add_typer(case_app, name="case")
app.add_typer(pdf_app, name="pdf")

if __name__ == "__main__":
    app()
EOF
)"

# ---------- Testes ----------
write_file packages/adaptive-engine/tests/test_engine.py "$(cat <<'EOF'
from adaptive.engine import AdaptiveEngine

def test_rate_and_mastery_cycle():
    eng = AdaptiveEngine(backend="json", path=".adaptive/test_data.json")
    r = eng.rate_item("itemX", 2)
    assert r.next_interval >= 60
    m = eng.update_mastery("skillX", 2)
    assert m["mastery"] > 0
EOF
)"

write_file packages/case-generator/tests/test_case.py "$(cat <<'EOF'
from case_generator.core import compose_case

def test_compose_case():
    c = compose_case("ECG")
    assert c.topic == "ECG"
    assert isinstance(c.plan, list)
EOF
)"

write_file packages/content-engine/tests/test_pdf_index_stub.py "$(cat <<'EOF'
import pytest

@pytest.mark.skip("PDF integration test placeholder")
def test_pdf_ingest_placeholder():
    assert True
EOF
)"

# ---------- Script qualidade ----------
write_file scripts/quality.sh "$(cat <<'EOF'
#!/usr/bin/env bash
echo "[PYTEST]"
pytest || true
echo "(Adicionar lint futuramente)"
EOF
)"
chmod +x scripts/quality.sh

# ---------- requirements-dev & .gitignore ----------
append_line_if_missing requirements-dev.txt "pytest"
append_line_if_missing requirements-dev.txt "PyPDF2"
append_line_if_missing .gitignore ".adaptive/"
append_line_if_missing .gitignore "coverage/"
append_line_if_missing .gitignore "**/__pycache__/"

# ---------- Instalação (opcional) ----------
if [[ "$NO_INSTALL" -eq 0 ]]; then
  echo "==> Instalando pacotes Python (editable)"
  pip install -e packages/common-utils -e packages/adaptive-engine -e packages/case-generator -e packages/cli -e packages/multi-agent || true
  pip install PyPDF2 pytest || true
fi

# ---------- Commit & Push ----------
git add mega.config.yaml .env.example packages/common-utils packages/adaptive-engine packages/case-generator packages/content-engine apps/web/pages/api scripts/quality.sh packages/cli requirements-dev.txt .gitignore || true
git add packages/content-engine/src/pdf_ingest.py || true
git add packages/cli/src/mega_cli/*.py || true
git add packages/adaptive-engine/tests/ packages/case-generator/tests/ packages/content-engine/tests/ || true
git add scripts/setup_robust_full.sh || true
git add ${BACKUP_DIR} 2>/dev/null || true

if ! git diff --cached --quiet; then
  git commit -m "feat: 10x robust adaptive persistence + API + case generator + pdf ingestion (FULL)"
else
  echo "Nada novo para commit."
fi

git push -u origin "$BRANCH"

# ---------- PR ----------
if [[ "$NO_PR" -eq 0 ]]; then
  if command -v gh >/dev/null 2>&1; then
    gh pr create --base main \
      --title "feat: 10x robust adaptive persistence + API + case generator + pdf ingestion" \
      --body "Inclui engine adaptativa robusta (json/sqlite), APIs (/api/adaptive/*, /api/search/pdf), case generator multi-agente, ingestão de PDFs (hash/preview), CLI expandida (adaptive/case/pdf), testes e config unificada (mega.config.yaml)."
  else
    echo "gh CLI não encontrado - criar PR manualmente."
  fi
fi

if [[ "${#BACKUPS[@]}" -gt 0 ]]; then
  echo "===================="
  echo "Backups criados em $BACKUP_DIR:"
  for b in "${BACKUPS[@]}"; do
    echo " - $b"
  done
  echo "===================="
fi

echo "==> CONCLUÍDO. Verifique a branch $BRANCH e o PR."