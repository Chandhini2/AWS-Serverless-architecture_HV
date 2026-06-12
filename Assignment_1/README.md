# AWS-Serverless-architecture_HV - Assigment 1
This Repository hold multiple assignments
# Assignment 1: Automated Instance Management Using AWS Lambda and Boto3

## Overview

This project demonstrates the automation of Amazon EC2 instance management using AWS Lambda and the Boto3 SDK for Python. The solution automatically starts or stops EC2 instances based on predefined tags, eliminating the need for manual intervention and improving operational efficiency.

---

# Objective

The objective of this assignment is to gain hands-on experience with:

* AWS Lambda
* Amazon EC2
* AWS IAM
* Amazon CloudWatch
* Boto3 (AWS SDK for Python)

The Lambda function identifies EC2 instances based on their tags and performs the required action:

* Stop instances tagged with **Action = Auto-Stop**
* Start instances tagged with **Action = Auto-Start**

---

# Solution Architecture

```text
EC2 Instances
     │
     ▼
Tag-Based Identification
(Action = Auto-Stop / Auto-Start)
     │
     ▼
AWS Lambda Function
     │
     ▼
Boto3 EC2 API Calls
     │
 ┌───┴─────────┐
 ▼             ▼
Stop EC2    Start EC2
     │
     ▼
CloudWatch Logs
```

---

# AWS Services Used

| Service           | Purpose                                  |
| ----------------- | ---------------------------------------- |
| Amazon EC2        | Virtual server instances                 |
| AWS Lambda        | Serverless execution environment         |
| AWS IAM           | Permission management                    |
| Amazon CloudWatch | Monitoring and logging                   |
| Boto3             | Python SDK to interact with AWS services |

---

# Implementation Steps

## Step 1: Create EC2 Instances

Created two EC2 instances using the t3.micro instance type.

### Instance Configuration

| Instance Name  | Tag Key | Tag Value  |
| -------------- | ------- | ---------- |
| EC2 Instance 1 | Action  | Auto-Stop  |
| EC2 Instance 2 | Action  | Auto-Start |

### Screenshot



<img width="940" height="315" alt="image" src="https://github.com/user-attachments/assets/53622a43-be6a-464d-a3bb-817864695928" />



* <img width="940" height="416" alt="image" src="https://github.com/user-attachments/assets/ada605a2-1069-470f-8b07-e094b8d14597" />


Ec2 -2

<img width="940" height="418" alt="image" src="https://github.com/user-attachments/assets/34e52890-29e0-478b-a3e4-c75ff15fd623" />



---

## Step 2: Create IAM Role for Lambda

Created an IAM role to allow Lambda to interact with EC2 resources.

### Permissions Assigned

* AmazonEC2FullAccess

**Note:** This permission was used for assignment purposes. In a production environment, permissions should follow the Principle of Least Privilege.

### Screenshot


<img width="940" height="438" alt="image" src="https://github.com/user-attachments/assets/7f15747f-ab65-4cb9-bc16-637e5aa0938b" />


---

## Step 3: Create AWS Lambda Function

Created a Lambda function using:

* Runtime: Python 3.x
* Execution Role: Lambda EC2 Management Role

### Screenshot

<img width="940" height="444" alt="image" src="https://github.com/user-attachments/assets/b5d82274-b9f6-43eb-a8ea-439a51fabff4" />


---

## Step 4: Develop and Deploy Boto3 Code

The Lambda function performs the following actions:

1. Connects to EC2 using Boto3.
2. Retrieves all instances containing the tag key `Action`.
3. Identifies:

   * Auto-Stop instances
   * Auto-Start instances
4. Stops Auto-Stop instances.
5. Starts Auto-Start instances.
6. Logs affected instance IDs.

### Python Code

```python
import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):

    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag-key',
                'Values': ['Action']
            }
        ]
    )

    auto_stop_instances = []
    auto_start_instances = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']

            for tag in instance.get('Tags', []):
                if tag['Key'] == 'Action' and tag['Value'] == 'Auto-Stop':
                    auto_stop_instances.append(instance_id)

                elif tag['Key'] == 'Action' and tag['Value'] == 'Auto-Start':
                    auto_start_instances.append(instance_id)

    if auto_stop_instances:
        ec2.stop_instances(
            InstanceIds=auto_stop_instances
        )
        print(f"Stopped Instances: {auto_stop_instances}")

    if auto_start_instances:
        ec2.start_instances(
            InstanceIds=auto_start_instances
        )
        print(f"Started Instances: {auto_start_instances}")

    return {
        "statusCode": 200,
        "stopped_instances": auto_stop_instances,
        "started_instances": auto_start_instances
    }
```

### Screenshot

<img width="940" height="403" alt="image" src="https://github.com/user-attachments/assets/8052fb7d-2c6c-43ac-92d4-75d88f5b770d" />


# Testing

## Manual Invocation

The Lambda function was manually executed using the Test feature available in AWS Lambda.

### Expected Result

| Tag Value  | Expected Action       |
| ---------- | --------------------- |
| Auto-Stop  | Instance should stop  |
| Auto-Start | Instance should start |

### Actual Result

The Lambda function executed successfully and returned the following output:

```json
{
  "statusCode": 200,
  "stopped_instances": [
    "i-xxxxxxxxxxxxx"
  ],
  "started_instances": [
    "i-yyyyyyyyyyyyy"
  ]
}
```

### Verification

Verified from the EC2 Console that:

* Auto-Stop tagged instance transitioned to Stopped state.
* Auto-Start tagged instance transitioned to Running state.

### Screenshot

<img width="940" height="266" alt="image" src="https://github.com/user-attachments/assets/456ca3b6-b80d-4b61-89e3-3c2eac20992f" />


---

# CloudWatch Logging Verification

Initially, CloudWatch logs were unavailable due to missing logging permissions.

Error displayed:

```text
Missing permissions

Your function doesn't have permission to write to Amazon CloudWatch Logs.
To view logs, add the AWSLambdaBasicExecutionRole managed policy.
```

---

# Challenge Faced

### Issue

Although the Lambda function executed successfully and managed EC2 instances correctly, CloudWatch logs were not being generated.

### Root Cause

The Lambda execution role did not have permissions to:

* Create Log Groups
* Create Log Streams
* Write Log Events

As a result, CloudWatch could not create log entries.

---

# Solution Implemented

### Step 1

Opened:

Lambda → Configuration → Permissions

### Step 2

Selected the Lambda Execution Role.

### Step 3

Attached the AWS managed policy:

```text
AWSLambdaBasicExecutionRole
```

This policy grants:

```json
{
  "logs:CreateLogGroup",
  "logs:CreateLogStream",
  "logs:PutLogEvents"
}
```

### Step 4

Executed the Lambda function again.

### Result

CloudWatch Log Groups and Log Streams were successfully created and execution logs became visible.

### CloudWatch Navigation Path

```text
Lambda
 └── Function
      └── Monitor
           └── View CloudWatch Logs
                └── Log Group
                     └── Log Stream
```

### Screenshot

Insert Screenshot:

* Missing Permission Error

<img width="940" height="433" alt="image" src="https://github.com/user-attachments/assets/10a726a0-a275-40a6-b8bd-e6e9e5fe542c" />


* IAM Policy Attachment
<img width="940" height="386" alt="image" src="https://github.com/user-attachments/assets/11118e73-b13c-4060-b045-ba841f8534a8" />


* CloudWatch Logs
<img width="940" height="365" alt="image" src="https://github.com/user-attachments/assets/d8903f5e-3934-4818-91b2-92ad7a0de42d" />

---

# Results

Successfully achieved the following:

✅ Created EC2 instances

✅ Tagged instances appropriately

✅ Created IAM role

✅ Developed and deployed Lambda function

✅ Automated EC2 start and stop operations

✅ Verified execution through testing

✅ Configured CloudWatch logging

✅ Verified generated logs

---

# Future Enhancements

The current implementation satisfies the assignment requirements. However, the solution can be improved further:

### 1. Principle of Least Privilege

Instead of using:

```text
AmazonEC2FullAccess
```

Create a custom IAM policy containing only:

* ec2:DescribeInstances
* ec2:StartInstances
* ec2:StopInstances

This improves security.

---

### 2. Automated Scheduling

Integrate Amazon EventBridge to execute the Lambda function automatically on a schedule.

Examples:

* Start instances at 9:00 AM
* Stop instances at 7:00 PM

---

### 3. Enhanced Logging

Implement structured logging using Python's logging module instead of print statements.

Benefits:

* Better troubleshooting
* Easier monitoring
* Improved observability

---

### 4. Notification Integration

Integrate Amazon SNS to send notifications whenever instances are started or stopped.

Example notifications:

* Email Alerts
* SMS Alerts

---

### 5. Multi-Environment Support

Extend the solution to support:

* Development
* Testing
* Production

using environment-specific tags.

---

### 6. Error Handling

Add exception handling to manage:

* Permission errors
* Invalid instance states
* API failures

This improves reliability and maintainability.

---

# Conclusion

This assignment successfully demonstrated the use of AWS Lambda and Boto3 to automate EC2 instance management using tag-based actions. The solution reduced manual effort, validated serverless automation concepts, and provided practical experience with IAM permissions, CloudWatch logging, and AWS infrastructure automation.
