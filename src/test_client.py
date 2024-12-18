from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
import sys

async def main():
    # Create server parameters for stdio connection
    server_params = StdioServerParameters(
        command="/opt/homebrew/bin/python3.11",
        args=["server.py"],
        env={"PHABRICATOR_TOKEN": "api-ojdk6nbvu35wh5g67l6nbxk3kmh7"}  # Replace with your token
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print("Available tools:")
            for tool in tools:
                print(f"- {tool.name}: {tool.description}")

            # Try getting a task
            task_id = input("\nEnter a task ID to fetch (without 'T' prefix): ")
            result = await session.call_tool("get-task", {"task_id": task_id})
            print("\nTask details:")
            print(result[0].text)

if __name__ == "__main__":
    asyncio.run(main())
