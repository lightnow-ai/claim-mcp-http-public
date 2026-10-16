import os

from mcp.server import MCPServer

SERVER_NAME = "io.github.lightnow-ai/claim-mcp-http-public"
SERVER_VERSION = "0.1.0"

mcp = MCPServer(SERVER_NAME)


@mcp.tool()
def identify(message: str = "ready") -> dict[str, str]:
    """Return deterministic identity data for ownership-claim acceptance tests."""
    return {
        "server": SERVER_NAME,
        "version": SERVER_VERSION,
        "transport": "streamable-http",
        "message": message,
    }


def main() -> None:
    port = int(os.getenv("PORT", "8000"))
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=port,
        stateless_http=True,
        json_response=True,
    )


if __name__ == "__main__":
    main()

