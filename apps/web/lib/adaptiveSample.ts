export interface MasterySnapshot {
  [subskill: string]: number; // percent
}

export function sampleMastery(): MasterySnapshot {
  return {
    "fundamentos-ecg": 42,
    "morfologia-basica": 65,
    "analise-eixo": 30,
    "intervalos": 55,
    "regularidade": 20,
    "largura-qrs": 10
  };
}

export function dueItemsSample(): string[] {
  return ["qrs-interpret-001", "interval-av-block-002", "axis-calc-003"];
}