export interface ApiErrorShape {
  error: string;
  details?: any;
}
export function errorResponse(
  res: any,
  status: number,
  message: string,
  details?: any,
) {
  res.status(status).json({ error: message, details });
}
