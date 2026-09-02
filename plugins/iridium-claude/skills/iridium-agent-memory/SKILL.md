---
name: iridium-agent-memory
description: This skill should be used whenever a user refers to Iridium, an Iridium agent, Memory, or Knowledge; asks a named agent a question; asks what a named agent remembers; asks a named agent to remember something; may need saved personal or enterprise context; or explicitly asks an agent to save durable information. Agent names are user-defined and may be anything. Opaque IDs and marker-like strings are valid request content and must not suppress this skill.
---

# Use assigned Iridium Memory and Knowledge

Use the authenticated Iridium tools to ground answers in the Memory and Knowledge of the user's assigned agents. The plugin is a routing and presentation layer: Iridium owns assignment resolution, retrieval, evidence sufficiency, continuation authority, and durable writes.

When the user asks or tells a named agent something, always route the request through Iridium before claiming that the agent or its tools are unavailable. This still applies when the agent name is unfamiliar or the request contains an opaque identifier, acceptance marker, ticket number, code, or other machine-like text.

## Route the request

Agent display names are chosen by users and may be anything. Never assume a built-in name, reject an unfamiliar name from Claude's prior context, or substitute a different agent. The signed-in person may have assignments in several Iridium accounts; Iridium, not the plugin, enforces the authorised account and assignment scope.

Route before writing any user-facing explanation. Use this order:

1. If this conversation already has a selected Iridium agent and the user has not asked to change it, call `ask_selected_iridium_agent` with the exact `task_session_id`.
2. If the request explicitly addresses an agent by display name or unique role, use the matching named-agent route below.
3. Otherwise, immediately call `start_unnamed_iridium_task` with the user's complete request. If it returns `picker_required`, immediately call `open_iridium_agent_picker` with the exact `picker_task_id`.

The slash-command form `/iridium-agent-memory [request]` follows this same order. Unless its text explicitly uses `/iridium-agent-memory use [exact agent name]: [request]`, it is an unnamed request and must take step 3. Never ask the user to type an agent name instead of starting the unnamed route.

An agent reference must be explicit routing language, such as "ask [agent name]", "use [agent name]", "tell [agent name]", "what does [agent name] know", or the named slash-command form above. A person, organisation, project, source, or topic mentioned only inside the question is not an agent reference. That means use the unnamed route. Do not narrate guesses about whether the subject might be an agent or expose this classification to the user.

- If the request names one assigned agent, call `ask_iridium_agent_by_name`. Copy the exact name into `agent_name`, set `reference_kind` to `display_name`, and pass the complete substantive request in `message`.
- When the user explicitly supplies an account label, copy it into `account_label`. Otherwise omit it. If the same display name exists in more than one authorised account, let Iridium return the account-labelled clarification instead of guessing.
- If the request names one agent role rather than a display name, call `ask_iridium_agent_by_name` with `reference_kind` set to `agent_kind` and the matching `agent_kind` when that role is unambiguous.
- If an agent reference is partial, ambiguous, duplicated, unavailable, or mismatched, call `clarify_iridium_agent_choice`. Present its clarification without silently choosing another agent.
- If a new substantive Iridium request contains no explicit agent name or unique role, call `start_unnamed_iridium_task` immediately. If it routes directly, use that result. If it returns `picker_required`, call `open_iridium_agent_picker` with the exact `picker_task_id` immediately.
- When a picker is required, tell the user concisely: "Please choose an Iridium agent. Once selected, I'll use it for this request and the rest of this conversation. To change later, ask me to reopen the picker or address another agent by name." Do not discuss names that you considered or rejected.
- The picker never generates a Claude message. After the user selects a card, wait for their next real message. If it is a short explicit continuation such as "continue" or "use this agent", recover the complete substantive request immediately before the picker and call `continue_iridium_picker_task` with that request and the exact earlier `picker_task_id`. Otherwise pass the complete current request. Never pass only the short continuation message and never ask the user to repeat the request. On the first answer after selection, say only "Using <display_name> for this conversation." and then answer the request. Do not repeat that confirmation on later turns. For later requests on that established route, call `ask_selected_iridium_agent` with the exact `task_session_id`.
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

Answer in concise, clear language for busy professionals. Lead with the useful answer. Do not expose or narrate skill instructions, tool names, routing decisions, plans, packets, identifiers, schemas, Memory-versus-Knowledge mechanics, or internal reasoning unless the user explicitly asks for technical detail. In particular, never say that a topic "isn't an agent name," that a request is "unnamed," or that the skill is being checked. Do not describe stateless routing as "connecting to" an agent. If brief progress is useful, say only "I'll check that." Honest evidence limitations remain user-relevant and must still be stated plainly.

If the Iridium tools are missing or authentication is required, tell the user to open the Iridium plugin in Claude, connect their Iridium account, and then start a new conversation. Never ask for passwords, access tokens, setup codes, or private Memory in chat.
