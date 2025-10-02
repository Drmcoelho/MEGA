import fs from 'fs';
import path from 'path';
import YAML from 'yaml';

export interface ModuleManifest {
  id: string;
  title: string;
  version?: string;
  objectives?: string[];
  subskills?: string[];
  prerequisites?: string[];
  estimated_time_hours?: number;
  disclaimer?: string;
}

export function loadManifests(): ModuleManifest[] {
  // Try from repo root first (when building from apps/web, go up two levels)
  let base = path.join(process.cwd(), '..', '..', 'content', 'modules');
  if (!fs.existsSync(base)) {
    // Fallback to direct path (when building from monorepo root)
    base = path.join(process.cwd(), 'content', 'modules');
  }
  if (!fs.existsSync(base)) return [];
  const dirs = fs.readdirSync(base).filter(d => fs.statSync(path.join(base, d)).isDirectory());
  const manifests: ModuleManifest[] = [];
  for (const d of dirs) {
    const manifestPath = path.join(base, d, 'manifest.yaml');
    if (fs.existsSync(manifestPath)) {
      const raw = fs.readFileSync(manifestPath, 'utf-8');
      try {
        const data = YAML.parse(raw);
        manifests.push(data);
      } catch (e) {
        console.warn('Erro ao parsear manifest', manifestPath, e);
      }
    }
  }
  return manifests.sort((a,b)=>a.id.localeCompare(b.id));
}