# MEGA

MEGA (Medical Education Generation Assistant) is a modular platform for advanced medical education, featuring adaptive learning systems, multi-language support, and comprehensive educational modules.

## Features

- **Modular Content**: Organized medical education modules with YAML-based manifests
- **Adaptive Learning**: Spaced repetition system with intelligent scheduling
- **Multi-language Support**: i18n support with Portuguese and English translations
- **Static Site Generation**: Fully static export for GitHub Pages deployment

## Development

### Prerequisites

- Node.js 20+
- pnpm (package manager)
- Python 3.11+ (for backend packages)

### Installation

```bash
# Install pnpm if you haven't
npm install -g pnpm

# Install dependencies
pnpm install

# Install web app dependencies
cd apps/web
pnpm install
```

### Running Locally

```bash
cd apps/web
pnpm dev
```

The application will be available at http://localhost:3000

### Building

```bash
cd apps/web
pnpm build
```

For static export (used for GitHub Pages):

```bash
cd apps/web
pnpm build:static
```

The static files will be generated in `apps/web/out/`

## Deployment

The site is automatically deployed to GitHub Pages when changes are pushed to the `main` branch. The deployment workflow:

1. Builds the Next.js app with static export
2. Adds `.nojekyll` file to prevent GitHub from ignoring `_next` directory
3. Creates SPA fallback by copying `index.html` to `404.html`
4. Deploys to GitHub Pages

### Manual Deployment

To manually trigger a deployment, go to the Actions tab and run the "Deploy to GitHub Pages" workflow.

## Project Structure

```
MEGA/
├── apps/
│   └── web/              # Next.js frontend application
│       ├── pages/        # Pages router (main app)
│       ├── lib/          # Utilities and helpers
│       ├── messages/     # i18n translation files
│       └── styles/       # Global styles
├── content/
│   └── modules/          # Educational modules with YAML manifests
├── packages/             # Shared packages
└── scripts/              # Build and setup scripts
```

## Contributing

This is an educational platform. Contributions should maintain the focus on medical education quality and accuracy.

## License

See LICENSE-DRAFT.md for details.

## Disclaimer

This content is for educational purposes only and does not substitute clinical guidelines or professional judgment.