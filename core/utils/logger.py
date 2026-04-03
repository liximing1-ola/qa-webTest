"""
日志管理模块

提供统一的日志配置和管理功能
"""
import logging
import os
from logging.handlers import TimedRotatingFileHandler
from core.config.settings import config


# 日志格式定义
LOG_FORMAT = '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'

# 日期格式
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# 日志记录器缓存（避免重复创建）
_logger_cache = {}


class LoggerManager:
    """日志管理类"""

    @staticmethod
    def _ensure_log_directory():
        """确保日志目录存在"""
        if not os.path.exists(config.LOG_PATH):
            os.makedirs(config.LOG_PATH, exist_ok=True)

    @staticmethod
    def _create_formatter():
        """创建日志格式化器"""
        return logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    @staticmethod
    def _create_console_handler(level=logging.ERROR):
        """
        创建控制台输出处理器
        
        :param level: 日志级别
        :return: StreamHandler 对象
        """
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(LoggerManager._create_formatter())
        return handler

    @staticmethod
    def _create_file_handler(log_name, when='midnight', backup_count=7):
        """
        创建文件输出处理器
        
        :param log_name: 日志文件名
        :param when: 日志轮转间隔 ('S', 'M', 'H', 'D', 'W', 'midnight')
        :param backup_count: 备份文件个数
        :return: TimedRotatingFileHandler 对象
        """
        log_file_path = os.path.join(config.LOG_PATH, log_name)

        handler = TimedRotatingFileHandler(
            filename=log_file_path,
            when=when,
            backupCount=backup_count,
            encoding='utf-8'
        )
        handler.setFormatter(LoggerManager._create_formatter())
        return handler

    @staticmethod
    def get_logger(log_name, level=logging.DEBUG, when='midnight', backup_count=7):
        """
        获取日志记录器
        
        使用缓存机制，避免重复创建日志记录器
        
        :param log_name: 日志文件名
        :param level: 日志级别（默认：DEBUG）
        :param when: 日志轮转间隔（默认：每天午夜）
        :param backup_count: 备份文件个数（默认：7个）
        :return: logging.Logger 对象
        """
        # 检查缓存
        if log_name in _logger_cache:
            return _logger_cache[log_name]

        # 确保日志目录存在
        LoggerManager._ensure_log_directory()

        # 创建日志记录器
        logger = logging.getLogger(log_name)
        logger.setLevel(level)

        # 清除已有的处理器（避免重复添加）
        logger.handlers.clear()

        # 添加控制台处理器（仅输出错误）
        console_handler = LoggerManager._create_console_handler(level=logging.ERROR)
        logger.addHandler(console_handler)

        # 添加文件处理器
        file_handler = LoggerManager._create_file_handler(log_name, when, backup_count)
        logger.addHandler(file_handler)

        # 缓存记录器
        _logger_cache[log_name] = logger

        return logger


# 向后兼容的函数接口
def get_log(log_name, level=logging.DEBUG, when='midnight', back_count=7):
    """
    获取日志记录器（向后兼容接口）
    
    参数说明：
    - log_name: 日志文件名
    - level: 日志级别
    - when: 轮转间隔
      * S: 秒
      * M: 分钟
      * H: 小时
      * D: 天
      * W: 周
      * midnight: 每天午夜
    - back_count: 备份文件个数
    
    :return: logging.Logger 对象
    """
    return LoggerManager.get_logger(log_name, level, when, back_count)


if __name__ == '__main__':
    # 测试日志功能
    logger = get_log('test.log')
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
