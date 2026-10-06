# Set up Iridium Memory in Claude

1. Install **Iridium Memory** in Claude.
2. Open its connector and choose **Connect**.
3. Sign in with the Iridium account that holds your agent assignments and approve access.
4. Start a new Claude conversation after the tools finish loading.

Try a natural request such as:

- "Ask my personal agent what it remembers about my role."
- "Ask Project Desk what our latest agreed actions were."
- "What does my Iridium agent know about our product?"

You can also choose an agent directly with the skill command, for example:

`/iridium-agent-memory use [exact agent name]: [your request]`

An explicit agent name bypasses the picker. Without one, Claude asks you to choose an agent once and keeps that choice for the conversation. Ask Claude to reopen the picker or address another agent by name whenever you want to switch.

Agent names are set by each user. Use the exact name shown in the person's Iridium account; the plugin does not require a fixed agent name.

If Claude asks to connect again, open the Iridium Memory connector settings and complete Iridium sign-in there. Never paste a password or access token into chat.
