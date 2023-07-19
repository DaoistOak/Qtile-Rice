#!/bin/python3
#  ____     ____
# / ___|   |  _ \
# \___ \   | | | |
#  ___) |  | |_| |
# |____(_) |____(_)
#
# Imports
import os, subprocess
from libqtile import hook, layout, qtile
from libqtile.config import Key, KeyChord, Group, Match, Click, Drag, Screen
from libqtile.lazy import lazy


# Modifier keys
mod = "mod4"
mod1 = "mod1"
mod2 = "mod2"
mod3 = "mod3"


# Applications
my_terminal = "alacritty"
my_browser = "firefox"
my_musicplayer = "rhythmbox"
my_editor = "kate"
my_video = "mpv", "zoom"
my_filemanager = "dolphin"
my_messaging = "discord"

if qtile.core.name == "x11":
    term = "urxvt"
elif qtile.core.name == "wayland":
    term = "foot"


home = os.path.expanduser('~')

# Define the group names and their associated attributes
groups = [
    Group('1', label='\uf120', layout='Tiled',
          matches=[Match(wm_class=my_terminal)]),
    Group('2', label='\ue007', layout='  Fill ',
          matches=[Match(wm_class=my_browser)]),
    Group('3', label='\uf121', layout='Tiled',
          matches=[Match(wm_class=my_editor)]),
    Group('4', label='\uf115', layout='Tiled',
          matches=[Match(wm_class=my_filemanager)]),
    Group('5', label='\uf001', layout='Tiled',
          matches=[Match(wm_class=my_musicplayer)]),
    Group('6', label='\uf167', layout='Tiled',
          matches=[Match(wm_class=my_video)]),
    Group('7', label='\uf086', layout='Tiled',
          matches=[Match(wm_class=my_messaging)]),
    Group('8', label='\uf1d3', layout='Tiled'
          ),
]




keys = [
      # Window navigation
      Key([mod],                 "left",                      lazy.layout.left(), desc="Move focus to left"),
      Key([mod],                 "right",                     lazy.layout.right(), desc="Move focus to right"),
      Key([mod],                 "down",                      lazy.layout.down(), desc="Move focus down"),
      Key([mod],                 "up",                        lazy.layout.up(), desc="Move focus up"),

      # Window shuffling
      Key([mod,   "shift"],      "left",                      lazy.layout.shuffle_left(), desc="Move window to the left"),
      Key([mod,   "shift"],      "right",                     lazy.layout.shuffle_right(), desc="Move window to the right"),
      Key([mod,   "shift"],      "down",                      lazy.layout.shuffle_down(), desc="Move window down"),
      Key([mod,   "shift"],      "up",                        lazy.layout.shuffle_up(), desc="Move window up"),

      # Window resizing
      Key([mod, "control"],      "f",                         lazy.window.toggle_floating(), desc='toggle floating'),
      Key([mod, "control"],      "left",                      lazy.layout.grow_left(), desc="Grow window to the left"),
      Key([mod, "control"],      "right",                     lazy.layout.grow_right(), desc="Grow window to the right"),
      Key([mod, "control"],      "down",                      lazy.layout.grow_down(), desc="Grow window down"),
      Key([mod, "control"],      "up",                        lazy.layout.grow_up(), desc="Grow window up"),
      Key([mod, "control"],      "n",                         lazy.layout.normalize(), desc="Reset all window sizes"),

      # Window layout control
      Key([mod],                 "Tab",                       lazy.next_layout(), desc="Toggle between layouts"),

      # Application launchers
      Key([mod],                 "Return",                    lazy.spawn(my_terminal), desc="Launch terminal"),
      Key([mod,   "shift"],      "Return",                    lazy.spawn("kitty --start-as=fullscreen")),
      Key([mod],                 "w",                         lazy.spawn(my_browser), desc="Launch browser"),
      Key([mod,   "shift"],      "w",                         lazy.spawn('firefox --private-window'), desc="Launch private browser"),
      Key([mod],                 "e",                         lazy.spawn(my_editor), desc="Launch editor"),
      Key([mod],                 "f",                         lazy.spawn(my_filemanager), desc="Launch file manager"),
      Key([mod],                 "q",                         lazy.spawn('emacs'), desc="Launch emacs"),

      # Miscellaneous
      Key([mod],                 "c",                         lazy.window.kill(), desc="Kill focused window"),
      Key([mod, "control"],      "r",                         lazy.spawn(f"killall picom"),
                                                              lazy.reload_config(),
                                                              lazy.spawn([home + '/.config/qtile/script/picom']),desc="Reload the config"),

      # Audio controls
      Key([],                    "XF86AudioLowerVolume",      lazy.spawn("/home/shridal/bin/Volume down")),
      Key([],                    "XF86AudioRaiseVolume",      lazy.spawn("/home/shridal/bin/Volume up")),
      Key([],                    "XF86AudioMute",             lazy.spawn("/home/shridal/bin/Volume mute")),
      Key([],                    "XF86MonBrightnessUp",       lazy.spawn("/home/shridal/bin/Brightness up")),
      Key([],                    "XF86MonBrightnessDown",     lazy.spawn("/home/shridal/bin/Brightness down")),
      Key([],                    "XF86AudioNext",             lazy.spawn("playerctl next")),
      Key([],                    "XF86AudioPrev",             lazy.spawn("playerctl previous")),
      Key([],                    "XF86AudioPlay",             lazy.spawn("playerctl play-pause")),

      # Rofi
      Key([mod],                 "p",                         lazy.spawn([home + '/bin/player'])),
      Key([mod],                 "n",                         lazy.spawn("networkmanager_dmenu")),
      Key([mod],                 "m",                         lazy.spawn(my_musicplayer)),
      Key([mod],                 "b",                         lazy.spawn([home + '/.config/rofi/script/bluetooth'])),
      Key([mod],                 "t",                         lazy.spawn([home + '/.config/rofi/script/themes'])),
      Key([mod1],                "F1",                        lazy.spawn([home + '/.config/rofi/script/launcher'])),
      Key([mod],                 "r",                         lazy.spawn([home + '/bin/d-launcher'])),
      Key([mod],                 "s",                         lazy.spawn([home + '/bin/sidebar'])),
      Key([mod],                 "d",                         lazy.spawn([home + '/bin/dashboard'])),

      # Screenshot
      Key([],                    "print",                     lazy.spawn("flameshot gui")),

      # Window switching
      Key([mod1],                "Tab",                       lazy.spawn([home + '/.config/rofi/script/windows'])),

      # Screen Lock
      Key([mod],                 "l",                         lazy.spawn("betterlockscreen --lock dim")),
]

def open_jgmenu():
    lazy.spawn([home + '/.config/'])

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]


for group in groups:
    keys.extend([
        Key([mod], group.name,
            lazy.group[group.name].toscreen(),
            desc=f"Switch to group {group.name}"),

        Key([mod, "shift"], group.name,
            lazy.window.togroup(group.name,switch_group=True),
            desc=f"Switch to & move focused window to group {group.name}"),
                ])




