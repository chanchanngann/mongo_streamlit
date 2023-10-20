
# Objective
To implement data pipeline involving MongoDB, AWS and Streamlit.


# Architecture
I divided the architecture into 3 parts.
  - Part 1 - MongoDB server is installed on docker (AWS EC2).
  - Part 2 - Data source is JSON data located in a S3 source bucket. The data will be pushed to MongoDB by using AWS Glue.
  - Part 3 - The data is pulled from MongoDB and visualized on Streamlit Cloud.

![architecture](/architecture.png)

# Steps

## Part 1 - launch MongoDB on EC2

1. Use the attached [CloudFormation template](/ec2_cfn_template_mongodb.yaml) to launch EC2. 
    - S3 access granted to EC2
    - Port 5000 is added in security group inbound rule for MongoDB

2. SSH into EC2
		(let say EC2 public IP = 12.34.56.78)
  
	   ssh -i Downloads/rachel3.pem ec2-user@12.34.56.78

3. Upload & run [mongo_kickoff.sh](/mongo_kickoff.sh) to launch docker and mongoDB server on EC2.

	   scp -i Downloads/rachel3.pem  Downloads/mongo_kickoff.sh ec2-user@12.34.56.78:~/.

__What is being done in ```mongo_kickoff.sh```__
  - install docker
  - pull MongoDB docker image
  - run MongoDB docker container

         sudo docker run --name mongodb -d -e MONGO_INITDB_ROOT_USERNAME=myuser -e MONGO_INITDB_ROOT_PASSWORD=mypassword -p 5000:27017 mongo
  
     - Include DB login info in environment parameter: 
    
           MONGO_INITDB_ROOT_USERNAME = myuser
           MONGO_INITDB_ROOT_PASSWORD = mypassword
  
     - Specify port on docker host to be mapped with: 5000
      
     - The URI to connect with MongoDB will be (let say EC2 public IP = 12.34.56.78):
       
            mongodb://myuser:mypassword@12.34.56.78:5000
	
## Part 2 - Push data to MongoDB

1. Upload [JSON data](/heart_attack.json) to S3 bucket: *s3://<bucket_name>/heart_attack.json*
2. Create secrets at Secret Manager
   - secret name: mongo_secret
   - secret type: Other type of secret (Key/value pairs)
     
         username		myuser
         password		mypassword
         server_addr		12.34.56.78:5000

3. Create IAM role for glue with following permissions granted
	- AWSGlueServiceRole
	- secret_manager_read_policy (*in-line policy*)
	- s3_access_policy (*in-line policy*)
	
4. Create glue job to do the data integration.
   refer to the attach script: [glue_s3_to_mongo.py](/glue_s3_to_mongo.py) 
	
   - language: pyspark
   - version: glue 3.0
   - worker type: G1X
   - #of workers: 2
   - job params:
	
			--source_path	s3://<bucket_name>/heart_attack.json
			--db_name		HealthDB
			--collection_name	HeartAttack
			--secret_name	mongo_secret
			--region_name	ap-northeast-2

5. Review data at MongoDB Client.

   
![mongoDB](/mongoDB.PNG)
  
## Part 3 - Visualize data on streamlit Cloud

*My Streamlit app URL: https://mongo-chel-testing.streamlit.app/

1. Visit streamlit cloud and create a new app.
	- Repository: select this github repo
	- Main file path: Enter [streamlit_app.py](/streamlit_app.py)
	
	* *Note: The Streamlit app URL is linked to [streamlit_app_local_csv.py](/local_testing/streamlit_app_local_csv.py) currently instead since mongoDB server is off*

2. In the app's *Settings* section, add MongoDB secret so that streamlit will be able to pull data from MongoDB.

    	[mongo]
    	host = "12.34.56.78"
    	port = 5000
    	username = "myuser"
    	password = "mypassword"
		
3. Make sure to put [requirements.txt](/requirements.txt) in the github repo so that streamlit will install the Python dependencies accordingly.

![streamlit-app](/streamlit-app.png)

### About the dataset
The data is about heart attack risk given with different attributes.

*Data source: https://www.kaggle.com/datasets/iamsouravbanerjee/heart-attack-prediction-dataset/data*

### *References*
- https://medium.com/towardsdev/guide-to-mongodb-explained-like-youre-15-d977480e0f4e
- https://aws.amazon.com/blogs/big-data/compose-your-etl-jobs-for-mongodb-atlas-with-aws-glue/
- https://docs.aws.amazon.com/glue/latest/dg/connection-mongodb.html
- https://docs.streamlit.io/knowledge-base/tutorials/databases/mongodb
- https://medium.com/@lukas.forst/dashboarding-possibilities-using-python-or-other-solutions-e806f939d5d7
