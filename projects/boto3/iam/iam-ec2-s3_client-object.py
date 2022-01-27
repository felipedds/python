import boto3

aws_management_console = boto3.session.Session(region_name='us-east-1') # Get AWS Management Console

iam_console_client = aws_management_console.client(service_name='iam', region_name='us-east-1') # IAM Client Object
ec2_console_client = aws_management_console.client(service_name='ec2', region_name='us-east-1') # EC2 Client Object
s3_console_client = aws_management_console.client(service_name='s3', region_name='us-east-1') # S3 Client Object

def list_iam_users(): # List all IAM users using client object
    response_iam = iam_console_client.list_users()
    for user in response_iam['Users']:
        print(user['UserName'], user['UserId'])

def list_ec2_instances(): # List all EC2 instances using client object
    response_ec2 = ec2_console_client.describe_instances()
    for reservation in response_ec2['Reservations']:
        for instance in reservation['Instances']:
            print(instance['InstanceId'])

def list_s3_buckets(): # List all S3 buckets using client object
    response_s3 = s3_console_client.list_buckets()
    for bucket in response_s3['Buckets']:
        print(bucket['Name'])

if __name__ == '__main__':
    print(list_iam_users())
    print(list_ec2_instances())
    print(list_s3_buckets())