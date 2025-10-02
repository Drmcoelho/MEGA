/** @type {import('next').NextConfig} */

// Detect if we're building in GitHub Actions for deployment
const isGitHubActions = process.env.GITHUB_ACTIONS === 'true';
const repoName = process.env.GITHUB_REPOSITORY?.split('/')[1] || '';

const nextConfig = {
  output: 'export',
  images: {
    unoptimized: true,
  },
  // For GitHub Pages (project page), we need basePath and assetPrefix
  // Only apply when building in GitHub Actions
  ...(isGitHubActions && repoName ? {
    basePath: `/${repoName}`,
    assetPrefix: `/${repoName}`,
  } : {}),
};

module.exports = nextConfig;