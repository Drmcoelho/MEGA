import type { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs';
import path from 'path';
import { errorResponse } from '../../../lib/apiErrors';

const DATA = path.join(process.cwd(), '.adaptive', 'data.json');

export default function handler(_req: NextApiRequest, res: NextApiResponse) {
  try {
    if (!fs.existsSync(DATA)) return res.status(200).json({ mastery: {} });
    const raw = JSON.parse(fs.readFileSync(DATA, 'utf-8'));
    const m = raw.mastery || {};
    const snapshot: Record<string, number> = {};
    Object.entries(m).forEach(([subskill, [sum, attempts]]: any) => {
      snapshot[subskill] = attempts === 0 ? 0 : Math.round((sum / (2 * attempts)) * 10000) / 100;
    });
    res.status(200).json({ mastery: snapshot });
  } catch (e: any) {
    errorResponse(res, 500, 'MASTERy_READ_ERROR', e?.message);
  }
}