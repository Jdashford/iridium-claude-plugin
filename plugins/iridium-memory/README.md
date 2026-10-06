# Iridium Memory

Iridium Memory connects Claude to the Iridium agents assigned to you, and to the Memory and Knowledge each of those agents is authorised to use. Ask a question and Claude answers from what your agent knows. Ask your agent to remember something and it is saved to that agent's Memory.

## What you can do

- Ask your personal agent what it remembers, for example "Ask my agent what we decided about the launch."
- Ask a team agent about shared Knowledge, for example "What does our team agent know about the pricing policy?"
- Save something only when you ask, for example "Ask my agent to remember that the review moved to Tuesday."

Agent names are chosen by each Iridium account, so use the name shown in yours. If you have more than one agent and do not name one, Claude asks you to pick an agent once and uses it for the rest of the conversation.

## Before you start

You need an Iridium account with at least one assigned agent. Your account administrator controls which agents you can reach; connecting Claude does not add agents or change who can use them.

## Set up

1. Install **Iridium Memory** in Claude.
2. Choose **Connect** and sign in with your Iridium account, then approve access.
3. Start a new conversation once the Iridium tools have loaded.

## What this plugin sends, and where

- **One remote server.** The plugin connects Claude to Iridium's MCP server at `https://mcp.iridiumai.co/mcp/v26`, operated by Iridium. It adds no other servers.
- **Sign-in.** You sign in to Iridium through OAuth with PKCE. Claude receives an access token for your Iridium account; it never sees your password or authenticator code.
- **Your requests.** When you ask an agent something, Claude sends your request and the agent you chose to Iridium, and Iridium returns the relevant Memory and Knowledge that agent is authorised to share with you.
- **Saves.** When you explicitly ask an agent to remember something, Claude sends the content you asked to save. Nothing is saved otherwise.
- **Nothing runs on your computer.** The plugin contains one skill (instructions that help Claude use the Iridium tools) and the server address. It has no hooks, scripts, local servers or bundled credentials.

## Privacy

Iridium handles your data under its privacy policy: <https://iridiumai.co/privacy-policy>. Terms of service: <https://iridiumai.co/terms-of-service>.

To remove access, disconnect Iridium in Claude, or revoke the connection from your Iridium account.

## Support

Contact Iridium at <https://iridiumai.co/contact>.

## Licence

Proprietary. Copyright Iridium. You may install and use this plugin with an Iridium account; you may not redistribute or modify it.
