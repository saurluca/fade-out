# Fade Out 🌅

A minimalist break timer for Hyprland/Wayland that gently reminds you to take breaks by fading your screen to grey.

## Features

- ⏱️ Configurable break intervals
- 🌑 Smooth fade-out effect using GTK overlays
- 🎯 Minimalist design - no bloat
- 🔔 Graceful fallback to notifications
- ⌨️ Easy dismissal (ESC key or click)

## Requirements

- Python 3.7+
- Hyprland or Wayland compositor
- GTK+ 3.0 (for overlay effect)

### On Manjaro/Arch-based systems:

```bash
sudo pacman -S python python-gobject gtk3
```

### On other systems:

```bash
# Debian/Ubuntu
sudo apt install python3 python3-gi gir1.2-gtk-3.0

# Fedora
sudo dnf install python3 python3-gobject gtk3
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/saurluca/fade-out.git
cd fade-out
```

2. Install Python dependencies (optional, if system packages aren't sufficient):
```bash
pip install -r requirements.txt
```

3. Make the script executable:
```bash
chmod +x fade_out.py
```

## Usage

### Basic usage (30-minute breaks):
```bash
./fade_out.py
```

### Custom break interval (20 minutes):
```bash
./fade_out.py -i 20
```

### Custom fade duration (10 seconds):
```bash
./fade_out.py -i 30 -d 10
```

### View all options:
```bash
./fade_out.py --help
```

## Options

- `-i, --interval MINUTES`: Set break interval in minutes (default: 30)
- `-d, --duration SECONDS`: Set fade duration in seconds (default: 5)
- `--version`: Show version information

## Running at Startup

To automatically start Fade Out when you log in to Hyprland:

1. Add to your Hyprland config (`~/.config/hypr/hyprland.conf`):
```bash
exec-once = /path/to/fade-out/fade_out.py -i 30
```

2. Or create a systemd user service (`~/.config/systemd/user/fade-out.service`):
```ini
[Unit]
Description=Fade Out Break Timer
After=graphical-session.target

[Service]
Type=simple
ExecStart=/path/to/fade-out/fade_out.py -i 30
Restart=on-failure

[Install]
WantedBy=default.target
```

Then enable it:
```bash
systemctl --user enable --now fade-out.service
```

## How It Works

1. The timer counts down your specified interval
2. When time's up, a grey overlay gradually fades in over your screen
3. A message appears: "Time for a break!"
4. Press ESC or click anywhere to dismiss and restart the timer
5. If GTK is unavailable, it falls back to desktop notifications

## Philosophy

Fade Out embraces minimalism:
- Simple Python codebase
- No complex dependencies
- Clean, focused functionality
- Respects your workflow

Take breaks. Your eyes (and brain) will thank you! 👀✨

## License

MIT License - Feel free to use and modify!