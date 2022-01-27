import boto3

# Collections of Resouce Objects
aws_management_console = boto3.session.Session(region_name='us-east-1') # Gets AWS Management Console.
ec2_console_resource = aws_management_console.resource(service_name='ec2', region_name='us-east-1')
ec2_console_client = aws_management_console.client(service_name='ec2', region_name='us-east-1') # EC2 Client Object

# Describe volumes and Deleting volumes case don't use it.
for volume in ec2_console_client.describe_volumes()['Volumes']:
    print(volume['VolumeId'], volume['Tags'])
    if volume['State'] == 'available':
        print(f"Deleting {volume['VolumeId']}")
        ec2_console_client.delete_volume(VolumeId=volume['VolumeId'])
print('Deleted all unused volume.')

# Filtering volumes(EBS) that don't are used.
filter_ebs_unused = {'Name': 'status', 'Values':['available']}
for volume in ec2_console_resource.volumes.filter(Filters=[filter_ebs_unused]):
    print(f'VolumeID: {volume.id} - Volume State: {volume.state} - Volume Tag: {volume.tags}')

# Filtering volumes(EBS) that are used.
filter_ebs_inuse = {'Name': 'status', 'Values':['in-use']}
for volume in ec2_console_resource.volumes.filter(Filters=[filter_ebs_inuse]):
    print(f'VolumeID: {volume.id} Volume State: {volume.state} - Volume Tag: {volume.tags}')


