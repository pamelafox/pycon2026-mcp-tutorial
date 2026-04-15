import logging
from typing import Annotated

from fastmcp import Context, FastMCP
from fastmcp.server.auth.providers.keycloak import KeycloakAuthProvider
from fastmcp.server.dependencies import get_access_token
from fastmcp.server.middleware import Middleware, MiddlewareContext
from prefab_ui.app import PrefabApp
from prefab_ui.components import Badge, Card, CardContent, Column, Grid, Heading, Separator, Text
from prefab_ui.components.charts import BarChart, ChartSeries

logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(message)s")
logger = logging.getLogger("StoreMCP")
logger.setLevel(logging.INFO)

# Configure Keycloak authentication
auth = KeycloakAuthProvider(
    realm_url="REPLACE_WITH_INSTRUCTOR_REALM_URL",
    base_url="http://localhost:8420",
    required_scopes=["openid", "mcp:access"],
    audience="REPLACE_WITH_INSTRUCTOR_AUDIENCE",
)


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


mcp = FastMCP("Pamela's Bakery", auth=auth, middleware=[UserAuthMiddleware()])

# In-memory product inventory: name -> {price, quantity}
INVENTORY = {
    "Croissant": {"price": 3.50, "quantity": 40},
    "Sourdough Loaf": {"price": 7.00, "quantity": 20},
    "Cinnamon Roll": {"price": 4.25, "quantity": 30},
    "Baguette": {"price": 5.00, "quantity": 25},
    "Chocolate Muffin": {"price": 3.75, "quantity": 35},
}


@mcp.tool
async def list_products() -> dict:
    """List all available products with their prices and stock levels."""
    return INVENTORY


@mcp.tool
async def buy_product(
    product_name: Annotated[str, "Exact name of the product to buy"],
    quantity: Annotated[int, "Number of items to buy (must be positive)"],
    ctx: Context,
) -> str:
    """Buy a product from the store, reducing its inventory."""
    user_id = await ctx.get_state("user_id")

    if product_name not in INVENTORY:
        return f"Error: '{product_name}' not found. Use list_products to see available items."

    product = INVENTORY[product_name]

    if quantity <= 0:
        return "Error: Quantity must be positive."

    if product["quantity"] < quantity:
        return f"Error: Only {product['quantity']} '{product_name}' in stock, but you requested {quantity}."

    product["quantity"] -= quantity
    total = product["price"] * quantity
    return f"User {user_id} bought {quantity}x {product_name} for ${total:.2f}. Remaining stock: {product['quantity']}."


@mcp.tool(app=True)
def show_inventory_chart() -> PrefabApp:
    """Show current inventory levels as an interactive bar chart."""
    data = [{"product": name, "quantity": info["quantity"]} for name, info in INVENTORY.items()]

    with Column(gap=4, css_class="p-6") as view:
        Heading("Inventory Levels")
        BarChart(
            data=data,
            series=[ChartSeries(data_key="quantity", label="In Stock")],
            x_axis="product",
        )

    return PrefabApp(view=view)


@mcp.tool(app=True)
def show_product_catalog() -> PrefabApp:
    """Show the product catalog as a visual card layout."""
    with Column(gap=4, css_class="p-6") as view:
        Heading("Product Catalog")
        Separator()
        with Grid(columns=2, gap=4):
            for name, info in INVENTORY.items():
                with Card():
                    with CardContent():
                        Text(name, css_class="font-medium")
                        Text(f"${info['price']:.2f}")
                        if info["quantity"] > 0:
                            Badge(f"{info['quantity']} in stock", variant="success")
                        else:
                            Badge("Out of Stock", variant="destructive")

    return PrefabApp(view=view)


if __name__ == "__main__":
    logger.info("Store MCP server starting (HTTP mode on port 8420)")
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8420)
