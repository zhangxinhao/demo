# FastAPI 用户管理样例项目

基于FastAPI和Pydantic的用户CRUD操作演示。

## 项目结构

```
my_fastapi/
├── models.py          # Pydantic用户模型定义
├── main.py           # FastAPI主应用文件
├── requirements.txt  # 项目依赖
└── README.md        # 项目说明
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行应用

```bash
python main.py
```

或者使用uvicorn：

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API文档

启动后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API端点

- `POST /users` - 创建用户
- `GET /users` - 获取所有用户
- `GET /users/{user_id}` - 获取指定用户
- `PUT /users/{user_id}` - 更新用户
- `DELETE /users/{user_id}` - 删除用户

## 模型说明

- **UserCreate**: 创建用户时使用的数据模型
- **UserUpdate**: 更新用户时使用的数据模型  
- **UserResponse**: API响应的用户数据模型
- **User**: 内部完整用户数据模型
