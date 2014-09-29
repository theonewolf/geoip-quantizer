#!/usr/bin/env python
#
#
#
# geoip-quantizer.py - This program computes statistics on IPs mapped to
#                      geolocation from presumably log files of some sort.
#
#
#
#       Copyright 2014 (c) Wolfgang Richter <wolf@cs.cmu.edu>
#
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.



import fileinput
import GeoIP

from operator import itemgetter

def setup_geo():
    return GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)

def parse_unique_ips():
    ips = set()
    for line in fileinput.input():
        ip = line.split()[0]
        ips.add(ip)
    return ips

def count_countries(ips, geo):
    country_counter = {}

    for ip in ips:
        country = geo.country_code_by_addr(ip)
        country_code = geo.country_name_by_addr(ip)
        ctuple = (country, country_code)
        count = country_counter.get(ctuple, 0) + 1
        country_counter[ctuple] = count

    return sorted(country_counter.items(), key=itemgetter(1), reverse=True)

def print_results(sorted_countries):
    for ctuple,count in sorted_countries:
        if ctuple[0] != None:
            print ctuple,
            print count

def print_total(sorted_countries):
    counts = [c[1] for c in sorted_countries if c[0][0] != None]

    print 'Total IPs from Known Geolocations: ',
    print str(sum(counts))

if __name__ == '__main__':
    print 'Apache Log GeoIP Quantizer'
    print 'Author: Wolfgang Richter <wolf@cs.cmu.edu>'

    geo = setup_geo()
    ips = parse_unique_ips()
    countries = count_countries(ips, geo)

    print_total(countries)
    print_results(countries)
