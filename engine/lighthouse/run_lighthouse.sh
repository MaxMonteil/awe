export DISPLAY=:1.5
TMP_PROFILE_DIR=$(mktemp -d -t lighthouse.XXXXXXXXXX)

# start up chromium inside xvfb
xvfb-run --server-args='-screen 0, 1024x768x16' \
             sudo google-chrome \
                 --headless \
                 --no-sandbox \
                 --user-data-dir=$TMP_PROFILE_DIR \
                 --start-maximized \
                 --no-first-run \
                 --remote-debugging-port=9222 "about:blank" & lighthouse \
                 --output $OUTPUT_FORMAT \
                 --output-path stdout
                 --quiet
                 --port=9222 $URL
