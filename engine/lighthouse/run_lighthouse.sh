# $1 url
# $2 output format
# $3 path to chrome executable
CHROME_PATH=$3
lighthouse --output $2 \
    --emulated-form-factor=none \
    --output-path stdout \
    --config-path /home/mhmurtada/new/awe/engine/lighthouse/lighthouse_config.js \
    --quiet \
    --chrome-flags="--headless --no-first-run" \
    $1
