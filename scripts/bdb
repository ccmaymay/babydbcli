#!/usr/bin/env python2.7

# Largely copied from Dropbox Python Core API SDK tutorial:
# https://www.dropbox.com/developers/core/start/python

import dropbox
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import logging
import os
import json


def pull(client, path):
    remote_path = '/%s' % path
    (remote_f, remote_metadata) = client.get_file_and_metadata(remote_path)

    dirname = os.path.dirname(path)
    if dirname and not os.path.isdir(dirname):
        os.path.makedirs(dirname)

    with open(path, 'wb') as f:
        f.write(remote_f.read())

    logging.info(
        '%s <- %s (v%d)' % (path, remote_path, remote_metadata['revision'])
    )


def push(client, path):
    remote_path = '/%s' % path

    with open(path, 'rb') as f:
        response = client.put_file(remote_path, f)

    logging.info(
        '%s -> %s (v%d)' % (path, remote_path, response['revision'])
    )


parser = ArgumentParser(
    description='pull/push individual files',
    formatter_class=ArgumentDefaultsHelpFormatter,
)
parser.add_argument('command', type=str, choices=('pull', 'push'),
                    help='command to execute against server')
parser.add_argument('path', type=str,
                    help='relative path to file to pull or push')
ns = parser.parse_args()


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)-15s %(levelname)s %(funcName)s: %(message)s'
)


secrets_path = os.path.expanduser('~/.babydbcli/client_secrets.json')
with open(secrets_path) as f:
    secrets = json.load(f)
    app_key = secrets['app_key']
    app_secret = secrets['app_secret']

token_path = os.path.expanduser('~/.babydbcli/dbauth.cred')

if os.path.exists(token_path):
    with open(token_path) as f:
        access_token = f.read()
else:
    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

    authorize_url = flow.start()
    print 'Go to: ' + authorize_url
    code = raw_input('Authorization code: ').strip()

    (access_token, user_id) = flow.finish(code)

    with open(token_path, 'w') as f:
        f.write(access_token)
    os.chmod(token_path, 0600)

client = dropbox.client.DropboxClient(access_token)

if ns.command == 'pull':
    pull(client, ns.path)
elif ns.command == 'push':
    push(client, ns.path)
else:
    raise ValueError('unknown command %s' % ns.command)
