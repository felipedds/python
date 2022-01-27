import boto3

aws_management_console = boto3.session.Session(region_name='us-east-1') # Get AWS Management Console
ec2_console_resource = aws_management_console.resource(service_name='ec2', region_name='us-east-1')

for snapshot in ec2_console_resource.snapshots.all():
    print(snapshot)

size = {'Name':'volume-size', 'Values':['8']}
for snapshot in ec2_console_resource.snapshots.filter(Filters=[size]):
    print(snapshot)