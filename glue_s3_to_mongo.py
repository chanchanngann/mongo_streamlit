import sys
import json
import boto3
from botocore.exceptions import ClientError

###################GLUE import##############
from awsglue.job import Job
from awsglue.transforms import *
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from awsglue.dynamicframe import DynamicFrame
from pyspark.context import SparkContext

#retreive desired job parameters 
args = getResolvedOptions(sys.argv, ['JOB_NAME','source_path','db_name','collection_name','secret_name','region_name'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

################### Load Secret ##############
def get_secret():

    secret_name = args['secret_name']
    region_name = args['region_name']

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']
    secrets_json = json.loads(secret)
    return (secrets_json['username'], secrets_json['password'], secrets_json['server_addr'])

user_name, password, server_addr = get_secret()
print("loaded secrets.")

################### Load data from S3 ##############

path = args['source_path']
ds = glueContext.create_dynamic_frame_from_options(\
    connection_type = "s3", \
    connection_options={"paths": [path]}, \
    format="json", \
    format_options={}, \
    transformation_ctx = ""\
    )

print("pulled data from s3.")
################### Write data to MongoDB ##############
uri = f"mongodb://{server_addr}"

mongo_options = {
    "uri": uri,
    "database":args['db_name'],
    "collection": args['collection_name'],   
    "username": user_name,   
    "password": password  
}

glueContext.write_dynamic_frame.from_options(\
    ds, \
    connection_type="mongodb", \
    connection_options=mongo_options\
    )

print("written to MongoDB.")