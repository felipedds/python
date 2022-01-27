import boto3
import sys

aws_management_console = boto3.session.Session(region_name='us-east-1') # Get AWS Management Console
ec2_console_resource = aws_management_console.resource(service_name='ec2', region_name='us-east-1') # EC2 Client Resource
ec2_console_client = aws_management_console.client(service_name='ec2', region_name='us-east-1') # EC2 Client Object

while True:
    print('This script performs the following actions on EC2 instance: ')
    print('''
        1. Start
        2. Stop
        3. Terminate
        4. Exit
        ''')
    option = int(input('Enter the option: '))

    if option == 1:
        instance_id = int(input('Input your instance ID: '))
        required_instance = ec2_console_resource.Instance(instance_id)
        print('Start ec2 instance.')
        required_instance.start()
    elif option == 2:
        instance_id = int(input('Input your instance ID: '))
        required_instance = ec2_console_resource.Instance(instance_id)
        print('Stop ec2 instance.')
        required_instance.stop()
    elif option == 3:
        instance_id = int(input('Input your instance ID: '))
        print('Terminate ec2 instance.')
        required_instance.terminate()
    elif option == 4:
        print('Exit system.')
        sys.exit()
    else:
        print('Your option is invalid.')
