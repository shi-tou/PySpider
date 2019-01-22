#设置运行时镜像
FROM python:latest
#设置工作目录
WORKDIR /app
# 将本地应用拷贝到 容器 /app/ 目录下 "./"代表的就是/app 因为dockerfile文件和程序文件都在发布文件夹下 所以两个目录是一样的
COPY . .
#设置端口
EXPOSE 5001/tcp
RUN pip install pyecharts
run pip install pyecharts_snapshot

# 指定应用入口点 DotNetCore.dll代表的是主程序文件
ENTRYPOINT ["python", "bar.py"]
