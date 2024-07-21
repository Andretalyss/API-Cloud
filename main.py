from flask import Flask, jsonify

from src.aws.eks.listEKS import listEKS
from src.aws.ec2.listEC2 import listEC2
from src.aws.ebs.listEBS import listEBS

api = Flask(__name__)
api.register_blueprint(listEKS, url_prefix='/api')
api.register_blueprint(listEC2, url_prefix='/api')
api.register_blueprint(listEBS, url_prefix='/api')

if __name__ == '__main__':
    api.run(host="0.0.0.0", port=5000, debug=True)