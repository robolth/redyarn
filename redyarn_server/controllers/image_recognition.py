import json
import boto3
from botocore.exceptions import ClientError
from io import BytesIO

BUCKET = "redyarn-recognition"
CONFIDENCE = 85

def detect_labels(bucket, key, max_labels=10, min_confidence=CONFIDENCE, region="eu-west-1"):

    rekognition = boto3.client("rekognition", region)
    response = rekognition.detect_labels(Image={"S3Object": {"Bucket": bucket, "Name": key}},
                                         MaxLabels=max_labels,
                                         MinConfidence=min_confidence)
    return response['Labels']

def detect_celebrities(bucket, key, region="eu-west-1"):
    rekognition = boto3.client("rekognition", region)
    response = rekognition.recognize_celebrities(
                Image={"S3Object": {"Bucket": bucket, "Name": key}})
    return response['CelebrityFaces']


def analyze_image(file) -> dict:


    # First load the image file to S3    
    client = boto3.client('s3')
    fileObj = BytesIO(file.read())
    temp_key="temp_image"

    try:
        client.upload_fileobj(fileObj, BUCKET, temp_key)
    except Exception as error:
        print('Warning: boto3:', str(error))
        return None

    #Now analyze the image
    output = {}


    # Labels recognition
    labels = []
    try:
        for label in detect_labels(BUCKET, temp_key):
            labels.append("{Name}".format(**label))
    except ClientError as error:
        print(error)
        output["aws_rekognition"] = "Please allow on RosettaHub"
        print("Please allow AWS Rekognition on RosettaHub")

    if len(labels) > 0:
        output.update({"Labels":labels})

    # Celebs recognition
    celebrities = {}
    try:

        for celebrity in detect_celebrities(BUCKET, temp_key):
            celeb = {}
            celeb.update({"Name": "{Name}".format(**celebrity)})
            celeb.update({"Urls:": "{Urls}".format(**celebrity)})
            celeb.update({"MatchConfidence":format(float("{MatchConfidence}".format(**celebrity))/100, '.3f')})
            celebrities.update(celeb)

    except ClientError as error:
        output["aws_rekognition"] = "Please allow on RosettaHub"
        print(error)
        print("Please allow AWS Rekognition on RosettaHub")

    # Aggregate results
    if len(celebrities) > 0:
        output.update({"Celebrities":celebrities})

    # Finally, delete the image file in the bucket
    try:
        client.delete_object(Bucket=BUCKET, Key=temp_key) #retour type response[]
    except ClientError as error:
         print("Warning: error during deletion of temp image:", error)

    return output