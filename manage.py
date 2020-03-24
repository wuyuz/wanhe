# coding: utf-8

from flask_migrate import MigrateCommand
from wanhe import create_app
from flask_script import Manager

app = create_app()
manager = Manager(app=app)

manager.add_command('db',MigrateCommand)  # 新增脚本命令，用于迁移数据

if __name__ == "__main__":
    manager.run()