# API Test Framework

一个基于 Python 的 API 自动化测试框架。

## 项目结构

```
qa-apiTest/
├── core/                    # 核心框架层
│   ├── client/             # HTTP 客户端封装
│   ├── assertion/          # 断言封装
│   ├── utils/              # 工具类
│   └── config/             # 配置管理
├── tests/                   # 测试用例层
│   └── test_suites/        # 测试套件
├── monitors/                # 监控脚本层
│   ├── release/            # 发布监控
│   └── crash/              # 崩溃监控
├── config/                  # 配置文件层
│   ├── yaml_files/         # YAML 配置
│   └── json_files/         # JSON 配置
├── libs/                    # 第三方集成
├── tools/                   # 工具脚本
├── web/                     # Web 工具层
└── data/                    # 数据文件层
    ├── logs/               # 日志文件
    └── reports/            # 测试报告
```

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_suites/test_bb_userInfo.py

# 生成 HTML 报告
pytest --html=data/reports/report.html
```

### 运行监控脚本

```bash
# 成就排行监控
python monitors/release/achievement_rank.py

# 礼物排行监控
python monitors/release/gift_rank.py
```

### 压力测试

```bash
# 运行 Locust 压测
python tools/locust_test.py
```

## 主要特性

- ✅ 统一的 HTTP 请求封装
- ✅ 灵活的断言机制
- ✅ 完善的日志系统
- ✅ 配置文件管理
- ✅ 实时监控告警
- ✅ 压力测试支持

## 使用说明

### 添加新测试用例

1. 在 `tests/test_suites/` 目录下创建新的测试文件
2. 使用 `core` 模块提供的工具类编写测试
3. 运行测试验证

### 配置管理

- YAML 配置文件放在 `config/yaml_files/`
- JSON 配置文件放在 `config/json_files/`
- 通过 `core.config.settings` 访问配置

## 技术栈

- **Python 3.x**
- **requests** - HTTP 请求库
- **pytest** - 测试框架
- **PyYAML** - YAML 解析
- **jsonschema** - JSON 校验
- **locust** - 压力测试