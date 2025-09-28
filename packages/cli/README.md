# MEGA CLI

Command line interface for Medical Education with Generative AI.

## Installation

From project root:

```bash
cd packages/cli
pip install -e .
```

## Usage

```bash
# Show version
mega version

# List available modules
mega ingest

# Draft a case (placeholder)
mega draft-case ecg-basics --difficulty beginner
```

## Commands

- `version`: Show CLI version
- `ingest`: Scan and list educational modules from content/modules
- `draft-case`: Generate new clinical cases (placeholder for future implementation)