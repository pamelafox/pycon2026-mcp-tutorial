# Python + MCP: Authentication for MCP servers

- **Date:** 2025-12-18
- **Video:** https://www.youtube.com/watch?v=_Redi3ChzFA
- **Slides:** PythonMCP-Authentication.pdf

## Abstract

In our third session of the Python + MCP series, we're exploring the best ways to build authentication layers on top of your MCP servers. That could be as simple as an API key to gate access, but for the servers that provide user-specific data, we need to use an OAuth2-based authentication flow.

MCP authentication is built on top of OAuth2 but with additional requirements like PRM and DCR/CIMD, which can make it difficult to implement fully. In this session, we'll demonstrate the full MCP auth flow, and provide examples that implement MCP Auth on top of Microsoft Entra.

