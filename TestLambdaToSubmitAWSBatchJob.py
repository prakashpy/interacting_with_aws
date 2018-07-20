# https://aws.amazon.com/blogs/compute/creating-a-simple-fetch-and-run-aws-batch-job/
import json
import boto3

print('Loading function')

batch = boto3.client('batch')

def lambda_handler(event, context):
    # TODO implement
    try:
        # Submit a Batch Job
        response = batch.submit_job(jobQueue='fetch-and-run-job-queue', 
                                    jobName='ppatel-fetch-run-via-lambda', 
                                    jobDefinition='fetch_and_run',
                                    containerOverrides={'vcpus':1,
                                                        'memory':500,
                                                        'command':['myjob.sh,60'],
                                                        'environment':[{
                                                                            'name':'BATCH_FILE_TYPE',
                                                                            'value':'script'
                                                                        },
                                                                        {
                                                                            'name':'BATCH_FILE_S3_URL',
                                                                            'value':'s3://mytestbucket/myjob.sh'                                                                            
                                                                        }]
                                                        }
                                    )
        # Log response from AWS Batch
        print("Response: " + json.dumps(response, indent=2))
        # Return the jobId
        jobId = response['jobId']
        return 1
    except Exception as e:
        print(e)
        message = 'Error submitting Batch Job'
        print(message)
        raise Exception(message)

