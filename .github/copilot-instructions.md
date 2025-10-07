# GitHub Copilot Instructions for MEGA

## Project Overview

MEGA is an adaptive medical education platform focused on ECG (electrocardiogram) training. It uses spaced repetition, multi-agent LLM orchestration, and adaptive learning techniques to provide personalized medical education content.

## Architecture

This is a monorepo with the following main components:

### Backend (Python)
- **Adaptive Engine**: Spaced repetition system with JSON/SQLite backends
- **Case Generator**: Multi-agent system for generating clinical cases
- **Content Engine**: Parser for lesson manifests and content management
- **LLM Orchestrator**: Routes requests between multiple LLM models (local/Mistral, Gemini, GPT)
- **Multi-Agent System**: Coordinated agents (Tutor, Explainer, Critic, Failsafe)
- **CLI**: Command-line interface for adaptive learning, case generation, and PDF ingestion

### Frontend (TypeScript/Next.js)
- **Web App** (`apps/web`): Next.js 14 application with React 18
- UI for modules, quizzes, and progress tracking
- API routes for adaptive learning and search

### Project Generation Tools
- **Code Review Automation** (`proj_generation/`): Dual LLM code review workflow using GPT-5 and Gemini

## Tech Stack

- **Languages**: Python 3.11+, TypeScript/JavaScript
- **Frontend**: Next.js 14, React 18
- **Backend**: Python packages with pyproject.toml
- **Package Manager**: pnpm (workspace monorepo)
- **Testing**: vitest (TypeScript), pytest (Python)
- **Configuration**: `mega.config.yaml` for unified settings

## Workspace Structure

```
MEGA/
├── .github/                    # GitHub configurations
├── apps/
│   └── web/                   # Next.js web application
├── packages/
│   ├── adaptive-engine/       # Spaced repetition engine
│   ├── case-generator/        # Clinical case generation
│   ├── cli/                   # Command-line interface
│   ├── common-utils/          # Shared utilities (config, logging)
│   ├── content-engine/        # Content management & PDF ingestion
│   ├── llm-orchestrator/      # Multi-LLM routing
│   └── multi-agent/           # Agent coordination system
├── content/                   # Educational content (lessons, modules)
├── docs/                      # Documentation
├── proj_generation/           # Code review automation tools
├── mega.config.yaml           # Unified configuration
└── pnpm-workspace.json        # Workspace definition
```

## Code Style and Conventions

### Python
- Use Python 3.11+ features
- Type hints are required for function signatures
- Use dataclasses for configuration objects
- Follow PEP 8 style guide
- Docstrings for public functions
- Use descriptive variable names in Portuguese where appropriate (this is a Brazilian project)

### TypeScript/JavaScript
- Use TypeScript for all new code
- Prefer functional components with hooks
- Use explicit types, avoid `any`
- Export interfaces for public APIs

### Comments
- Code is primarily in Portuguese (comments, strings, documentation)
- Technical terms and API names remain in English
- Use English for code identifiers when they represent standard programming concepts

## Configuration

- **Unified Config**: All settings in `mega.config.yaml`
- **Environment Variables**: Can override config (e.g., `MEGA_ADAPTIVE_BACKEND`)
- **Dev Requirements**: Listed in `requirements-dev.txt` for Python

### Key Configuration Sections
```yaml
adaptive:      # Spaced repetition settings
pdf:           # PDF ingestion configuration
logging:       # Logging level and format
cli:           # CLI display options
case_generator: # Multi-agent case generation options
```

## Testing

### Python Tests
- Use pytest
- Test files in `tests/` directory within each package
- Run with: `pytest` from package root

### TypeScript Tests
- Use vitest
- Test files in `__tests__/` directories
- Configuration in root `vitest.config.ts`

## Development Workflows

### Python Package Development
```bash
# Install in editable mode
pip install -e packages/adaptive-engine
pip install -e packages/case-generator
# etc.

# Run tests
cd packages/adaptive-engine
pytest
```

### Next.js Development
```bash
cd apps/web
pnpm dev          # Development server
pnpm build        # Production build
pnpm start        # Start production server
```

### CLI Usage
```bash
mega adaptive mastery           # View mastery snapshot
mega case generate "Topic"      # Generate clinical case
mega pdf ingest docs/pdfs       # Ingest PDFs
```

## Multi-Agent System Patterns

### Agent Roles
- **Tutor**: Creates learning plans and objectives
- **Explainer**: Provides detailed educational content
- **Critic**: Reviews and validates outputs
- **Failsafe**: Ensures safety and accuracy

### LLM Orchestration Strategy
1. Draft with local model (Mistral via Ollama)
2. Refine with Gemini (if needed)
3. Polish with GPT (final pass)

Cost-aware routing based on complexity and requirements.

## API Patterns

### Adaptive Learning API
- `GET /api/adaptive/mastery` - Get mastery snapshot
- `GET /api/adaptive/due` - Get due items
- `POST /api/adaptive/rate` - Rate item performance

### Error Handling
- Standard error format: `{ error: string, details?: any }`
- Use appropriate HTTP status codes
- Log errors with context

## Code Review Automation

The `proj_generation/` directory contains automated code review tools:
- **GPT-5**: High-level architectural analysis
- **Gemini**: Concrete implementation suggestions
- Workflow triggered on pull requests via `code_review.yml`

## Data Management

### Storage Patterns
- **JSON Storage**: Atomic writes (temp file + replace)
- **Thread Safety**: Use RLock for concurrent access
- **PDF Index**: SHA-256 hash, metadata, preview text

### Custom Error Types
- `InvalidRatingError`: For adaptive rating validation
- `BackendNotSupportedError`: For unsupported storage backends

## Best Practices

1. **Make Minimal Changes**: Only modify what's necessary to fix the issue
2. **Test Before Committing**: Run relevant tests (pytest, vitest)
3. **Preserve Language**: Keep Portuguese comments/strings where they exist
4. **Use Existing Patterns**: Follow established conventions in the codebase
5. **Configuration Over Code**: Use `mega.config.yaml` for settings
6. **Type Safety**: Add type hints (Python) and interfaces (TypeScript)
7. **Documentation**: Update relevant documentation for significant changes
8. **Modular Design**: Keep packages independent, minimize cross-dependencies

## Important Notes

- This is an educational medical platform - accuracy is critical
- Content is focused on ECG interpretation and cardiology
- The adaptive engine uses spaced repetition algorithms (SM-2 variant)
- Multiple LLMs are used to balance cost and quality
- The project supports both Brazilian Portuguese and English content
