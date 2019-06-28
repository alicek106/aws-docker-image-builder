import awsutils
import pprint
import paramiko
from env_parser import EnvParser
import time
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class StatusCode:
    STOPPED = 80
    STOPPING = 64
    RUNNING = 16


class AwsEc2Manager:
    client = None
    key_path = None
    ec2_instance_data = None
    ec2_instance_name = None
    ssh_client = None

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

    def __set_ssh_object(self):
        public_ip = self.ec2_instance_data['PublicIpAddress']
        key = paramiko.RSAKey.from_private_key_file(self.key_path)
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(hostname=public_ip, username="ubuntu", pkey=key)

    def start_instance(self):
        # Check whether instance is already running
        if self.ec2_instance_data['State']['Code'] == StatusCode.RUNNING:
            logging.info('EC2 instance is in active.')
            self.__set_ssh_object()
            return

        # It not running, start and wait
        ec2_instance_id = self.ec2_instance_data['InstanceId']
        self.client.start_instances(InstanceIds=[ec2_instance_id])

        for i in range(1, 30):
            time.sleep(1)
            self.__update_instance_data(self.ec2_instance_name)
            if self.ec2_instance_data['State']['Code'] == StatusCode.RUNNING:
                logging.info('EC2 instance is in active. Waiting for 20 seconds for warm-up.')
                time.sleep(20)
                self.__set_ssh_object()
                return
            logging.info('Waiting for starting EC2 instance.. {} tries'.format(i))
        logging.error('Failed to start EC2 instance. Max tries : 30')
        exit(100)

    def stop_instance(self):
        ec2_instance_id = self.ec2_instance_data['InstanceId']
        self.client.stop_instances(InstanceIds=[ec2_instance_id])

    def exec_command(self, command):
        stdin, stdout, stderr = self.ssh_client.exec_command(command)
        stdin.close()
        for line in iter(lambda: stdout.readline(2048), ""):
            print(line, end="")


if __name__ == "__main__":
    # Takes configuration from config.ini
    envParser = EnvParser()
    awsEc2Manager = AwsEc2Manager(envParser.AWS_INSTANCE_NAME,
                                  envParser.EC2_SSH_PRIVATE_KEY)

    # 1. Start EC2 Instance
    awsEc2Manager.start_instance()

    # 2. Git Pull, Build, and Push to Docker Hub.
    logging.info('Cloning Git repository..')
    awsEc2Manager.exec_command('sudo git clone {} /tmp/remote-builder'.format(envParser.GITHUB_URL))

    logging.info('Building Docker image from Github repository..')
    awsEc2Manager.exec_command('sudo docker build /tmp/remote-builder/ -t {}'.format(envParser.DOCKER_IMAGE_NAME))

    logging.info('Checking if valid Docker Hub credential..')
    awsEc2Manager.exec_command('sudo docker login -u {} -p {}'.format(envParser.DOCKER_HUB_USER,
                                                                      envParser.DOCKER_HUB_PASSWORD))

    logging.info('Pushing built Docker image..')
    awsEc2Manager.exec_command('sudo docker push {}'.format(envParser.DOCKER_IMAGE_NAME))
    
    logging.info('Updating deployment...')
    cmd = 'curl "{}:30000?deploymentName={}&newImageName={}"'.format(envParser.IMAGE_UPDATER_ENDPOINT,
        envParser.IMAGE_UPDATE_TARGET_DEPLOYMENT_NAME,
        envParser.DOCKER_IMAGE_NAME)
    logging.info('cmd : {}'.format(cmd))
    awsEc2Manager.exec_command(cmd)
    
    logging.info('Cleaning up..')
    awsEc2Manager.exec_command('sudo rm -rf /tmp/remote-builder')

    # 3. Stop EC2 Instance
    if envParser.STOP_INSTANCE_AFTER_PUSH == "yes":
        logging.info('Stopping EC2 instance...')
        awsEc2Manager.stop_instance()
    else:
        logging.info('EC2 will be still running..')
        pass
