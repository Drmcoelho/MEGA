"""
Treino LoRA (placeholder). Não executa treino real — define pipeline base.
Integração futura: peft / transformers / bitsandbytes.
"""

from config import FinetuneConfig


def load_dataset():
    # Futuro: stream JSONL
    return [{"input": "Pergunta X", "output": "Resposta Y"}]


def main():
    cfg = FinetuneConfig()
    data = load_dataset()
    print(f"[LOADER] {len(data)} amostras carregadas.")
    print(f"[CONFIG] {cfg}")
    print("[LOOP] Simulando passos de treino...")
    for step in range(0, cfg.max_steps, 50):
        print(f"Step {step}: placeholder loss=1.{100 - step}")
    print("Treino LoRA placeholder finalizado.")


if __name__ == "__main__":
    main()
