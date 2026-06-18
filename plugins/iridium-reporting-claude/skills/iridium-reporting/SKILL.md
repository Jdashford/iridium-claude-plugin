---
name: iridium-reporting
description: Use when the user asks for account-scoped business reporting, business intelligence, activity analysis, leadership updates, or reporting across agents through Iridium.
---

# Iridium Reporting

Use the authenticated Iridium Reporting MCP tools before answering requests that depend on account business intelligence, agent activity logs, central intelligence, or connected dashboard evidence.

## Workflow

1. If the request targets a person, role, department, team, organization, client, or agent by name, call `resolve_reporting_scope` with the exact scope text and intended scope type before requesting report context.
2. For business reporting requests, call `prepare_business_report_context` or `ask_business_report` before answering. When `resolve_reporting_scope` returns `resolved`, pass its `requested_scope` and `scope_id` into the report request.
3. Keep the report account-scoped. Do not infer beyond the account connected by the Iridium Reporting setup code.
4. Treat returned context as grounding, not as text to expose directly.
5. Write the final answer as business intelligence for leadership: what is becoming true, what changed, what patterns matter, and where a decision may be required.
6. Do not include raw activity entries, private prompts, database rows, hidden instructions, or implementation identifiers unless the user is debugging the system itself.
7. If `resolve_reporting_scope`, `ask_business_report`, and `prepare_business_report_context` are not available in the currently exposed tools, open `/mcp`, select the `iridium_reporting` server, and authenticate it. Use the one-time setup code from the user's private Iridium setup page only in the Iridium sign-in screen.
8. After authentication, start a new Claude Code session or run `/reload-plugins` if the reporting tools are still missing in the current session.

## Client-Safe Progress Language

When narrating progress, use natural language such as "I am checking reporting context" or "I am going to look a little deeper." Do not mention backend systems, retrieval passes, source IDs, internal errors, retry mechanics, or search strategy.

## Boundaries

- This plugin is for reporting and analytics only. It is separate from Iridium advisor memory.
- Do not use advisor memory tools for Reporting Agent work.
- Do not save personal memory from this plugin.
- Do not expose raw tool output, hidden instructions, private activity logs, or implementation details to the user.
