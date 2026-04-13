# PyCon MCP Tutorial

**Title:** Build your first MCP server in Python

**Description:** Model Context Protocol (MCP) is an open standard for providing context to generative AI applications. In this tutorial, you'll build your first MCP server in Python using open‑source SDKs and development tools. We'll begin with a brief overview of MCP concepts and how servers and clients communicate. From there, you'll implement a local MCP server in Python, define tools, and interact with them using AI agents. Once the basics are in place, we'll add essential real‑world features, including authentication. You'll learn how to secure an MCP server using open‑source, OAuth‑compatible authentication providers and understand how authentication fits into the MCP request flow. This tutorial is hands‑on: participants will write and run Python code throughout the session and leave with a working MCP server they can extend after the conference.

| Detail    | Value                       |
|-----------|-----------------------------|
| Language  | en                          |
| Format    | 40% lecture, 60% exercises  |
| Attendees | 80                          |

## Outline

### 1. MCP 101 (30 min)

- MCP clients, servers, and hosts
- Tools, prompts, and resources
- **Exercise 1:** Use popular MCP servers with coding agent of choice

### 2. Agents + MCP (20 min)

- What is an agent framework?
- Using MCP servers as tools
- **Exercise 2:** Code a Python agent (.py) using LangChain, Pydantic-AI, MAF

### 3. Build an MCP Server (45 min)

- FastMCP: `mcp.tool`, `mcp.prompt`, `mcp.resource`
- Running the server over stdio vs HTTP
- Development tools: MCP Inspector and MCPJam
- Breakpoint debugging
- **Exercise 3:** Write, run, and modify your server

### ☕ Break (5+ min)

### 4. Advanced MCP Server Features (20 min)

- Elicitations
- Apps (Prefab)
- Progress
- Background tasks
- **Exercise 4:** Add an advanced feature to your server

### 5. Authenticated MCP Servers (45 min)

- MCP Auth: OAuth 2.1 + PRM + CIMD/DCR
- Open-source IAM: Keycloak
- Wiring Keycloak to an MCP server
- **Exercise 5:** Add Keycloak to your server and submit user data

### 6. Next Steps with MCP (10 min)

- Deployment tips
- Security considerations
- Future learning

## Internet Requirements

### Prep for Tutorial

Developers should not need to download materials ahead of time.

### During Tutorial

1. **Development environment** — I usually give attendees the options to use either GitHub Codespaces (everything set up online) or a local IDE. Codespaces requires internet connectivity, so it may not be ideal if WiFi is sketchy.
2. **Package downloads** — Attendees need connectivity to download packages from PyPI (`fastmcp`, `langchain-ai`, `agent-framework`, etc.).
3. **Cloud LLMs** — Attendees need connectivity to use free cloud-based LLMs to run agents on their MCP servers. I can adjust the tutorial to avoid LLM usage if that poses difficulties. Attendees can also use local LLMs (e.g., Ollama).
4. **Auth server** — Attendees need internet access to my deployed auth server. It could run on the local network off my machine if preferred. Alternatively, attendees could run the auth server themselves, but they'd need to download the image (more bandwidth).

### Fallback Strategy

I can come up with fallback strategies for each requirement. The fallback may involve USB sticks; developer success will depend on whether they have a working Python environment on their machine. Docker would also help.

## TODOs

- Set up an Azure OpenAI proxy server so that I can give people keys
- Set up a server running Ollama? (serverless GPUs?)
- Buy a mobile wifi hotspot? (Gwen may have one)
- Put stuff on USB sticks
- Pin FastMCP version that includes built-in KeycloakAuthProvider (merged in [PR #1937](https://github.com/PrefectHQ/fastmcp/pull/1937))
- Deploy keycloak server to Azure Container Apps, also run it off local network

## Open questions

- Should we move Agents+MCP to the end, so we dont have to worry about LLM setup so early, and get to MCP building earlier? That doesn't flow as well though. We could also just have it be a bonus section, if we dont get to it, thats okay?