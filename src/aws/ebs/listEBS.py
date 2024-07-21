from flask import Blueprint, jsonify, request
from concurrent.futures import ThreadPoolExecutor
from environments.config import get_account_and_regions

import string, random

listEBS = Blueprint('listEBS', __name__)

def generate_random_dates(len, resource):
    if resource == 'VolumeId':
        characters = string.ascii_letters + string.digits
        return 'id-' + ''.join(random.choice(characters) for _ in range(len))
    elif resource == 'Size':
        return random.randint(8,400)
    elif resource == 'VolumeType':
        choices = ['gp3', 'gp2']
        return random.choice(choices)
    elif resource == 'State':
        states = ['available', 'in-use']
        return random.choice(states)
    else:
        characters = string.ascii_letters + string.digits
        return 'ebs-' + ''.join(random.choice(characters) for _ in range(len))

def get_volumes(account, region):
    volumes = []

    for i in range(random.randint(2,8)):

        template = {
            "Name": generate_random_dates(10, 'Name'),
            "State": generate_random_dates(10, 'State'),
            "Size": f"{generate_random_dates(10, 'Size')} GB",
            "VolumeType": generate_random_dates(10, 'VolumeType'),
            "VolumeId": generate_random_dates(10, 'VolumeId'),
            "Account": account,
            "Region": region,
            "Encrypted": True
            
        }

        volumes.append(template)

    return volumes

def return_volumes(regions, account, state=None):
    volumes = []

    with ThreadPoolExecutor() as executor:
        threads = []

        for region in regions:
            threads.append(executor.submit(get_volumes, account, region))
    
    for thread in threads:
        response = thread.result()
        if state:
            for volume in response:
                if volume['State'] == state:
                    volumes.append(volume)
            
        else:
            for volume in response:
                volumes.append(volume)
    
    return volumes

@listEBS.route('/ec2/volumes', methods=['GET'], strict_slashes=False)
def list_ebs_volumes_route():
    account_to_scan = request.json.get('account')

    if not account_to_scan:
        return jsonify({
            "error": "account is required"
        }), 400
    
    try:
        state = request.json.get('state')
        if state:
            if state != 'in-use' and state != 'available':
                return jsonify({
                    "error": "state type not available, only 'available' or 'in-use'"
                }), 400
    except Exception as e:
        state = None

    accounts, regions = get_account_and_regions()

    if account_to_scan not in accounts:
        return jsonify({
            'error': f'account {account_to_scan} is not valid.'
        }), 400

    volumes = return_volumes(regions, account_to_scan, state)
    return jsonify(volumes), 200
    
