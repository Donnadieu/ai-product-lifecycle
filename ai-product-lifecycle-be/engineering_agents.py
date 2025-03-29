from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from llm_config import LLMConfig

def run_engineering_crew(prd_input: str) -> str:
    # Get LLM configuration
    llm = LLMConfig()
    config = llm.get_config(temperature=0.4)

    eng1 = AssistantAgent(name="Eng1", system_message="Focus on effort estimation and technical complexity.", **config)
    eng2 = AssistantAgent(name="Eng2", system_message="Focus on tech stack, system design, and integration requirements.", **config)
    eng3 = AssistantAgent(name="Eng3", system_message="Focus on technical risks, bottlenecks, and scalability.", **config)

    user = UserProxyAgent(name="User", human_input_mode="NEVER", **config)
    group = GroupChat(agents=[user, eng1, eng2, eng3], messages=[], max_round=6)
    manager = GroupChatManager(groupchat=group, **config)

    user.initiate_chat(manager, message=f"Based on the following PRD, create a technical engineering plan:\n\n{prd_input}")

    output = []
    for agent in [eng1, eng2, eng3]:
        for msg in agent.chat_messages.values():
            for m in msg:
                if m.get("role") == "assistant" and m.get("content"):
                    output.append(f"### {agent.name}\n{m['content']}")
    return "\n\n".join(output)
