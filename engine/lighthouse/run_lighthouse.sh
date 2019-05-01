# $1 url
# $2 output format
# $3 path to chrome executable
# $4 actual audits to run
CHROME_PATH=$3
lighthouse --output $2 \
    --emulated-form-factor=none \
    --output-path stdout \
    --onlyAudits $4
    --quiet \
    --chrome-flags="--headless --no-first-run" \
    $1
