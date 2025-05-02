#!/bin/bash

# Debian and Ubuntu
set -e

DRIVER_DIR="$HOME/drivers"
CHROME_DEB="google-chrome-stable_current_amd64.deb"

echo "Downloading and installing Google Chrome..."
wget -q https://dl.google.com/linux/direct/$CHROME_DEB
sudo apt install -y ./google-chrome-stable_current_amd64.deb
rm -f $CHROME_DEB

CHROME_VERSION=$(google-chrome --version | awk '{print $3}')
echo "Chrome version $CHROME_VERSION installed."
echo

echo "Downloading ChromeDriver for version $CHROME_VERSION..."
mkdir -p "$DRIVER_DIR"
cd "$DRIVER_DIR"

ZIP_NAME="chromedriver-linux64.zip"
CHROMEDRIVER_URL="https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROME_VERSION}/linux64/chromedriver-linux64.zip"

wget -q "$CHROMEDRIVER_URL" -O "$ZIP_NAME"
unzip -o "$ZIP_NAME"
chmod +x chromedriver-linux64/chromedriver
echo

echo "Installing ChromeDriver in '/usr/local/bin'..."
sudo mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver
rm -rf "$DRIVER_DIR/$ZIP_NAME" chromedriver-linux64
echo

echo "Installed:"
echo "- $(google-chrome --version)"
echo "- $(chromedriver --version)"
echo

echo "Installation completed successfully!"
