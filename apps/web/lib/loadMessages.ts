import path from 'path';
import fs from 'fs';

export async function loadMessages(locale: string) {
  // Try web app directory first (when building from apps/web)
  let file = path.join(process.cwd(), 'messages', `${locale}.json`);
  if (!fs.existsSync(file)) {
    // Fallback to repo root structure (when building from monorepo root)
    file = path.join(process.cwd(), 'apps', 'web', 'messages', `${locale}.json`);
  }
  if (!fs.existsSync(file)) {
    return {};
  }
  return JSON.parse(fs.readFileSync(file, 'utf-8'));
}