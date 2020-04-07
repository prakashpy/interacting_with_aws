
# script to get count of files, and some modifications can get me size as well...
import boto3

my_file = []
total_size = 0

s3 = boto3.client('s3')

paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket='your-bucket-name"', Prefix='your/prefix/goes/here')
for page in pages:
    for obj in page['Contents']:
        total_size = total_size + obj['Size']
        my_file.append(obj['Key'])

print("count:", len(my_file), " files")
print("size: ", total_size, " bytes")