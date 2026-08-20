#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件名: mcp_attraction_server.py
作者: ZZS
项目: LlmProject
创建日期: 2026/2/4
描述: 景点推荐MCP服务器 - 提供景点数据查询工具
"""
import mysql.connector
import json
from datetime import date, datetime, timedelta
from decimal import Decimal
from mcp.server.fastmcp import FastMCP

from SmartVoyage.config import Config
from SmartVoyage.create_logger import logger
from SmartVoyage.utils.format import DateEncoder, default_encoder

conf = Config()


# 景点服务类
class AttractionService:
    """定义景点服务类，封装数据库操作逻辑"""
    
    def __init__(self):
        # 连接数据库
        self.conn = mysql.connector.connect(
            host=conf.host,
            user=conf.user,
            password=conf.password,
            database=conf.database
        )

    def execute_query(self, sql: str) -> str:
        """
        执行SQL查询方法，输入SQL字符串，返回JSON字符串
        
        Args:
            sql (str): SQL查询语句
            
        Returns:
            str: JSON格式的查询结果
        """
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            
            # 格式化结果
            for result in results:
                for key, value in result.items():
                    if isinstance(value, (date, datetime, timedelta, Decimal)):
                        result[key] = default_encoder(value)
            
            # 序列化为JSON
            return json.dumps(
                {"status": "success", "data": results} if results 
                else {"status": "no_data", "message": "未找到景点数据，请确认查询条件。"},
                cls=DateEncoder,
                ensure_ascii=False
            )
        except Exception as e:
            logger.error(f"景点查询错误: {str(e)}")
            return json.dumps(
                {"status": "error", "message": str(e)},
                ensure_ascii=False
            )


# 创建景点推荐MCP服务器
def create_attraction_mcp_server():
    """创建并启动景点推荐MCP服务器"""
    
    # 创建FastMCP实例
    attraction_mcp = FastMCP(
        name="AttractionTools",
        instructions="景点推荐工具，基于景点数据库表提供查询、评价和推荐服务。",
        log_level="ERROR",
        host="127.0.0.1",
        port=8004
    )

    # 实例化景点服务对象
    service = AttractionService()

    @attraction_mcp.tool(
        name="query_attractions",
        description="查询景点数据，输入SQL，如 'SELECT * FROM attractions WHERE city = \"北京\"' 或 'SELECT * FROM attractions WHERE province = \"浙江\" ORDER BY rating DESC LIMIT 10'"
    )
    def query_attractions(sql: str) -> str:
        """
        查询景点信息
        
        Args:
            sql (str): SQL查询语句，支持按城市、省份、评分、类别等筛选
            
        Returns:
            str: JSON格式的景点数据
        """
        logger.info(f"执行景点查询: {sql}")
        return service.execute_query(sql)

    @attraction_mcp.tool(
        name="get_attraction_details",
        description="获取特定景点的详细信息和用户评价，输入景点ID或景点名称"
    )
    def get_attraction_details(attraction_id: int = None, name: str = None) -> str:
        """
        获取景点详细信息
        
        Args:
            attraction_id (int): 景点ID
            name (str): 景点名称
            
        Returns:
            str: JSON格式的景点详细信息
        """
        if attraction_id:
            sql = f"SELECT * FROM attractions WHERE id = {attraction_id}"
        elif name:
            sql = f"SELECT * FROM attractions WHERE name = '{name}'"
        else:
            return json.dumps({"status": "error", "message": "需要提供景点ID或名称"}, ensure_ascii=False)
        
        logger.info(f"获取景点详情: {sql}")
        return service.execute_query(sql)

    @attraction_mcp.tool(
        name="get_top_rated_attractions",
        description="获取指定城市或省份的高评分景点，可指定返回数量和最低评分"
    )
    def get_top_rated_attractions(location: str, limit: int = 10, min_rating: float = 4.0) -> str:
        """
        获取高评分景点
        
        Args:
            location (str): 城市或省份名称
            limit (int): 返回结果数量，默认10
            min_rating (float): 最低评分，默认4.0
            
        Returns:
            str: JSON格式的高评分景点列表
        """
        sql = f"""
        SELECT * FROM attractions 
        WHERE (city = '{location}' OR province = '{location}') 
        AND rating >= {min_rating}
        ORDER BY rating DESC 
        LIMIT {limit}
        """
        logger.info(f"查询高评分景点: {sql}")
        return service.execute_query(sql)

    # 打印服务器信息
    logger.info("=== 景点推荐MCP服务器信息 ===")
    logger.info(f"名称: {attraction_mcp.name}")
    logger.info(f"描述: {attraction_mcp.instructions}")
    logger.info(f"监听地址: http://127.0.0.1:8004")

    # 运行服务器
    try:
        print("景点推荐MCP服务器已启动，请访问 http://127.0.0.1:8004/mcp")
        attraction_mcp.run(transport="streamable-http")
    except Exception as e:
        print(f"景点推荐MCP服务器启动失败: {e}")


if __name__ == "__main__":
    create_attraction_mcp_server()
