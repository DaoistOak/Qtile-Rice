    #!/bin/python3

# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Non Qtile imports
from cgitb import text
import subprocess
import os
import functools

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
mod1= "mod1"
mod = "mod4"
terminal = "alacritty"
rofi_theme = "one-dark" #"tomorrow-dark-cyan"
launcher_theme = ".config/rofi/theme/launcher.rasi"
home = os.path.expanduser('~')

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "up", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "w", lazy.spawn('firefox'), desc="Launch firefox"),
    Key([mod, "shift"], "w", lazy.spawn('firefox --private-window'), desc="Launch firefox private"),
    Key([mod], "e", lazy.spawn('kate')),
    Key([mod], "f", lazy.spawn('thunar')),
    Key([mod], "q", lazy.spawn('emacs')),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "c", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

###
    # Rofi
    Key([mod],"space", lazy.spawn([home + '/.config/rofi/script/launcher'])),
    Key([mod], "x", lazy.spawn([home + '/.config/rofi/script/powermenu'])),
    Key([mod], "m", lazy.spawn([home + '/.config/rofi/script/mpd'])),
    Key([mod], "s", lazy.spawn([home + '/.config/rofi/script/screenshot'])),
    Key([mod], "n", lazy.spawn(f"networkmanager_dmenu")),
    Key([mod, "shift"], "r", lazy.spawn([home + '/.config/rofi/script/asroot'])),
    Key([mod], "l", lazy.spawn(f"betterlockscreen --lock")),
    # Audio key keybindings
    Key([], "XF86AudioLowerVolume", lazy.spawn("pulsemixer --change-volume -5")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pulsemixer --change-volume +5")),
    Key([], "XF86AudioMute", lazy.spawn("pulsemixer --toggle-mute")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl s 46.85+")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl s 46.85-")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl prev")),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    # key([], "print", lazy.spawn(f"flameshot gui")),
    Key([mod1], "Tab", lazy.spawn([home + '/.config/rofi/script/windows'])),
]
def init_group_names():
    """
    Returns a list of group names.
    """
    return [
        ('\uf120', {'layout': 'Tiled'}),
        ('\ue007', {'layout': 'Full'}),        # Firefox
        ('\uf121', {'layout': 'Tiled'}),        # Code
        ('', {'layout': 'Tiled'}),  # Thunar
        ('\uf001', {'layout': 'Tiled'}),        # StackOverflow
        ('\uf167', {'layout': 'Tiled'}),        # YouTube
        ('\uf086', {'layout': 'Tiled'}),        # Chat
        ('', {'layout': 'Full'})         # Music
    ]

def init_groups():
    """
    Returns a list of groups.
    """
    return [Group(name, **kwargs) for name, kwargs in group_names]

if __name__ in ['config', '__main__']:
    group_names = init_group_names()
    groups = init_groups()

    for i, (name, kwargs) in enumerate(group_names, 1):
        keys.append(Key([mod], str(i), lazy.group[name].toscreen()))         # Switch to another group
        keys.append(Key([mod, 'shift'], str(i), lazy.window.togroup(name)))  # Send current window to another group

# def create_icon():
#     """
#     Returns an icon to be used in text elements of Qtile.
#     """
#     textbox = widget.TextBox(**widget_defaults)
#     textbox.font = "Font Awesome 6 Free Solid"
#     return textbox

dark = {
    "background": "2e3440",
    "foreground": "f8f8f2",
    "black":      "5c6370",
    "red":        "e06c75",
    "green":      "98c379",
    "yellow":     "d19a66",
    "blue":       "61afef",
    "magenta":    "c678dd",
    "cyan":       "56b6c2",
    "white":      "828791",
    "back":       "2e3440",
    "fore":       "d8dee9",
    "select":     "81a1c1",
    "highlight":  "ebcb8b",
    "urgent":     "bf616a",
    "on":         "c679FF",
    "off":        "212B30",
    "BG":         "212B30",
    "BG1":        "263035",
    "BG2":        "2B353A",
    "BG3":        "303A3F",
    "BG4":        "353F44",
    "BG5":        "3A4449",
    "BG6":        "3F494E"
}

theme = dark
accent_color = theme["cyan"]

layout_defaults = {
    "border_width": 2,
    "border_focus": accent_color,
    "border_normal": theme["black"],
}
layout_mine = {
    "border_width": 1,
    "border_focus": theme["on"],
    "border_normal": theme["off"],
    "margin": 8,
}
layout_mine2 = {
    "border_width": 1,
    "border_focus": theme["on"],
    "border_normal": theme["off"],
}
layouts = [
    layout.MonadTall(**layout_mine, name = "Tiled"),
    layout.Max(name= "Full"),
    # Try more layouts by unleashing below layouts.
    #layout.Stack(num_stacks=2),
    #layout.Bsp(),
    #layout.Matrix(),
    #layout.Tile(),
    #layout.TreeTab(),
    #layout.VerticalTile(),
    layout.Floating( name = "Float"),
    layout.Zoomy(**layout_mine, name = "MStack")
]
widget_defaults = dict(
    font="Cantarell Bold",
    fontsize=12,#14
    padding=6,
)
extension_defaults = widget_defaults.copy()

left_arrow = lambda background, foreground: widget.TextBox(
    font="FiraCode Nerd Font Regular",
    text="\uf438",
    fontsize=60,
    background=background,
    foreground=foreground,
    padding=-8,
)

icon = lambda char, foreground, background: widget.TextBox(
    font="Font Awesome 6 Free Solid",
    text=char,
    background=background,
    foreground=foreground,
)

separator = lambda color: widget.Sep(
    background=color,
    foreground=color,
)

separator_background_color = functools.partial(separator, color=theme["background"])

def open_nmd(qtile):
    qtile.cmd_spawn('networkmanager_dmenu')

def open_htop(qtile):
    qtile.cmd_spawn('alacritty -e htop')

def open_pacman(qtile):
    qtile.cmd_spawn('alacritty -e sudo pacman -Syu')


screens = [
    Screen(
        top=bar.Bar(

            [
                # ------
                widget.CurrentLayout(
                    background=theme["fore"],
                    foreground=theme["back"],
                    fontsize=13
                ),
                # ------
                widget.TextBox(
                    text = '',
                    background = theme["BG1"],
                    foreground = theme["fore"],
                    padding = 0,
                    fontsize = 26,
                # center_aligned=True
                ),
                # -----
                separator(color=theme["BG1"]),
                # -----
                widget.GroupBox(
                    font="Font Awesome 6 Free Solid",
                    highlight_method="block",
                    fmt="{}",
                    this_current_screen_border=theme["on"],
                    #this_other_screen_border=theme["blue"],
                    #this_current_screen=theme["background"],
                    block_highlight_text_color=theme["background"],
                    inactive=theme["black"],
                    background=theme["BG1"],
                    borderwidth=0,
                    rounded=True,
                    padding_x=10,
                    padding_y=8,
                    margin_x=0
                    #margin=0
                ),
                # ------
                widget.TextBox(
                    text = '',
                    background = theme["BG"],
                    foreground = theme["BG1"],
                    padding = 0,
                    fontsize = 26,
                    center_aligned=True
                ),
                # ------
                widget.WindowName(
                    fmt='  {}',
                    font="JetBrainsMono NL Nerd Font",
                    fontsize=13,
                    background=theme["BG"],
                    center_aligned=True
                ),
                # ------
                widget.Systray(
                    fontsize=12,
                    background=theme["BG"],
                    center_aligned=True
                ),
                # ------
                widget.TextBox(
                    text = '',
                    background = theme["BG"],
                    foreground = theme["BG1"],
                    padding = 0,
                    fontsize = 26,
                    center_aligned=True
                ),
                # ------
                # icon("\uf1eb", background=theme["background"], foreground=theme["red"]),
                widget.Net(
                    interface="wlan0",
                    format=" {down} ↓/↑{up}",
                    prefix="k",
                    background = theme["BG1"],
                    foreground=theme["red"],
                    font="JetBrainsMono NL Nerd Font",
                    fontsize=14,
                    center_aligned=True,
                ),
                # ------
                widget.TextBox(
                    text = '',
                    background = theme["BG1"],
                    foreground = theme["BG2"],
                    padding = 0,
                    fontsize = 26,
                    center_aligned=True
                ),
                # ------
                icon("\uf021", foreground=theme["magenta"], background=theme["background"]),
                widget.CheckUpdates(
                    distro="Arch",
                    font="JetBrainsMono NL Nerd Font",
                    fontsize=14,
                    dislpay_format = '{updates}',
                    no_update_string="Up To Date",
                    colour_no_updates=theme["white"],
                    colour_have_updates=theme["red"],
                    background=theme["BG2"],
                    foreground=theme["magenta"],
                    center_aligned=True
                ),
                # ------
                widget.TextBox(
                    text = '',
                    background = theme["BG2"],
                    foreground = theme["BG3"],
                    padding = 0,
                    fontsize = 26,
                    center_aligned=True
                ),
                # ------
                widget.Volume(
                    foreground=theme["yellow"],
                    background = theme["BG3"],
                    font="JetBrainsMono NL Nerd Font",
                    fmt='墳 {}',
                    fontsize=14,
                    center_aligned=True,
                    update_interval = 0.2,
                ),
                # ------
                widget.TextBox(
                    text = '',
                    background = theme["BG3"],
                    foreground = theme["BG4"],
                    padding = 0,
                    fontsize = 26,
                    center_aligned=True
                ),
                # ------
                widget.Backlight(
                    backlight_name='intel_backlight',
                    brightnessfile='brightness',
                    max_brightness_file='max_brightness',
                    background = theme["BG4"],
                    foreground=theme["cyan"],
                    font="JetBrainsMono NL Nerd Font",
                    fmt=' {}',
                    fontsize=14,
                    center_aligned=True
                ),
                # ------
                widget.TextBox(
                    text = '',
                    background = theme["BG4"],
                    foreground = theme["BG5"],
                    padding = 0,
                    fontsize = 26,
                    center_aligned=True
                ),
                # ------
                widget.Battery(
                    update_interval=3,
                    format = '{char} {percent:2.0%}',
                    full_char = '',
                    unknown_char = '?',
                    empty_char = '',
                    charge_char = '',
                    discharge_char = '',
                    center_aligned = True,
                    foreground=theme["green"],
                    background=theme["BG5"],
                    font="JetBrainsMono NL Nerd Font",
                    fontsize= 14,
                ),
                # ------
                widget.TextBox(
                    text = '',
                    background = theme["BG5"],
                    foreground = theme["BG6"],
                    padding = 0,
                    fontsize = 26,
                    center_aligned=True
                ),
                # ------
                icon("\uf017", foreground=theme["red"], background=theme["BG6"]),
                widget.Clock(
                    font="JetBrainsMono NL Nerd Font",
                    format="%I:%M %p",
                    background=theme["BG6"],
                    foreground=theme["fore"],
                    fontsize= 15,
                    center_aligned=True
                ),
                # ------
            ],
            24,
            # background=theme["background"]
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]
# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(

    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]

)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
#wmname = "LG3D"
wmname = "Qtile"

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([home])

