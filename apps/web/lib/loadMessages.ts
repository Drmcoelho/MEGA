import path from 'path';
import fs from 'fs';

export async function loadMessages(locale: string) {
  const file = path.join(process.cwd(), 'apps', 'web', 'messages', `${locale}.json`);
  if (!fs.existsSync(file)) {
    return {};
  }
  return JSON.parse(fs.readFileSync(file, 'utf-8'));
}