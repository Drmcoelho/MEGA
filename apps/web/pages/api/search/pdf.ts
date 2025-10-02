import type { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs';
import path from 'path';
import { errorResponse } from '../../../lib/apiErrors';

const INDEX = path.join(process.cwd(), 'data', 'pdf_index.json');

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const q = (req.query.q || '').toString().toLowerCase();
  if (!q) return errorResponse(res, 400, 'QUERY_REQUIRED');
  try {
    if (!fs.existsSync(INDEX)) return res.status(200).json({results:[]});
    const data = JSON.parse(fs.readFileSync(INDEX,'utf-8'));
    const results = Object.entries<any>(data)
      .filter(([_, meta]) => (meta.preview || "").toLowerCase().includes(q))
      .map(([file, meta]) => ({ file, snippet: meta.preview.slice(0,300), pages: meta.pages, chars: meta.chars }));
    res.status(200).json({results});
  } catch (e:any) {
    errorResponse(res, 500, 'PDF_SEARCH_ERROR', e?.message);
  }
}