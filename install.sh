#!/bin/bash
: ${ENV_PATH:="./venv"}
: ${MODELS_PATH:="./models"}
: ${PYTHON_CMD:="python3"}
if [ ! -d $ENV_PATH ]; then
    ${PYTHON_CMD} -m pip install virtualenv
    ${PYTHON_CMD} -m venv $ENV_PATH
    source $ENV_PATH/bin/activate
    ${PYTHON_CMD} -m pip install -r requirements.txt
else
    echo "The Python environment already exists. Skiped"
fi

${PYTHON_CMD} ./scripts/generate_cfg.py
source $ENV_PATH/bin/activate
MODEL_REPO_ID=$(python -c "from utils.cfg import Settings; \
                        print(Settings('spellchecker.cfg').model)")
MODEL_DIR_NAME=$(echo "$MODEL_REPO_ID" | tr / _)

if [ ! -d $MODELS_PATH/$MODEL_DIR_NAME ]; then
    ${PYTHON_CMD} -c "from huggingface_hub import snapshot_download; \
                    snapshot_download( \
                        repo_id=\"${MODEL_REPO_ID}\", \
                        local_dir=\"${MODELS_PATH}/${MODEL_DIR_NAME}\", \
                        local_dir_use_symlinks=False, \
                        allow_patterns=[ \
                            \"*.md\", \
                            \"*.json\", \
                            \"*.model\", \
                            \"*.bin\" \
                            ] \
                    )"
fi
