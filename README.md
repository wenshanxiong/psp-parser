# PSP Parser
A parser for Ameren Power Smart Pricing

## How to use
### Prerequisite
Create virtual environment
```
python3 -m venv venv
```
Activate virtual env
```
source venv/bin/activate
```
Install libraries
```
pip install -r requirements.txt
```
### PSP Parser
```
python3 psp_parser.py

Options:
-t, --tomorrow      fetch tomorrow's prices (avalible after 5:30PM CT)
```
### PSP API
```
python3 psp_api.py

Options:
-p, --port      Port to expose the API on. Defaul=6969
-d, --debug     Run API in debug mode. If true, changes will be loaded in real time. Default=false
```