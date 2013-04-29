#!/usr/bin/env python
import json
import tornado.httpclient
import tornado.httputil
import sys
import os
import urllib

api_host = ""
api_password = ""
campaigns = []
http_client = tornado.httpclient.HTTPClient()
limit = 100

filename = "HillHolidayMTAGS.csv"
header = "Name,Appid,Conversion,Date,Direct Conversions,WOM Conversions"
start = "20120404"
end = "20120731"

def format(data, campaign, conversion):
    row = "%s,%s,%s-%s-%s,%s,%s" % (
        campaign,
        conversion,
        data['date']['year'],
        data['date']['month'],
        data['date']['day'],
        data['stats']['direct_conversions'],
        data['stats']['wom_conversions'])
    return row

def general_pull(campaign):
    url = "%s/campaign/%s/media_tags/overall/sorted/direct/dates/%s/%s?limit=2000" % (
        api_host,
        campaign,
        start,
        end)
    try:
        res = http_client.fetch(url, auth_username=campaign, auth_password=api_password)
    except tornado.httpclient.HTTPError:
        print >> sys.stderr, ("FAILED to pull conversion names for %s" % campaign)
        return ""
    else:
        data = json.loads(res.body)
        return format(data['data'], campaign)

def conversions_by_date(campaign, conversion):
    names = []
    url = "%s/campaign/%s/conversions/named/by_conversion_date/%s/dates/%s/%s?reduce=true" % (
        api_host,
        campaign,
        conversion,
        start,
        end)
    try:
        res = http_client.fetch(url, auth_username=campaign, auth_password=api_password)
    except tornado.httpclient.HTTPError:
        print >> sys.stderr, ("FAILED to pull conversion names for %s" % campaign)
        return ""
    else:
        data = json.loads(res.body)
        return format(data['data'], campaign, conversion)

def conversion_names(campaign):
    names = []
    url = "%s/campaign/%s/conversions/named/by_conversion_date/sorted/total/all?limit=%s" % (
        api_host,
        campaign,
        limit)
    try:
        res = http_client.fetch(url, auth_username=campaign, auth_password=api_password)
    except tornado.httpclient.HTTPError:
        print >> sys.stderr, ("FAILED to pull conversion names for %s" % campaign)
        print >> sys.stderr, url
    else:
        res = json.loads(res.body)
        for r in res['data']['rows']:
            name = r.keys()[0]
            names.append(urllib.quote(name))
    return names

if __name__ == '__main__':
    try:
        with open(filename, "w") as the_file:
            the_file.write(header)
            for c in campaigns:
                print >> sys.stderr, c[0]
                names = conversion_names(c[1])
                for n in names:
                    the_file.write("%s," % c[0])
                    res = conversions_by_date(c[1], n)
                    the_file.write(res)
                    the_file.write('\n')
    except IOError as e:
        print >> sys.stderr, "File error (main): " + str(e)

