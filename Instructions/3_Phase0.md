#### EHR Data

- Download data from following link
- https://www.kaggle.com/datasets/isaacritharson/mimic-iv-cleaned-medical-transcripts
- save it in data folder in project root directory.

#### EC2 Instance

- Must have and awd account
- Create a security group. Inbound rules(ssh and PostgresSql) connect only from MY IP, and other rule(Postgresql) as well. 
- Create an ec2 instance and attach that security group
- EC2 Attributes: ec2 instance with 4GB ram and 20GB storage
- Attach ec2 instance to that security group
- Why 20GB?: Linux and postgressql and other softwares we need to install etc

- Create and Launch the EC2 instance.

- We will use Elastic IP (Single IP address for my EC2 Instance so it should not change.)
- Create Elastic IP. then Associate it with our ec2 instance through actions button.
- Why Elastic IP: So that after each restart of the service our public IP remains same.
- Note down that public ip in your environment, we need to connect  through it.

#### Installations:

- Install PostgresSql
- Connect the elastic IP with local system and do the data Ingestion.

- All about how to connect and install guide is inside AWD-test-FWD-Database folder.

<hr />

#### Create schema

- In AWS-test-FWD-Database folder, there are command to connect to ssh and install run postgresql. do it.
- Create Schema
- CSV from data folder we need to convert -> save into EC2 Database instance
- Then we will test
- Run the scripts 01_... and 02_... in this phase to save that data once data is save verify it. that's it for phase 0 

Hopefully everything is completed.
