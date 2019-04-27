# $1 url
# $2 output format
# $3 path to chrome executable
CHROME_PATH=$3
lighthouse --output $2 \
    --output-path stdout \
    --quiet \
    --chrome-flags="--headless --no-first-run" \
    $1
