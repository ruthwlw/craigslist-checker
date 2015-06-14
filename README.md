Craiglist Checker
=================

forked from https://github.com/gjreda/craigslist-checker

Send an email when there are new sales by owner in SF post for a furniture brand like "west elm" "design within reach".

The script sends an email to a given email address using GMail's SMTP protocol, so you'll need to add your GMail username and password to the config file.

Setup
-----
Install the required libraries via pip:

    pip install -r requirements.txt

Usage
-----
    python craigslist-checker.py <search-term> <email>

It's useful to setup a cronjob that will run the script every N minutes.