# Exercise 5: Add Keycloak Authentication to Your MCP Server

In this exercise, you'll add OAuth 2.1 authentication to your store server using [Keycloak](https://www.keycloak.org/), an open-source identity server. After this, only authenticated users can access your server's tools — and the server can identify who is making each request.

- [Step 1: Add Keycloak auth to your server](#step-1-add-keycloak-auth-to-your-server)
- [Step 2: Test the OAuth flow](#step-2-test-the-oauth-flow)
- [Bonus: Make tools user-aware](#bonus-make-tools-user-aware)
- [Further reading](#further-reading)

---

## Step 1: Add Keycloak auth to your server

Your instructor has a Keycloak instance running with a pre-configured realm and test user accounts. You'll connect your store server to it.

**Instructor-provided values:**

| Setting | Value |
| --- | --- |
| Keycloak Realm URL | `________` |
| Audience | `________` |
| Test username | `________` |
| Test password | `________` |

Open your `servers/store_server.py` and make the following changes:

**1. Add the import** at the top of the file:

```python
from fastmcp.server.auth.providers.keycloak import KeycloakAuthProvider
```

**2. Configure the auth provider** (before your tool definitions):

```python
auth = KeycloakAuthProvider(
    realm_url="________",  # TODO: Paste the Keycloak Realm URL from the table above
    base_url="http://localhost:8420",
    required_scopes=["openid", "mcp:access"],
    audience="________",  # TODO: Paste the audience from the table above
)
```

**3. Pass `auth` to your FastMCP constructor:**

```python
mcp = FastMCP("Your Store Name", auth=auth)
```

That's it — three changes. FastMCP handles everything else: the PRM endpoint, the `WWW-Authenticate` header, and the full OAuth 2.1 flow with Keycloak.

---

## Step 2: Test the OAuth flow

Restart your server:

```bash
uv run servers/store_server.py
```

Now connect from your coding agent. In VS Code, your `.vscode/mcp.json` stays the same — the URL doesn't change, but the server will now require authentication.

```json
{
  "servers": {
    "product-store": {
      "type": "http",
      "url": "http://localhost:8420/mcp"
    }
  }
}
```

When you ask Copilot to use a tool on this server:

1. VS Code detects the server requires authentication (it gets a 401 response).
2. A browser window opens to the Keycloak login page.
3. Log in with the test credentials from the table above.
4. Keycloak shows a consent page — click **Allow**.
5. The browser redirects back to VS Code, and the tool call succeeds.

Try asking:

> "Buy a product from the store"

You should see the normal response, but now it went through the full OAuth flow first. Check your server's terminal output — you'll see the 401, the token exchange, and then the authenticated 200.

---

## Bonus: Make tools user-aware

Now that users are authenticated, you can identify who is making each request. This requires adding middleware that extracts the user ID from the OAuth token and makes it available to your tools.

**1. Add these imports:**

```python
from fastmcp import Context
from fastmcp.server.dependencies import get_access_token
from fastmcp.server.middleware import Middleware, MiddlewareContext
```

**2. Add the middleware class** (before your tool definitions):

```python
class UserAuthMiddleware(Middleware):
    def _get_user_id(self):
        token = get_access_token()
        if not (token and hasattr(token, "claims")):
            return None
        return token.claims.get("sub")

    async def on_call_tool(self, context: MiddlewareContext, call_next):
        user_id = self._get_user_id()
        if context.fastmcp_context is not None:
            await context.fastmcp_context.set_state("user_id", user_id)
        return await call_next(context)
```

**3. Wire the middleware into your server:**

```python
mcp = FastMCP("Your Store Name", auth=auth, middleware=[UserAuthMiddleware()])
```

**4. Update `buy_product` to use the user ID:**

If you didn't add `ctx: Context` in Exercise 4, add it now. Then extract and use the user ID:

```python
@mcp.tool
async def buy_product(
    product_name: Annotated[str, "Name of the product to buy"],
    quantity: Annotated[int, "Number of items to buy"],
    ctx: Context,
) -> str:
    """Buy a product from the store, reducing its inventory."""
    user_id = await ctx.get_state("user_id")

    # ... your existing buy logic ...

    return f"User {user_id} bought {quantity}x {product_name} for ${total:.2f}"
```

Restart the server and buy a product — you should see your Keycloak user ID in the response.

---

## Further reading

- [MCP Auth specification](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization) — The full OAuth 2.1 protocol for MCP
- [FastMCP auth providers](https://gofastmcp.com/servers/auth) — Built-in providers for Keycloak, Entra, Auth0, ScaleKit, and more
- [Python + MCP: Authentication session](https://aka.ms/pythonmcp/slides/auth) — Slides covering key-based, OAuth, Keycloak, and Entra auth
- [python-mcp-demos](https://github.com/Azure-Samples/python-mcp-demos) — Full examples with Keycloak and Entra deployment
