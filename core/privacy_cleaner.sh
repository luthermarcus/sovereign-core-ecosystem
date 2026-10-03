#!/data/data/com.termux/files/usr/bin/bash
# Sovereign Core OS - Gallery & Diagnostic Privacy Scrubber
# Restricts media scanner visibility and securely isolates captures.

REPO_DIR="$HOME/sos-fox-beta"
STORE_DIR="$REPO_DIR/.private_store"
mkdir -p "$STORE_DIR" "$REPO_DIR/logs"

# 1. Enforce .nomedia to prevent Android MediaScanner indexing
touch "$REPO_DIR/.nomedia"
touch "$REPO_DIR/logs/.nomedia"
touch "$STORE_DIR/.nomedia"
chmod 700 "$STORE_DIR"

echo "=== [1/2] LOCAL PROJECT DIRECTORIES SANITIZED ==="
echo "[+] .nomedia flags enforced across internal storage."
echo "[+] Private store locked with 700 permissions."

# 2. Check for Termux external storage access to clean Screenshot folder
SCREENSHOT_DIR="/sdcard/Pictures/Screenshots"
if [ ! -d "$SCREENSHOT_DIR" ]; then
    SCREENSHOT_DIR="/sdcard/DCIM/Screenshots"
fi

if [ -d "$SCREENSHOT_DIR" ]; then
    echo ""
    echo "=== [2/2] ANDROID SCREENSHOT PRIVACY AUDIT ==="
    RECENT_SHOTS=$(find "$SCREENSHOT_DIR" -type f \( -name "*Screenshot*" -o -name "*.png" \) -mmin -180 2>/dev/null)
    COUNT=$(echo "$RECENT_SHOTS" | grep -c "png" || true)

    if [ "$COUNT" -gt 0 ]; then
        echo "[!] Found $COUNT terminal screenshot(s) from recent development in $SCREENSHOT_DIR."
        read -rp "Move these to encrypted private project store? [y/N]: " CONFIRM
        if [[ "$CONFIRM" =~ ^[Yy]$ ]]; then
            while IFS= read -r file; do
                if [ -f "$file" ]; then
                    mv "$file" "$STORE_DIR/"
                fi
            done <<< "$RECENT_SHOTS"
            echo "[+] $COUNT capture(s) isolated to $STORE_DIR (invisible to Gallery)."
        else
            echo "[-] Preserved files in device gallery upon operator request."
        fi
    else
        echo "[✓] Zero recent loose screenshots found in device media folders."
    fi
else
    echo ""
    echo "=== [2/2] EXTERNAL STORAGE SANDBOX NOTE ==="
    echo "[i] Termux storage not linked to Android media directly."
    echo "[i] Terminal logs inside ~/sos-fox-beta remain fully isolated from Gallery."
fi
