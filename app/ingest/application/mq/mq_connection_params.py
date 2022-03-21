class MqConnectionParams:
    def __init__(self, mq_host, mq_port, mq_user, mq_password) -> None:
        """
        :param mq_host: MQ host to connect
        :type mq_host: str
        :param mq_port: MQ port to connect
        :type mq_port: str
        :param mq_user: MQ user to connect
        :type mq_user: str
        :param mq_password: MQ password to connect
        :type mq_password: str
        """
        self.mq_host = mq_host
        self.mq_port = mq_port
        self.mq_user = mq_user
        self.mq_password = mq_password
