#!/usr/bin/python

import sys

import boto
import boto.s3.connection
from boto.s3.key import Key

access_key = 'PYVPOGO2ODDQU24NXPXZ'
secret_key = 'pM1QULv2YgAEbvzFr9zHRwdQwpQiT9uJ8hG6JUZK'
rgw_hostname = 'ceph1.lab.com'
rgw_port = 8080
local_testfile = '/tmp/testfile'
bucketname = 'mybucket'


conn = boto.connect_s3(
	aws_access_key_id = access_key,
	aws_secret_access_key = secret_key,
	host = rgw_hostname,
	port = rgw_port,
	is_secure=False,
	calling_format = boto.s3.connection.OrdinaryCallingFormat(),
	)

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '#'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix))
    if iteration == total: 
        print()

def percent_cb(complete, total):
    printProgressBar(complete, total)

bucket = conn.create_bucket('mybucket')
for bucket in conn.get_all_buckets():
	print "{name}\t{created}".format( name = bucket.name, created = bucket.creation_date,)

bucket = conn.get_bucket(bucketname) 

k = Key(bucket)
k.key = 'my test file'
k.set_contents_from_filename(local_testfile, cb=percent_cb, num_cb=20)
