import boto3
import time


aws_management_console = boto3.session.Session(region_name='us-east-1') # Get AWS Management Console
ec2_console_resource = aws_management_console.resource(service_name='ec2')
ec2_console_client = aws_management_console.client(service_name='ec2') # EC2 Client Object

def start_instance_ec2(): # Start EC2 Instance
    instance_ec2 = ec2_console_resource.Instance('i-00c991b8f6689871f')
    print('Starting instance.')
    instance_ec2.start()

def verify_instance_ec2(): # Verify EC2 Instance, if is running nothing do, else if instance is stopped so start it.
    while True:
        instance_ec2 = ec2_console_resource.Instance('i-00c991b8f6689871f')
        print(f"The current status of instance is: {instance_ec2.state['Name']}")
        if instance_ec2.state['Name'] == 'running':
            break
        elif instance_ec2.state['Name'] == 'stopped':
            print('Starting instance.')
            instance_ec2.start()
        time.sleep(5)
    print('Now your instance is up and running.')

def start_instance_ec2_waiter(): # Start EC2 Instance and waiting util it's running.
    instance_ec2 = ec2_console_resource.Instance('i-00c991b8f6689871f')
    print('Starting instance.')
    instance_ec2.start()
    instance_ec2.wait_until_running() # Waiter (waits for 200 seconds, 40 check after every 5 seconds)
    print('Now your instance is up and running.')

def start_instance_ec2_waiter_2(): # Start EC2 Instance and waiting util it's running.
    ec2_console_client.start_instances(InstanceIds=['i-00c991b8f6689871f'])
    waiter = ec2_console_client.get_waiter('instance_running')
    waiter.wait(InstanceIds=['i-00c991b8f6689871f'])
    print('Now your instance is up and running.')


if __name__ == '__main__':
    start_instance_ec2_waiter()