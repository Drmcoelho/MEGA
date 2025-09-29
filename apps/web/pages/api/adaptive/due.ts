import type { NextApiRequest, NextApiResponse } from "next";
import fs from "fs";
import path from "path";
import { errorResponse } from "../../../lib/apiErrors";

const DATA = path.join(process.cwd(), ".adaptive", "data.json");

export default function handler(_req: NextApiRequest, res: NextApiResponse) {
  try {
    if (!fs.existsSync(DATA)) return res.status(200).json({ due: [] });
    const raw = JSON.parse(fs.readFileSync(DATA, "utf-8"));
    const intervals = raw.intervals || {};
    const now = Math.floor(Date.now() / 1000);
    const due: string[] = [];
    Object.entries(intervals).forEach(([itemId, [interval, ts]]: any) => {
      if (now - ts >= interval) due.push(itemId);
    });
    res.status(200).json({ due });
  } catch (e: any) {
    errorResponse(res, 500, "DUE_READ_ERROR", e?.message);
  }
}
