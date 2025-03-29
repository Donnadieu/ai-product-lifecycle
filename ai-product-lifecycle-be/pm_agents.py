from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from llm_config import LLMConfig

def run_pm_crew(prd_input: str) -> str:
    # Get LLM configuration
    llm = LLMConfig()
    config = llm.get_config(temperature=0.4)

    pm1 = AssistantAgent(name="PM1", system_message="Focus on feature completeness and end-user goals.", **config)
    pm2 = AssistantAgent(name="PM2", system_message="Focus on business alignment and product vision.", **config)
    pm3 = AssistantAgent(name="PM3", system_message="Focus on edge cases, non-goals, and measurable success metrics.", **config)

    user = UserProxyAgent(name="User", human_input_mode="NEVER", **config)
    group = GroupChat(agents=[user, pm1, pm2, pm3], messages=[], max_round=6)
    manager = GroupChatManager(groupchat=group, **config)

    user.initiate_chat(manager, message=f"Use this input to create a Product Requirements Document (PRD):\n\n{prd_input}")

    output = []
    for agent in [pm1, pm2, pm3]:
        for msg in agent.chat_messages.values():
            for m in msg:
                if m.get("role") == "assistant" and m.get("content"):
                    output.append(f"### {agent.name}\n{m['content']}")
    return "\n\n".join(output)
