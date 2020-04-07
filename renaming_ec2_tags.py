import urllib
import boto3


def update_ec2_tags(self):
    '''
    a function to update tags of ec2 instance
    Retruns:
        None
    '''
    instance_id = None
    instance_type = None
    try:
        instance_id = urllib.request.urlopen('http://169.254.169.254/latest/meta-data/instance-id',
                                             timeout=5).read().decode()
        instance_type = urllib.request.urlopen('http://169.254.169.254/latest/meta-data/instance-type',
                                               timeout=5).read().decode()

    except Exception as exc:
        print('Could not retrieve instance_id or instance_type. Error:', exc)

    try:
        ec2_client = boto3.client('ec2', region_name='us-east-1')
        response = ec2_client.describe_tags(
            Filters=[{'Name': 'resource-id', 'Values': [instance_id]}]
        )
        tags = response['Tags']
    except Exception as exc:
        print('Could not retrieve tags of instance id {}. Error: exc'.format(instance_id, exc))

    try:
        ec2_resource = boto3.resource('ec2', region_name='us-east-1')  # FIXME region
        ec2_resource.create_tags(
            Resources=[instance_id],
            Tags=[{'Key': 'new_tag_key', 'Value': 'new_tag_value'}]
        )

    except Exception as exc:
        print('Could not create tags of instance id {}. Error: exc'.format(instance_id, exc))

    return
