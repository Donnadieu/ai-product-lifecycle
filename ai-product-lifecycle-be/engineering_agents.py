from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from llm_config import LLMConfig

def run_engineering_crew(prd_input: str) -> str:
    # Get LLM configuration
    llm = LLMConfig()
    config = llm.get_config(temperature=0.4)

    # Create engineering agents with more focused prompts
    eng1 = AssistantAgent(
        name="Eng1",
        system_message="You are a technical lead focused on effort estimation. Keep responses concise and practical.",
        **config
    )

    eng2 = AssistantAgent(
        name="Eng2",
        system_message="You are a system architect focused on tech stack and design. Keep responses concise and practical.",
        **config
    )

    eng3 = AssistantAgent(
        name="Eng3",
        system_message="You are a DevOps engineer focused on scalability and risks. Keep responses concise and practical.",
        **config
    )

    user = UserProxyAgent(
        name="User",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=3,  # Limit consecutive replies
        **config
    )

    # Create a focused group chat with fewer rounds
    group = GroupChat(
        agents=[user, eng1, eng2, eng3],
        messages=[],
        max_round=3  # Reduce max rounds to prevent getting stuck
    )

    manager = GroupChatManager(
        groupchat=group,
        **config
    )

    # Start with a more structured prompt
    prompt = f"""Based on this PRD, create a technical plan. Focus on:
1. Effort estimation (days/complexity)
2. Tech stack & architecture
3. Key risks & scalability

PRD:
{prd_input}

Keep the discussion focused and practical."""

    # Initiate the chat with a timeout
    try:
        user.initiate_chat(
            manager,
            message=prompt,
            timeout=60  # 60 second timeout
        )
    except TimeoutError:
        return "Error: Engineering discussion timed out. Please try again."
    except Exception as e:
        return f"Error in engineering discussion: {str(e)}"

    # Collect messages from each agent's last response
    output = []
    for agent in [eng1, eng2, eng3]:
        messages = list(agent.chat_messages.values())
        if messages:
            last_message = messages[-1][-1]  # Get the last message from the last conversation
            if isinstance(last_message, dict) and last_message.get("content"):
                output.append(f"### {agent.name}\n{last_message['content']}")
    return "\n\n".join(output)
