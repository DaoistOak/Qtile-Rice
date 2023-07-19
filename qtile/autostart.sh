#!/bin/sh
DIR="/usr/bin"
#xrandr --output Virtual1 --mode 1920x1080
setxkbmap latam &
nitrogen --restore &
"$DIR/eww" daemon &
pulsemixer --unmute &
paplay $HOME/.local/share/sounds/startup.ogg &
#nm-applet &
dunst -print&
flameshot &
/usr/lib/polkit-kde-authentication-agent-1 &
"$DIR/eww" open-many blur_full weather profile quote search_full disturb-icon vpn-icon home_dir screenshot power_full reboot_full lock_full logout_full suspend_full close_full &
mkdir /tmp/wm &
mkdir /tmp/wm/quotes &
bash ~/.config/eww/scripts/getweather &
bash ~/.config/eww/scripts/getwethquote &
bash ~/.config/eww/scripts/getwethquote2 &
bash ~/.config/eww/scripts/weather-trimmer &
bash ~/.config/eww/scripts/quote &
bash ~/.config/eww/scripts/quote-trimmer &
ksuperkey -d &
sleep 3
picom --experimental-backends &
redshift -l 27.700001:85.333336 &
xfce4-power-manager --daemon &
# volumeicon &

