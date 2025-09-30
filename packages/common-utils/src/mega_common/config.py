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
