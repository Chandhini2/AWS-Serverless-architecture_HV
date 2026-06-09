import boto3

# Initialize EC2 client
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

    # Stop instances tagged Auto-Stop
    if auto_stop_instances:
        ec2.stop_instances(
            InstanceIds=auto_stop_instances
        )
        print(f"Stopped Instances: {auto_stop_instances}")

    # Start instances tagged Auto-Start
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
