from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

def run_stakeholder_crew(product_idea: str, context: dict = {}) -> str:
    config = {
        "llm_config": {
            "model": "gpt-4",
            "temperature": 0.4,
            "api_key": context.get("openai_api_key") or "YOUR_API_KEY"
        }
    }

    # Define specialized stakeholder agents
    marketing = AssistantAgent(
        name="MarketingAI",
        system_message="You represent marketing. Translate product ideas into customer-driven value propositions.",
        **config
    )

    sales = AssistantAgent(
        name="SalesAI",
        system_message="You represent sales. Focus on objections, user pains, and opportunities from the field.",
        **config
    )

    support = AssistantAgent(
        name="SupportAI",
        system_message="You represent customer support. Think in terms of user feedback, usability gaps, and frustrations.",
        **config
    )

    user = UserProxyAgent(name="User", human_input_mode="NEVER", **config)

    group = GroupChat(
        agents=[user, marketing, sales, support],
        messages=[],
        max_round=8
    )

    manager = GroupChatManager(groupchat=group, **config)

    user.initiate_chat(manager, message=f"""Here's a product idea:\n\n{product_idea}\n\nYour task: Work together to generate structured business requirements. Include personas, pain points, and feature ideas.""")

    # Extract final output from all agents
    outputs = []
    for agent in [marketing, sales, support]:
        for msg in agent.chat_messages.values():
            for m in msg:
                if m.get("role") == "assistant" and m.get("content"):
                    outputs.append(f"### {agent.name}\n{m['content']}")

    return "\n\n".join(outputs)
