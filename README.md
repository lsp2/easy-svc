## Easy-SVC

### 简介

一个在线人声转换的web应用，提供了3个人声音色。

模型使用so-vits-svc-4.1，体积太大不便上传，可参考原项目地址：https://github.com/svc-develop-team/so-vits-svc 自行训练

菜鸡练手项目。

### 安装&运行

1.启动客户端
```
  cd client
  npm install
  npm run dev
```
2.启动服务端

```
  cd server
  pip install -r requirements.txt
  python app.py
```
### 部署

1. 修改以下配置：

1.cilent/vite.config.ts

```
  base: "./",
```
改为：

```
  base: "/static",
```

2.client/src/api/request.ts

```
  baseURL: '/api',
```
改为：

```
  baseURL: '',
```

2. 打包

```
  cd client
  npm run build
```

3. 生成dist目录，将assets放进server/static中，index.html放进server/template中。启动服务端，即可直接访问。

