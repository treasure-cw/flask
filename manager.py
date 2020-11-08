# 导入flask对象创建函数
# 从flask_script导入Manager
from flask_script import Manager
from app import create_app

# app:flask对象
# manager:app管理对象
app = create_app()
manager = Manager(app)

'''
调试程序入口
导入livereload中的Server;
以达到热更新的目的；
'''


@manager.command
def dev():
    from livereload import Server
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url_delay=True)


'''
主程序入口
'''
if __name__ == '__main__':
    manager.run()
