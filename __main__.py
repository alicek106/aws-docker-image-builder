import awsutils
import pprint


class StatusCode:
    STOPPED = 80
    STOPPING = 64
    RUNNING = 16


class AwsEc2Manager:
    client = None
    ec2_instance_data = None

    def __init__(self, ec2_instance_name):
        session = awsutils.get_session('ap-northeast-2')
        self.client = session.client('ec2')
        self.ec2_instance_data = self.__get_instance_data(ec2_instance_name)
        if self.ec2_instance_data['State']['Code'] != StatusCode.RUNNING and \
                self.ec2_instance_data['State']['Code'] != StatusCode.STOPPED:
            pprint.pprint('Instance is stopping or staring. Try again after few seconds.')
            exit(100)

    def __get_instance_data(self, instance_name):
        instance_data = self.client.describe_instances(
            Filters=[
                {'Name': 'tag:Name', 'Values': [instance_name]}
            ]
        )
        return instance_data['Reservations'][0]['Instances'][0]

    def start_instance(self):
        ec2_instance_id = self.ec2_instance_data['InstanceId']
        self.client.start_instances(InstanceIds=[ec2_instance_id])

    def stop_instance(self):
        ec2_instance_id = self.ec2_instance_data['InstanceId']
        self.client.stop_instances(InstanceIds=[ec2_instance_id])


if __name__ == "__main__":
    awsEc2Manager = AwsEc2Manager('Test')
    awsEc2Manager.start_instance()
    # Git Pull, Build, and Push to Docker Hub.
    awsEc2Manager.stop_instance()