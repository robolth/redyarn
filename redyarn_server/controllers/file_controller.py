import os
import connexion
import six
#import pprint
import magic
import hashlib
import json
import boto3
from datetime import date

#import logging

from botocore.exceptions import ClientError, NoCredentialsError
from werkzeug.utils import secure_filename
from flask import request
from redyarn_server.models.metadata import Metadata  # noqa: E501
from redyarn_server import util
from pathlib import Path

from io import StringIO, BytesIO

from .image_recognition import analyze_image
from .image_converter import get_ascii_conversion, get_exif_data
from .file_converter import get_pdf_info, get_pdf_text, get_office_info, get_id3_info, get_mp4_info, get_csv_info, get_epub_info

FILEBUCKET = "redyarn-files"
BUCKET = "redyarn-metadata"
BLOCKSIZE = 65536

def post_file(data=None):  # noqa: E501
    """Upload a file

    Upload a file and get its metadata # noqa: E501

    :param data: 
    :type data: str

    :rtype: Metadata
    """

    # Specific metadata
    filename = secure_filename(data.filename)
    extension = filename.split(".")[-1]
    mimetype = data.mimetype
    size = request.content_length

    # Set buffer to beginning of file to get the file type
    data.seek(0)
    filetype = magic.from_buffer(data.read())

    # Get the file
    file = request.files.get('data')

    # Hash a unique identifier
    hasher = hashlib.md5()

    file.seek(0)
    buf = file.read(BLOCKSIZE)
    while len(buf) > 0:
        hasher.update(buf)
        buf = file.read(BLOCKSIZE)
    hasher.update(buf)

    id_file = hasher.hexdigest()

    if id_file is None:
        print("Cannot open file")
        return {"detail": "cannot read file","status": 500,"title": "Error","type": "about:blank"}

    # Specific metadata
    text = None
    exif_data = None
    image_recognition = None
    ascii_art = None
    pdf_info = None
    office_info = None
    csv_info = None
    epub_info = None
    id3_info = None
    mp4_info = None

    #Set file stream to beginning
    file.seek(0)

    # Save file to S3
    client = boto3.client('s3')
    fileObj = BytesIO(file.read())

    try:
        client.upload_fileobj(fileObj, FILEBUCKET, id_file)
    except Exception as error:
        print('Warning: boto3:', str(error))

    file.seek(0)

    #Plain text
    if 'UTF-8' in filetype or 'utf-8' in filetype or 'text/plain' in mimetype:
        text = file.read().decode('utf-8')
    elif 'ASCII' in filetype or 'ascii' in filetype:
        text = file.read().decode('ascii')

    # csv
    elif 'CSV' in filetype or 'csv' in mimetype:

        #Serverless conversion
        csv_file = StringIO(file.read().decode('utf-8'))

        csv_info = get_csv_info(csv_file)

        file.seek(0)
        text = file.read().decode('utf-8')

    # epub
    elif 'EPUB' in filetype or 'epub' in mimetype:
        epub_info = get_epub_info(file)

    # Image
    elif 'image' in filetype or 'image' in mimetype:
        exif_data = get_exif_data(file)
        file.seek(0)

        width = exif_data['width']
        height = exif_data['height']

        # Compute optimal scaling for image aspect ratio
        image_ratio = height / width
        scaling = int(image_ratio * 100)

        # Generate ascii art
        ascii_art = get_ascii_conversion(file,scaling)

        ascii_art += "\nAscii art generated for 1440x900 screen resolution"

        #Analyze image with Aws reckognition
        file.seek(0)
        image_recognition = analyze_image(file)

    # PDF
    elif 'PDF' in filetype or 'pdf' in mimetype:
        pdf_info = get_pdf_info(file)
        file.seek(0)
        text = get_pdf_text(file)

    # Bloated shit
    elif 'Microsoft' in filetype or 'openxmlformats-officedocument' in mimetype:
        office_info = get_office_info(file)

    # MP3
    elif 'ID3' in filetype or 'mpeg' in mimetype:
        id3_info = get_id3_info(file)

    # MP4
    elif 'MP4' in filetype or 'mp4' in mimetype:
        mp4_info = get_mp4_info(file)

    today = date.today().strftime("%Y-%m-%d")

    #Create json file
    metadata = Metadata(id_file=id_file,
                        date_created=today,
                        filename=filename,
                        mimetype=mimetype,
                        filetype=filetype,
                        size=size,
                        extension=extension,
                        text=text,
                        ascii_art=ascii_art,
                        exif_data=exif_data,
                        image_recognition=image_recognition,
                        csv_info=csv_info,
                        epub_info=epub_info,
                        pdf_info=pdf_info,
                        office_info=office_info,
                        id3_info=id3_info,
                        mp4_info=mp4_info)


    #Save metedata to another S3 bucket
    fileObj = BytesIO(json.dumps(metadata.to_str()).encode())

    try:
        client.upload_fileobj(fileObj, BUCKET, id_file)
#        logging.info("S3: upload OK")
#        result = True
    except Exception as error:
        print('Warning: boto3:' + error)

    """
#    if not os.path.isdir('metadata'): Path('metadata').mkdir(parents=True, exist_ok=True)
    metadata_path ='metadata/' + id_file + '.json'

    with open(metadata_path, 'w') as f:
        json_file = json.dump(metadata.to_dict(),f)
        f.close()

    """

    return metadata
