#!/bin/bash

echo "🔍 Raspberry Pi Camera Diagnostics"
echo "==================================="

# 1. OS and Kernel Info
echo -e "\n📦 OS Version:"
cat /etc/os-release | grep PRETTY_NAME

echo -e "\n🧠 Kernel Version:"
uname -a

# 2. Camera Detection
echo -e "\n📸 Camera Detection (vcgencmd get_camera):"
vcgencmd get_camera

# 3. Camera Module Detected (I2C check)
echo -e "\n🔌 Detected I2C Camera Modules (should show 0x36 for Cam Module 2 or similar):"
i2cdetect -y 10 2>/dev/null || echo "⚠️  i2cdetect not available or camera not detected on i2c-10"

# 4. Firmware Info
echo -e "\n🧬 Firmware Version:"
vcgencmd version

# 5. Stack Type Check
echo -e "\n🗃 Camera Stack in Use:"
if [ -f /boot/config.txt ] && grep -q "^camera_auto_detect=1" /boot/config.txt; then
    echo "📷 libcamera stack (likely Bookworm)"
elif grep -q "^start_x=1" /boot/config.txt; then
    echo "📷 Legacy stack (likely Bullseye or earlier)"
else
    echo "📷 Stack unclear – check /boot/config.txt manually"
fi

echo -e "\n✅ Done. Review the output above."

