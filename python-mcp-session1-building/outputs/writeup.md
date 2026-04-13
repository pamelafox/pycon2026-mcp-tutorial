# Python + MCP: Building servers with FastMCP

This session introduces Model Context Protocol by starting with the integration problem it solves and then building a working Python server with FastMCP. The talk stays practical: it shows how to run a local server in VS Code, how tools, resources, and prompts differ, when to move from stdio to HTTP, how to debug and observe a server, and how the same server can be consumed by agent frameworks. The slides are available at [aka.ms/pythonmcp/slides/servers](https://aka.ms/pythonmcp/slides/servers), and the demo code lives in [aka.ms/python-mcp-demos](https://aka.ms/python-mcp-demos).

## Table of contents

- [Python + MCP series schedule](#python--mcp-series-schedule)
- [Building MCP servers with FastMCP](#building-mcp-servers-with-fastmcp)
- [Today we'll cover...](#today-well-cover)
- [Want to follow along?](#want-to-follow-along)
- [What is MCP?](#what-is-mcp)
- [Before MCP](#before-mcp)
- [Model Context Protocol](#model-context-protocol)
- [After MCP](#after-mcp)
- [Overview of MCP architecture](#overview-of-mcp-architecture)
- [MCP clients](#mcp-clients)
- [VS Code: compliant MCP client](#vs-code-compliant-mcp-client)
- [MCP server components](#mcp-server-components)
- [Build an MCP server in Python](#build-an-mcp-server-in-python)
- [Python MCP frameworks](#python-mcp-frameworks)
- [Why use FastMCP?](#why-use-fastmcp)
- [Running local FastMCP server in VS Code](#running-local-fastmcp-server-in-vs-code)
- [Tool with FastMCP](#tool-with-fastmcp)
- [Resource with FastMCP](#resource-with-fastmcp)
- [Prompt with FastMCP](#prompt-with-fastmcp)
- [MCP transports: STDIO vs. HTTP](#mcp-transports-stdio-vs-http)
- [Serve FastMCP servers over HTTP](#serve-fastmcp-servers-over-http)
- [Development tips for MCP servers](#development-tips-for-mcp-servers)
- [Breakpoint debugging in VS Code](#breakpoint-debugging-in-vs-code)
- [MCP Inspector](#mcp-inspector)
- [Observability with Aspire dashboard](#observability-with-aspire-dashboard)
- [Using AI agents with MCP servers](#using-ai-agents-with-mcp-servers)
- [Agent-framework with local MCP server](#agent-framework-with-local-mcp-server)
- [Langchain v1 with local MCP server](#langchain-v1-with-local-mcp-server)
- [Next steps](#next-steps)
- [Q&A](#qa)

## Python + MCP series schedule

![Series schedule for three Python and MCP sessions](slide_images/slide_1.png)
[Watch from 01:02](https://www.youtube.com/watch?v=_mUuhOwv9PY&t=62s)

This is a three-part series happening Tuesday through Thursday. Today covers the basics of building an MCP server with FastMCP. Tomorrow covers deploying MCP servers into production on Azure with private networking. Thursday covers authentication: key-based access, OAuth-based access, and Entra. All sessions are recorded and available on YouTube. Register for the series at [aka.ms/PythonMCP/series](https://aka.ms/PythonMCP/series) to get notified when each recording goes live.

## Building MCP servers with FastMCP

![Title slide for building MCP servers with FastMCP](slide_images/slide_2.png)
[Watch from 02:11](https://www.youtube.com/watch?v=_mUuhOwv9PY&t=131s)

The slides for this session are available at [aka.ms/pythonmcp/slides/servers](https://aka.ms/pythonmcp/slides/servers). They are freely reusable, including for teaching this material to others. MCP is the biggest new standard of the last six months and has taken the industry by storm.

## Today we'll cover...

![Agenda for MCP concepts server building and tooling](slide_images/slide_3.png)
[Watch from 03:11](https://www.youtube.com/watch?v=_mUuhOwv9PY&t=191s)

Today covers what MCP is, building a basic MCP server with the FastMCP SDK in Python, running that server in VS Code, using tools, resources, and prompts, debugging and inspecting and observing MCP servers with different development tools, and finally pointing AI agents at a local server to see what they can do with it.

## Want to follow along?

![Follow along slide linking to the Python MCP demos repository](slide_images/slide_4.png)
[Watch from 03:43](https://www.youtube.com/watch?v=_mUuhOwv9PY&t=223s)

All of the code samples live in one repository at [aka.ms/python-mcp-demos](https://aka.ms/python-mcp-demos). It can be opened locally, in GitHub Codespaces, forked, or cloned. This same repo is used throughout the entire series and contains a lot of helpful code, so bookmark it as a reference.

## What is MCP?

![Section divider asking what MCP is](slide_images/slide_5.png)
[Watch from 04:16](https://www.youtube.com/watch?v=_mUuhOwv9PY&t=256s)

Time to answer the basic question: what is MCP, and why does the ecosystem need it?

## Before MCP

![Diagram showing an AI app separately integrated with a database Slack and GitHub](slide_images/slide_6.png)
[Watch from 04:23](https://www.youtube.com/watch?v=_mUuhOwv9PY&t=263s)

Before MCP, building generative AI applications like agents, chat apps, and workflows meant building custom integrations for every external service. Connecting to a database required one approach, Slack required another, GitHub required a third. Every time a new application wanted access to the same services, someone had to figure out how to wire them all up again from scratch. This was such a common need that people wanted a standard way to connect applications to services.

## Model Context Protocol

![Definition of Model Context Protocol as an open protocol for tools data and applications](slide_images/slide_7.png)
[Watch from 05:24](https://www.youtube.com/watch?v=_mUuhOwv9PY&t=324s)

Model Context Protocol is a protocol that defines how a model can get context to answer questions and achieve tasks. Anthropic created it just over a year ago as an open protocol originally for Claude Desktop. It became very popular, and as of December 2025 MCP is part of the Agentic AI Foundation under the Linux Foundation, the same organization that maintains Linux as an open operating system. MCP defines how external tools and data sources can be brought into AI applications in a standard way. The protocol homepage is [modelcontextprotocol.io](https://modelcontextprotocol.io/).

## After MCP

![Diagram showing services connecting through MCP instead of direct custom integrations](slide_images/slide_8.png)
[Watch from 06:50](https://www.youtube.com/watch?v=_mUuhOwv9PY&t=410s)

Thanks to MCP, the database exposes itself as an MCP server, Slack exposes itself as an MCP server, and GitHub has an MCP server as well. Any application that understands MCP can act as an MCP client and interface with any of these servers. That has opened up a bigger world of possibilities and made it easier to start plugging things into each other.

## Overview of MCP architecture

![Architecture diagram of MCP hosts clients and servers](slide_images/slide_9.png)
[Watch from 07:32](https://www.youtube.com/watch?v=_mUuhOwv9PY&t=452s)

MCP servers can expose tools, prompts, and resources. Tools are what most people think of: the GitHub MCP server might have tools like "add comment to issue" or "read pull review." Servers can also expose prompts and resources, which are covered later. On the other side, MCP clients connect to servers and sit inside an MCP host. A host is something like Claude Desktop, GitHub Copilot, or ChatGPT. There is a real risk whenever you give more functionality to an agent, especially if the MCP server is authenticated and has access to your data, but there is also a huge benefit. Within an MCP host, a single host can connect to multiple servers using the MCP protocol. The reference architecture is at [modelcontextprotocol.io/docs/learn/architecture](https://modelcontextprotocol.io/docs/learn/architecture).

## MCP clients

![MCP clients slide pointing to the feature support matrix](slide_images/slide_10.png)
[Watch from 10:09](https://www.youtube.com/watch?v=_mUuhOwv9PY&t=609s)

There is a long and growing list of MCP clients on the Model Context Protocol website. The MCP protocol is quite large now with many different parts. Every single client supports tools, because that is what most people think of. But for other aspects like resources, prompts, discovery, sampling, roots, elicitation, and instructions, there is a lot more variability. VS Code with GitHub Copilot has check marks for all of them, meaning it is fully compliant with all aspects of MCP. The feature matrix is linked from [modelcontextprotocol.io/clients#feature-support-matrix](https://modelcontextprotocol.io/clients#feature-support-matrix).

## VS Code: compliant MCP client

![VS Code slide showing installation from the marketplace and usage from Copilot](slide_images/slide_11.png)
[Watch from 12:06](https://www.youtube.com/watch?v=_mUuhOwv9PY&t=726s)

VS Code is generally the first client to adopt new MCP features and is a great developer playground for testing servers. You can install other people's MCP servers from the VS Code extensions marketplace by searching "MCP". The servers in the gallery have been vetted and can be removed if security issues are detected. For example, the Microsoft Learn MCP server can access learn.microsoft.com documentation and provide up-to-date information for Azure and Microsoft technologies. Context7 is another popular one for open-source project documentation.

Once a server is installed, it appears in the Copilot Chat tools menu. One tricky thing: with many MCP servers enabled, the agent has to choose among all the available tools. Sometimes the agent does not realize a particular tool would be useful. If the model is not choosing the right server, you can mention the server by name in your prompt, or try switching models. Some models are better at tool selection than others.

## MCP server components

![Comparison table for tools resources and prompts](slide_images/slide_12.png)
[Watch from 15:35](https://www.youtube.com/watch?v=_mUuhOwv9PY&t=935s)

MCP servers have three component types. Tools are functions the LLM can call and decide when to use depending on the user's request. They can write to databases, call external APIs, modify files, or trigger other logic, and the model controls when they run. Resources are passive data sources that provide read-only access for context, like file contents, database schemas, or API documentation, and the application controls them. Prompts are pre-built instruction templates that tell the model how to work with specific tools and resources, and the user controls them. The server concepts reference is [modelcontextprotocol.io/docs/learn/server-concepts](https://modelcontextprotocol.io/docs/learn/server-concepts).

## Build an MCP server in Python

![Section divider for building an MCP server in Python](slide_images/slide_13.png)
[Watch from 18:00](https://www.youtube.com/watch?v=_mUuhOwv9PY&t=1080s)

Now it is time to actually build an MCP server in Python. Building from scratch by reading and adhering to the raw specification is not recommended. Use one of the popular SDKs instead.

## Python MCP frameworks

![Framework comparison between the official Python SDK and FastMCP](slide_images/slide_14.png)
[Watch from 18:09](https://www.youtube.com/watch?v=_mUuhOwv9PY&t=1089s)

The Python SDK is the official SDK, part of the Model Context Protocol GitHub organization. It stays as close to the specification as possible, and whenever something new lands in the spec it gets added to the SDK. However, the recommended choice is FastMCP. It is a framework built on top of the official SDK, so it has all the same functionality plus a lot more. FastMCP includes integration with Entra and about 15 other auth providers, easier integration with FastAPI, easier deployment to production, logging, and OpenTelemetry support. That is why FastMCP is the framework used in this series.

## Why use FastMCP?

![Feature list for FastMCP including decorators type hints async and metadata](slide_images/slide_15.png)
[Watch from 19:44](https://www.youtube.com/watch?v=_mUuhOwv9PY&t=1184s)

FastMCP lets you write servers in a very Pythonic way. Decorators define tools, prompts, and resources with `@mcp.tool`, `@mcp.prompt`, and `@mcp.resource`. Python type hints automatically generate input and output schemas for LLMs. Both async and sync functions are supported. Tool annotations can mark tools as read-only, idempotent, or destructive for clearer behavior. Multiple transports, both stdio and HTTP, work without changing server code.

## Running local FastMCP server in VS Code

![Steps for configuring and enabling a local FastMCP server in VS Code](slide_images/slide_16.png)
[Watch from 20:34](https://www.youtube.com/watch?v=_mUuhOwv9PY&t=1234s)

To run a local server, open the `.vscode/mcp.json` configuration file. This file lists the available server configurations, and there is also an "Add Server" button that walks through a wizard. The server entry specifies a type of `stdio`, a command of `uv`, and arguments to run the Python file. `uv` is a tool for running Python programs and managing environments, and it is very popular in the MCP community. Click start, and VS Code runs that command automatically. The output pane confirms that the server is running with its advertised tools and prompts. Then go to Copilot Chat, open the tools menu, and check the server on so Copilot knows it can use those tools.

## Tool with FastMCP

![Code example of a FastMCP tool with annotated parameters](slide_images/slide_17.png)
[Watch from 23:22](https://www.youtube.com/watch?v=_mUuhOwv9PY&t=1402s)

This expense tracking server stores expenses in a CSV file locally. To define a tool, use the `@mcp.tool` decorator on a function. The function signature has a name and typed arguments. Each argument uses `Annotated` types to provide the name, the Python type, and a human-readable description. For example, the date parameter is `Annotated[date, "Date of the expense in YYYY-MM-DD format"]`, amount is `Annotated[float, "Positive numeric amount of the expense"]`, and category is an `Enum` that constrains values to a fixed set. All of this information gets sent to the LLM used by GitHub Copilot, which sees the argument names, types, and descriptions but never the implementation. Getting specific with annotations is important because it directly affects how well the model selects the tool and fills in arguments. The agent can also ask follow-up questions if it has any doubt about the arguments.

VS Code asks for permission before running MCP server actions, with options to allow per session, per workspace, or always. After allowing, the tool runs, and the expense is added to the CSV file. To improve accuracy over time, monitor the requests that come in, see what the model gets right and what it messes up, and refine the annotations and argument descriptions accordingly.

## Resource with FastMCP

![Code example of a FastMCP resource that returns expense data](slide_images/slide_18.png)
[Watch from 30:28](https://www.youtube.com/watch?v=_mUuhOwv9PY&t=1828s)

A resource uses the `@mcp.resource` decorator with a URI like `"resource://expenses"`. This one reads the entire CSV and returns it as text. Resources act like static documents that can be attached to a conversation. In VS Code, click the "Add Context" button (the paper clip icon), select MCP Resources, and choose the resource. It gets attached to the conversation, and then you can ask questions about it like "analyze my expenses and tell me what's the biggest expense."

In practice, getting your expenses probably should be a tool rather than a resource, because tools are what agents can discover and invoke on their own. Resources are useful when there is documentation or reference material that users might want to manually add. Most of the time, expose everything at least as a tool, and optionally add resources for power users who know how to attach them.

## Prompt with FastMCP

![Code example of a FastMCP prompt for spending analysis](slide_images/slide_19.png)
[Watch from 32:42](https://www.youtube.com/watch?v=_mUuhOwv9PY&t=1962s)

Prompts are helpful when users commonly do the same things over and over with a server. To define one, use `@mcp.prompt` and return a template string. This one analyzes spending patterns with optional category and date range filters. To trigger a prompt in VS Code, type `/` in chat and select from the available prompts exposed by MCP servers. It pops up asking for optional argument values, and then sends the prompt to the model. Prompts can be templatized, so they accept parameters and build the final instruction string dynamically.

## MCP transports: STDIO vs. HTTP

![Comparison table for STDIO and HTTP transports](slide_images/slide_20.png)
[Watch from 36:12](https://www.youtube.com/watch?v=_mUuhOwv9PY&t=2172s)

The server so far was running using standard input/output (stdio). Many servers run locally this way: Python servers typically use `uv run` and JavaScript/TypeScript servers use `npx`. Anything you can run with a command in a terminal is an stdio server. This is convenient because VS Code launches it on demand, but it means the local environment must have the right tools installed and paths configured. Path issues with `uv` or `npx` can become a real barrier.

HTTP servers run as a network service accessible through a URL. The client does not need to know how the server started or what language it was written in. HTTP supports multiple simultaneous clients and is scalable, with bidirectional streaming. The tradeoff is needing network and host/port configuration. For production, HTTP is the recommended transport. FastMCP's transport guidance is at [gofastmcp.com/deployment/running-server](https://gofastmcp.com/deployment/running-server).

## Serve FastMCP servers over HTTP

![HTTP configuration example for a FastMCP server](slide_images/slide_21.png)
[Watch from 38:23](https://www.youtube.com/watch?v=_mUuhOwv9PY&t=2303s)

Switching to HTTP requires changing the last line of the server code to `mcp.run(transport="http", host="0.0.0.0", port=8000)`. The transport options are `stdio`, `sse` (deprecated), and `streamable_http`. Start the server explicitly with `uv run basic_mcp_http.py` and it begins listening in HTTP mode on port 8000.

In `mcp.json`, the HTTP entry uses `"type": "http"` and `"url": "http://localhost:8000/mcp"`. All VS Code knows is that there is an MCP endpoint at that URL. It does not know the implementation language or how the server started. After starting the HTTP server and enabling it in Copilot Chat, the JSON MCP requests flowing over the server are visible in the terminal logs.

## Development tips for MCP servers

![Section divider for development tips](slide_images/slide_22.png)
[Watch from 42:52](https://www.youtube.com/watch?v=_mUuhOwv9PY&t=2572s)

With the basic server working over both transports, the focus shifts to the developer tools that help when building and testing MCP servers locally.

## Breakpoint debugging in VS Code

![VS Code debugging setup for a FastMCP server using debugpy](slide_images/slide_23.png)
[Watch from 42:59](https://www.youtube.com/watch?v=_mUuhOwv9PY&t=2579s)

VS Code can do breakpoint debugging with MCP servers. Set up an `mcp.json` entry that runs the server through `debugpy` by adding `"--", "python", "-m", "debugpy", "--listen", "0.0.0.0:5678"` to the args. Add a matching launch configuration in `launch.json` to attach the debugger. Once attached, set breakpoints on any line, and when a tool call comes in, the debugger stops there. You can see the values of all arguments, inspect variables, watch them change, and step line by line.

Set this up before you actually need it. When you are dealing with a real bug, you will be too frustrated to configure debugging infrastructure from scratch. Get the `launch.json` and `mcp.json` entries working while everything is fine, so the debugger is ready when you need it. The VS Code guidance is at [code.visualstudio.com/docs/copilot/customization/mcp-servers#_debug-an-mcp-server](https://code.visualstudio.com/docs/copilot/customization/mcp-servers#_debug-an-mcp-server).

## MCP Inspector

![MCP Inspector UI showing tool testing for a local server](slide_images/slide_24.png)
[Watch from 46:47](https://www.youtube.com/watch?v=_mUuhOwv9PY&t=2807s)

MCP Inspector is a developer tool for testing and debugging MCP servers without going through an agent. Run it with `npx @modelcontextprotocol/inspector`, connect it to a running server, and it shows all the server's capabilities: resources, prompts, tools, sampling, elicitations, roots, auth, and metadata. Select a tool, fill in the arguments manually, and run it to see the result. The history shows all tool calls made during the session.

This is useful when developing a server and you want to interact with it directly instead of going through GitHub Copilot and an LLM. It removes the extra agent layer and makes it easier to tell whether an issue is in the server or in the model's tool selection. MCP Inspector works best locally due to CORS issues in GitHub Codespaces. The project is at [github.com/modelcontextprotocol/inspector](https://github.com/modelcontextprotocol/inspector).

## Observability with Aspire dashboard

![Aspire dashboard showing structured logs for an MCP server](slide_images/slide_25.png)
[Watch from 49:04](https://www.youtube.com/watch?v=_mUuhOwv9PY&t=2944s)

Observability means being able to see what servers are doing: the requests that come in, the logs, the calls to other services. It is usually a combination of logs, traces, and metrics, implemented through the OpenTelemetry standard. Observability is critical in production, which the next session covers in depth, but it can also be set up locally.

The Aspire dashboard runs in Docker with `docker run --rm -d -p 18888:18888 -p 4317:18889 --name aspire-dashboard mcr.microsoft.com/dotnet/aspire-dashboard:latest`. Set the `OTEL_EXPORTER_OTLP_ENDPOINT` environment variable to point the server at this dashboard. The server code checks for that variable and, if set, configures OpenTelemetry middleware to export traces. The Aspire dashboard then shows structured logs with messages like "MCP Expenses server starting" and attached OpenTelemetry traces with metadata from each tool call.

## Using AI agents with MCP servers

![Section divider for using AI agents with MCP servers](slide_images/slide_26.png)
[Watch from 53:23](https://www.youtube.com/watch?v=_mUuhOwv9PY&t=3203s)

So far, GitHub Copilot has been the AI agent consuming the MCP server. That is great and might be why you are building your server, but many people build MCP servers so they can use them as part of agent orchestration and agentic workflows. Within a company, you might expose functionality as an MCP server and then have multiple agents interacting with that server.

## Agent-framework with local MCP server

![Code example using Microsoft agent framework with a local MCP server](slide_images/slide_27.png)
[Watch from 54:11](https://www.youtube.com/watch?v=_mUuhOwv9PY&t=3251s)

Microsoft agent-framework is the newest AI agent framework and the successor to AutoGen and Semantic Kernel. If you were using either of those, you should move to agent-framework, which has everything from both plus more, including built-in MCP support. The example connects to the local MCP server with `MCPStreamableHTTPTool` and creates a `ChatAgent` with a system prompt and access to those MCP server tools.

The agent needs an LLM for deciding which tools to call. The code supports Azure, GitHub Models, OpenAI, or Ollama, as long as the model supports tool calling. When the agent runs a query like "yesterday I bought a laptop for $1200 using my visa," it decides on the arguments and calls the tool. If the model is unsure, it can ask the user for clarification before logging the expense. You can give an agent access to multiple MCP servers and each server can have multiple tools. The risk is that the more tool definitions you send, the more likely the LLM is to get confused, so keep names and descriptions unambiguous.

## Langchain v1 with local MCP server

![Code example using LangChain v1 with a local MCP server](slide_images/slide_28.png)
[Watch from 58:08](https://www.youtube.com/watch?v=_mUuhOwv9PY&t=3488s)

LangChain v1 is the latest version of LangChain, centered around agents and tools. The code creates a `MultiServerMCPClient` configured with the MCP endpoint URL and transport type. It fetches the available tools, creates an agent with those tools, and sends a query. All modern agent frameworks have built-in MCP support where the framework acts as an MCP client, connects to servers, and passes the server's tools to the agent. The same MCP server works across multiple frameworks without any changes.

## Next steps

![Closing slide with recordings office hours and next sessions](slide_images/slide_29.png)
[Watch from 59:10](https://www.youtube.com/watch?v=_mUuhOwv9PY&t=3550s)

The recording is available on YouTube immediately after the session. All resources, slides, recordings, and code samples are linked from [aka.ms/pythonmcp/resources](https://aka.ms/pythonmcp/resources). Office hours run on Discord after every session at [aka.ms/pythonai/oh](https://aka.ms/pythonai/oh). The MCP for Beginners tutorial at [aka.ms/mcp-for-beginners](https://aka.ms/mcp-for-beginners) is another way to learn after the series.

## Q&A

### Why use VS Code instead of another MCP client

VS Code with GitHub Copilot has check marks for every part of the MCP specification. Most other clients only support tools. That means VS Code is the best developer playground when building a server and testing features like resources, prompts, sampling, and elicitation. It also provides permission prompts, tool inspection, server lifecycle controls, and debugging support.

### When should a resource become a tool instead

Most of the time, expose everything at least as a tool. Resources are not exposed to the agent, so the agent cannot decide to fetch them on its own. Once data needs to be user-specific or requires parameters, it should be a tool. The expense data in this demo was turned into a tool for the later sessions once user authentication was added.

### Why prefer HTTP over stdio for production

Stdio requires the local environment to have the right commands, paths, and runtimes configured. That is a real barrier. HTTP separates the server from the client, supports multiple concurrent clients, and lets the client connect to a server written in any language. For production, HTTP is the recommended transport.

### Can one agent use many MCP servers at once

Yes. You can give an agent access to multiple MCP servers, and each server can have multiple tools. You can send hundreds of tool definitions to an LLM as long as it has a big enough context window. The tradeoff is that the more tools you send, the more likely the LLM is to get confused. Keep tool names and descriptions unambiguous so tool selection stays reliable.