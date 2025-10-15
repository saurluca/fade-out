#!/bin/bash
# Simple installation script for Fade Out

set -e

echo "🌅 Installing Fade Out..."

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not found"
    echo "   Install it with: sudo pacman -S python"
    exit 1
fi

# Make script executable
chmod +x fade_out.py

echo "✓ Script made executable"

# Check for GTK (optional)
if python3 -c "import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk" 2>/dev/null; then
    echo "✓ GTK bindings found - full overlay support available"
else
    echo "⚠ GTK bindings not found - will use notification fallback"
    echo "  Install with: sudo pacman -S python-gobject gtk3"
fi

# Offer to create systemd service
read -p "📦 Create systemd user service? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    SERVICE_DIR="$HOME/.config/systemd/user"
    SERVICE_FILE="$SERVICE_DIR/fade-out.service"
    
    mkdir -p "$SERVICE_DIR"
    
    cat > "$SERVICE_FILE" << EOF
[Unit]
Description=Fade Out Break Timer
After=graphical-session.target

[Service]
Type=simple
ExecStart=$(pwd)/fade_out.py -i 30
Restart=on-failure

[Install]
WantedBy=default.target
EOF
    
    echo "✓ Created service file: $SERVICE_FILE"
    echo "  Enable with: systemctl --user enable --now fade-out.service"
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "Quick start:"
echo "  ./fade_out.py              # Start with 30-minute breaks"
echo "  ./fade_out.py -i 20        # Start with 20-minute breaks"
echo "  ./fade_out.py --help       # See all options"
echo ""
echo "Take breaks. Your eyes will thank you! 👀✨"
