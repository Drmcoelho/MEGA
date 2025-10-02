import type { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs';
import path from 'path';
import { errorResponse } from '../../../lib/apiErrors';

const DATA = path.join(process.cwd(), '.adaptive', 'data.json');

function load(): any {
  if (!fs.existsSync(DATA)) return { intervals:{}, mastery:{} };
  return JSON.parse(fs.readFileSync(DATA,'utf-8'));
}
function save(obj:any) {
  const dir = path.dirname(DATA);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, {recursive:true});
  fs.writeFileSync(DATA, JSON.stringify(obj, null, 2), 'utf-8');
}

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') return errorResponse(res, 405, 'METHOD_NOT_ALLOWED');
  try {
    const { itemId, rating } = req.body || {};
    if (!itemId || typeof rating !== 'number') return errorResponse(res, 400, 'INVALID_PAYLOAD');
    if (![0,1,2].includes(rating)) return errorResponse(res, 400, 'INVALID_RATING');
    const store = load();
    const prev = store.intervals[itemId] || [0,0];
    const lastInterval = prev[0];
    let nextInterval:number;
    if (rating <= 0) nextInterval = 10; else if (rating === 1) nextInterval = Math.max(30, parseInt(String(lastInterval*1.4)) || 30); else nextInterval = Math.max(60, parseInt(String(lastInterval*2.2)) || 60);
    store.intervals[itemId] = [nextInterval, Math.floor(Date.now()/1000)];
    save(store);
    res.status(200).json({ itemId, nextInterval });
  } catch (e:any) {
    errorResponse(res, 500, 'RATE_ERROR', e?.message);
  }
}