import os
import connexion
import six
import json
import boto3
import botocore

import ast

from botocore.exceptions import ClientError

from redyarn_server.models.metadata import Metadata  # noqa: E501
from redyarn_server import util

BUCKET = "redyarn-metadata"



def delete_all_metadata():  # noqa: E501
    """Delete all metadata

    Delete all metadata previously uploaded on server. This requires an admin passphrase. # noqa: E501

    :param id_file: File ID
    :type id_file: str

    :rtype: None
    """

    client = boto3.client('s3')
    res = boto3.resource('s3')

    failed_id = "" 

    for fileObject in res.Bucket(BUCKET).objects.all():
        key = fileObject.key

        try:
            result = client.delete_object(Bucket=BUCKET, Key=key) #retour type response[]
        except ClientError as error:
            print(error)
            print("FileID", key, "could not be deleted")
            failed_id += key + ", "

    if failed_id == "":
        return {"detail": "All file metadata deleted","status": 200,"title": "successful operation","type": "about:blank"}

    else:
        failed_id = "Files " + failed_id + " could not be deleted"
        return {"detail": failed_id,"status": 400,"title": "Error","type": "about:blank"}

def get_all_metadata():  # noqa: E501
    """List all metadata

    List all metadata previously uploaded on server. This requires an admin passphrase. # noqa: E501

    :param id_file: File ID
    :type id_file: str

    :rtype: str
    """

    output = "<!DOCTYPE html><html><body><h1>Metadata available</h1><p>Click on a metadata ID to open its JSON file. (For images, click on mimetype to open ascii art.)</p><p>"

    res = boto3.resource('s3')

    for fileObject in res.Bucket(BUCKET).objects.all():

        key = fileObject.key

        #Security to avoid deleting hashes!
        if "hashes" not in str(key):

            file = fileObject.get()['Body'].read().decode('utf-8')

            try:
                metadata = json.loads(file)

                #Parse string to dict since json.loads is too dumb to do it itself
                metadata = ast.literal_eval(metadata)

                if metadata['id_file'] is None:
                    output += "no idFile"
                else:
                    output += "<a href=\"../?idFile="
                    output += metadata['id_file']
                    output += "\">"
                    output += metadata['id_file']
                    output += "</a>"

                output += " --- "

                if metadata['date_created'] is None:
                    output += "-   no date   -"
                else:
                    output += metadata['date_created']

                output += " --- "

                if metadata['filename'] is None:
                    output += "- no filenalme -"
                else:
                    output += metadata['filename']

                output += " --- "

                if metadata['mimetype'] is None:
                    output += "<no filetype>"
                else:

                    if 'image' in metadata['mimetype']:
                        output += "<a href=\"../ascii-art/?idFile="
                        output += metadata['id_file']
                        output += "\">"
                        output += metadata['mimetype']
                        output += "</a>"
                    else:
                        output += metadata['mimetype']

                output += "<br>"

            except:
                print("unreadable fileobject\n")

    output += "</p></body></html>"

    return output




def delete_metadata(id_file):  # noqa: E501
    """Deletes a file metadata

    Delete the JSON metadata of a file previously uploaded on server # noqa: E501

    :param id_file: File ID
    :type id_file: str

    :rtype: None
    """

    res = boto3.resource('s3')

    try:
        res.Object(BUCKET,id_file).load()
    except ClientError as error:
        if error.response['Error']['Code'] == "404":
            return {"detail": "File metadata not found","status": 404,"title": "Error","type": "about:blank"}
        else:
            return {"detail": "error loading metadata","status": 400,"title": "Error","type": "about:blank"}
    else:

        client = boto3.client('s3')

        try:
            result = client.delete_object(Bucket=BUCKET, Key=id_file) #retour type response[]
        except ClientError as error:
             return {"detail": error,"status": 400,"title": "Error","type": "about:blank"}

        return {"detail": "File metadata deleted","status": 200,"title": "successful operation","type": "about:blank"}


    """
    # Old method on server
    metadata_path ='metadata/' + id_file + '.json'

    if os.path.exists(metadata_path):
        os.remove(metadata_path)
        return {"detail": "File metadata deleted","status": 200,"title": "successful operation","type": "about:blank"}

    else:
        return {"detail": "id_file not found","status": 400,"title": "Error","type": "about:blank"}
    """

def get_metadata(id_file):  # noqa: E501
    """Get a file metadata

    Get the JSON metadata of a file previously uploaded on server # noqa: E501

    :param id_file: File ID
    :type id_file: str

    :rtype: Metadata
    """

    """
    temp = json.loads(temp.decode('utf-8'))
    if type(temp) is tuple:
        result = temp
    else:    
        result = jsonify(result), 200
    return result
    """

    res = boto3.resource('s3')
    try:
        fileObject = res.Object(BUCKET, id_file)
    except ClientError as error:
         return {"detail": error,"status": 400,"title": "Error","type": "about:blank"}
    except:
         return {"detail": "File metadata not found","status": 400,"title": "Error","type": "about:blank"}

    file = fileObject.get()['Body'].read().decode('utf-8')
    metadata = json.loads(file)

    return metadata



    """
    #Old methode on server
    metadata_path ='metadata/' + id_file + '.json'

    if os.path.exists(metadata_path):
        if os.path.getsize(metadata_path) > 0:
            with open(metadata_path, 'r') as f:
                output = json.load(f)
                f.close()
                return output
    else:
        return {"detail": "id_file not found","status": 400,"title": "Error","type": "about:blank"}
    """


def get_asciiart(id_file):  # noqa: E501
    """Get a file metadata

    Get the ascii-art of an image previously uploaded on server. # noqa: E501

    :param id_file: File ID
    :type id_file: str

    :rtype: str
    """

    res = boto3.resource('s3')
    try:
        fileObject = res.Object(BUCKET, id_file)

    except ClientError as error:
         return {"detail": error,"status": 400,"title": "Error","type": "about:blank"}
    except:
         return {"detail": "File metadata not found","status": 400,"title": "Error","type": "about:blank"}

    file = fileObject.get()['Body'].read().decode('utf-8')

    metadata = json.loads(file)

    #Parse string to dict since json.loads is too dumb to do it itself
    metadata = ast.literal_eval(metadata)

    output = metadata['ascii_art']

    if output == None: output = "No ascii art in thi metadata"
    else: output = output +"\n\nPlease enlarge terminal or browser if image seems distorted.\n\n"

    return output


    """
    #Old method on server
    metadata_path ='metadata/' + id_file + '.json'

    if os.path.exists(metadata_path):
        if os.path.getsize(metadata_path) > 0:
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
                f.close()
                return metadata['ascii_art']+"\n\nPlease enlarge terminal or browser if image seems distorted.\n\n"

    else:
        return {"detail": "id_file not found","status": 400,"title": "Error","type": "about:blank"}
    """