#!/bin/python3
#  ____     ____
# / ___|   |  _ \
# \___ \   | | | |
#  ___) |  | |_| |
# |____(_) |____(_)
#
# Qtile imports
import os, subprocess
from libqtile import bar, layout, hook, widget, qtile
from libqtile.config import Screen, Match
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.dgroups import simple_key_binder

from keys import keys, home, mod1, mod2, mod3, mod, groups, mouse
from themes import Dracula, Midnight, Monokai, Tomorrow, One_dark, Nordic, Catppuccin

from qtile_extras import widget
from qtile_extras.widget import WiFiIcon
from qtile_extras.widget.decorations import PowerLineDecoration

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([home])




theme = Dracula

accent_color=None




# Define the layout options
layout_defaults = {
    "border_width": 2,
    "border_focus": accent_color,
    "border_normal": theme["black"],
}
layout_mine = {
    "border_width": 1,
    "border_focus": theme["on"],
    "border_normal": theme["background"],
    "margin": 8,
}
layout_mine2 = {
    "border_width": 1,
    "border_focus": theme["on"],
    "border_normal": theme["background"],
}
layouts = [
    layout.MonadTall(**layout_mine, name="Tiled"),
        layout.Spiral(**layout_mine),
    layout.Bsp(
        **layout_mine,
        border_on_single=False,
        fair=True,
        grow_amount=10,
        lower_right=True,
        margin_on_single=None,
        ratio=1.6,
        wrap_clients=False
    ),
    layout.Max(name="  Fill "),
    layout.Floating(name="Float"),
    layout.Zoomy(**layout_mine, name="MStack"),
]

widget_defaults = dict(
    font="FiraCode Nerd Font Regular",
    fontsize=12,
    padding=6,
)
extension_defaults = widget_defaults.copy()

icon = lambda char, foreground, background, fontsize: widget.TextBox(
    font="Font Awesome 6 Free Solid",
    text=char,
    padding=1,
    margin=0,
    fontsize=fontsize,
    background=background,
    foreground=foreground,
    center_aligned=True,
)

# Works only with qtile-extras, add **powerline in all widgets

powerline = {
    "decorations": [
        PowerLineDecoration(path='forward_slash')
    ]
}


screens = [
    Screen(
        top=bar.Bar(

            [
                widget.Sep(
                    background=theme["foreground"],
                    foreground=theme["foreground"],
                    padding=1,
                ),
                # ------
                widget.TextBox(
                    font="Font Awsome 6 Nerd Font",
                    text=" ",
                    fontsize=20,
                    background=theme["foreground"],
                    foreground=theme["background"],
                    margin=10,
                    padding=2,
                    mouse_callbacks={
                        'Button1': lazy.spawn([home + '/bin/sidebar'])
                        },

                ),
                # ------
                widget.CurrentLayout(
                    use_mask=True,
                    font="Font Awesome 6 Free Solid",
                     # scale=0.7,
                    padding=5,
                    background=theme["foreground"],
                    foreground=theme["background"],
                    fontsize=11,
                    **powerline
                ),
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
                    borderwidth=1,
                    rounded=True,
                    padding_x=10,
                    padding_y=8,
                    margin_x=2,
                    disable_drag=True,
                    center_aligned=True,
                    hide_unused=True,
                    # visible_groups=['1', '2', '3'],
                    **powerline,
                    #margin=0
                ),
                # ------
                widget.WindowName(
                    format= '{name}',
                    font="FiraCode Nerd Font Regular",
                    fontsize=13,
                    background=theme["BG"],
                    foreground=theme["white"],
                    center_aligned=True,
                    max_chars=40,
                ),
                # ------
                widget.Systray(
                    fontsize=12,
                    background=theme["BG"],
                    center_aligned=True,
                    **powerline
                ),
                # ------
                icon("\uf021", foreground=theme["magenta"], background=theme["BG1"], fontsize=14,),
                widget.CheckUpdates(
                    distro="Arch",
                    font="JetBrainsMono NL Nerd Font",
                    fontsize=14,
                    dislpay_format = '{updates}',
                    no_update_string="Updates:0",
                    colour_no_updates=theme["white"],
                    colour_have_updates=theme["magenta"],
                    background=theme["BG1"],
                    foreground=theme["magenta"],
                    update_interval=10,
                    padding=5,
                    **powerline,
                    mouse_callbacks={
                        'Button1': lazy.spawn(f"alacritty -e sudo pacman -Syu")
                        },
                ),
                # -----
                widget.TextBox(
                    font="Font Awsome 6 Nerd Font",
                    text=" ",
                    fontsize=16,
                    foreground=theme["orange"],
                    background=theme["BG2"],
                    margin=3,
                    padding=2,
                    center_aligned=True,
                    mouse_callbacks={
                        'Button1': lazy.spawn("nitrogen --set-zoom-fill --random"),
                        'Button3': lazy.spawn([home + '/bin/ngen']),
                        },
                **powerline
                ),
                # ------
                widget.Net(
                    interface="wlan0",
                    format=" {down}",
                    background=theme["BG3"],
                    prefix="k",
                    foreground=theme["cyan"],
                    font="JetBrainsMono NL Nerd Font",
                    fontsize=14,
                    padding=5,  # Adjust the padding as needed
                    mouse_callbacks={'Button1': lazy.spawn(f"networkmanager_dmenu")},
                    **powerline
                ),

                # widget.WiFiIcon(
                #     interface="wlan0",
                #     active_colour=theme["cyan"],
                #     inactive_colour=theme["BG"],
                #     foreground=theme["cyan"],
                #     background = theme["BG3"],
                #     font="JetBrainsMono NL Nerd Font",
                #     fontsize=14,
                #     wifi_arc=100,
                #     expanded_timeout=None,
                #     update_interval=1,
                #     **powerline,
                #     mouse_callbacks={
                #         'Button1': lazy.spawn(f"networkmanager_dmenu")
                #         },
                #     ),
                # ------
                widget.BatteryIcon(
                    scale=1,
                    theme_path='/home/shridal/.local/share/icons/Panel/',
                    update_interval=3,
                    foreground=theme["green"],
                    background=theme["BG4"],
                    **powerline,
                    ),

                # ------
                icon("\uf017", foreground=theme["red"], background=theme["BG5"], fontsize=15,),
                widget.Clock(
                    font="JetBrainsMono NL Nerd Font",
                    format="%I:%M %p",
                    background=theme["BG5"],
                    foreground=theme["white"],
                    fontsize= 16,
                    center_aligned=True
                ),
            ],
            24,
            background=theme["background"],
            # margin=[8,8,0,8],
            # border_width=[5, 5, 0, 5],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
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
        Match(wm_class="kitty"),
        Match(wm_class="pinentry-gtk-2"),
        Match(wm_class="zoom"),
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
wmname = "Elysium/Q-tile"


