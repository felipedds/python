import boto3

aws_management_console = boto3.session.Session(region_name='us-east-1') # Get AWS Management Console
iam_console_resource = aws_management_console.resource(service_name='iam', region_name='us-east-1')
ec2_console_resource = aws_management_console.resource(service_name='ec2', region_name='us-east-1')
s3_console_resource = aws_management_console.resource(service_name='s3', region_name='us-east-1')

def list_iam_users(): # List all IAM users using resource object
    for user in iam_console_resource.users.all():
        print(user.user_name)

def list_ec2_instances(): # List all EC2 instances using resource object
    for instance in ec2_console_resource.instances.all():
        print(instance.instanceid)

def list_s3_buckets(): # List all S3 buckets using resource object
    for bucket in s3_console_resource.buckets.all():
        print(bucket.name)

if __name__ == '__main__':
    print(list_iam_users())
    print(list_ec2_instances())
    print(list_s3_buckets())