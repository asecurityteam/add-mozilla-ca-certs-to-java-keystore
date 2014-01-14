### What is this?
This repository contains a `add_mozilla_ca_certs_to_java_keystore.py` python script
that will allow allow you to download, extract mozilla's trusted ca pem files
and import them into a java keystore.


### Requirements
The [Go Programming Language](http://golang.org/doc/install).

The python requirements that the script needs can be installed by running

    pip install -r requirements.txt

### Usage

Here is an example of using the `add_mozilla_ca_certs_to_java_keystore` script

    python add_mozilla_ca_certs_to_java_keystore.py  -w . -k $JAVA_HOME/jre/lib/security/cacerts

###### Help
Help information for the `add_mozilla_ca_certs_to_java_keystore.py`
script can be obtained by running `python add_mozilla_ca_certs_to_java_keystore.py -h`
as shown below.

    python add_mozilla_ca_certs_to_java_keystore.py -h
    usage: A script to add mozilla's trusted CA certs to a java keystore.
           [-h] [-u MOZILLA_CERT_URL] [-w WORKING_DIR] -k KEYSTORE_LOC

    optional arguments:
      -h, --help            show this help message and exit
      -u MOZILLA_CERT_URL, --url MOZILLA_CERT_URL
                        Url to the mozilla certdata.txt file. Defaults to
                        using certdata.txt from hg.mozilla.org.
      -w WORKING_DIR, --working-directory WORKING_DIR
                        The directory to work in
      -k KEYSTORE_LOC, --keystore KEYSTORE_LOC
                        Path to the java keystore to update.


