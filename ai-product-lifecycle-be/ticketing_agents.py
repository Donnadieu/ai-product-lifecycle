from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

def run_ticketing_crew(plan_input: str, context: dict = {}) -> str:
    config = {
        "llm_config": {
            "model": "gpt-4",
            "temperature": 0.4,
            "api_key": context.get("openai_api_key") or "YOUR_API_KEY"
        }
    }

    pm = AssistantAgent(name="PM", system_message="Generate functional user stories and group them by feature.", **config)
    tech = AssistantAgent(name="TechLead", system_message="For each story, generate developer subtasks and architecture notes.", **config)
    qa = AssistantAgent(name="QA", system_message="Add test cases and edge case coverage for all user stories.", **config)

    user = UserProxyAgent(name="User", human_input_mode="NEVER", **config)
    group = GroupChat(agents=[user, pm, tech, qa], messages=[], max_round=6)
    manager = GroupChatManager(groupchat=group, **config)

    user.initiate_chat(manager, message=f"Use this engineering plan to generate Jira-style tasks, user stories, subtasks, and testing notes:\n\n{plan_input}")

    output = []
    for agent in [pm, tech, qa]:
        for msg in agent.chat_messages.values():
            for m in msg:
                if m.get("role") == "assistant" and m.get("content"):
                    output.append(f"### {agent.name}\n{m['content']}")
    return "\n\n".join(output)
