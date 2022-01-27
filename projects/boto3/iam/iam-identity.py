import boto3


aws_management_console = boto3.session.Session(region_name='us-east-1') # Gets AWS Management Console.
sts_console_client = aws_management_console.client(service_name='sts', region_name='us-east-1') # STS Client Object.

def get_iam_identity():
    iam_identity = sts_console_client.get_caller_identity() # Returns details about the IAM identity whose credentials are used to call the API.
    return iam_identity


if __name__ == '__main__':
    print(get_iam_identity()) # Gets various informations about the IAM identity.
    print(get_iam_identity().get('Account')) # Gets the account.

