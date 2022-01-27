import boto3


def get_users_iam(): # Get IAM Users.
    aws_management_console = boto3.session.Session(region_name='us-east-1') # Get AWS Management Console
    iam_console = aws_management_console.resource('iam') # Get IAM Console
    for user in iam_console.users.all():
        return user.name
        
def get_users_iam2(): # Get IAM Users in other form.
    iam = boto3.resource('iam')
    for user in iam.users.all():
        print(user.name)

def get_details_users_iam(): #  Get IAM Users with resources object.
    aws_management_console = boto3.session.Session(region_name='us-east-1') # Get AWS Management Console
    iam_console = aws_management_console.client(service_name='iam', region_name='us-east-1')
    for user in iam_console.list_users()['Users']:
        return user


if __name__ == '__main__':
    print(get_users_iam())
    print(get_details_users_iam())