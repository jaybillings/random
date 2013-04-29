#!/usr/bin/env python
# encoding: utf-8
"""
report_munger.py

Created by Jessica Billings on 2012-06-25.
Copyright (c) 2012 Meteors Solutions. All rights reserved.
"""

import getopt, sys, os, re

def format(data):
    filedata = ['Site,Direct,Social,Total,% Social']
    for key in data.keys():
        percwom = float(data[key][1]) / float(data[key][2]) * 100
        row = "%s,%s,%s,%s,%.1f" % (key,
                                    str(data[key][0]),
                                    str(data[key][1]),
                                    str(data[key][2]),
                                    percwom)
        if _debug:
            print >> sys.stderr, row
        filedata.append(row)
    return filedata

def site_strip(line):
    preg = re.compile(".*\/.*\/")
    ereg = re.compile("(.aspx|.asp)")
    line = preg.sub("", line)
    line = ereg.sub("", line)
    return line

def run(dirtyfile):
    seen = {}
    misciter = 0
    #cleandata.append('Page,Direct,Social,Total,% Social')
    try:
        with open(dirtyfile) as dfile:
            data = dfile.readlines()
        for line in data:
            # Clean data
            line = site_strip(line)
            linearr = line.split(",")
            for x in range(1,len(linearr)):
                linearr[x] = int(linearr[x])
            # Name missing sites
            if linearr[0] == '':
                linearr[0] = "misc%s" % (misciter + 1)
                misciter = misciter + 1
            if _debug:
                print >> sys.stderr, "*** %s ***" % linearr[0]
            # Put in dict
            if linearr[0] not in seen.keys():
                seen.update({linearr[0]: linearr[1:]})
                if _debug:
                    print >> sys.stderr, "NOT seen"
            else:
                for i in range(len(seen[linearr[0]])):
                    seen[linearr[0]][i] += linearr[i+1]
                if _debug:
                    print >> sys.stderr, "SEEN"
            if _debug:
                print >> sys.stderr, seen[linearr[0]]
    except IOError as ioerr:
        print >> sys.stderr, "File error (parse_file): %s" % str(ioerr)
        return None
    else:
        cleandata = format(seen)
    return cleandata

def main(argv):
    usage = "Usage is report_munger.py -s <source file> [-x,--debug]"
    try:
        opts, args = getopt.getopt(argv, "xs:", ["debug"])
    except getopt.GetoptError as err:
        print(err)
        print(usage)
        sys.exit(2)

    global _debug
    _debug = False
    cleanfile = ""
    dirtyfile = ""
    for opt, arg in opts:
        if opt == '-s':
            dirtyfile = arg
        elif opt in ("-x", "--debug"):
            _debug = True
        else:
            assert False, "unhandled option"
    if dirtyfile == "":
        print(usage)
        sys.exit(2)
    else:
        cleanfile = dirtyfile[0:-4] + "Munged.csv"
        if _debug:
            print >> sys.stderr, cleanfile

    try:
        results = run(dirtyfile)
        try:
            with open(cleanfile, "w") as the_file:
                for line in results:
                    the_file.write(line + "\n")
        except IOError as ioerr:
            print("File error (main): " + str(ioerr))
    except TypeError as terr:
        print("File error (main): " + str(terr))

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/munge", ReportHandler)
])

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start

