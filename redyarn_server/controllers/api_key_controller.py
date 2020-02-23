import os
import connexion
import six
import json
import boto3
import botocore

from botocore.exceptions import ClientError

from werkzeug.security import generate_password_hash
from redyarn_server import util

from io import StringIO, BytesIO

from redyarn_server.models.metadata import Metadata  # noqa: E501
from redyarn_server import util

BUCKET = "redyarn-hashes"
hashes_id = "hashes"

# Old copde for on premises stock
#hashes_path = 'hashes.json'

def add_api_key(new_passphrase):  # noqa: E501
    """Create an api key with a new passphrase

    Create a regular api key (limited to 10 requests per day). Requires an admin passphrase. # noqa: E501

    :param body: new passphrase to generate a new regular api key
    :type body: str

    :rtype: object
    """

    body = new_passphrase

    # Load existing hashes JSON from s3 bucket
    res = boto3.resource('s3')
    try:
        fileObject = res.Object(BUCKET, hashes_id)
        file = fileObject.get()['Body'].read().decode('utf-8')
        hashes = json.loads(file)
    except ClientError as error:
        hashes = {}
        print({"detail": "Hashes" + str(error),"status": 400,"title": "Error","type": "about:blank"})
    except:
        print({"detail": "Hashes not found","status": 400,"title": "Error","type": "about:blank"})
        hashes = {}


    """
    Old method for on premises storage
    # Load existing hashes
    if os.path.exists(hashes_path):
        if os.path.getsize(hashes_path) > 0:
            with open(hashes_path, 'r') as f:
                hashes = json.load(f)
                f.close()
        else:
            hashes = {}
    else:
        hashes = {}
    """

    # Find new unique uid
    max_uid = 0
    for uid, _ in hashes.items():
        uid_num = int(uid.split("user", 1)[1])
        if uid_num > max_uid:
            max_uid = uid_num

    #Set new uid
    new_uid = "user"+str(max_uid + 1)
    new_hash = generate_password_hash(body)

    # Save new hashes
    hashes[new_uid] = {'hash':new_hash}

    #Save new hashes file on S3
    client = boto3.client('s3')
    fileObj = BytesIO(json.dumps(hashes).encode())

    try:
        client.upload_fileobj(fileObj, BUCKET, hashes_id)
#        logging.info("S3: upload OK")
#        result = True
    except Exception as error:
        print('Warning: boto3:' + error)

    """
    # old method on premises
    if os.path.exists(hashes_path): os.remove(hashes_path)


    with open(hashes_path, 'w') as f:
        json.dump(hashes, f)
        f.close()
    """

    return {"detail": "api key created for uid "+ new_uid,"status": 200,"title": "successful operation","type": "about:blank"}


def delete_api_key(uid):  # noqa: E501
    """Revoke an api key

    Revoke an api key. This requires an admin passphrase. # noqa: E501

    :param uid: user id of api key to delete
    :type uid: str

    :rtype: None
    """

    # Load existing hashes JSON from s3 bucket
    res = boto3.resource('s3')
    try:
        fileObject = res.Object(BUCKET, hashes_id)
        file = fileObject.get()['Body'].read().decode('utf-8')
        hashes = json.loads(file)
    except ClientError as error:
        return {"detail": error,"status": 400,"title": "Error","type": "about:blank"}
    except:
        return {"detail": "Hashes not found","status": 400,"title": "Error","type": "about:blank"}


    """
    #Old method for on premises storage

    # Load existing hashes
    if os.path.exists(hashes_path):
        if os.path.getsize(hashes_path) > 0:
            with open(hashes_path, 'r') as f:
                hashes = json.load(f)
                f.close()
        else:
            return {"detail": "api key not found","status": 400,"title": "Error","type": "about:blank"}
    else:
        return {"detail": "api key not found","status": 400,"title": "Error","type": "about:blank"}
    """

    popped_uid = hashes.pop(uid, None)

    if popped_uid is None:
        return {"detail": "api key not found","status": 400,"title": "Error","type": "about:blank"}
    else:

        # Save new hashes

        client = boto3.client('s3')
        fileObj = BytesIO(json.dumps(hashes).encode())

        try:
            client.upload_fileobj(fileObj, BUCKET, hashes_id)
    #        logging.info("S3: upload OK")
    #        result = True
        except Exception as error:
            return {"detail": "Warning: boto3:" + str(error),"status": 400,"title": "Error","type": "about:blank"}

        """
        #Old method for on premises storage

        if os.path.exists(hashes_path): os.remove(hashes_path)

        with open(hashes_path, 'w') as f:
            json.dump(hashes, f)
        """

        return {"detail": "api key deleted for uid "+ uid,"status": 200,"title": "successful operation","type": "about:blank"}

