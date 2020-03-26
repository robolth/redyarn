import os
import json
import boto3
import botocore

from botocore.exceptions import ClientError

from datetime import date

from io import StringIO, BytesIO

from typing import List
from werkzeug.security import check_password_hash

BUCKET = "redyarn-hashes"
hashes_id = "hashes"

# Old method on premises
#hashes_path = 'hashes.json'

daily_limit = 10

# We will only keep the hash of the master admin api keys for security reasons
admin_hash = 'pbkdf2:sha256:150000$NQmwQ424$07d00bc3fa5f635695745e05770d436f68db6838dbf656ef734a677fd41b5f61'


def info_from_admin_passphrase(api_key, required_scopes):
    """
    Check and retrieve authentication information from api_key.
    Returned value will be passed in 'token_info' parameter of your operation function, if there is one.
    'sub' or 'uid' will be set in 'user' parameter of your operation function, if there is one.

    :param api_key API key provided by Authorization header
    :type api_key: str
    :param required_scopes Always None. Used for other authentication method
    :type required_scopes: None
    :return: Information attached to provided api_key or None if api_key is invalid or does not allow access to called API
    :rtype: dict | None
    """

    if check_password_hash(admin_hash,api_key):
        return {'uid':'admin'}


def info_from_passphrase(api_key, required_scopes):
    """
    Check and retrieve authentication information from api_key.
    Returned value will be passed in 'token_info' parameter of your operation function, if there is one.
    'sub' or 'uid' will be set in 'user' parameter of your operation function, if there is one.

    :param api_key API key provided by Authorization header
    :type api_key: str
    :param required_scopes Always None. Used for other authentication method
    :type required_scopes: None
    :return: Information attached to provided api_key or None if api_key is invalid or does not allow access to called API
    :rtype: dict | None
    """

    # Load existing hashes JSON from s3 bucket
    res = boto3.resource('s3')
    try:
        fileObject = res.Object(BUCKET, hashes_id)
        file = fileObject.get()['Body'].read().decode('utf-8')
        hashes = json.loads(file)
    except ClientError as error:
        print({"detail": "Hashes" + str(error),"status": 400,"title": "Error","type": "about:blank"})
        return None
    except:
        print({"detail": "Hashes not found","status": 400,"title": "Error","type": "about:blank"})
        return None

    for uid, hash_key in hashes.items():
        if check_password_hash(hash_key['hash'],api_key):

            today = date.today().strftime("%Y/%m/%d")

            if 'last_access_date' in hash_key:

                print(hash_key['last_access_date'])
                print(today)

                if hash_key['last_access_date'] != today:

                    print("a")

                    hash_key['last_access_date'] = today
                    hash_key['requests_count'] = 1

                    save_hashes(hashes)

                    """
                    # save hashes
                    if os.path.exists(hashes_path): os.remove(hashes_path)
                    with open(hashes_path, 'w') as f:
                        json.dump(hashes, f)
                        f.close()
                    """

                    return {'uid':uid}

                else:

                    print("b")

                    if hash_key['requests_count'] < daily_limit:
                        hash_key['requests_count'] = hash_key['requests_count'] + 1

                        save_hashes(hashes)

                        """
                        # save hashes
                        if os.path.exists(hashes_path): os.remove(hashes_path)
                        with open(hashes_path, 'w') as f:
                            json.dump(hashes, f)
                            f.close()
                        """

                        return {'uid':uid}
            else:
                hash_key['last_access_date'] = today
                hash_key['requests_count'] = 1

                save_hashes(hashes)

                """
                # save hashes
                if os.path.exists(hashes_path): os.remove(hashes_path)
                with open(hashes_path, 'w') as f:
                    json.dump(hashes, f)
                    f.close()
                """

                return {'uid':uid}

    return None


def save_hashes(hashes):

    #Save new hashes file on S3
    client = boto3.client('s3')
    fileObj = BytesIO(json.dumps(hashes).encode())

    try:
        client.upload_fileobj(fileObj, BUCKET, hashes_id)
    except Exception as error:
        print('Warning: boto3:' + error)

