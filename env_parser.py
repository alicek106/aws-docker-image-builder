import configparser


class EnvParser:
    AWS_INSTANCE_NAME = None
    EC2_SSH_PRIVATE_KEY = None
    GITHUB_URL = None
    DOCKER_IMAGE_NAME = None
    DOCKER_HUB_USER = None
    DOCKER_HUB_PASSWORD = None
    STOP_INSTANCE_AFTER_PUSH = None
    IMAGE_UPDATE_TARGET_DEPLOYMENT_NAME = None
    IMAGE_UPDATER_ENDPOINT = None

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./config.ini')

        self.AWS_INSTANCE_NAME = config['CONFIG']['AWS_INSTANCE_NAME']
        self.EC2_SSH_PRIVATE_KEY = config['CONFIG']['EC2_SSH_PRIVATE_KEY']
        self.GITHUB_URL = config['CONFIG']['GITHUB_URL']
        self.DOCKER_IMAGE_NAME = config['CONFIG']['DOCKER_IMAGE_NAME']
        self.DOCKER_HUB_USER = config['CONFIG']['DOCKER_HUB_USER']
        self.DOCKER_HUB_PASSWORD = config['CONFIG']['DOCKER_HUB_PASSWORD']
        self.STOP_INSTANCE_AFTER_PUSH = config['CONFIG']['STOP_INSTANCE_AFTER_PUSH']
        self.IMAGE_UPDATE_TARGET_DEPLOYMENT_NAME = config['CONFIG']['IMAGE_UPDATE_TARGET_DEPLOYMENT_NAME']
        self.IMAGE_UPDATER_ENDPOINT = config['CONFIG']['IMAGE_UPDATER_ENDPOINT']
