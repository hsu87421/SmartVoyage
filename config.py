

import os
from dotenv import load_dotenv

load_dotenv()

# 项目根目录
project_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

# 生产环境
# env = "prod"
# 测试环境
env = "test"
# 开发环境
# env = "dev"
# 预生产环境
# env = "pre_prod"



#定义配置文件
class Config:

    def __init__(self):
        # 数据库配置
        self.host = os.getenv('MYSQL_HOST', 'localhost')
        self.user = os.getenv('MYSQL_USER', 'root')
        self.password = os.getenv('MYSQL_PASSWORD', '')
        self.database = os.getenv('MYSQL_DATABASE', 'travel_rag')

        # 日志配置
        self.log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', 'app.log')

        # 票务查询的12306接口地址
        self.url_123 = ""

        self.intent = {
            "weather":"WeatherQueryAssistant",
            "train":"TicketQueryAssistant",
            "attraction":"AttractionRecommendAssistant"
        }

        self.temperature = 0.1


    def get_mysql_config(self,env):
        """
        返回 .env 中的数据库配置。
        :return:
        """
        return self.host, self.user, self.password, self.database


if __name__ == '__main__':
    print(Config().log_file)
    print(Config().get_mysql_config(env))
