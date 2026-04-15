import logging
from typing import Annotated

from fastmcp import Context, FastMCP
from prefab_ui.app import PrefabApp
from prefab_ui.components import Badge, Card, CardContent, Column, Grid, Heading, Separator, Text
from prefab_ui.components.charts import BarChart, ChartSeries
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(message)s")
logger = logging.getLogger("StoreMCP")
logger.setLevel(logging.INFO)

mcp = FastMCP("Pamela's Bakery")

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


class PurchaseConfirmation(BaseModel):
    confirm: bool = Field(title="Confirm purchase", description="Approve this transaction?")


@mcp.tool
async def buy_product(
    product_name: Annotated[str, "Exact name of the product to buy"],
    quantity: Annotated[int, "Number of items to buy (must be positive)"],
    ctx: Context,
) -> str:
    """Buy a product from the store, with user confirmation."""
    if product_name not in INVENTORY:
        return f"Error: '{product_name}' not found. Use list_products to see available items."

    product = INVENTORY[product_name]

    if quantity <= 0:
        return "Error: Quantity must be positive."

    if product["quantity"] < quantity:
        return f"Error: Only {product['quantity']} '{product_name}' in stock, but you requested {quantity}."

    total = product["price"] * quantity

    # Ask the user to confirm before purchasing
    response = await ctx.elicit(
        message=f"Buy {quantity}x {product_name} for ${total:.2f}?",
        response_type=PurchaseConfirmation,
    )

    if response.action != "accept" or not response.data.confirm:
        return "Purchase cancelled."

    product["quantity"] -= quantity
    return f"Successfully bought {quantity}x {product_name} for ${total:.2f}. Remaining stock: {product['quantity']}."


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
