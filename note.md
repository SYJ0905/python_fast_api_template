# 安裝virtualenv

$ pip install virtualenv

# 在project_folder裡面建立一個叫env的虛擬環境

$ cd project_folder
$ virtualenv env

# 現在應該會有個env/的folder

# 進入env/這個虛擬環境

$ env/Scripts/activate

# 離開env

$ deactivate

# 在env裡面安裝新package (例如Flask)

(env) $ pip install Flask

# 查看已安裝packages

(env) $ pip freeze
Flask==0.12.2

# 保存現在的environment裡所有packages的version到requirement.txt

(env) $ pip freeze > requirement.txt

# 看看requirement.txt

(env) $ cat requirement.txt
Flask==0.12.2

# -------------

# 在另一部電腦重建一模一樣的environment

$ git pull
$ virtualenv env  # 建立env
$ source env/bin/activate

(env) $ pip freeze

# 沒有package

(env) $ pip install -r requirement.txt  # 裝回packages

$ pip freeze
Flask==0.12.2
