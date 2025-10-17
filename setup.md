# Hector Setup Guide (Raspberry Pi)

## Clone the Repo

```bash
git clone https://github.com/PlaybookNexus/Hector.git
cd Hector

## Create and Activate Virtual Environment

```bash
sudo apt install python3-venv python3-full
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py