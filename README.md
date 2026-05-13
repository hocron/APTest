# 安全漏洞测试项目

这是一个用于安全测试的示例项目，包含多种常见的安全漏洞，旨在用于安全审计工具的测试和学习。

## 项目结构

```
Test/
├── README.md
├── web_app/
│   ├── user_auth.py
│   └── blog.py
├── admin/
│   └── system_admin.py
├── utils/
│   └── crypto_utils.py
└── data/
    └── data_processor.py
```

## 文件说明

### 1. web_app/user_auth.py - 用户认证模块

**包含的漏洞：**
- **SQL注入漏洞** - `get_user()`, `authenticate()`, `delete_user()` 函数直接拼接SQL查询，没有使用参数化查询
- **硬编码密钥/密码** - `SECRET_KEY` 和 `ADMIN_PASSWORD` 硬编码在源代码中

### 2. admin/system_admin.py - 系统管理模块

**包含的漏洞：**
- **命令注入漏洞** - `ping_host()`, `backup_file()`, `list_files()`, `run_command()` 使用 `shell=True` 直接执行用户输入
- **任意代码执行** - `execute_script()` 使用 `exec()` 执行任意脚本文件

### 3. utils/crypto_utils.py - 加密工具模块

**包含的漏洞：**
- **硬编码敏感信息** - API密钥、数据库密码、AWS凭证直接硬编码
- **弱加密算法** - 使用固定密钥和IV的AES-CBC加密
- **不安全哈希** - 使用MD5哈希密码（MD5已被破解）
- **自制加密** - 使用简单XOR加密存储信用卡号
- **弱令牌生成** - Token生成方式不安全，容易被伪造

### 4. web_app/blog.py - 博客模块

**包含的漏洞：**
- **XSS跨站脚本攻击** - `render_post()`, `display_user_profile()` 直接渲染用户输入到HTML
- **路径遍历/任意文件读取** - `get_config_file()`, `load_template()` 没有对文件名进行验证
- **不安全文件写入** - `save_uploaded_file()` 允许上传任意文件

### 5. data/data_processor.py - 数据处理模块

**包含的漏洞：**
- **不安全反序列化** - `load_data()`, `unsafe_deserialize()` 使用 pickle 反序列化不受信任的数据
- **YAML反序列化漏洞** - `load_yaml_config()` 使用不安全的 yaml.load()
- **任意代码执行** - `eval_expression()`, `execute_code()` 直接调用 eval() 和 exec()
- **恶意类设计** - `User` 类的 `__reduce__` 方法设计用于执行系统命令

## 漏洞类型总结

| 漏洞类型 | 出现位置 |
|---------|---------|
| SQL注入 | web_app/user_auth.py:10,19,28 |
| 命令注入 | admin/system_admin.py:6,10,14,18 |
| 硬编码密钥 | web_app/user_auth.py:4-5; utils/crypto_utils.py:6-9 |
| 弱加密/哈希 | utils/crypto_utils.py:11-32 |
| XSS攻击 | web_app/blog.py:1-8,22-27 |
| 文件访问控制不当 | web_app/blog.py:10-37 |
| 不安全反序列化 | data/data_processor.py:6-36 |
| 任意代码执行 | admin/system_admin.py:21-22; data/data_processor.py:12-24 |

## 注意事项

⚠️ **警告：本项目仅用于安全研究和测试目的，请勿在生产环境中使用！**

所有代码都包含故意设计的安全漏洞，用于：
- 安全审计工具的测试
- 安全开发学习
- 渗透测试练习
