import React, { useRef, useEffect } from 'react';
import { MasterySnapshot } from '../lib/adaptiveSample';

interface Props {
  data: MasterySnapshot;
  size?: number;
  stroke?: number;
  maxValue?: number;
}

const colors = [
  '#0d47a1','#1976d2','#42a5f5','#66bb6a','#ffa726','#ef5350','#8e24aa'
];

export const RadialMastery: React.FC<Props> = ({ data, size=340, stroke=10, maxValue=100 }) => {
  const canvasRef = useRef<HTMLCanvasElement|null>(null);
  useEffect(()=>{
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    ctx.clearRect(0,0,size,size);

    const entries = Object.entries(data);
    const total = entries.length;
    const center = size/2;
    const radiusBase = size/2 - stroke - 10;
    const step = radiusBase / (total+1);

    ctx.font = '12px sans-serif';
    ctx.textAlign = 'center';

    entries.forEach(([skill, val], idx)=>{
      const r = radiusBase - idx*step;
      const pct = Math.min(val, maxValue)/maxValue;
      const start = -Math.PI/2;
      const end = start + pct * Math.PI*2;

      // trilho
      ctx.beginPath();
      ctx.strokeStyle = '#ddd';
      ctx.lineWidth = stroke;
      ctx.arc(center, center, r, 0, Math.PI*2);
      ctx.stroke();

      // progresso
      ctx.beginPath();
      ctx.strokeStyle = colors[idx % colors.length];
      ctx.lineCap = 'round';
      ctx.arc(center, center, r, start, end);
      ctx.stroke();

      ctx.fillStyle = '#333';
      ctx.fillText(`${skill} (${val}%)`, center, center - r + stroke/2);
    });
  }, [data,size,stroke,maxValue]);
  return <canvas ref={canvasRef} width={size} height={size} />;
};