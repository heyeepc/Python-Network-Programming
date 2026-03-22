import requests

session = requests.Session()

# 登录
session.post("https://example.com/login", data={
    "username": "test",
    "password": "123456"
})

# 访问需要登录的页面
res = session.get("https://example.com/profile")

print(res.text)
