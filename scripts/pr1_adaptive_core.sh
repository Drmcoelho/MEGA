#!/usr/bin/env bash
# =========================================================
# PR 1 - Adaptive Core (json/sqlite) + Unified Config
# =========================================================
# Uso:
#   bash scripts/pr1_adaptive_core.sh
#
# Variáveis ambiente opcionais:
#   BRANCH=feat/adaptive-core
#   NO_PR=1          (não abre o PR automaticamente)
#   FORCE=1          (sobrescreve arquivos existentes)
#
# Requisitos:
#   - git, python3.11+, pip, (opcional) gh CLI autenticado
# =========================================================

BRANCH="${BRANCH:-feat/adaptive-core}"
FORCE="${FORCE:-0}"
NO_PR="${NO_PR:-0}"

echo "==> Branch: $BRANCH"
echo "==> FORCE overwrite: $FORCE"
echo "==> Abrir PR automaticamente: $(( NO_PR==0 ))"

write_file () {
  local path="$1"
  local content="$2"
  if [[ -f "$path" && "$FORCE" -ne 1 ]]; then
    echo "[skip] $path (já existe; use FORCE=1 para sobrescrever)"
    return 0
  fi
  mkdir -p "$(dirname "$path")"
  printf "%s\n" "$content" > "$path"
  echo "[ok] wrote $path"
}

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

write_file mega.config.yaml "$(cat <<'EOF2'
version: 0.1.0
adaptive:
  backend: json
  path: .adaptive/data.json
  min_interval_seconds: 10
  medium_interval_seconds: 30
  long_interval_seconds: 60
  growth_factor_partial: 1.4
  growth_factor_correct: 2.2
  mastery_scale: 2
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
EOF2
)"

write_file packages/common-utils/pyproject.toml "$(cat <<'EOF2'
[project]
name = "mega-common-utils"
version = "0.1.0"
description = "Utilidades compartilhadas (config, logging)"
requires-python = ">=3.11"

[tool.setuptools.packages.find]
where=["src"]
EOF2
)"

write_file packages/common-utils/src/mega_common/config.py "$(cat <<'EOF2'
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
            logging=LoggingConfig(**data.get("logging", {})),
            cli=CLIConfig(**data.get("cli", {})),
            case_generator=CaseGenConfig(**data.get("case_generator", {})),
        )

CONFIG = MegaConfig.load(os.getenv("MEGA_CONFIG_PATH"))
EOF2
)"

write_file packages/common-utils/src/mega_common/logging.py "$(cat <<'EOF2'
import logging, os
from .config import CONFIG

_LEVEL = os.getenv("MEGA_LOG_LEVEL", CONFIG.logging.level)
_FMT = CONFIG.logging.format

logging.basicConfig(level=_LEVEL, format=_FMT)

def get_logger(name: str):
    return logging.getLogger(name)
EOF2
)"

write_file packages/adaptive-engine/src/adaptive/exceptions.py "$(cat <<'EOF2'
class AdaptiveError(Exception):
    pass

class InvalidRatingError(AdaptiveError):
    pass

class BackendNotSupportedError(AdaptiveError):
    pass
EOF2
)"

write_file packages/adaptive-engine/src/adaptive/scheduler.py "$(cat <<'EOF2'
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
    def __init__(self, *, min_interval: int | None = None, medium: int | None = None,
                 long: int | None = None, growth_partial: float | None = None,
                 growth_correct: float | None = None):
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

    def next(self, item_id: str, last_interval: int, rating: int):
        nxt = self.compute_interval(last_interval, rating)
        return IntervalResult(item_id=item_id, rating=rating, previous_interval=last_interval, next_interval=nxt)
EOF2
)"

write_file packages/adaptive-engine/src/adaptive/storage.py "$(cat <<'EOF2'
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
EOF2
)"

write_file packages/adaptive-engine/src/adaptive/engine.py "$(cat <<'EOF2'
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
EOF2
)"

write_file packages/cli/src/mega_cli/adaptive_commands.py "$(cat <<'EOF2'
import typer, json
from adaptive.engine import AdaptiveEngine
from adaptive.exceptions import InvalidRatingError
from mega_common.config import CONFIG

adaptive_app = typer.Typer(help="Comandos do motor adaptativo")
_engine = AdaptiveEngine()

@adaptive_app.command("rate")
def rate(item_id: str, rating: int = typer.Argument(..., min=0, max=2)):
    try:
        r = _engine.rate_item(item_id, rating)
        payload = {
            "item": r.item_id,
            "previous_interval": r.previous_interval,
            "next_interval": r.next_interval,
            "rating": r.rating
        }
        typer.echo(json.dumps(payload, ensure_ascii=False, indent=2 if CONFIG.cli.json_pretty else None))
    except InvalidRatingError:
        typer.echo("Rating inválido (use 0,1,2).")
        raise typer.Exit(1)

@adaptive_app.command("mastery")
def mastery(subskill: str, rating: int):
    res = _engine.update_mastery(subskill, rating)
    typer.echo(json.dumps(res, ensure_ascii=False, indent=2 if CONFIG.cli.json_pretty else None))

@adaptive_app.command("due")
def due():
    typer.echo(json.dumps({"due": _engine.due()}, ensure_ascii=False, indent=2 if CONFIG.cli.json_pretty else None))

@adaptive_app.command("snapshot")
def snapshot():
    typer.echo(json.dumps({"mastery": _engine.snapshot()}, ensure_ascii=False, indent=2 if CONFIG.cli.json_pretty else None))
EOF2
)"

write_file packages/adaptive-engine/tests/test_engine.py "$(cat <<'EOF2'
from adaptive.engine import AdaptiveEngine

def test_rate_and_mastery_cycle():
    eng = AdaptiveEngine(backend="json", path=".adaptive/test_data.json")
    r = eng.rate_item("itemX", 2)
    assert r.next_interval >= 60
    m = eng.update_mastery("skillX", 2)
    assert m["mastery"] > 0
EOF2
)"

# Instalar (best effort)
echo "==> Instalando pacotes (editable)"
pip install -e packages/common-utils -e packages/adaptive-engine -e packages/cli >/dev/null 2>&1 || true

# Teste rápido se pytest existir
if command -v pytest >/dev/null 2>&1; then
  echo "==> Testando..."
  pytest packages/adaptive-engine/tests -q || true
fi

git add mega.config.yaml packages/common-utils packages/adaptive-engine packages/cli packages/adaptive-engine/tests || true

if ! git diff --cached --quiet; then
  git commit -m "feat: adaptive core (json/sqlite) + unified config"
else
  echo "Nenhuma alteração para commit."
fi

git push -u origin "$BRANCH"

# PR body
write_file PR_ADAPTIVE_CORE.md "$(cat <<'EOF2'
# Adaptive Core (json/sqlite) + Unified Config

## Conteúdo
- mega.config.yaml (adaptive)
- mega-common-utils (config + logging)
- Engine (scheduler, storage JSON/SQLite, engine, erros)
- CLI: mega adaptive rate|mastery|due|snapshot
- Teste básico

## Teste rápido
pip install -e packages/common-utils -e packages/adaptive-engine -e packages/cli
mega adaptive rate demo 2
mega adaptive snapshot

## Próximos
Multi-agent case generator, PDF ingestion, embeddings, lint & typing
EOF2
)"

if [[ "$NO_PR" -eq 0 ]]; then
  if command -v gh >/dev/null 2>&1; then
    gh pr create --base main \
      --title "feat: adaptive core (json/sqlite) + unified config" \
      --body-file PR_ADAPTIVE_CORE.md || echo "Falha ao abrir PR automaticamente."
  else
    echo "gh não disponível - abra PR manualmente:"
    echo "gh pr create --base main --title 'feat: adaptive core (json/sqlite) + unified config' --body-file PR_ADAPTIVE_CORE.md"
  fi
fi

echo "==> Finalizado PR 1."
