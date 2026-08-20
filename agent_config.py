#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件名: agent_config.py
作者: ZZS
项目: LlmProject
创建日期: 2026/2/6
描述: Agent 网络配置文件 - 集中管理所有 Agent 的 URL 和元数据
"""

# Agent 配置字典 - 便于扩展和维护
AGENT_CONFIG = {
    "WeatherQueryAssistant": {
        "url": "http://localhost:5005",
        "description": "天气查询服务",
        "port": 5005,
        "mcp_port": 8002,
        "intents": ["weather"],
        "requires_summarization": True,  # 是否需要结果汇总
    },
    "TicketQueryAssistant": {
        "url": "http://localhost:5006",
        "description": "票务查询服务",
        "port": 5006,
        "mcp_port": 8001,
        "intents": ["flight", "train", "concert"],
        "requires_summarization": True,
    },
    "AttractionRecommendAssistant": {
        "url": "http://localhost:5008",
        "description": "景点推荐服务",
        "port": 5008,
        "mcp_port": 8004,
        "intents": ["attraction"],
        "requires_summarization": False,
    },
}

# 意图到 Agent 的映射 - 用于快速查找
INTENT_TO_AGENT = {
    "weather": "WeatherQueryAssistant",
    "flight": "TicketQueryAssistant",
    "train": "TicketQueryAssistant",
    "concert": "TicketQueryAssistant",
    "attraction": "AttractionRecommendAssistant",
}

# Agent URLs 字典 - 用于 Streamlit session_state
AGENT_URLS = {agent_name: config["url"] for agent_name, config in AGENT_CONFIG.items()}


def get_agent_name_by_intent(intent: str) -> str:
    """
    根据意图获取对应的 Agent 名称
    
    Args:
        intent (str): 用户意图
        
    Returns:
        str: Agent 名称，如果不存在则返回 None
    """
    return INTENT_TO_AGENT.get(intent)


def get_agent_config(agent_name: str) -> dict:
    """
    获取指定 Agent 的配置信息
    
    Args:
        agent_name (str): Agent 名称
        
    Returns:
        dict: Agent 配置信息
    """
    return AGENT_CONFIG.get(agent_name)


def requires_summarization(agent_name: str) -> bool:
    """
    检查指定 Agent 的结果是否需要汇总
    
    Args:
        agent_name (str): Agent 名称
        
    Returns:
        bool: 是否需要汇总
    """
    config = get_agent_config(agent_name)
    return config.get("requires_summarization", False) if config else False


def get_all_agent_urls() -> dict:
    """
    获取所有 Agent 的 URL 映射
    
    Returns:
        dict: {Agent 名称: URL} 的映射
    """
    return AGENT_URLS


def get_all_agents() -> list:
    """
    获取所有已配置的 Agent 名称
    
    Returns:
        list: Agent 名称列表
    """
    return list(AGENT_CONFIG.keys())


if __name__ == "__main__":
    # 测试配置
    print("=== Agent 配置信息 ===")
    print(f"总共配置了 {len(AGENT_CONFIG)} 个 Agent")
    print()
    
    for agent_name, config in AGENT_CONFIG.items():
        print(f"Agent: {agent_name}")
        print(f"  URL: {config['url']}")
        print(f"  描述: {config['description']}")
        print(f"  支持的意图: {config['intents']}")
        print()
    
    print("=== 意图到 Agent 的映射 ===")
    for intent, agent_name in INTENT_TO_AGENT.items():
        print(f"{intent} -> {agent_name}")
