# 使用官方的Python Docker映像作為基礎映像
FROM python:3.10.11-slim

# 設定工作目錄
WORKDIR /app

# 複製必要的檔案到工作目錄
COPY ./requirements.txt /app/requirements.txt
# 安裝依賴項
RUN pip install --no-cache-dir -r requirements.txt

# 複製必要的檔案到工作目錄
COPY ./src /app/src

# 定義環境變數，用於設置DATABASE_URL
# ENV DATABASE_URL="mysql+pymysql://root:MySQL0905@localhost:3306/message_board"
ENV DATABASE_URL="mysql+pymysql://root:MySQL0905@customdbhost:3306/message_board"

# 暴露 FastAPI 的監聽端口 (預設為8000)
EXPOSE 8000

# 啟動 FastAPI 應用程式
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]