#!/usr/bin/env python3

#import redyarn_server
import connexion
from zappa.asynchronous import task

from redyarn_server import encoder

app = connexion.App(__name__, specification_dir='./redyarn_server/openapi/')
app.app.json_encoder = encoder.JSONEncoder
app.add_api('openapi.yaml',
            arguments={'title': 'Red Yarn Project'},
            pythonic_params=True)


def main():
    app.run(port=8080)


if __name__ == '__main__':
    main()
