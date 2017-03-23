#!/usr/bin/env python2.7

# Largely copied from Dropbox Python Core API SDK tutorial:
# https://www.dropbox.com/developers/core/start/python

import dropbox
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import logging
import os
import json


def pull(client, remote_path, local_path):
    if not remote_path.startswith('/'):
        remote_path = '/' + remote_path

    if os.path.isdir(local_path) and not local_path.endswith('/'):
        local_path = local_path + '/'

    if local_path.endswith('/'):
        local_path = local_path + os.path.basename(remote_path)

    (remote_f, remote_metadata) = client.get_file_and_metadata(remote_path)

    dirname = os.path.dirname(local_path)
    if dirname and not os.path.isdir(dirname):
        os.path.makedirs(dirname)

    with open(local_path, 'wb') as local_f:
        local_f.write(remote_f.read())

    logging.info(
        '%s <- %s (v%d)' %
        (local_path, remote_path, remote_metadata['revision'])
    )


def push(client, local_path, remote_path):
    if not remote_path.startswith('/'):
        remote_path = '/' + remote_path

    if remote_path.endswith('/'):
        remote_path = remote_path + os.path.basename(local_path)

    with open(local_path, 'rb') as local_f:
        response = client.put_file(remote_path, local_f)

    logging.info(
        '%s -> %s (v%d)' %
        (local_path, remote_path, response['revision'])
    )


def main():
    parser = ArgumentParser(
        description='pull/push individual files',
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('command', type=str, choices=('pull', 'push'),
                        help='command to execute against server')
    parser.add_argument('path1', type=str,
                        help='local/remote path to push/pull (respectively)')
    parser.add_argument('path2', type=str,
                        help='remote/local path to push/pull (respectively)')
    args = parser.parse_args()

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

    if args.command == 'pull':
        pull(client, remote_path=args.path1, local_path=args.path2)
    elif args.command == 'push':
        push(client, local_path=args.path1, remote_path=args.path2)
    else:
        raise ValueError('unknown command %s' % args.command)


if __name__ == '__main__':
    main()
