#!/bin/bash
: ${ENV_PATH:="./venv"}
: ${PYTHON_CMD:="python3"}

source $ENV_PATH/bin/activate
${PYTHON_CMD} console_demo.py
