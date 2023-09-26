# 使用官方 MySQL 映像作為基本映像
FROM mysql:8.1.0

# 複製 SQL 初始化腳本到容器內
COPY init.sql /docker-entrypoint-initdb.d/

# 在這裡添加MySQL用戶和權限的設置
# ENV MYSQL_ROOT_PASSWORD=MySQL0905
# ENV MYSQL_USER=myuser
# ENV MYSQL_PASSWORD=mypassword
# ENV MYSQL_DATABASE=mydatabase

# HEALTHCHECK --interval=30s --timeout=10s \
#     CMD mysqladmin ping -h localhost || exit 1

# 啟動MySQL服務並執行初始化SQL腳本
CMD ["docker-entrypoint.sh", "mysqld"]