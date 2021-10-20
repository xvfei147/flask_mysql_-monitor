class Logger:
    def __init__(self, log_name, log_file):
        self._logger = logging.getLogger(log_name)
        log_dir = "./logs"
        if os.path.exists(log_dir) is False:
            os.mkdir(log_dir)
        log_filename = log_dir + '/' + log_file
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(filename)s [line:%(lineno)d] %(funcName)s  %(message)s')
        # 往文件中输出
        handler = logging.FileHandler(log_filename,encoding="utf-8")
        # 往文件中输出的格式
        handler.setFormatter(formatter)
        # 往控制台上输出
        sh = logging.StreamHandler()
        # 设置控制台上显示的格式
        sh.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.addHandler(sh)
        self._logger.setLevel(logging.DEBUG)

    def get_logger(self):
        return self._logger

    # def info(self, msg):
    #     if self._logger is not None:
    #         self._logger.info(msg)
    #
    # def exception(self, msg):
    #     if self._logger is not None:
    #         self._logger.exception(msg)
    #
    # def error(self, msg):
    #     if self._logger is not None:
    #         self._logger.error(msg)
    #
    # def debug(self, msg):
    #     if self._logger is not None:
    #         self._logger.de