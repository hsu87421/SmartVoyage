#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件名: attraction_server.py
作者: ZZS
项目: LlmProject
创建日期: 2026/2/6
描述: 景点推荐Agent服务器 - A2A服务
"""
import asyncio
import uuid
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from python_a2a import AgentCard, AgentSkill, run_server, TaskStatus, TaskState, A2AServer, Message, \
    TextContent, MessageRole, Task

from SmartVoyage.create_logger import logger
from SmartVoyage.config import Config
from SmartVoyage.main_prompts import SmartVoyagePrompts

conf = Config()

# 初始化LLM
llm = ChatOpenAI(
    model=conf.model_name,
    base_url=conf.base_url,
    api_key=conf.api_key,
    temperature=conf.temperature
)

# Agent 卡片定义
agent_card = AgentCard(
    name="AttractionRecommendAssistant",
    description="基于用户偏好生成景点推荐的智能助手",
    url="http://localhost:5008",
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
            
            # 2. 调用LLM生成推荐
            chain = SmartVoyagePrompts.attraction_prompt() | self.llm
            recommendation = chain.invoke({"query": query}).content.strip()
            
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
