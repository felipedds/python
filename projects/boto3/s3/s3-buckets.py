import boto3


user = boto3.client('sts').get_caller_identity().get('Account') # Returns details about the IAM user or role whose credentials are used to call the operation.

def list_buckets(): # List buckets in Amazon S3.
    s3 = boto3.resource('s3')
    for bucket in s3.buckets.all(): 
        print(bucket.name)

def create_bucket(user): # Create buckets in Amazon S3.
    s3 = boto3.resource('s3')
    s3.create_bucket(Bucket=f'my-bucket{user}', CreateBucketConfiguration={'LocationConstraint': 'us-west-1'})
    print('Created with success.')  

def insert_object_bucket(user): # Upload a new file in Amazon S3.
    s3 = boto3.resource('s3')
    data = open('requirements.txt', 'rb') 
    s3.Bucket(f'my-bucket{user}').put_object(Key='requirements.txt', Body=data)
    print('Inserted with success.')


if __name__ == '__main__':
    list_buckets()