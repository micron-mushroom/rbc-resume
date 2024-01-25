#!/usr/bin/bash
# I would prefer to stay away from node_modules bloat for a single webpage.
ROOT_DIR=$(dirname "${BASH_SOURCE[0]}")
TARGET=${ROOT_DIR}/target
SRC=${ROOT_DIR}/src

if [[ -d "${TARGET}" ]]; then
    rm -r ${TARGET}
fi

mkdir ${TARGET}

# source ${ROOT_DIR}/ml/.converter/bin/activate
# mkdir ${TARGET}/model
# tensorflowjs_converter --input_format keras ${ROOT_DIR}/ml/weights.h5 ${TARGET}/model

# cd ${TARGET}/model
# I couldn't get firefox to decompress by setting Content-Type header through <media-type>
# 7z a -t7z weights.7z group1-shard1of1.bin
# gzip -k group1-shard1of1.bin

# base64 --wrap=0 group1-shard1of1.bin > weights.b64
# base64 --wrap=0 model.json > model.b64

# cd ../..

pandoc --standalone --template ${SRC}/index.html ${SRC}/resume.md -o ${TARGET}/index.html
# python template.py ${TARGET}/index.html
