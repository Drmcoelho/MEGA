from dataclasses import dataclass

@dataclass
class FinetuneConfig:
    base_model: str = "mistral-7b-instruct"
    output_dir: str = "outputs"
    learning_rate: float = 2e-4
    lora_rank: int = 16
    batch_size: int = 4
    max_steps: int = 200