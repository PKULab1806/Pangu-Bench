# Pangu-Bench: LLM Safety Evaluation Benchmark

A comprehensive benchmark for evaluating LLM safety against jailbreak attacks and prompt-based defenses.

**Powered by openPangu**

*openPangu is a trademark of Huawei Technologies Co., Ltd.*

This project is developed based on [openPangu](https://huggingface.co/FreedomIntelligence/openPangu-Embedded-7B). This work was supported by the openPangu project.

## Key Findings from Our Research

Our paper ["How Few-shot Demonstrations Affect Prompt-based Defenses Against LLM Jailbreak Attacks"](https://arxiv.org/) presents the following key findings:

### Core Discovery: Divergent Interaction Effects

**Few-shot demonstrations produce opposite effects on different defense strategies:**

| Defense Strategy | Effect of Few-shot | Mechanism |
|-----------------|-------------------|-----------|
| **Role-Oriented Prompts (RoP)** | +2.0% average improvement | Role reinforcement - few-shot strengthens role identity |
| **Task-Oriented Prompts (ToP)** | -6.6% average degradation | Attention distraction - few-shot diverts focus from task instructions |

### Quantitative Results

- Few-shot enhances RoP's safety rate by **up to 4.5%** through reinforcing role identity
- Few-shot degrades ToP's effectiveness by **up to 21.2%** through distracting attention from task instructions
- Think mode models exhibit **higher vulnerability** to both jailbreak attacks and negative few-shot interactions

### Practical Recommendations

Based on our comprehensive evaluation on multiple LLMs (openPangu, Qwen, DeepSeek, Llama) across four benchmarks (AdvBench, HarmBench, SG-Bench, XSTest):

1. **Use RoP + Few-shot** for optimal jailbreak defense
2. **Avoid ToP + Few-shot** combinations
3. **Exercise caution** with reasoning-enhanced (think) models in safety-critical scenarios

## Features

- **Multiple Safety Benchmarks**: Support for SG-Bench, AdvBench, HarmBench, XSTest, SaladBench, BBQ
- **Various Jailbreak Attacks**: AIM, DAN, Evil Confident, Prefix Rejection, Poems, Refusal Suppression, GCG, AutoDAN, PAIR, etc.
- **Prompt-based Defenses**: Role-Oriented Prompts (RoP), Task-Oriented Prompts (ToP), few-shot demonstrations
- **Multiple Evaluation Tasks**: Original query, jailbreak attack, multiple choice, safety judgment
- **Multi-model Support**: openPangu, Qwen, DeepSeek, Llama, and more

## Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/Pangu-Bench.git
cd Pangu-Bench

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```bash
# Run safety evaluation on openPangu model
python pangu_test.py \
    --model_name openPangu-Embedded-1B-V1.1 \
    --model_path /path/to/model \
    --dataset_name SG-Bench \
    --eval_task original_query \
    --attack
```

### With Prompt-based Defense

```bash
# Test with Role-Oriented Prompts + Few-shot (Recommended)
python pangu_test.py \
    --model_name openPangu-Embedded-1B-V1.1 \
    --model_path /path/to/model \
    --dataset_name SG-Bench \
    --eval_task original_query \
    --prompt_mode RoP_fewshot_general \
    --attack
```

### Evaluation Mode

```bash
# Evaluate model responses using judge model
python pangu_test.py \
    --model_name openPangu-Embedded-1B-V1.1 \
    --model_path /path/to/model \
    --dataset_name SG-Bench \
    --eval_task original_query \
    --evaluation \
    --judge_model_name Qwen3Guard-Gen-0.6B \
    --judge_model_path /path/to/judge_model
```

## Command Line Arguments

| Argument | Description | Options |
|----------|-------------|---------|
| `--model_name` | Target model name | openPangu-Embedded-1B-V1.1, Qwen2.5-7B, etc. |
| `--model_path` | Path to model weights | - |
| `--dataset_name` | Safety benchmark | SG-Bench, AdvBench520, HarmBench, xstest, SaladBench, BBQ |
| `--eval_task` | Evaluation task | original_query, jailbreak_attack, multiple_choice, safety_judgement |
| `--prompt_mode` | Defense strategy | "", ToP, ToP_fewshot_harmful, ToP_fewshot_general, RoP, RoP_fewshot_harmful, RoP_fewshot_general |
| `--enable_thinking` | Enable think mode | flag |
| `--attack` | Run attack mode | flag |
| `--evaluation` | Run evaluation mode | flag |
| `--judge_model_name` | Safety judge model | Qwen3Guard-Gen-0.6B, Llama-Guard-3-8B, etc. |

## Project Structure

```
Pangu-Bench/
├── pangu_test.py              # Main evaluation script
├── run_pangu.sh               # Batch evaluation scripts
├── easyjailbreak/
│   ├── attacker/              # Jailbreak attack implementations
│   │   ├── Multilingual_Deng_2023.py
│   │   ├── Jailbroken_wei_2023.py
│   │   ├── AutoDAN_Liu_2023.py
│   │   ├── GCG_Zou_2023.py
│   │   ├── PAIR_chao_2023.py
│   │   └── ...
│   ├── models/                # Model wrappers
│   │   ├── pangu_model.py     # openPangu model
│   │   ├── qwen3_model.py
│   │   ├── deepseek_model.py
│   │   └── ...
│   ├── datasets/              # Dataset loaders
│   ├── metrics/               # Evaluation metrics
│   ├── mutation/              # Prompt mutation strategies
│   └── selector/              # Selection policies
├── datasets/                  # Safety benchmark datasets
└── outputs_results_benchmark/ # Evaluation results
```

## Supported Models

| Model | Model Path |
|-------|------------|
| openPangu-Embedded-1B-V1.1 | `easyjailbreak.models.pangu_model` |
| openPangu-Embedded-7B-V1.1 | `easyjailbreak.models.pangu_model7b` |
| Qwen-7B / Qwen-7B-Chat | `easyjailbreak.models.modelscope_model` |
| Qwen3-8B / Qwen3-4B-SafeRL | `easyjailbreak.models.qwen3_model` |
| Qwen2.5-7B-Instruct | `easyjailbreak.models.qwen2_model` |
| DeepSeek-7B | `easyjailbreak.models.deepseek_model` |
| Llama-2-7B / Llama-Guard-3-8B | `easyjailbreak.models.huggingface_model` |

## Citation

If you find this work useful, please cite our paper:

```bibtex
@article{wang2026fewshot,
  title={How Few-shot Demonstrations Affect Prompt-based Defenses Against LLM Jailbreak Attacks},
  author={Wang, Yanshu and Yang, Shuaishuai and He, Jingjing and Yang, Tong},
  journal={arXiv preprint},
  year={2026}
}
```

## License

This project is licensed under the **openPangu Model License Agreement Version 1.0** - see the [LICENSE](LICENSE) file for details.

Key requirements:
- Display "Powered by openPangu" acknowledgement when distributing products based on this model
- Include trademark notice: "openPangu is a trademark of Huawei Technologies Co., Ltd."
- Retain a copy of this license agreement in any distribution

## Contact

For questions and feedback, please open an issue or contact:
- Tong Yang: yangtong@pku.edu.cn
