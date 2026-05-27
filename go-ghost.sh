#!/bin/bash

# 1. Get the IP address automatically
IP_ADDR=$(hostname -I | awk '{print $1}')

# 2. Start the stealth assistant in the background (Ghost Mode)
nohup python3 tools/manual_stealth_assistant.py > /dev/null 2>&1 &

echo "=========================================="
echo "      RSNW STEALTH MODE ACTIVATED         "
echo "=========================================="
echo ""
echo "1. On your PHONE, open this link:"
echo "   http://$IP_ADDR:5000"
echo ""
echo "2. Press F9 on this laptop to get answers."
echo "3. Press F12 to EMERGENCY SHUTDOWN."
echo ""
echo "You can now close this terminal window."
echo "=========================================="
