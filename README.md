# PSP Parser
PSP Parser is a Python-based tool designed to parse Ameren Power Smart Pricing data and provide hourly electricity price information. The parsed data is stored in an SQLite database and served via a RESTful API, enabling integration with smart IoT applications and services.

## Installation
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

## Usage
### PSP Parser
```
python3 psp_parser.py

Options:
-t, --tomorrow      fetch tomorrow's prices (Usually avalible after 5:30PM CT)
```
### PSP API
```
python3 psp_api.py

Options:
-p, --port      Port to expose the API on. Defaul=6969
-d, --debug     Run API in debug mode. If true, changes will be loaded in real time. Default=false
```
Fetch the price for a date with
```
[host]:[port]/psp?date=[yyyy-mm-dd]
```
Fetch the price for a date range with
```
[host]:[port]/psp?start=[yyyy-mm-dd]&end=[yyyy-mm-dd]
```

## Contributing
Contributions are welcome! If you find issues or have suggestions for improvements, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
