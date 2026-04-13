import logging
from typing import Annotated

from fastmcp import FastMCP

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


@mcp.tool
async def buy_product(
    product_name: Annotated[str, "Exact name of the product to buy"],
    quantity: Annotated[int, "Number of items to buy (must be positive)"],
) -> str:
    """Buy a product from the store, reducing its inventory."""
    if product_name not in INVENTORY:
        return f"Error: '{product_name}' not found. Use list_products to see available items."

    product = INVENTORY[product_name]

    if quantity <= 0:
        return "Error: Quantity must be positive."

    if product["quantity"] < quantity:
        return f"Error: Only {product['quantity']} '{product_name}' in stock, but you requested {quantity}."

    product["quantity"] -= quantity
    total = product["price"] * quantity
    return f"Successfully bought {quantity}x {product_name} for ${total:.2f}. Remaining stock: {product['quantity']}."


if __name__ == "__main__":
    logger.info("Store MCP server starting (HTTP mode on port 8420)")
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8420)
