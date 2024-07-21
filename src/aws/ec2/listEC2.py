from flask import Blueprint, jsonify, request
from concurrent.futures import ThreadPoolExecutor
from environments.config import get_account_and_regions

import string, random

listEC2 = Blueprint('listEC2', __name__)

def generate_random_dates(len, resource):
    if resource == 'InstanceId':
        characters = string.ascii_letters + string.digits
        return 'id-' + ''.join(random.choice(characters) for _ in range(len))
    elif resource == 'InstanceType':
        types = ["c5a.xlarge", "t3a.large", "m6a.large"]
        return random.choice(types)
    elif resource == 'State':
        states = ['running', 'stopped']
        return random.choice(states)
    else:
        characters = string.ascii_letters + string.digits
        return 'ec2-' + ''.join(random.choice(characters) for _ in range(len))
    
def generate_ip():
    return f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

def get_instances(account, region):
    instances = []

    for i in range(random.randint(2,8)):
                
        template = {
            "InstanceId": generate_random_dates(10, 'InstanceId'),
            "State": generate_random_dates(5, 'State'),
            "PrivateIpAddress": generate_ip(),
            "InstanceType": generate_random_dates(5, 'InstanceType'),
            "Region": region,
            "Name": generate_random_dates(5, 'Name'),
            "Account": account
        }

        instances.append(template)
    
    return instances
                
def return_instances(regions, account, state=None):
    instances = []

    with ThreadPoolExecutor() as executor:
        threads = []

        for region in regions:
            threads.append(executor.submit(get_instances, account, region))
    
    for thread in threads:
        response = thread.result()
        if state:
            for instance in response:
                if instance['State'] == state.lower():
                    instances.append(instance)
        else:
            for instance in response:
                instances.append(instance)
    
    return instances

@listEC2.route('/ec2/instances', methods=['GET'], strict_slashes=False)
def list_ec2_instances_route():
    account_to_scan = request.json.get('account')

    try:
        state = request.json.get('state')
        if state:
            if state != 'running' and state != 'stopped':
                return jsonify({
                    "error": "state type not available, only 'running' or 'stopped'"
                }), 400
    except Exception as e:
        state = None

    accounts, regions = get_account_and_regions()
    if account_to_scan not in accounts:
        return jsonify({
            'error': f'account {account_to_scan} is not valid.'
        }),400


    if not account_to_scan:
        return jsonify({
            "error": "account is required"
        }), 400
    else:
        instances = return_instances(regions, account_to_scan, state)
        return jsonify(instances), 200