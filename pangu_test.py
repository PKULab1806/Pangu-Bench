# main_test_pangu_npu.py

import argparse
import os

from easyjailbreak.attacker.Multilingual_Deng_2023 import Multilingual
from easyjailbreak.attacker.Jailbroken_wei_2023 import Jailbroken
from easyjailbreak.attacker.AutoDAN_Liu_2023 import AutoDAN
from easyjailbreak.attacker.SelfEval import (
    selfevalcheck,
    selfevalcheck_evaluation,
    claude3_check_dataset,
)
from easyjailbreak.datasets import JailbreakDataset
from easyjailbreak.models.openai_model import OpenaiModel


def check_json_valid(json_file):
    import json
    import os
    import time

    if not os.path.exists(json_file):
        return False
    try:

        def is_file_stable(path, interval=120):
            try:
                size1 = os.path.getsize(path)
                time.sleep(interval)
                size2 = os.path.getsize(path)
                return size1 == size2
            except FileNotFoundError:
                # 中途被删除 / 重建，视为不稳定
                return False

        # 文件大小还在变化 → 直接退出
        if not is_file_stable(json_file):
            return True
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return True
    except json.JSONDecodeError:
        return False


def main():
    parser = argparse.ArgumentParser(
        description="SG-Bench Evaluation with Pangu Model on NPU"
    )
    parser.add_argument(
        "--model_name", default="openPangu-Embedded-1B-V1.1", type=str, required=True
    )
    parser.add_argument(
        "--model_path",
        default="../models/openPangu-Embedded-1B-V1.1",
        type=str,
        required=True,
    )
    parser.add_argument("--dataset_name", type=str, default="SG-Bench", required=True)
    parser.add_argument(
        "--eval_task",
        default="original_query",
        type=str,
        choices=[
            "original_query",
            "jailbreak_attack",
            "multiple_choice",
            "safety_judgement",
        ],
        required=True,
    )
    parser.add_argument(
        "--prompt_mode",
        default="",
        type=str,
        choices=[
            "",
            "ToP",
            "ToP_fewshot_harmful",
            "ToP_fewshot_general",
            "RoP",
            "RoP_fewshot_harmful",
            "RoP_fewshot_general",
            "COT",
            "fewshot",
            "explanation",
        ],
    )
    parser.add_argument("--enable_thinking", action="store_true", default=False)

    parser.add_argument("--multi_turn", action="store_true", default=False)
    parser.add_argument("--judge_model_name", default="Qwen3Guard-Gen-0.6B", type=str)
    parser.add_argument(
        "--judge_model_path", default="../models/Qwen3Guard-Gen-0.6B", type=str
    )
    parser.add_argument("--attack", action="store_true", default=False)
    parser.add_argument("--evaluation", action="store_true", default=False)
    args = parser.parse_args()

    supprted_dataset_list = {
        "SG-Bench": [
            "../datasets/SG-Bench/original_query",
            "../datasets/SG-Bench/original_query",
            "../datasets/SG-Bench/mcq_test/mcq_test.json",
            "../datasets/SG-Bench/judge_test/judge_test.json",
            1442,
        ],
        "SG-Bench-Fix": [
            "../datasets/SG-Bench/original_query",
            "../datasets/SG-Bench/jailbreak_prompt",
            "../datasets/SG-Bench/mcq_test/mcq_test.json",
            "../datasets/SG-Bench/judge_test/judge_test.json",
            1442,
        ],
        "AdvBench520": [
            "../datasets/AdvBench520/original_query",
            "../datasets/AdvBench520/original_query",
            "",
            520,
        ],
        "SaladBench": [
            "../datasets/SaladBench/base_set",
            "../datasets/SaladBench/attack_enhanced_set",
            "../datasets/SaladBench/mcq_set.json",
            "",
            "",
        ],
        "HarmBench": [
            "../datasets/HarmBench/original_query",
            "../datasets/HarmBench/original_query",
            "",
            "",
            300,
        ],
        "xstest": [
            "../datasets/xstest/original_query",
            "../datasets/xstest/original_query",
            "",
            "",
            450,
        ],
        "BBQ": [
            "",
            "",
            "../datasets/BBQ/mcq_test/bbq_all.json",
            "",
            58492,
        ],
        "BBQ_Age": [
            "",
            "",
            "../datasets/BBQ_split/Age/BBQ_MCQ-Age.json",
            "",
            58492,
        ],
        "BBQ_Disability_status": [
            "",
            "",
            "../datasets/BBQ_split/Disability_status/BBQ_MCQ-Disability_status.json",
            "",
            58492,
        ],
        "BBQ_Gender_identity": [
            "",
            "",
            "../datasets/BBQ_split/Gender_identity/BBQ_MCQ-Gender_identity.json",
            "",
            58492,
        ],
        "BBQ_Nationality": [
            "",
            "",
            "../datasets/BBQ_split/Nationality/BBQ_MCQ-Nationality.json",
            "",
            58492,
        ],
        "BBQ_Physical_appearance": [
            "",
            "",
            "../datasets/BBQ_split/Physical_appearance/BBQ_MCQ-Physical_appearance.json",
            "",
            58492,
        ],
        "BBQ_Race_ethnicity": [
            "",
            "",
            "../datasets/BBQ_split/Race_ethnicity/BBQ_MCQ-Race_ethnicity.json",
            "",
            58492,
        ],
        "BBQ_Race_x_gender": [
            "",
            "",
            "../datasets/BBQ_split/Race_x_gender/BBQ_MCQ-Race_x_gender.json",
            "",
            58492,
        ],
        "BBQ_Race_x_SES": [
            "",
            "",
            "../datasets/BBQ_split/Race_x_SES/BBQ_MCQ-Race_x_SES.json",
            "",
            58492,
        ],
        "BBQ_Religion": [
            "",
            "",
            "../datasets/BBQ_split/Religion/BBQ_MCQ-Religion.json",
            "",
            58492,
        ],
        "BBQ_SES": [
            "",
            "",
            "../datasets/BBQ_split/SES/BBQ_MCQ-SES.json",
            "",
            58492,
        ],
        "BBQ_Sexual_orientation": [
            "",
            "",
            "../datasets/BBQ_split/Sexual_orientation/BBQ_MCQ-Sexual_orientation.json",
            "",
            58492,
        ],
    }
    supported_model_list = [
        "llama-2-7b",
        "Llama-Guard-3-8B",
        "openPangu-Embedded-1B-V1.1",
        "openPangu-Embedded-7B-V1.1",
        "Qwen2.5-7B",
        "Qwen3-4B-SafeRL",
        "Qwen3Guard-Gen-4B",
        "Qwen3Guard-Gen-8B",
        "Qwen2.5-7B-Instruct",
        "Llama-2-7b-chat-hf",
        "Qwen-7B-Chat",
        "deepseek-llm-7b-base",
        "deepseek-llm-7b-chat",
        "Qwen-7B",
        "Qwen3-8B",
    ]
    if args.model_name == "openPangu-Embedded-7B-V1.1":
        from easyjailbreak.models.pangu_model7b import from_pretrained
    elif "Qwen-" in args.model_name:
        from easyjailbreak.models.modelscope_model import from_pretrained
    elif "Qwen3-" in args.model_name:
        from easyjailbreak.models.qwen3_model import from_pretrained
    elif "deepseek-" in args.model_name:
        from easyjailbreak.models.deepseek_model import from_pretrained
    else:
        from easyjailbreak.models.pangu_model import from_pretrained
    if args.judge_model_name == "":
        args.judge_model_name = "Qwen3Guard-Gen-8B"
        args.judge_model_path = "../models/Qwen3Guard-Gen-8B"

    if args.attack:
        print("-----------Attack Mode-----------")
        print("target model:", args.model_name)

        if args.model_name in supported_model_list:
            target_model = from_pretrained(
                model_name_or_path=args.model_path, model_name="llama-2"
            )
            eval_model = target_model
        else:
            print("model does not implement yet.....")
            exit()
    elif args.evaluation:
        print("-----------Evaluation Mode-----------")
        eval_model = from_pretrained(
            model_name_or_path=args.judge_model_path, model_name="llama-2"
        )
        target_model = eval_model
    else:
        print("The mode is not supported ....")
        exit()
    if args.enable_thinking:
        args.model_name += "_think"
    if args.eval_task == "original_query":
        dataset = JailbreakDataset(supprted_dataset_list[args.dataset_name][0])
        print(len(dataset))
        attacker = Multilingual(
            attack_model=target_model,
            target_model=target_model,
            eval_model=eval_model,
            jailbreak_datasets=dataset,
            multi_turn=args.multi_turn,
            special_method=(
                "LlamaGuard"
                if args.judge_model_name == "Llama-Guard-3-8B"
                else "Qwen3Guard"
            ),
            enable_think=args.enable_thinking,
        )

        save_path_template = "./outputs_results_benchmark/llm_response/{dataset_name}/{prompt_mode}/{dataset_name}-{model_name}.json"
        eval_path_template = "./outputs_results_benchmark/eval_results/{judge_model_name}/{dataset_name}/{prompt_mode}/{dataset_name}-{model_name}_eval.json"

        if args.attack:
            save_path = save_path_template.format(
                dataset_name=args.dataset_name,
                prompt_mode=args.prompt_mode,
                model_name=args.model_name,
            )
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            if check_json_valid(save_path):
                print(
                    f"{save_path} already exists and is a valid JSON. Skipping attack."
                )
                return
            print("save_path:", save_path)
            attacker.attack(save_path, args.prompt_mode)
        elif args.evaluation:
            save_path = save_path_template.format(
                dataset_name=args.dataset_name,
                prompt_mode=args.prompt_mode,
                model_name=args.model_name,
            )
            eval_path = eval_path_template.format(
                judge_model_name=args.judge_model_name,
                dataset_name=args.dataset_name,
                prompt_mode=args.prompt_mode,
                model_name=args.model_name,
            )
            os.makedirs(os.path.dirname(eval_path), exist_ok=True)
            if check_json_valid(eval_path):
                print(
                    f"{eval_path} already exists and is a valid JSON. Skipping evaluation."
                )
                return
            print("save_path:", save_path)
            attacker.evaluation(input_path=save_path, eval_output_path=eval_path)

    elif args.eval_task == "jailbreak_attack":
        # Then instantiate the recipe.
        dataset = JailbreakDataset(supprted_dataset_list[args.dataset_name][1])
        print(len(dataset))
        attacker = Jailbroken(
            attack_model=target_model,
            target_model=target_model,
            eval_model=eval_model,
            jailbreak_datasets=dataset,
            special_method=(
                "LlamaGuard"
                if args.judge_model_name == "Llama-Guard-3-8B"
                else "Qwen3Guard"
            ),
            enable_think=args.enable_thinking,
        )

        # attacker = AutoDAN(attack_model=target_model,
        #                 target_model=target_model,
        #                 eval_model=eval_model,
        #                 eval_by_gpt4=args.eval_by_gpt4,
        #                 jailbreak_datasets=dataset)

        save_path_template = "./outputs_results_benchmark/llm_response_jailbreak/{dataset_name}/{prompt_mode}/{dataset_name}_jailbreak-{model_name}.json"
        eval_path_template = "./outputs_results_benchmark/eval_results_jailbreak/{judge_model_name}/{dataset_name}/{prompt_mode}/{dataset_name}_jailbreak-{model_name}_eval.json"

        if args.attack:
            save_path = save_path_template.format(
                dataset_name=args.dataset_name,
                prompt_mode=args.prompt_mode,
                model_name=args.model_name,
            )
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            if check_json_valid(save_path):
                print(
                    f"{save_path} already exists and is a valid JSON. Skipping attack."
                )
                return
            attacker.attack(save_path, args.prompt_mode)
        elif args.evaluation:
            save_path = save_path_template.format(
                dataset_name=args.dataset_name,
                prompt_mode=args.prompt_mode,
                model_name=args.model_name,
            )
            eval_path = eval_path_template.format(
                judge_model_name=args.judge_model_name,
                dataset_name=args.dataset_name,
                prompt_mode=args.prompt_mode,
                model_name=args.model_name,
            )
            os.makedirs(os.path.dirname(eval_path), exist_ok=True)
            if check_json_valid(eval_path):
                print(
                    f"{eval_path} already exists and is a valid JSON. Skipping evaluation."
                )
                return
            print(save_path)
            print(eval_path)
            ASR = attacker.evaluation(input_path=save_path, eval_output_path=eval_path)
            print(args.dataset_name + "/" + args.model_name + "/" + args.eval_task)
            print("jailbreak attack success rate:", str(ASR))

    elif args.eval_task == "multiple_choice":
        if "BBQ" in args.dataset_name:
            from easyjailbreak.attacker.MCQ_v2 import (
                MultipleChioceQuestion,
                MultipleChioceQuestion_evaluation,
            )
        else:
            from easyjailbreak.attacker.MCQ import (
                MultipleChioceQuestion,
                MultipleChioceQuestion_evaluation,
            )
        if args.enable_thinking:
            args.model_name += "ing"
        save_path_template = "./outputs_results_benchmark/llm_response_mcq/{dataset_name}/{prompt_mode}/{dataset_name}_MCQ-{model_name}.json"
        eval_path_template_1 = "./outputs_results_benchmark/eval_results_mcq/{judge_model_name}/{dataset_name}/{prompt_mode}/{dataset_name}_MCQ-{model_name}_eval.json"
        eval_path_template_2 = "./outputs_results_benchmark/eval_results_mcq/{judge_model_name}/{dataset_name}/{prompt_mode}/{dataset_name}_MCQ-{model_name}_eval-2.json"
        if args.attack:
            save_path = save_path_template.format(
                dataset_name=args.dataset_name,
                prompt_mode=args.prompt_mode,
                model_name=args.model_name,
            )
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            if check_json_valid(save_path):
                print(
                    f"{save_path} already exists and is a valid JSON. Skipping attack."
                )
                return
            MultipleChioceQuestion(
                target_model=target_model,
                test_file=supprted_dataset_list[args.dataset_name][2],
                save_path=save_path,
                prompt_mode=args.prompt_mode,
                enable_thinking=args.enable_thinking,
            )
        elif args.evaluation:
            save_path = save_path_template.format(
                dataset_name=args.dataset_name,
                prompt_mode=args.prompt_mode,
                model_name=args.model_name,
            )
            eval_path_1 = eval_path_template_1.format(
                judge_model_name=args.judge_model_name,
                dataset_name=args.dataset_name,
                prompt_mode=args.prompt_mode,
                model_name=args.model_name,
            )
            eval_path_2 = eval_path_template_2.format(
                judge_model_name=args.judge_model_name,
                dataset_name=args.dataset_name,
                prompt_mode=args.prompt_mode,
                model_name=args.model_name,
            )
            os.makedirs(os.path.dirname(eval_path_1), exist_ok=True)
            os.makedirs(os.path.dirname(eval_path_2), exist_ok=True)
            (
                false_rate_non_format_1,
                false_rate_format_1,
                false_format_nums_1,
                error_format_nums_1,
            ) = MultipleChioceQuestion_evaluation(
                eval_model=eval_model, results_file=save_path, save_path=eval_path_1
            )
            (
                false_rate_non_format,
                false_rate_format,
                false_format_nums,
                error_format_nums,
            ) = MultipleChioceQuestion_evaluation(
                eval_model=eval_model,
                results_file=save_path,
                save_path=eval_path_2,
                format_mode=False,
            )
            # print("false_rate_non_format / false_rate_format / false_format_nums / error_format_nums")
            # print(false_rate_non_format_1, false_rate_format_1, false_format_nums_1, error_format_nums_1)
            # print("--------------------------------------")
            # print("false_rate_non_format / false_rate_format / false_format_nums / error_format_nums")
            print("multiple-choice question test -- false rate:", false_rate_non_format)


if __name__ == "__main__":
    main()
