#!/usr/bin/python
from __future__ import print_function
import argparse
import getpass
import os
import subprocess


def setup_args(parser=None):
    if parser is None:
        parser = argparse.ArgumentParser('A script that shows the difference '
                                         'in the trusted CAs of two java '
                                         'keystores.'
                                         )
    parser.add_argument('--keystore-one', dest='keystore_loc_one',
                        help='Path to the first keystore file.',
                        required=True)
    parser.add_argument('--keystore-two', dest='keystore_loc_two',
                        help='Path to the second keystore file.',
                        required=True)
    args = parser.parse_args()
    return args


def keystore_output_to_get_entries(lines):
    sha_to_alias_mapping = {}
    current_alias = None
    sha_text = 'Certificate fingerprint (%s):'
    sha1_text = sha_text % 'SHA1'
    sha256_text = sha_text % 'SHA-256'
    for line in lines:
        if current_alias is None and 'trustedCertEntry' not in line:
            continue
        if 'trustedCertEntry' in line:
            if current_alias is not None:
                raise ValueError('unexpected trustedCertEntry line!')
            current_alias = line.strip()
        elif current_alias and (sha1_text in line or sha256_text in line):
            if sha1_text in line:
                sha = line.split(sha1_text)[-1].strip()
            else:
                sha = line.split(sha256_text)[-1].strip()
            sha_to_alias_mapping[sha] = current_alias
            current_alias = None
    return sha_to_alias_mapping


def list_keys_in_keystore(path_to_keystore, password):
    command = [
        'keytool',
        '-list',
        '-keystore', path_to_keystore,
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate(
        (password + os.linesep).encode('utf-8'))
    return stdout.decode('utf-8').split(os.linesep)


def main(args):
    keystore_msg = 'Enter the %s keystore password:'
    first_store_passwd = getpass.getpass(keystore_msg % 'first')
    second_store_passwd = getpass.getpass(keystore_msg % 'second')
    first_dict = keystore_output_to_get_entries(
        list_keys_in_keystore(args.keystore_loc_one,
                              first_store_passwd)
    )
    second_dict = keystore_output_to_get_entries(
        list_keys_in_keystore(args.keystore_loc_two,
                              second_store_passwd)
    )
    first_shas = set(first_dict.keys())
    second_shas = set(second_dict.keys())
    if not first_shas:
        raise ValueError('The first keystore is empty.')
    if not second_shas:
        raise ValueError('The second keystore is empty.')
    for sha in sorted(list(second_shas - first_shas)):
        print('added', sha, second_dict[sha])
    for sha in sorted(list(first_shas - second_shas)):
        print('removed', sha, first_dict[sha])


if __name__ == "__main__":
    main(setup_args())
