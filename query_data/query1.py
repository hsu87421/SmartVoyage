

import mysql.connector
import json
import os
import re
import requests
from datetime import date, datetime, timedelta
from decimal import Decimal
from mcp.server.fastmcp import FastMCP

from SmartVoyage.config import Config
from SmartVoyage.create_logger import logger
from SmartVoyage.utils.format import DateEncoder, default_encoder

conf = Config()


# 票务服务类
class TicketService:  # 定义票务服务类，封装数据库操作逻辑
    def __init__(self):
        self.conn = None

    def _query_train_api(self, sql: str):
        """将火车票 SQL 查询转换为阿里云市场 API 请求。"""
        appcode = os.getenv("TRAIN_API_APPCODE", "").strip()
        if not appcode or appcode.startswith("replace-with-"):
            return None

        # Accept both exact values and wildcard values such as LIKE '%南阳%'.
        value_pattern = r"\s*(?:=|LIKE)\s*(?:['\"])?%?([^'\"%]+?)%?(?:['\"])?(?=\s|$)"
        start = re.search(r"(?:departure_city|departure_station|start)" + value_pattern, sql, re.I)
        end = re.search(r"(?:arrival_city|arrival_station|end)" + value_pattern, sql, re.I)
        travel_date = re.search(r"(?:departure_time|date)\s*(?:=|BETWEEN)\s*['\"]?(\d{4}-\d{2}-\d{2})", sql, re.I)
        if not travel_date:
            travel_date = re.search(r"DATE\s*\(\s*departure_time\s*\)\s*=\s*['\"]?(\d{4}-\d{2}-\d{2})", sql, re.I)
        if not (start and end and travel_date):
            return {"status": "input_required", "message": "火车票查询需要出发城市、到达城市和日期。"}

        # .env stores the complete endpoint; keep a complete fallback for standalone use.
        api_url = os.getenv(
            "TRAIN_API_BASE_URL",
            "https://jisutrainf.market.alicloudapi.com/train/station2s",
        ).strip().rstrip("/")
        try:
            response = requests.get(
                api_url,
                params={
                    "start": start.group(1).strip(),
                    "end": end.group(1).strip(),
                    "date": travel_date.group(1),
                    # station2s accepts 0 for all trains and 1 for high-speed only.
                    "ishigh": "0",
                },
                headers={"Authorization": f"APPCODE {appcode}"},
                timeout=15,
            )
            response.raise_for_status()
            payload = response.json()
            result = payload.get("result", payload.get("data", payload))
            if isinstance(result, dict):
                result = result.get("list", result.get("data", result))
            if isinstance(result, dict):
                result = [result]
            normalized = []
            for item in result if isinstance(result, list) else []:
                # Normalize the station2s response to the fields used by the Agent.
                normalized.append({
                    "departure_city": item.get("station", start.group(1)),
                    "arrival_city": item.get("endstation", end.group(1)),
                    "departure_time": item.get("departuretime", ""),
                    "arrival_time": item.get("arrivaltime", ""),
                    "train_number": item.get("trainno", item.get("trainno12306", "")),
                    "seat_type": item.get("typename", ""),
                    "price": item.get("pricesw", item.get("priceyd", item.get("priceed", ""))),
                    "remaining_seats": item.get("ishigh", ""),
                    "raw": item,
                })
            return {"status": "success", "data": normalized}
        except (requests.RequestException, ValueError) as exc:
            logger.error(f"阿里云火车票接口调用失败: {exc}")
            return {"status": "error", "message": f"火车票接口调用失败: {exc}"}

    # 定义执行SQL查询方法，输入SQL字符串，返回JSON字符串
    def execute_query(self, sql: str) -> str:
        if re.search(r"\btrain_tickets\b", sql, re.I):
            api_result = self._query_train_api(sql)
            if api_result is not None:
                return json.dumps(api_result, ensure_ascii=False)

        try:
            if self.conn is None:
                self.conn = mysql.connector.connect(
                    host=conf.host,
                    user=conf.user,
                    password=conf.password,
                    database=conf.database
                )
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            # 格式化结果
            for result in results:  # 遍历每个结果字典
                for key, value in result.items():
                    if isinstance(value, (date, datetime, timedelta, Decimal)):  # 检查值是否为特殊类型
                        result[key] = default_encoder(value)  # 使用自定义编码器格式化该值
            # 序列化为JSON，如果有结果返回success，否则no_data；使用DateEncoder，非ASCII不转义
            return json.dumps({"status": "success", "data": results} if results else {"status": "no_data",
                                                                                      "message": "未找到票务数据，请确认查询条件。"},
                              cls=DateEncoder, ensure_ascii=False)
        except Exception as e:
            logger.error(f"票务查询错误: {str(e)}")
            # 返回错误JSON响应
            return json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False)
