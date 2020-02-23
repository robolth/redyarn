# Rapport projet fil rouge

## Architecture

### Spécifications
L’architecture de l’API devant repecter les spécifications[OpenAPI](https://github.com/OAI/OpenAPI-Specification), mon choix s’est rapidement porté sur l’utilisation de l’outil [Swagger Editor](https://editor.swagger.io/) pour la génération du fichier de spécifications au format [YAML](https://yaml.org/).

J’ai décidé d’implémenter les fonctionnalités suivantes :

- une requête POST sur le chemin d’accès /file/ permettant de charger un document sur le serveur et renvoyant un fichier JSON  contenant les métadonnées et les éventuelles données extraites du fichier,

- une requête GET sur le chemin d’accès /metadata/ permettant de renvoyer le fichier JSON généré par une requête précédent,

- une requête GET sur le chemin d’accès /metadata/ascii-art/ permettant de renvoyer le contenu d’une image converti en texte simple (méthode généralement connue sous le nom d’[*ASCII art*](https://en.wikipedia.org/wiki/ASCII_art) (ce contenu est également intégré au JSON de la requête normale, mais cette requête spécifique permet de l’afficher directement sans décalage de ligne afin que l’usager reconnaisse immédiatement l’image),

- une requête GET sur le chemin d’accès /metadata/ls/ renvoyant un page html listant l’ensemble des métadonnées déjà extraites avec des liens pour y accéder plus facilement,

- une requête DELETE sur le chemin d’accès /metadata/ pour effacer un fichier JSON de métadonnées précédemment extrait,

- une requête DELETE sur le chemin d’accès /metadata/ls/ pour effacer l’ensemble des métadonnées précédemment extraites,

- une requête POST sur le chemin /api_key/ permettant d’enregistrer un nouvel usager 



### Code du serveur
J’avais à l’origine développé un premier prototype de serveur Flask permettant répondant aux attentes du projet, sur la base de travaux pratiques réalisés en cours de Python. J’ai ensuite cherché à adapter ce code aux spécifications OpenAPI suite aux cours de _Services Oriented Architecure_ (SOA). Néanmoins cette approche ascendante s’est rapidement avérée fastidieuse, source d’erreurs et surtout d’un code brouillon.

Afin d’optimiser la conformité du code avec les normes de qualité Python ainsi que les bonnes pratiques en vigueur, j’ai donc décidé d’adopter une approche descendante en générant automatiquement l’architecture du serveur Flask à partir de mon fichier de spécifications grâce à l’outil open source [OpenAPI Generator](https://github.com/OpenAPITools/openapi-generator).

Néanmoins cela a conduit à des difficultés :

- bouts de code Java
- système d'imports tiré de Python 2 adapté à Python 3 avec Python -m ce qui bloque un déploiement serverless (voir plus loin)


## Fonctionnalités

- pdf

- epub

- csv

- fichiers Microsoft

- images
    - ascii art

- mp3

- mp4

- aws reckognition

## Sécurité

- Chiffrement des passphrases
- Hachage et conservation uniquement des hashes
- Proxy
- Limitation à 10 requêtes par jour
- SecureFileName()

- Buckets S3 différents pour les différents types d'objets



## Déploiement

### Local

### S3, Ubuntu puis FreeBSD


- Pour effacer automatiquement les métadonnées chargées au bout d'une année, une règle de gestion a été ajoutée sur le bucket S3 approprié.

**(Ajouter l'image.)**

J'ai choisi d'isoler les métadonnées des hashes afin de faciliter cette règle de gestion.

Enfin, par commodité, j'ai alloué une [adresse ip elastique statique](https://eu-west-1.console.aws.amazon.com/ec2/v2/home?region=eu-west-1#Addresses)

### Serverless

- Full stateless conversion

- Conversion du serveur par [zappa](https://github.com/Miserlou/Zappa) :

problème de noms de domaine, puis problème de taille géré par [slim handler](https://github.com/Miserlou/zappa-blog/blob/master/posts/slim-handler.md)

# Procédure pour le déploiement serverless :

Si tu n'as pas installé Xcode sur ton mac (pas sûr que ce soit nécessaire):
$ xcode-select --install

Tous les trucs à installer/màj au préalable :
$ pip install awscli
$ pip install boto
$ pip install --upgrade boto
$ pip install boto3
$ pip install --upgrade boto3
$ pip install botocore
$ pip install --upgrade botocore

Configurer le dossier .aws si ce n'est pas déjà fait :
$ aws configure
(Il faudra entrer les clefs RosettaHub)

Si ce n'est pas déjà fait, créer un environnement virtuel Python :
$ python3 -m venv venv

Activer son venv :
$ source venv/bin/activate

Installer les trucs nécessaires dans son venv :

$ pip install connexion[swagger-ui]
(Nécessaire pour générer la doc API)

$ pip install zappa
(Outil de conversion serverless)

Faire tourner l'app dans le venv et installer toutes les librairies nécessaires

Une fois que tout est prêt :

$ zappa init
(On peut fournir un S3 existant si on veut)

Modifier le fichier zappa_settings.json qui a été généré en ajoutant : "slim_handler": true

Modifier venv/lib/python3.6/site-packages/zappa/core.py :
Commenter les lignes 1038 et 1039 :

            Environment={'Variables': aws_environment_variables},
            KMSKeyArn=aws_kms_key_arn,

(Ces deux lignes servent à contourner une limitation de RosettaHub)

A ce stade tout devrait être prêt :
$ zappa deploy dev

Si tout se déroule correctement, on obtient une url !

(A ce stade, me contacter sur whatsapp car il n'y a aucune chance que ça marche du premier coup...)


Troubleshoot:

Check if Flask, werkzeug, etc. is in requirements (not installed globally)
Delete all python cache files : find . -name \*.pyc -delete
pip install tqdm==4.32.2


Useful links:
Zappa: https://blog.apcelent.com/deploy-flask-aws-lambda.html
Another useful one: https://serverless.com/framework/docs/providers/aws/guide/credentials/

https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html#configuration-envvars-encryption

https://github.com/Miserlou/Zappa#setting-environment-variables

https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html#configuration-envvars-encryption







- explication de l'api : sécurité, etc.

—  get pour ascii-art

- génération du serveur flask avec openapi generator

- bug du generateur : lignes java à remplacer

- problème Password request dans query

- premier déploiement très facile avec venv dans elastic beanstalk, mais passage à ec2 sur demande du prof

- freebsd -> installation bash

- problème FreeBSD (PYTHONPATH) réglé par venv

- problème scikit-image : https://www.freshports.org/graphics/py-scikit-image

- elastic ip adresse statique

- code python : totalement serverless sauf pour les epub

- Ne pas oublier de configurer les credentials sur la machine serveur : https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html


Rapport : parler du stockage des hashes et de la gestion des certificats de sécurité dans la partie crypto

- Contrôle du nombre de requêtes par jour

- Nettoyage automatique et organisé de S3

Suivi : aws API gateway : fournir direct le projet .yaml