#!/usr/bin/env python3
"""
Fade Out - A minimalist break timer for Hyprland/Wayland
Gradually fades the screen to grey when it's time for a break.
"""

import time
import argparse
import sys
import subprocess
from pathlib import Path


class FadeOutTimer:
    """Simple break timer with screen fade-out effect."""
    
    def __init__(self, break_interval=1800, fade_duration=5):
        """
        Initialize the timer.
        
        Args:
            break_interval: Time in seconds before break reminder (default: 30 minutes)
            fade_duration: Duration of fade effect in seconds (default: 5)
        """
        self.break_interval = break_interval
        self.fade_duration = fade_duration
        self.config_dir = Path.home() / '.config' / 'fade-out'
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
    def show_overlay(self, opacity):
        """Create a grey overlay using Hyprland layer shell."""
        # Use hyprctl to create a simple notification-like overlay
        # For a proper overlay, we'll use a simple GTK window
        try:
            import gi
            gi.require_version('Gtk', '3.0')
            gi.require_version('Gdk', '3.0')
            from gi.repository import Gtk, Gdk
            return self._show_gtk_overlay(opacity)
        except ImportError:
            # Fallback: use hyprctl notifications
            self._show_notification_overlay(opacity)
            return None
    
    def _show_gtk_overlay(self, opacity):
        """Show overlay using GTK (for Wayland/Hyprland)."""
        import gi
        gi.require_version('Gtk', '3.0')
        gi.require_version('Gdk', '3.0')
        from gi.repository import Gtk, Gdk
        
        window = Gtk.Window()
        window.set_decorated(False)
        window.set_app_paintable(True)
        window.fullscreen()
        
        # Make window draw on all workspaces
        window.set_keep_above(True)
        
        # Set background color (grey)
        screen = window.get_screen()
        visual = screen.get_rgba_visual()
        if visual:
            window.set_visual(visual)
        
        # Set opacity
        window.set_opacity(opacity)
        
        # Add a label to inform user
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        box.set_valign(Gtk.Align.CENTER)
        box.set_halign(Gtk.Align.CENTER)
        
        label = Gtk.Label()
        label.set_markup('<span size="xx-large" weight="bold">Time for a break!</span>')
        label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 1, 1, 1))
        
        dismiss_label = Gtk.Label()
        dismiss_label.set_markup('<span size="large">Press ESC or click to dismiss</span>')
        dismiss_label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.9, 0.9, 0.9, 1))
        
        box.pack_start(label, False, False, 0)
        box.pack_start(dismiss_label, False, False, 0)
        
        # Set grey background
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
            window {
                background-color: rgba(64, 64, 64, 1);
            }
        """)
        context = window.get_style_context()
        context.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        
        window.add(box)
        
        # Allow dismissal
        window.connect('key-press-event', lambda w, e: w.destroy() if e.keyval == Gdk.KEY_Escape else False)
        window.connect('button-press-event', lambda w, e: w.destroy())
        window.connect('destroy', Gtk.main_quit)
        
        window.show_all()
        return window
    
    def _show_notification_overlay(self, opacity):
        """Fallback: Show a notification using notify-send."""
        try:
            subprocess.run([
                'notify-send',
                '-u', 'critical',
                '-t', '10000',
                'Fade Out',
                'Time for a break! Take a moment to rest your eyes.'
            ], check=False)
        except FileNotFoundError:
            print("⏰ Time for a break! Take a moment to rest your eyes.")
    
    def fade_out(self):
        """Gradually fade the screen to grey."""
        try:
            import gi
            gi.require_version('Gtk', '3.0')
            from gi.repository import Gtk, GLib
            
            steps = 20
            step_duration = self.fade_duration / steps
            
            window = None
            for i in range(steps + 1):
                opacity = i / steps
                if window:
                    window.set_opacity(opacity)
                else:
                    window = self.show_overlay(opacity)
                    if window:
                        # Process events to show the window
                        while Gtk.events_pending():
                            Gtk.main_iteration()
                
                time.sleep(step_duration)
            
            # Keep overlay visible
            if window:
                Gtk.main()
                
        except ImportError:
            # Fallback without GTK
            print("⏰ Break time! (GTK not available for visual fade effect)")
            self._show_notification_overlay(1.0)
            time.sleep(10)
    
    def run(self):
        """Run the timer loop."""
        print(f"🎯 Fade Out timer started!")
        print(f"⏱️  Break reminder in {self.break_interval // 60} minutes")
        print(f"💡 Press Ctrl+C to stop\n")
        
        try:
            while True:
                # Wait for break interval
                time.sleep(self.break_interval)
                
                # Show fade out effect
                print(f"\n⏰ Break time!")
                self.fade_out()
                
                print(f"\n⏱️  Next break in {self.break_interval // 60} minutes")
                
        except KeyboardInterrupt:
            print("\n\n👋 Fade Out stopped. Take care of yourself!")
            sys.exit(0)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Fade Out - A minimalist break timer for Hyprland',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # 30-minute breaks (default)
  %(prog)s -i 20              # 20-minute breaks
  %(prog)s -i 60 -d 10        # 60-minute breaks with 10s fade
        """
    )
    
    parser.add_argument(
        '-i', '--interval',
        type=int,
        default=30,
        metavar='MINUTES',
        help='break interval in minutes (default: 30)'
    )
    
    parser.add_argument(
        '-d', '--duration',
        type=int,
        default=5,
        metavar='SECONDS',
        help='fade duration in seconds (default: 5)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Fade Out 1.0.0'
    )
    
    args = parser.parse_args()
    
    # Convert minutes to seconds
    break_interval = args.interval * 60
    
    # Validate inputs
    if args.interval < 1:
        print("❌ Error: Interval must be at least 1 minute", file=sys.stderr)
        sys.exit(1)
    
    if args.duration < 1:
        print("❌ Error: Duration must be at least 1 second", file=sys.stderr)
        sys.exit(1)
    
    # Create and run timer
    timer = FadeOutTimer(break_interval=break_interval, fade_duration=args.duration)
    timer.run()


if __name__ == '__main__':
    main()
