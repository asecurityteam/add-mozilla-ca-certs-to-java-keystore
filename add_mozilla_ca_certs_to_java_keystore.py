#!/usr/bin/python
__version__ = "1.0.0"

import argparse
import getpass
import os
import subprocess

import requests


def setup_args(parser=None):
	if parser is None:
		parser = argparse.ArgumentParser('''A script to add mozilla's'''
			' trusted CA certs to a java keystore.')
	parser.add_argument('-u', '--url', dest='mozilla_cert_url',
		help='Url to the mozilla certdata.txt file. Defaults to using'
		' certdata.txt from hg.mozilla.org.',
		default='https://hg.mozilla.org/mozilla-central/raw-file/'
			'tip/security/nss/lib/ckfw/builtins/certdata.txt'
	)
	parser.add_argument('-w', '--working-directory', dest='working_dir',
		help='The directory to work in')
	parser.add_argument('-k', '--keystore', dest='keystore_loc',
		help='Path to the java keystore to update.',
		required=True)
	args = parser.parse_args()
	return args


def download_url_to_file(url, filename):
	with open(filename, 'wb') as outf:
		outf.write(requests.get(url, verify=True).content)


def extract_certs_to_files(command, directory):
	if os.path.exists(directory):
		raise IOError('Please delete the "%s" directory and run this'
			' script again.' % directory)
	os.mkdir(directory)
	subprocess.Popen(command, cwd=directory).communicate()


def import_ca_certs_to_keystore(keystore_loc, store_passwd, cert_dir):
	for file_ in os.listdir(cert_dir):
		if not file_.endswith('.pem'):
			continue
		command = ['keytool', '-import', '-trustcacerts',
			'-noprompt',
			'-keystore', keystore_loc,
			'-storepass', store_passwd,
			'-file', os.path.join(cert_dir, file_),
			'-alias', file_]
		subprocess.Popen(command).communicate()


def check_requirements():
	try:
		subprocess.call(['go', 'version'], stdout=subprocess.PIPE)
	except OSError:
		raise SystemError('go is not installed')


def main(args):
	go_extract_script_url = ('https://raw.github.com/agl/extract-nss-root-certs/'
		'master/convert_mozilla_certdata.go')
	cert_dir = 'certificates'
	if args.working_dir:
		os.chdir(args.working_dir)
		cert_dir = os.path.join(args.working_dir, cert_dir)
	check_requirements()
	store_passwd = getpass.getpass('Enter the keystore password:')
	download_url_to_file(go_extract_script_url,
		'convert_mozilla_certdata.go')
	download_url_to_file(args.mozilla_cert_url, 'certdata.txt')
	go_command = ['go', 'run',  '../convert_mozilla_certdata.go',
		'-to-files', '../certdata.txt']
	extract_certs_to_files(go_command, cert_dir)
	import_ca_certs_to_keystore(args.keystore_loc, store_passwd, cert_dir)


if __name__=='__main__':
	main(setup_args())
