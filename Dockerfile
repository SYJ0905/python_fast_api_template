# 使用官方的Python Docker映像作為基礎映像
FROM python:3.10.11-slim

# 設定工作目錄
WORKDIR /app

# 安裝需要的套件
RUN apt-get update && apt-get install -y curl

# 複製必要的檔案到工作目錄
COPY ./requirements.txt /app/requirements.txt
# 安裝依賴項
RUN pip install --no-cache-dir -r requirements.txt

# 複製必要的檔案到工作目錄
COPY ./src /app/src

# 将 .env 文件复制到容器中
COPY .env /app/

# 暴露 FastAPI 的監聽端口 (預設為8000)
EXPOSE 8000

# HEALTHCHECK --interval=30s --timeout=10s \
#     CMD curl -f http://localhost:8000/ || exit 1

# 啟動 FastAPI 應用程式
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0"]
# CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]