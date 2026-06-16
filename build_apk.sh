#!/bin/bash
# Build APK script for Kivy Demo Collection
# Run this on a Linux machine with sudo access

set -e

echo "=== Kivy Demo APK Builder ==="

# Install dependencies
echo "[1/5] Installing system dependencies..."
sudo apt-get update -qq
sudo apt-get install -y build-essential zip unzip git \
    zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 \
    cmake libffi-dev libssl-dev pkg-config autoconf libtool \
    openjdk-17-jdk python3-pip python3-venv

# Setup JDK
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

echo "[2/5] Installing buildozer..."
pip3 install --break-system-packages buildozer cython

echo "[3/5] Initializing buildozer (first run downloads SDK/NDK ~2GB)..."
cd "$(dirname "$0")"
buildozer android debug 2>&1 | head -20
echo "..."
echo "[4/5] Building APK (this takes 10-30 minutes on first run)..."

# Build
buildozer android debug

echo "[5/5] Done!"
echo "APK location: $(ls -t bin/*.apk 2>/dev/null | head -1)"
echo "Install on phone: adb install bin/*.apk"
