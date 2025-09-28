import fs from 'fs'
import path from 'path'
import yaml from 'js-yaml'

export interface ModuleManifest {
  id: string
  title: string
  version: string
  objectives: string[]
  subskills: string[]
  prerequisites: string[]
  estimated_time_hours: number
  disclaimer?: string
}

export function loadModules(): ModuleManifest[] {
  const modulesDir = path.join(process.cwd(), '../../content/modules')
  
  try {
    const moduleNames = fs.readdirSync(modulesDir)
    const modules: ModuleManifest[] = []
    
    for (const moduleName of moduleNames) {
      const manifestPath = path.join(modulesDir, moduleName, 'manifest.yaml')
      if (fs.existsSync(manifestPath)) {
        const manifestContent = fs.readFileSync(manifestPath, 'utf8')
        const manifest = yaml.load(manifestContent) as ModuleManifest
        modules.push(manifest)
      }
    }
    
    return modules
  } catch (error) {
    console.warn('Could not load modules:', error)
    return []
  }
}