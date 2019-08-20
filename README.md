# dailyRainfall
A script to query NWS climate summary data to find how much it rained yesterday

Written by Matthew Beckler - matthew.beckler at gmail dot com

Released into the public domain

# Usage
`python dailyRainfall.py [reportDate]`
* reportDate : A date string like YYYYMMDD of the report to query. As far as we've seen, reports contain information for the previous day, it's kind of weird. The script does parse out the date the data belongs to. By default it queries for today's report, which should contain data about yesterday.

# Output
`reportDate,rainfall_in`
* reportDate : A date string like YYYYMMDD of the report's contents
* rainfall_in : The number of inches of rainfall for that day. Sometimes they report a letter code instead, such as T = "trace rainfall" or MM = "missing data".

# Notes
* Please change the `station` variable near the top of the script to match your nearest NWS station ID code.
* Please don't run this in a rapid-fire loop. Please add at least a few seconds delay between subsequent requests. Don't ruin this for everyone!
