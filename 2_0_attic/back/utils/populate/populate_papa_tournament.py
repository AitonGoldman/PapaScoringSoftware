#!/usr/bin/python

import subprocess
import getopt
import sys
import json
import argparse

parser = argparse.ArgumentParser(description='setup division (or metadivision) for PAPA')
parser.add_argument('-d', metavar='DIVISION_ID', help='divisions for metadivision',type=int,nargs='+')
parser.add_argument('-m', metavar='METADIVISION_NAME', help='name for metadivision')
parser.add_argument('-s', metavar='STRIPE_SKU', help='sku for single ticket')
parser.add_argument('-ds', metavar='DISCOUNT_STRIPE_SKU', help='sku for discount ticket')
parser.add_argument('-dtc', metavar='DISCOUNT_TICKET_COUNT', help='discount ticket count', type=int)
parser.add_argument('-u', metavar='BASE_URL', help='base url')

args = parser.parse_args()

json_blob = {'meta_division_name':args.m,'divisions':args.d,'use_stripe':True,'stripe_sku':args.s,'discount_stripe_sku':args.ds,'discount_ticket_count':args.dtc}

filled_in_url = '%s/meta_division' % (args.u)
print json.dumps(json_blob)
results = subprocess.check_output(["curl","-b","/tmp/cookie","-H","Content-Type: application/json","-X","POST","-d %s"%json.dumps(json_blob),"%s"%(filled_in_url)])
print results
