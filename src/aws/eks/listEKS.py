from flask import Blueprint, jsonify, request
from concurrent.futures import ThreadPoolExecutor
from environments.config import get_account_and_regions

import string, random

listEKS = Blueprint('listEKS', __name__)

def generate_random_dates(len, resource):
    if resource == 'version':
        versions = ['1.27', '1.28', '1.29', '1.30']
        return random.choice(versions)
    else:
        characters = string.ascii_letters + string.digits
        return 'eks-' + ''.join(random.choice(characters) for _ in range(len))
    

def get_clusters(account, region):
    clusters = []

    for i in range(random.randint(2,4)):
        template = {
            "cluster_name": generate_random_dates(5, 'Name'),
            "version": generate_random_dates(5, 'version'),
            "region": region,
            "account": account
        }

        clusters.append(template)

    return clusters

def return_clusters(regions, account=None, version=None):
    clusters = []

    with ThreadPoolExecutor() as executor:
        threads = []
        if not account:
            accounts, _ = get_account_and_regions()

            for account in accounts:
                for region in regions:
                    threads.append(executor.submit(get_clusters, account, region))
        else:
            for region in regions:
                threads.append(executor.submit(get_clusters, account, region))
    
    for thread in threads:
        response = thread.result()
        if version:
            for cluster in response:
                if cluster['version'] == version:
                    clusters.append(cluster)
        else:
            for cluster in response:
                clusters.append(cluster)
    
    return clusters

@listEKS.route('/eks/clusters', methods=['GET'], strict_slashes=False)
def list_eks_route():
    account_to_scan = request.json.get('account')
    version = request.json.get('version')

    accounts, regions = get_account_and_regions()

    if account_to_scan not in accounts:
        return jsonify({
            'error': f'account {account_to_scan} is not valid.'
        }), 400

    if not account_to_scan and not version:
        clusters = return_clusters(regions)
        return jsonify(clusters), 200
    elif account_to_scan and not version:
        clusters = return_clusters(regions, account_to_scan)
        return jsonify(clusters), 200
    elif account_to_scan and version:
        clusters = return_clusters(regions, account_to_scan, version)
        return jsonify(clusters), 200
    else:
        clusters = return_clusters(regions,None,version)
        return jsonify(clusters), 200

