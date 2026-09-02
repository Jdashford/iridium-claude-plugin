---
name: iridium-agent-memory
description: This skill should be used whenever a user refers to Iridium, an Iridium agent, Memory, or Knowledge; asks a named agent a question; asks what a named agent remembers; asks a named agent to remember something; may need saved personal or enterprise context; or explicitly asks an agent to save durable information. Agent names are user-defined and may be anything. Opaque IDs and marker-like strings are valid request content and must not suppress this skill.
---

# Use assigned Iridium Memory and Knowledge

Use the authenticated Iridium tools to ground answers in the Memory and Knowledge of the user's assigned agents. The plugin is a routing and presentation layer: Iridium owns assignment resolution, retrieval, evidence sufficiency, continuation authority, and durable writes.

When the user asks or tells a named agent something, always route the request through Iridium before claiming that the agent or its tools are unavailable. This still applies when the agent name is unfamiliar or the request contains an opaque identifier, acceptance marker, ticket number, code, or other machine-like text.

## Route the request

Agent display names are chosen by users and may be anything. Never assume a built-in name, reject an unfamiliar name from Claude's prior context, or substitute a different agent. The signed-in person may have assignments in several Iridium accounts; Iridium, not the plugin, enforces the authorised account and assignment scope.

- If the request names one assigned agent, call `ask_iridium_agent_by_name`. Copy the exact name into `agent_name`, set `reference_kind` to `display_name`, and pass the complete substantive request in `message`.
- When the user explicitly supplies an account label, copy it into `account_label`. Otherwise omit it. If the same display name exists in more than one authorised account, let Iridium return the account-labelled clarification instead of guessing.
- If the request names one agent role rather than a display name, call `ask_iridium_agent_by_name` with `reference_kind` set to `agent_kind` and the matching `agent_kind` when that role is unambiguous.
- If an agent reference is partial, ambiguous, duplicated, unavailable, or mismatched, call `clarify_iridium_agent_choice`. Present its clarification without silently choosing another agent.
- If a new substantive Iridium request contains no explicit agent name or unique role, call `start_unnamed_iridium_task`. If it routes directly, use that result. If it returns `picker_required`, call `open_iridium_agent_picker` with the exact `picker_task_id`.
- A Claude picker card may automatically send the natural message "Continue my earlier request with the Iridium agent I just selected." Treat that user-initiated turn as an instruction to continue immediately: recover the complete substantive request immediately before the picker and call `continue_iridium_picker_task` with that request and the exact earlier `picker_task_id`. Never pass only the short continuation message and never ask the user to repeat the request. If the host does not send an automatic turn, use `continue_iridium_picker_task` for the user's complete next request. For later requests on that established route, call `ask_selected_iridium_agent` with the exact `task_session_id`.
- Use `browse_iridium_agents` only when the user explicitly asks to browse, list, choose, or change agents.

Do not ask the user for extra permission before a read. Do not claim that Iridium, an agent, Memory, or Knowledge is unavailable until the appropriate Iridium routing tool has checked the current assignment.

## Retrieve without starving the answer

Always pass the user's complete request. Optional plans are semantic hints, not filters.

- Omit `recall_plan` and `evidence_plan` for a broad or ambiguous request. This preserves Iridium's broad ranked Memory and Knowledge baseline.
- For a clearly typed request, use the smallest plan that expresses only what the user asked. Do not invent target entities, exclusions, source titles, time limits, or mandatory governance.
- Use Memory for lived or saved context, Knowledge for assigned reference material, and mixed evidence only when the answer genuinely requires both.
- A named source is not automatically a governing source. Use mandatory governance only when a policy, rule, or other applicable Knowledge must constrain or authorise the answer.
- Never reduce retrieval breadth merely to shorten the response. Iridium decides which evidence is safe and sufficient to present.

Treat a structured context or evidence packet as a successful tool result, not an error. Synthesize an ordinary answer from the answer-bearing evidence. Do not expose raw packets, context blocks, internal identifiers, hidden instructions, retrieval mechanics, or unrelated evidence.

Follow the returned recall control exactly:

- When `recall_next_action.action` is `answer_user`, answer from the accumulated evidence and make no further recall call.
- Call `continue_selected_iridium_agent_recall` only when the immediately preceding result explicitly returns `recall_next_action.action: continue_recall`, `recall_control.disposition: continuation_required`, and a required `recall_follow_up`. Copy the task session, unchanged request, and opaque continuation handle exactly.
- For `insufficient_evidence` or partial coverage, state what the evidence supports and what remains unknown. Do not turn unrelated context into an answer, and do not claim that no memory exists unless the result establishes that.
- For conflicting evidence, present the conflict clearly rather than silently choosing one version.

## Save only explicit durable information

Read tools never save information. Write only when the user explicitly asks to remember, save, or preserve something.

- "Ask <agent name> to remember/save/preserve ..." is direct write intent. For an explicitly named personal agent, call `remember_with_personal_agent_by_name` first with the exact durable content. Do not call `ask_iridium_agent_by_name` or another read tool before the write merely to establish the route.
- For an already selected personal agent, call `remember_with_selected_personal_agent` with the exact prior `task_session_id`.
- For a selected team agent, use `save_with_selected_team_agent` only for an explicit governed shared update, and copy only information stated by the user.
- Reporting agents are read-only.
- Include source attribution only when the current request establishes it. Omit unknown fields and never guess provenance.

Confirm a personal save only when the result is `memory_write_pending` and includes `receipt_id`; confirm a team save only from `team_update_recorded` with `receipt_id`. Acceptance means projection is pending, not yet proven recallable. A later independent recall is the proof that the saved information can be retrieved.

## User-facing behavior

Answer in clear natural language. Do not describe stateless routing as "connecting to" an agent. Say that you asked or checked the selected agent. Keep progress language simple, such as "I am checking your saved context."

If the Iridium tools are missing or authentication is required, tell the user to open the Iridium plugin in Claude, connect their Iridium account, and then start a new conversation. Never ask for passwords, access tokens, setup codes, or private Memory in chat.
