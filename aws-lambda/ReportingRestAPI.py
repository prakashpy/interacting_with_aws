from botocore.vendored import requests
import json
import boto3

print "Calling lambda function for reporting success to the api"

s3 = boto3.client('s3')


def lambda_handler(event, context):
    # Example of input event json:
    # {
    #   "parameters": [
    #     {
    #       "ob_job_id": "GP-935"
    #     }
    #   ]
    # }

    # Log the received event
    print("Received event: " + json.dumps(event, indent=2))

    Jobid = event['parameters'][0]['job_id']

    if Jobid is None:
        print "Job Id is missing!"
        raise Exception('I failed without jobId!')

    jobId = event["parameters"][0]["job_id"]
    bucket_name = 'my-dev-bucket'
    key_for_config = "jobs/{}/config.json".format(Jobid)

    try:
        data = s3.get_object(Bucket=bucket_name, Key=key_for_config)
        json_data = json.loads(data['Body'].read().decode('utf-8'))
        api_url = json_data['APIEndPointURL']

    except Exception as e:
        print(e)
        raise e

    response_dict = {"JobId": jobId, "Success": "True"}

    try:
        res = requests.post(url=api_url, data=response_dict)
        print res.status_code
        print res.text
    except Exception as e:
        print(e)
        raise e