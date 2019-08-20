#!/usr/bin/env python
#
# A script to query the US national weather service daily climate summary to find the daily rainfall.
# Written by Matthew Beckler - matthew.beckler at gmail dot com
# Released into the public domain
#
# See the entire reponse with this CURL command (change the date to something more recent)
# curl -v -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "product=CLI&station=MSP&recent=no&date=20190819" -e "https://w2.weather.gov/climate/index.php?wfo=mpx"  'https://w2.weather.gov/climate/getclimate.php?wfo=mpx'
#
# Usage:
# dailyRainfall.py [reportDate]
# - reportDate : A date string like YYYYMMDD of the report to query. As far as we've seen, reports contain information for the previous day, it's kind of weird. The script does parse out the date the data belongs to. By default it queries for today's report, which should contain data about yesterday.
#
# Output:
# reportDate,rainfall_in
# - reportDate : A date string like YYYYMMDD of the report's contents
# - rainfall_in : The number of inches of rainfall for that day. Sometimes they report a letter code instead, such as T = "trace rainfall" or MM = "missing data".
#
# Notes:
# * Please change the `station` variable below to your nearest NWS station ID code.
# * Please don't run this in a rapid-fire loop. Please add at least a few seconds delay between subsequent requests. Don't ruin this for everyone!

# Be sure to change the station to your nearest NWS station
# Go here: https://w2.weather.gov/climate/index.php
# Then click on your nearest set of readings to get that NWS office's page
# For example: https://w2.weather.gov/climate/index.php?wfo=mpx for the Twin Cities, MN office
# Then click on the Location you desire (typically airports and major cities) and click Go
# In the window that opens, look for the third line of the actual report, it'll be something like "CLI***" where the *** is your station code needed for this variable:
station = 'MSP'

import sys
import urllib2
import urllib
import re
import datetime
import time


try:
    url = 'https://w2.weather.gov/climate/getclimate.php?wfo=mpx'

    data = {}
    data['product'] = 'CLI'
    data['station'] = station
    data['recent'] = 'no'
    data['date'] = datetime.date.today().strftime("%Y%m%d") # request today's report which should contain yesterday's data
    if (len(sys.argv) == 2):
        data['date'] = sys.argv[1]
    values = urllib.urlencode(data)

    headers = {"Content-Type": "application/x-www-form-urlencoded",
               "Referer": "https://w2.weather.gov/climate/index.php?wfo=mpx",}

    req = urllib2.Request(url, values, headers)
    resp = urllib2.urlopen(req)
    the_page = resp.read()
    time.sleep(1)

    # Update 2019-08-20 - I think that we can request yesterday's climate report (maybe at noon CT each day?) that it should always have the YESTERDAY line (which actually means today, because the report was prepared the next day)
    # So we request the 0819 date in the request, and the response header says
    # CLIMATE REPORT
    # NATIONAL WEATHER SERVICE CHANHASSEN MN
    # 208 AM CDT MON AUG 19 2019
    # And then later on says
    # ...THE TWIN CITIES MN CLIMATE SUMMARY FOR AUGUST 18 2019...
    # And then the actual contents we care about:
    # PRECIPITATION (IN)
    #  YESTERDAY        1.74          2.26 1907   0.14   1.60     0.00

    # TODO Figure out if they release reports every day, or if the weekend reports show up on Monday morning?

    res = re.search(r'...THE TWIN CITIES MN CLIMATE SUMMARY FOR ([^\.]*)...', the_page)
    if res:
        dt = datetime.datetime.strptime(res.group(1), "%B %d %Y")
        actualDate = dt.strftime("%Y%m%d")
    else:
        raise Exception("Unable to parse climate summary line to find actual date!")

    res = re.search(r'^PRECIPITATION \(IN\)\s*YESTERDAY\s*([^\s]*)\s*', the_page, re.MULTILINE)
    precip_yesterday_in = "?"
    if res:
        precip_yesterday_in = res.group(1)
    print "%s,%s" % (actualDate, precip_yesterday_in)

    if False:
        # during the first half of the day it reports YESTERDAY's precipitation
        res = re.search(r'^PRECIPITATION \(IN\)\s*YESTERDAY\s*([0-9]*\.[0-9]*)\s*', the_page, re.MULTILINE)
        if res:
            precip_yesterday_in = res.group(1)
            print "yesterday's precip:", precip_yesterday_in
        # sometimes it reports TODAY's precipitation
        res = re.search(r'^PRECIPITATION \(IN\)\s*TODAY\s*([0-9]*\.[0-9]*)\s*', the_page, re.MULTILINE)
        if res:
            precip_today_in = res.group(1)
            print "today's precip:", precip_today_in
except Exception as e:
    print "exception", e
    sys.exit(1)

