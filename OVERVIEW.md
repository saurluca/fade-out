# Fade Out - Application Overview

## What It Does

Fade Out is a minimalist break timer designed for Hyprland/Wayland users who want gentle reminders to take breaks.

## Usage Examples

### 1. Start with Default Settings (30 minutes)
```bash
$ ./fade_out.py
🎯 Fade Out timer started!
⏱️  Break reminder in 30 minutes
💡 Press Ctrl+C to stop
```

### 2. Custom Break Interval (20 minutes)
```bash
$ ./fade_out.py -i 20
🎯 Fade Out timer started!
⏱️  Break reminder in 20 minutes
💡 Press Ctrl+C to stop
```

### 3. When Break Time Arrives
After the timer completes:
- A grey overlay gradually fades onto your screen over 5 seconds (default)
- The message "Time for a break!" appears in the center
- You can dismiss it by pressing ESC or clicking anywhere
- The timer automatically restarts for the next break cycle

## Visual Effect

The fade-out creates a smooth grey overlay that:
1. Starts transparent (0% opacity)
2. Gradually increases to 100% over the fade duration
3. Covers the entire screen with a semi-transparent grey
4. Shows a centered message: "Time for a break!"
5. Instructs: "Press ESC or click to dismiss"

## Fallback Mode

If GTK is not available, the app gracefully falls back to:
- Desktop notifications using notify-send
- Console messages

## Key Features

✅ **Simple**: Single Python file, minimal dependencies
✅ **Flexible**: Configurable intervals and fade duration  
✅ **Respectful**: Easy to dismiss, doesn't lock your screen
✅ **Minimalist**: No GUI, no bloat, just the essentials
✅ **Smart**: Auto-detects GTK availability and falls back gracefully

## System Integration

### Manual Start
```bash
./fade_out.py -i 30
```

### Hyprland Auto-start
Add to `~/.config/hypr/hyprland.conf`:
```bash
exec-once = /path/to/fade-out/fade_out.py -i 30
```

### Systemd Service
```bash
systemctl --user enable --now fade-out.service
```

## Philosophy

Taking regular breaks is essential for:
- 👀 Eye health (reduces strain)
- 🧠 Mental clarity (improves focus)
- 💪 Physical health (prevents repetitive strain)

Fade Out helps you remember without being intrusive.
