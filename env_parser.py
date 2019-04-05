import configparser


class EnvParser:
    AWS_INSTANCE_NAME = None
    EC2_SSH_PRIVATE_KEY = None
    GITHUB_URL = None
    DOCKER_IMAGE_NAME = None

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./config.ini')

        self.AWS_INSTANCE_NAME = config['CONFIG']['AWS_INSTANCE_NAME']
        self.EC2_SSH_PRIVATE_KEY = config['CONFIG']['EC2_SSH_PRIVATE_KEY']
        self.GITHUB_URL = config['CONFIG']['GITHUB_URL']
        self.DOCKER_IMAGE_NAME = config['CONFIG']['DOCKER_IMAGE_NAME']