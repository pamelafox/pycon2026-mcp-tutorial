# Exercise 1: MCP Servers and Coding Agents

In this exercise, you'll set up a development environment, connect a coding agent to public MCP servers, and then try an authenticated MCP server.

- [Step 1: Set up your development environment](#step-1-set-up-your-development-environment)
- [Step 2: Set up a coding agent](#step-2-set-up-a-coding-agent)
- [Step 3: Use a public MCP server (no auth)](#step-3-use-a-public-mcp-server-no-auth)
- [Step 4: Use an authenticated MCP server (GitHub)](#step-4-use-an-authenticated-mcp-server-github)

---

## Step 1: Set up your development environment

Pick **one** of the options below to get the tutorial repository open and ready.

### Option A: GitHub Codespaces (recommended)

Everything is pre-configured — no local installs needed. You just need a [GitHub account](https://github.com/).

1. Go to [github.com/pamelafox/pycon2026-mcp-tutorial](https://github.com/pamelafox/pycon2026-mcp-tutorial).
2. Click **Code → Codespaces → Create codespace on main**.
3. Wait for the Codespace to build. Once the editor loads, you're ready to go!

### Option B: VS Code + Dev Containers

This runs the same pre-configured environment locally inside a Docker container.

**Prerequisites:**

- [VS Code](https://code.visualstudio.com/) installed
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) installed in VS Code

**Steps:**

1. Clone the repository:

   ```bash
   git clone https://github.com/pamelafox/pycon2026-mcp-tutorial.git
   ```

2. Open the folder in VS Code:

   ```bash
   code pycon2026-mcp-tutorial
   ```

3. When prompted "Reopen in Container", click **Reopen in Container**. (Or open the Command Palette and run **Dev Containers: Reopen in Container**.)
4. Wait for the container to build. Once the editor reloads, you're ready to go!

### Option C: Local environment

If you prefer to work without Docker or Codespaces, you can set up a local Python environment.

**Prerequisites:**

- [Python 3.12+](https://www.python.org/downloads/) installed
- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed (Python package manager)

**Steps:**

1. Clone the repository:

   ```bash
   git clone https://github.com/pamelafox/pycon2026-mcp-tutorial.git
   cd pycon2026-mcp-tutorial
   ```

2. Install dependencies:

   ```bash
   uv sync
   ```

3. Open the folder in your editor of choice (VS Code, PyCharm, etc.).

### Verify your setup

From the terminal in your environment, run:

```bash
python --version
```

You should see Python 3.12 or later.

---

## Step 2: Set up a coding agent

Pick **one** of the coding agents below. You'll use this agent for the rest of the exercise.

### Option A: GitHub Copilot in VS Code

1. Make sure the [GitHub Copilot extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) is installed (it's pre-installed in Codespaces).
2. Sign in to your GitHub account if prompted.
3. Open the Copilot Chat panel and switch to **Agent** mode.

> **Tip:** If you're using GitHub Codespaces, Copilot is already available in the browser — no extra setup needed.

### Option B: GitHub Copilot CLI

> You need a [GitHub Copilot subscription](https://github.com/features/copilot) for this option.

1. Install GitHub Copilot CLI by following the [installation guide](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/install-copilot-cli).
2. Verify the installation:

   ```bash
   copilot
   ```

### Option C: Claude Code

> You need a [Claude Code](https://code.claude.com/) subscription for this option.

1. Install Claude Code by following the [installation guide](https://code.claude.com/docs/en/overview).
2. Verify the installation:

   ```bash
   claude --version
   ```

For more details on MCP in Claude Code, see the [Claude Code MCP docs](https://code.claude.com/docs/en/mcp).

### Option D: Goose

<!-- TODO: Add Goose instructions — still figuring out MCP server configuration for Goose. -->

Coming soon!

---

## Step 3: Use a public MCP server (no auth)

Now connect your coding agent to a **public MCP server** that requires no authentication. Pick one (or both!) of the servers below:

| Server | MCP Server URL | Description |
| --- | --- | --- |
| [Microsoft Learn](https://learn.microsoft.com/en-us/training/support/mcp) | `https://learn.microsoft.com/api/mcp` | MS Learn documentation |
| [Hugging Face](https://huggingface.co/settings/mcp) | `https://huggingface.co/mcp` | HuggingFace articles and generators |
| [French government](https://github.com/datagouv/datagouv-mcp) | `https://mcp.data.gouv.fr/mcp` | French government data |

Follow the instructions for your agent:

### Copilot in VS Code — public server

1. Open (or create) the file `.vscode/mcp.json` in your workspace and add:

   ```json
   {
     "servers": {
       "microsoft-learn": {
         "type": "http",
         "url": "https://learn.microsoft.com/api/mcp"
       }
     }
   }
   ```

2. In the Copilot Chat panel (Agent mode), click the tools icon (🔧) to confirm the Microsoft Learn tools are listed.
3. Ask a question:

   > What is the Model Context Protocol?

4. Approve the MCP tool call and review the grounded answer.

### Copilot CLI — public server

1. Open your MCP config file:
   - **macOS / Linux:** `~/.copilot/mcp-config.json`
   - **Windows:** `C:\Users\<USERNAME>\.copilot\mcp-config.json`

2. Add (or merge) the following:

   ```json
   {
     "mcpServers": {
       "microsoft-learn": {
         "type": "http",
         "url": "https://learn.microsoft.com/api/mcp"
       }
     }
   }
   ```

3. Query the server:

   ```bash
   copilot -i "What is the Model Context Protocol?"
   ```

### Claude Code — public server

1. Add the server:

   ```bash
   claude mcp add --transport http microsoft-learn https://learn.microsoft.com/api/mcp
   ```

2. Verify it was added:

   ```bash
   claude mcp list
   ```

3. Ask a question:

   ```text
   What is the Model Context Protocol?
   ```

---

## Step 4: Use an authenticated MCP server (GitHub)

The [GitHub MCP server](https://github.com/github/github-mcp-server) requires authentication — your agent will go through an OAuth login flow to access it.

### Copilot in VS Code — GitHub server

1. Add the GitHub MCP server to `.vscode/mcp.json`:

   ```json
   {
     "servers": {
       "microsoft-learn": {
         "type": "http",
         "url": "https://learn.microsoft.com/api/mcp"
       },
       "github": {
         "type": "http",
         "url": "https://api.githubcopilot.com/mcp/"
       }
     }
   }
   ```

2. Click the tools icon (🔧) and confirm the GitHub tools appear. You may be prompted to authenticate — follow the browser login flow.
3. Ask Copilot a question that uses GitHub context:

   > What are the open issues in pamelafox/pycon2026-mcp-tutorial?

### Copilot CLI — GitHub server

1. Add the GitHub server to `~/.copilot/mcp-config.json`:

   ```json
   {
     "mcpServers": {
       "microsoft-learn": {
         "type": "http",
         "url": "https://learn.microsoft.com/api/mcp"
       },
       "github": {
         "type": "http",
         "url": "https://api.githubcopilot.com/mcp/"
       }
     }
   }
   ```

2. Query the server:

   ```bash
   copilot -i "What are the open issues in pamelafox/pycon2026-mcp-tutorial?"
   ```

3. Follow the authentication prompt if required.

### Claude Code — GitHub server

1. Add the GitHub MCP server:

   ```bash
   claude mcp add --transport http github https://api.githubcopilot.com/mcp/
   ```

2. Authenticate when prompted (run `/mcp` inside Claude Code and follow the browser flow).
3. Ask a question:

   ```text
   What are the open issues in pamelafox/pycon2026-mcp-tutorial?
   ```