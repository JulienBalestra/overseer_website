try:
	from boto.s3.connection import S3Connection
	from boto.s3.key import Key
	from boto.s3.connection import Location
except ImportError:
	raise ImportError("pip install boto")

import glob
import os
import argparse


def create_connection(cred, proxy):
	if proxy is True:
		conn = S3Connection(cred["aws_id"], cred["aws_secret"], proxy=cred["proxy"], proxy_port=cred["proxy_port"],
		                    proxy_user=cred["proxy_user"],
		                    proxy_pass=cred["proxy_pass"])
	else:
		conn = S3Connection(cred["aws_id"], cred["aws_secret"])
	return conn


def get_bucket(connection, name):
	return connection.get_bucket(name)


def new_key(bucket):
	return Key(bucket)


def update_full_directory(path, local_key):
	print path
	for item in glob.glob(path):
		local_key.key = item
		try:
			local_key.set_contents_from_filename(item)
			bucket.set_acl("public-read", item)
		except IOError:
			update_full_directory(item + "/*", local_key)


if __name__ == "__main__":
	args = argparse.ArgumentParser()
	args.add_argument("aws_id", help="AWS id S3 capable")
	args.add_argument("aws_secret", help="AWS S3 secret")
	args.add_argument("-p", "--proxy", default=False, help="Proxy")
	args.add_argument('-pu', '--proxy_user', type=str, help='Proxy user')
	args.add_argument('-ps', '--proxy_ps', type=str, help='Proxy password')
	args.add_argument('-pi', '--proxy_ip', type=str, help='Proxy IP address')
	args.add_argument('-pp', '--proxy_port', type=str, help='Proxy port')

	credentials = {"aws_id": args.parse_args().aws_id, "aws_secret": args.parse_args().aws_secret}

	proxy = args.parse_args().proxy
	if proxy is True:
		credentials["proxy"] = args.parse_args().proxy_ip
		credentials["proxy_port"] = args.parse_args().proxy_port
		credentials["proxy_user"] = args.parse_args().proxy_user
		credentials["proxy_pass"] = args.parse_args().proxy_ps

	connection = create_connection(credentials, proxy)
	bucket_name = "overseer.julienbalestra.com"

	bucket = get_bucket(connection, bucket_name)
	new_key = new_key(bucket)

	os.chdir("srcs")
	update_full_directory("*", new_key)