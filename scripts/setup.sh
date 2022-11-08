cp -r config/qtile/ ~/.config/
sudo -H pip install psutil

# Setup Alacritty config
cp -r config/alacritty/ ~/.config/

# Setup picom config
cp -r config/picom/ ~/.config/

# Install rofi power menu
sudo cp themes/one-dark.rasi /usr/share/rofi/themes/
