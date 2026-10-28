#!/bin/sh
set -eu

if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
    echo "Usage: $0 /private/path/thesis.pdf [/var/lib/cycling-web/thesis-pages]" >&2
    exit 2
fi

SOURCE_PDF=$1
TARGET=${2:-/var/lib/cycling-web/thesis-pages}
TARGET_PARENT=$(dirname -- "$TARGET")
TARGET_NAME=$(basename -- "$TARGET")

test -r "$SOURCE_PDF"
command -v pdftoppm >/dev/null 2>&1 || {
    echo "Missing pdftoppm (package: poppler-utils)." >&2
    exit 1
}

install -d -o root -g cycling-web -m 0750 "$TARGET_PARENT"
STAGE=$(mktemp -d "$TARGET_PARENT/${TARGET_NAME}.new.XXXXXX")
cleanup() {
    if [ -d "$STAGE" ]; then
        find "$STAGE" -maxdepth 1 -type f -delete
        rmdir "$STAGE"
    fi
}
trap cleanup EXIT HUP INT TERM

pdftoppm -q -jpeg -jpegopt quality=84,progressive=y,optimize=y \
    -scale-to-x 1500 -scale-to-y -1 "$SOURCE_PDF" "$STAGE/page"
test -r "$STAGE/page-01.jpg"
chown root:cycling-web "$STAGE" "$STAGE"/page-*.jpg
chmod 0750 "$STAGE"
chmod 0640 "$STAGE"/page-*.jpg

if [ -e "$TARGET" ]; then
    BACKUP="${TARGET}.previous.$(date +%Y%m%d%H%M%S)"
    mv "$TARGET" "$BACKUP"
    echo "Previous reader assets: $BACKUP"
fi
mv "$STAGE" "$TARGET"
trap - EXIT HUP INT TERM

PAGES=$(find "$TARGET" -maxdepth 1 -type f -name 'page-*.jpg' | wc -l)
echo "Prepared $PAGES reader pages in $TARGET"
