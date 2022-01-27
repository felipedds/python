import boto3
import csv

aws_management_console = boto3.session.Session(region_name='us-east-1') # Get AWS Management Console
ec2_console_resource = aws_management_console.resource(service_name='ec2', region_name='us-east-1')
count = 1
csv_object = open('ec2-inventory.csv', 'w', newline='')
csv_write = csv.writer(csv_object)
csv_write.writerow(['number', 'instance_id', 'instance_type', 'architecture', 'launch_time', 'private_ip_address'])

for instance in ec2_console_resource.instances.all():
    print(count, instance.instance_id, instance.instance_type, instance.architecture, instance.launch_time.strftime('%Y-%m-%d'), instance.private_ip_address)
    csv_write.writerow([count, instance.instance_id, instance.instance_type, instance.architecture, instance.launch_time.strftime('%Y-%m-%d'), instance.private_ip_address])
    count += 1
csv_object.close()