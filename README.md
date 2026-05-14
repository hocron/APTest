# 安全漏洞测试项目

包含常见安全漏洞的测试项目，用于CodeQL等安全审计工具检测。

## 项目结构

```
Test/
├── README.md
├── web_app/
│   ├── user_auth.py      # SQL注入
│   └── blog.py           # XSS、文件读取
├── admin/
│   └── system_admin.py   # 命令注入
├── utils/
│   └── crypto_utils.py   # 弱加密、硬编码密钥
└── data/
    └── data_processor.py # 不安全反序列化、eval
```

## 各文件漏洞

| 文件 | 漏洞类型 |
|-----|---------|
| user_auth.py | SQL注入、硬编码密钥 |
| system_admin.py | 命令注入 |
| crypto_utils.py | 弱加密、硬编码密钥 |
| blog.py | XSS、任意文件读取 |
| data_processor.py | 不安全反序列化、eval |

## 运行

```bash
pip install flask cryptography pyyaml
cd web_app && python user_auth.py  # 或其他文件
```

## 注意

⚠️ 仅用于安全研究和测试，请勿在生产环境使用！
