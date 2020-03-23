# Red Yarn Project 4.0  
School project for CentraleSupelec. 

[https://ln2e8uzlpa.execute-api.eu-west-1.amazonaws.com/dev/openapi/ui/](https://ln2e8uzlpa.execute-api.eu-west-1.amazonaws.com/dev/openapi/ui/)  

Extract metadata from uploaded files, and output them in JSON format. Basic metadata are extracted from all files, as well as specific metadata from these types of files:  

- plain text (txt, markdown, python, etc., unicode or ascii encoded content)  
- csv (delimiters, line terminators, numbers of rows and columns, content)  
- images (exif data and ascii art generated from image)  
- pdf (various document info and text content for some files)  
- Microsoft Office document (various document info)  
- epub (various document info)  
- mp3 (various info)  
- mp4 (various info, experimental, limited results)  

You can also request any or all previously extracted metadata with its identifier. Metadata will be deleted after one year. Admin privilege let you delete any or all metadata. This server does not store any personnal information or ip adress. It uses passphrases to grant access to some requests, but all operations are anonymized and only the number of requests per day is logged to mitigate risk of abuse (in particular, uploaded files and metadata are NOT linked to passphrases).

Regular passphrases are limited to 10 requests per day, and can only upload files and access existing metadata. For security reasons, passphrases are NOT stored on server, we only have access to the hashes. Be sure to note down your passphrase as it cannot be recovered from the hashses if lost.
