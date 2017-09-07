"""
Author: Frank Fichtenmueller
Date Started: 24/8/2017
Purpose: Framework to extract Entities from unstructured and structured Data Sources
"""

# Import necessary external Dependencies
import re

string='Oct 12th 2012    12th December 2015  24 Nov 84  Dec 12, 2010  5th March 1983  Feb 2nd 2008  10-20-22'
string = 'Monday Tuesday Wednesday thursday Sunday'

# char_dates = re.findall(r'(?:\d{1,2}[\w]*,? )?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* (?:\d{1,2}[\w]*,? )?\d{2,4}', string)
weekdays = re.findall(r'(\w+day\b)', string)

print(weekdays)