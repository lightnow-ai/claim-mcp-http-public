import os
import socket
import subprocess
import sys
import time

import pytest
from mcp import Client

from claim_mcp_http_public.server import SERVER_NAME, SERVER_VERSION, mcp


def _free_port() -> int:
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        return int(listener.getsockname()[1])


def _wait_for_port(port: int) -> None:
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        with socket.socket() as client:
            if client.connect_ex(("127.0.0.1", port)) == 0:
                return
        time.sleep(0.05)
    raise TimeoutError(f"server did not listen on port {port}")


@pytest.mark.anyio
async def test_identify_tool_in_process() -> None:
    async with Client(mcp) as client:
        result = await client.call_tool("identify", {"message": "in-process"})

    assert result.structured_content == {
        "server": SERVER_NAME,
        "version": SERVER_VERSION,
        "transport": "streamable-http",
        "message": "in-process",
    }


@pytest.mark.anyio
async def test_identify_tool_over_streamable_http() -> None:
    port = _free_port()
    environment = {**os.environ, "PORT": str(port)}
    process = subprocess.Popen(
        [sys.executable, "-m", "claim_mcp_http_public.server"],
        env=environment,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        _wait_for_port(port)
        async with Client(f"http://127.0.0.1:{port}/mcp") as client:
            result = await client.call_tool("identify", {"message": "transport-smoke"})
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)

    assert process.returncode in {0, -15}
    assert result.structured_content == {
        "server": SERVER_NAME,
        "version": SERVER_VERSION,
        "transport": "streamable-http",
        "message": "transport-smoke",
    }

