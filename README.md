# GroceryGrabber
 Notifies you when a grocery delivery slot is open on Amazon Prime Now

## Dependencies
- Python 3+
- Selenium
- Firefox
- geckodriver 

## Installation

NOTE - Only tested with 64-bit windows

1. Install Firefox if you have not already
- https://www.mozilla.org/en-US/firefox/new/
2. Install Selenium if you have not already
- pip install selenium
3. Download geckodriver and add it to your path
- https://github.com/mozilla/geckodriver/releases
- Open an admin terminal and enter "SETX /m PATH=%PATH%;PATH_TO_GECKODRIVER"
4. Set up your config file
- Create a copy of "config_template.json" and rename it to "config.json"
- Enter your email credentials (or an account you would like to use to send email notifications)
- For URL, it is the smtp url. For Gmail that is smtp.gmail.com
- Enter your phone number and carrier. Supported carriers are (case sensitive) TMOBILE and VERIZON
- For each cart, enter your login information and set True to enable it (or false to disable, then no credentials are needed)

## Quickstart

1. Fill your grocery carts in advance, and set the carts to Enabled: True in the config file
2. Run the script. It will open a new firefox window
3. You can modify your config file at any time and the script will read the updates periodically
4. To quit, click the "x" on the firefox window

## Usage

python grocerygrabber.py [-c, --config config.json] [-v, --verbose] [-h, --help]

-c/--config  : json configuration file. Defaults to config.json

-v/--verbose : prints detailed runtime information to the console

## Author
Michael Kukar

## License
MIT License

Copyright (c) 2020 Michael Kukar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
