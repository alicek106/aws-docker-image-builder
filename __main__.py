import awsutils
import pprint
import paramiko
from env_parser import EnvParser


class StatusCode:
    STOPPED = 80
    STOPPING = 64
    RUNNING = 16


class AwsEc2Manager:
    client = None
    key_path = None
    ec2_instance_data = None
    ec2_instance_name = None

    def __init__(self, ec2_instance_name, key_path):
        session = awsutils.get_session('ap-northeast-2')
        self.client = session.client('ec2')
        self.ec2_instance_name = ec2_instance_name
        self.key_path = key_path
        self.__update_instance_data(ec2_instance_name)

        if self.ec2_instance_data['State']['Code'] != StatusCode.RUNNING and \
                self.ec2_instance_data['State']['Code'] != StatusCode.STOPPED:
            pprint.pprint('Instance is stopping or staring. Try again after few seconds.')
            exit(100)

    def __update_instance_data(self, instance_name):
        instance_data = self.client.describe_instances(
            Filters=[
                {'Name': 'tag:Name', 'Values': [instance_name]}
            ]
        )
        self.ec2_instance_data = instance_data['Reservations'][0]['Instances'][0]

    def start_instance(self):
        ec2_instance_id = self.ec2_instance_data['InstanceId']
        self.client.start_instances(InstanceIds=[ec2_instance_id])

    def stop_instance(self):
        ec2_instance_id = self.ec2_instance_data['InstanceId']
        self.client.stop_instances(InstanceIds=[ec2_instance_id])

    def exec_command(self, command):
        self.__update_instance_data(self.ec2_instance_name)
        public_ip = self.ec2_instance_data['PublicIpAddress']

        key = paramiko.RSAKey.from_private_key_file(self.key_path)
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=public_ip, username="ubuntu", pkey=key)

        stdin, stdout, stderr = ssh_client.exec_command(command)
        stdin.close()
        for line in iter(lambda: stdout.readline(2048), ""):
            print(line, end="")

        ssh_client.close()


if __name__ == "__main__":
    envParser = EnvParser()
    awsEc2Manager = AwsEc2Manager(envParser.AWS_INSTANCE_NAME,
                                  envParser.EC2_SSH_PRIVATE_KEY)
    # awsEc2Manager.start_instance()
    # awsEc2Manager.exec_command('sudo apt update'.format(envParser.GITHUB_URL))
    # Git Pull, Build, and Push to Docker Hub.

    # awsEc2Manager.stop_instance()