# DEVICE_ID=1
# export ASCEND_RT_VISIBLE_DEVICES=$DEVICE_ID
# MODEL_NAME="openPangu-Embedded-1B-V1.1"
# MODEL_PATH="/data/yangshuaishuai/models/${MODEL_NAME}/"
# python pangu_test.py \
#     --model_name ${MODEL_NAME} \
#     --model_path ${MODEL_PATH} \
#     --dataset_name SG-Bench \
#     --eval_task jailbreak_attack \
#     --attack 

# DEVICE_ID=1
# export ASCEND_RT_VISIBLE_DEVICES=$DEVICE_ID
# MODEL_NAME="openPangu-Embedded-1B-V1.1"
# MODEL_PATH="/data/yangshuaishuai/models/${MODEL_NAME}/"
# python pangu_test.py \
#     --model_name ${MODEL_NAME} \
#     --model_path ${MODEL_PATH} \
#     --dataset_name AdvBench520 \
#     --eval_task original_query \
#     --attack 

# DEVICE_ID=2
# export ASCEND_RT_VISIBLE_DEVICES=$DEVICE_ID
# MODEL_NAME="openPangu-Embedded-1B-V1.1"
# MODEL_PATH="/data/yangshuaishuai/models/${MODEL_NAME}/"
# JUDGE_MODEL_NAME="Qwen3Guard-Gen-0.6B"
# JUDGE_MODEL_PATH="/data/yangshuaishuai/models/${JUDGE_MODEL_NAME}/"
# python pangu_test.py \
#     --model_name ${MODEL_NAME} \
#     --model_path ${MODEL_PATH} \
#     --dataset_name AdvBench520 \
#     --eval_task original_query \
#     --evaluation \
#     --judge_model_name  ${JUDGE_MODEL_NAME} \
#     --judge_model_path  ${JUDGE_MODEL_PATH} \

# DEVICE_ID=1
# export ASCEND_RT_VISIBLE_DEVICES=$DEVICE_ID
# MODEL_NAME="openPangu-Embedded-1B-V1.1"
# MODEL_PATH="/data/yangshuaishuai/models/${MODEL_NAME}/"
# python pangu_test.py \
#     --model_name ${MODEL_NAME} \
#     --model_path ${MODEL_PATH} \
#     --dataset_name SaladBench \
#     --eval_task original_query \
#     --attack 

# DEVICE_ID=1
# export ASCEND_RT_VISIBLE_DEVICES=$DEVICE_ID
# MODEL_NAME="openPangu-Embedded-1B-V1.1"
# MODEL_PATH="/data/yangshuaishuai/models/${MODEL_NAME}/"
# python pangu_test.py \
#     --model_name ${MODEL_NAME} \
#     --model_path ${MODEL_PATH} \
#     --dataset_name HarmBench \
#     --eval_task original_query \
#     --attack 

# DEVICE_ID=1
# export ASCEND_RT_VISIBLE_DEVICES=$DEVICE_ID
# MODEL_NAME="openPangu-Embedded-1B-V1.1"
# MODEL_PATH="/data/yangshuaishuai/models/${MODEL_NAME}/"
# JUDGE_MODEL_NAME="Qwen3Guard-Gen-0.6B"
# JUDGE_MODEL_PATH="/data/yangshuaishuai/models/${JUDGE_MODEL_NAME}/"
# python pangu_test.py \
#     --model_name ${MODEL_NAME} \
#     --model_path ${MODEL_PATH} \
#     --dataset_name HarmBench \
#     --eval_task original_query \
#     --evaluation \
#     --judge_model_name  ${JUDGE_MODEL_NAME} \
#     --judge_model_path  ${JUDGE_MODEL_PATH} \

# DEVICE_ID=1
# export ASCEND_RT_VISIBLE_DEVICES=$DEVICE_ID
# MODEL_NAME="openPangu-Embedded-1B-V1.1"
# MODEL_PATH="/data/yangshuaishuai/models/${MODEL_NAME}/"
# JUDGE_MODEL_NAME="Qwen3Guard-Gen-0.6B"
# JUDGE_MODEL_PATH="/data/yangshuaishuai/models/${JUDGE_MODEL_NAME}/"
# python pangu_test.py \
#     --model_name ${MODEL_NAME} \
#     --model_path ${MODEL_PATH} \
#     --dataset_name SG-Bench \
#     --eval_task original_query \
#     --evaluation \
#     --judge_model_name  ${JUDGE_MODEL_NAME} \
#     --judge_model_path  ${JUDGE_MODEL_PATH} \

# DEVICE_ID=1
# export ASCEND_RT_VISIBLE_DEVICES=$DEVICE_ID
# MODEL_NAME="openPangu-Embedded-1B-V1.1"
# MODEL_PATH="/data/yangshuaishuai/models/${MODEL_NAME}/"
# python pangu_test.py \
#     --model_name ${MODEL_NAME} \
#     --model_path ${MODEL_PATH} \
#     --dataset_name SG-Bench \
#     --eval_task multiple_choice \
#     --attack 

# DEVICE_ID=1
# export ASCEND_RT_VISIBLE_DEVICES=$DEVICE_ID
# MODEL_NAME="openPangu-Embedded-1B-V1.1"
# MODEL_PATH="/data/yangshuaishuai/models/${MODEL_NAME}/"
# JUDGE_MODEL_NAME="Qwen3Guard-Gen-0.6B"
# JUDGE_MODEL_PATH="/data/yangshuaishuai/models/${JUDGE_MODEL_NAME}/"
# python pangu_test.py \
#     --model_name ${MODEL_NAME} \
#     --model_path ${MODEL_PATH} \
#     --dataset_name SG-Bench \
#     --eval_task multiple_choice \
#     --evaluation \
#     --judge_model_name  ${JUDGE_MODEL_NAME} \
#     --judge_model_path  ${JUDGE_MODEL_PATH} \


DEVICE_ID=1
export ASCEND_RT_VISIBLE_DEVICES=$DEVICE_ID
DATASET_NAME_LIST=("SG-Bench" "AdvBench520" "HarmBench")
MODEL_NAME="openPangu-Embedded-1B-V1.1"
MODEL_PATH="/data/yangshuaishuai/models/${MODEL_NAME}/"
for DATASET_NAME in ${DATASET_NAME_LIST[@]}
do
  echo "Attacking ${MODEL_NAME} on ${DATASET_NAME}..."
  python pangu_test.py \
    --model_name ${MODEL_NAME} \
    --model_path ${MODEL_PATH} \
    --dataset_name ${DATASET_NAME} \
    --eval_task jailbreak_attack \
    --attack 
    echo "Attack of ${MODEL_NAME} on ${DATASET_NAME} completed."
done

JUDGE_MODEL_NAME_LIST=("Qwen3Guard-Gen-0.6B" "Qwen3Guard-Gen-4B" "Qwen3Guard-Gen-8B" "Llama-Guard-3-8B")
for DATASET_NAME in ${DATASET_NAME_LIST[@]}
do
  for JUDGE_MODEL_NAME in ${JUDGE_MODEL_NAME_LIST[@]}
  do
    echo "Evaluating ${MODEL_NAME} on ${DATASET_NAME} with judge model ${JUDGE_MODEL_NAME}..."
    python pangu_test.py \
      --model_name ${MODEL_NAME} \
      --model_path ${MODEL_PATH} \
      --dataset_name ${DATASET_NAME} \
      --eval_task jailbreak_attack \
      --evaluation \
      --judge_model_name  ${JUDGE_MODEL_NAME} \
      --judge_model_path  "/data/yangshuaishuai/models/${JUDGE_MODEL_NAME}/"
    echo "Evaluation of ${MODEL_NAME} on ${DATASET_NAME} with judge model ${JUDGE_MODEL_NAME} completed."
  done
done