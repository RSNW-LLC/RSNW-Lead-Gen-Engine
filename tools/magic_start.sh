#!/bin/bash
# Move to the project folder
cd ~/RSNW_LeadGen

# 1. Check if Ollama is running, if not, start it in the background
if ! pgrep -x "ollama" > /dev/null
 Noahup ollama serve > /dev/null 2>&1 &
 sleep 2
fi

# 2. Get the IP address
IP_ADDR=$(hostname -I | awk '{print $1}')

# 3. Start the Stealth Assistant in the background
source .venv/bin/activate
nohup python3 tools/manual_stealth_assistant.py > /dev/null 2>&1 &

echo "=========================================="
echo "      RSNW STEALTH SYSTEM ONLINE          "
echo "=========================================="
echo "1. Open on your PHONE: http://$IP_ADDR:5000"
echo "2. Press F9 to get answers."
echo "3. Press F12 to kill everything."
echo "=========================================="
# Exit the terminal automatically to leave no trace
exit
