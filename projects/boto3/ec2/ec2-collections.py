import boto3

# Collections of Resouce Objects
aws_management_console = boto3.session.Session(region_name='us-east-1') # Gets AWS Management Console.
ec2_console_resource = aws_management_console.resource(service_name='ec2', region_name='us-east-1')

for instance in ec2_console_resource.instances.all(): # Exhibit all instances EC2.
    print(instance)

for instance in ec2_console_resource.instances.limit(2): # Exhibit only 2 instances EC2.
    print(instance)

filter1 = {'Name': 'instance-type', 'Values': ['t2.micro']}
for instance in ec2_console_resource.instances.filter(Filters=[filter1]): # Exhibit only instances t2.micro.
    print(instance)
