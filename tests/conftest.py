# -*- coding: utf-8 -*-
"""
pytest 配置文件
"""
import pytest
import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def pytest_configure(config):
    """
    pytest 配置钩子
    """
    # 注册自定义标记
    config.addinivalue_line(
        "markers", "smoke: marks test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: marks test as regression test"
    )


@pytest.fixture(scope="session")
def setup_config():
    """
    全局配置 fixture
    """
    from core.config.settings import config
    return config


@pytest.fixture(scope="function")
def setup_teardown():
    """
    每个测试用例的 setup/teardown
    """
    # Setup
    yield
    # Teardown
    pass
