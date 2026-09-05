
import asyncio
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from langchain_openai import ChatOpenAI
from python_a2a import AgentCard, AgentSkill, run_server, TaskStatus, TaskState, A2AServer, Message, \
    TextContent, MessageRole, Task

from SmartVoyage.create_logger import logger
from SmartVoyage.config import Config
from SmartVoyage.main_prompts import SmartVoyagePrompts

conf = Config()

# 初始化LLM
llm = ChatOpenAI(
    model=os.environ["LLM_MODEL_NAME"],
    base_url=os.environ["LLM_BASE_URL"],
    api_key=os.environ["LLM_API_KEY"],
    temperature=conf.temperature
)

attraction_sql_prompt = """
你是景点查询助手。请从用户问题中提取城市或省份，生成一条只读的 MySQL SELECT 语句。
表名是 attractions，字段包括 name, province, city, category, description,
opening_hours, ticket_price, rating, suitable_season, accessibility, tips。
优先按 city 或 province 查询，按 rating 降序，最多返回 5 条。
只输出 SQL，不要 Markdown、解释或其他文本。

用户问题：{query}
"""


def get_attraction_info(query: str) -> str:
    """通过景点 MCP 工具查询数据，返回 JSON 文本。"""
    sql = llm.invoke(attraction_sql_prompt.format(query=query)).content.strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()
    if not re.match(r"^select\b", sql, re.IGNORECASE) or re.search(
        r"\b(insert|update|delete|drop|alter|truncate)\b", sql, re.IGNORECASE
    ):
        raise ValueError("景点查询只允许执行 SELECT 语句")

    async def call_mcp():
        async with streamablehttp_client("http://127.0.0.1:8004/mcp") as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool("query_attractions", {"sql": sql})
                return result.content[0].text

    return asyncio.run(call_mcp())

# Agent 卡片定义
agent_card = AgentCard(
    name="AttractionRecommendAssistant",
    description="基于用户偏好生成景点推荐的智能助手",
    url="http://127.0.0.1:5008",
    version="1.0.0",
    capabilities={"streaming": True, "memory": True},
    skills=[
        AgentSkill(
            name="recommend attractions",
            description="根据用户查询推荐相关景点，包括景点描述、游览建议和注意事项",
            examples=["请推荐北京的历史文化景点",
                      "我想去上海，有什么好玩的地方吗",
                      "杭州有哪些适合拍照的景点"]
        )
    ]
)


# 景点推荐服务器类
class AttractionRecommendServer(A2AServer):
    def __init__(self):
        super().__init__(agent_card=agent_card)
        self.llm = llm

    def handle_task(self, task):
        """
        处理景点推荐任务
        
        输入：用户查询（如"推荐北京的景点"）
        处理：使用LLM + 提示工程生成景点推荐
        输出：结构化的景点推荐结果
        """
        try:
            # 1. 提取输入
            content = (task.message or {}).get("content", {})
            query = content.get("text", "") if isinstance(content, dict) else ""
            
            if not query:
                task.status = TaskStatus(
                    state=TaskState.FAILED,
                    message={"role": "agent", "content": {"text": "请提供景点推荐查询"}}
                )
                return task
            
            logger.info(f"景点推荐查询: {query}")
            
            # 2. 先通过 MCP 查询景点数据，再由 LLM 生成推荐
            raw_response = get_attraction_info(query)
            chain = SmartVoyagePrompts.attraction_prompt() | self.llm
            recommendation = chain.invoke(
                {
                    "query": query,
                    "raw_response": raw_response,
                }
            ).content.strip()
            
            logger.info(f"景点推荐结果: {recommendation}")
            
            # 3. 返回结果
            task.artifacts = [{"parts": [{"type": "text", "text": recommendation}]}]
            task.status = TaskStatus(state=TaskState.COMPLETED)
            
            return task
            
        except Exception as e:
            logger.error(f"景点推荐出错: {str(e)}")
            task.status = TaskStatus(
                state=TaskState.FAILED,
                message={"role": "agent", "content": {"text": f"景点推荐失败: {str(e)}"}}
            )
            return task


# 创建并运行服务器
if __name__ == "__main__":
    server = AttractionRecommendServer()
    logger.info("景点推荐Agent服务器启动，监听 http://localhost:5008")
    run_server(server, host="127.0.0.1", port=5008)
