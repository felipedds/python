import boto3

aws_management_console = boto3.session.Session(region_name='us-east-1') # Get AWS Management Console
ec2_console_resource = aws_management_console.resource(service_name='ec2')

for region in ec2_console_resource.meta.client.describe_regions()['Regions']:
    print(region['RegionName'])
