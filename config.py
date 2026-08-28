#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件名: config.py
作者: ZZS
项目: LlmProject
创建日期: 2026/1/17
描述: 
"""

import os

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
        # 大模型配置
        self.base_url = 'https://api.siliconflow.cn/v1'
        self.api_key = 'sk-xjpgcjnuhhkgucuvxuvhdbcfmgwlakyjqynshyectvcgifdw'
        self.model_name = 'Qwen/Qwen2.5-72B-Instruct'

        # 数据库配置
        self.host = 'localhost'
        self.user = 'root'
        self.password = '123456'
        self.database = 'travel_rag'

        # 日志配置
        self.log_file = os.path.join(project_root, 'SmartVoyage4', 'logs/app.log')

        # 票务查询的12306接口地址
        self.url_123 = ""

        self.intent = {
            "weather":"WeatherQueryAssistant",
            "flight":"TicketQueryAssistant",
            "train":"TicketQueryAssistant",
            "concert":"TicketQueryAssistant",
            "attraction":"AttractionRecommendAssistant"
        }

        self.temperature = 0.1


    def get_mysql_config(self,env):
        """
        通过不同的环境获取不同的数据库配置
        :return:
        """
        if env == 'prod':
            # 数据库配置 生产
            self.host = 'localhost'
            self.user = 'root'
            self.password = 'root'
            self.database = 'travel_rag'
        elif env == 'dev':
            # 数据库配置 开发
            self.host = 'localhost1'
            self.user = 'root1'
            self.password = 'root1'
            self.database = 'travel_rag'
        elif env == 'test':
            # 数据库配置 测试
            self.host = 'localhost2'
            self.user = 'root2'
            self.password = 'root2'
            self.database = 'travel_rag'
        else:
            # 数据库配置 预生产
            self.host = 'localhost3'
            self.user = 'root3'
            self.password = 'root3'
            self.database = 'travel_rag'

        return self.host, self.user, self.password, self.database


if __name__ == '__main__':
    print(Config().log_file)
    print(Config().get_mysql_config(env))
    # ('localhost', 'root', 'root', 'travel_rag')
    # ('localhost', 'root2', 'root2', 'travel_rag')