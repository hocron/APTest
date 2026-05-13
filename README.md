# 安全漏洞测试项目

这是一个用于安全测试的示例项目，包含多种常见的安全漏洞，旨在用于CodeQL等安全审计工具的测试和学习。项目中的代码包含完整的数据流路径，从外部输入到危险操作，便于静态分析工具检测。

## 项目结构

```
Test/
├── README.md
├── web_app/
│   ├── user_auth.py      # SQL注入漏洞
│   └── blog.py           # XSS跨站脚本、文件访问漏洞
├── admin/
│   └── system_admin.py   # 命令注入漏洞
├── utils/
│   └── crypto_utils.py   # 弱加密、硬编码密钥
└── data/
    └── data_processor.py # 不安全反序列化、代码执行漏洞
```

## 文件说明

### 1. web_app/user_auth.py - 用户认证模块

**数据流路径：**
- HTTP请求 (`request.args.get`, `request.get_json()`) → API函数 → SQL查询拼接

**包含的漏洞：**
- **SQL注入漏洞** - `get_user_from_db()`、`authenticate_user()`、`delete_user_from_db()` 函数直接拼接SQL查询
- **硬编码密钥/密码** - `SECRET_KEY` 和 `ADMIN_PASSWORD` 硬编码

**API端点：**
- GET `/api/user?username=<input>`
- POST `/api/login` with `{"username": "...", "password": "..."}`
- DELETE `/api/user/delete?username=<input>`

### 2. admin/system_admin.py - 系统管理模块

**数据流路径：**
- HTTP请求 (`request.args.get`, `request.get_json()`) → API函数 → 系统命令执行

**包含的漏洞：**
- **命令注入漏洞** - `ping_target_host()`、`backup_system_file()`、`list_directory_contents()`、`execute_system_command()` 使用 `shell=True`
- **任意代码执行** - `load_and_execute_script()` 使用 `exec()`

**API端点：**
- GET `/api/system/ping?host=<input>`
- POST `/api/system/backup` with `{"filename": "..."}`
- GET `/api/system/list?dir=<input>`
- POST `/api/system/execute` with `{"command": "..."}`
- POST `/api/system/script` with `{"script_path": "..."}`

### 3. utils/crypto_utils.py - 加密工具模块

**数据流路径：**
- HTTP请求 (`request.get_json()`) → API函数 → 弱加密/哈希操作

**包含的漏洞：**
- **硬编码敏感信息** - API密钥、数据库密码、AWS凭证直接硬编码
- **弱加密算法** - 使用固定密钥和IV的AES-CBC加密
- **不安全哈希** - 使用MD5哈希密码
- **自制加密** - 使用简单XOR加密存储信用卡号
- **弱令牌生成** - Token生成方式不安全

**API端点：**
- POST `/api/crypto/encrypt` with `{"data": "..."}`
- POST `/api/crypto/hash` with `{"password": "..."}`
- POST `/api/crypto/creditcard` with `{"card_number": "..."}`
- POST `/api/crypto/token` with `{"user_id": "..."}`

### 4. web_app/blog.py - 博客模块

**数据流路径：**
- HTTP请求 (`request.args.get`, `request.get_json()`) → API函数 → HTML渲染/文件操作

**包含的漏洞：**
- **XSS跨站脚本攻击** - `render_blog_post()`、`render_user_profile()` 直接渲染用户输入到HTML
- **路径遍历/任意文件读取** - `load_config_file()`、`load_html_template()` 没有路径验证
- **不安全文件写入** - `write_file_to_disk()`、`save_uploaded_file()` 允许任意文件操作

**API端点：**
- POST `/api/blog/post` with `{"title": "...", "content": "..."}`
- GET `/api/blog/render?title=<input>&content=<input>` (返回HTML)
- POST `/api/user/profile` with `{"username": "...", "bio": "..."}`
- GET `/api/config/get?name=<input>`
- GET `/api/template/load?name=<input>`
- POST `/api/file/write` with `{"filename": "...", "content": "..."}`
- GET `/api/file/read?filename=<input>`

### 5. data/data_processor.py - 数据处理模块

**数据流路径：**
- HTTP请求 (`request.get_json()`) → API函数 → 反序列化/代码执行

**包含的漏洞：**
- **不安全反序列化** - `deserialize_pickle()` 使用 pickle 反序列化不受信任数据
- **YAML反序列化漏洞** - `deserialize_yaml()` 使用不安全的 `yaml.load()`
- **任意代码执行** - `evaluate_expression()`、`execute_dynamic_code()` 调用 eval()/exec()
- **恶意类设计** - `User` 类的 `__reduce__` 方法设计用于执行系统命令

**API端点：**
- POST `/api/data/deserialize` with `{"data": "...", "format": "pickle|yaml"}`
- POST `/api/data/eval` with `{"expression": "..."}`
- POST `/api/data/exec` with `{"code": "..."}`
- POST `/api/data/user/save` with `{"name": "...", "email": "..."}`
- POST `/api/data/user/load` with `{"serialized_user": "..."}`

## 漏洞类型总结

| 漏洞类型 | 文件位置 | 数据流路径 |
|---------|---------|-----------|
| SQL注入 | web_app/user_auth.py | HTTP请求 → API → SQL拼接 |
| 命令注入 | admin/system_admin.py | HTTP请求 → API → subprocess/shell |
| 硬编码密钥 | web_app/user_auth.py, utils/crypto_utils.py | 源代码直接包含 |
| 弱加密/哈希 | utils/crypto_utils.py | HTTP请求 → API → 加密函数 |
| XSS攻击 | web_app/blog.py | HTTP请求 → API → HTML渲染 |
| 文件访问控制不当 | web_app/blog.py | HTTP请求 → API → 文件操作 |
| 不安全反序列化 | data/data_processor.py | HTTP请求 → API → pickle.loads |
| 任意代码执行 | data/data_processor.py | HTTP请求 → API → eval/exec |

## 运行方式

每个文件都可以独立运行，支持两种模式：

### 1. Web服务模式
```bash
cd web_app
python user_auth.py
```
然后访问 http://localhost:5000

### 2. CLI模式
```bash
cd web_app
python user_auth.py get admin
python user_auth.py login admin password
```

## CodeQL检测说明

项目设计遵循以下原则以便CodeQL检测：

1. **完整数据流**：从外部输入源（HTTP请求、CLI参数）到危险操作的完整路径
2. **明确的污点来源**：使用 `request.args.get()`, `request.get_json()`, `sys.argv` 等作为污点源
3. **明确的危险操作**：使用 `cursor.execute()`、`subprocess.call()`、`eval()`、`pickle.loads()` 等作为危险操作点
4. **无中间混淆**：数据直接从来源流向危险操作，无复杂转换

## 注意事项

⚠️ **警告：本项目仅用于安全研究和测试目的，请勿在生产环境中使用！**

所有代码都包含故意设计的安全漏洞，用于：
- CodeQL等安全审计工具的测试
- 安全开发学习
- 渗透测试练习

## 依赖安装

```bash
pip install flask cryptography pyyaml
```