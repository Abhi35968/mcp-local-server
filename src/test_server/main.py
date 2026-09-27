from fastmcp import FastMCP
import os
import json
import random

mcp= FastMCP(name="Simple Calculator Server")

@mcp.tool
def add(a: int, b: int) ->int:
    """Add two numbers.
    Args:
        a (int): The first number.
        b (int): The second number.
    Returns:
        int: The sum of the two numbers.
    """
    return a + b

@mcp.tool
def random_number(min_value: int=1, max_value: int=100) -> int:
    """Generate a random number between min_value and max_value.
    Args:
        min_value (int): The minimum value (default: 1).
        max_value (int): The maximum value (default: 100).
    Returns:
        int: A random number between min_value and max_value.
    """
    
    return random.randint(min_value, max_value)

@mcp.resource("info://server")
def server_info() -> str:
    """Get server information."""
    info={
        "name":"Simple Calculator Server",
        "version":"1.0.0",
        "description":"A simple calculator server that provides basic arithmetic operations and random number generation.",
        "tools": ["add", "random_number"],
        "author": "Your Name"
    }
    return json.dumps(info, indent=2)


def main() -> None:
    mcp.run(transport="http", host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()