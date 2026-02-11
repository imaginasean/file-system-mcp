# File System MCP

An MCP (Model Context Protocol) server built with [FastMCP](https://gofastmcp.com) that exposes file system operations as tools for LLM applications.

## Installation

```bash
# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Server

**With FastMCP CLI (recommended):**

```bash
fastmcp run server.py
```

**Or directly:**

```bash
python server.py
```

The server uses **Streamable HTTP** transport by default (port 8010, path `/mcp`). Connect at `http://127.0.0.1:8010/mcp`. For STDIO or SSE, see [FastMCP deployment docs](https://gofastmcp.com/deployment).

## Cursor Configuration

Add to your Cursor MCP settings (e.g. `~/.cursor/mcp.json` or Cursor Settings → MCP). Use the **URL** transport for streaming HTTP:

```json
{
	"mcpServers": {
		"file-system": {
			"url": "http://127.0.0.1:8010/mcp"
		}
	}
}
```

Start the server first: `fastmcp run server.py` (or `python server.py`).

## Tools

| Tool               | Description                      |
| ------------------ | -------------------------------- |
| `read_file`        | Read file contents               |
| `list_directory`   | List directory contents          |
| `file_exists`      | Check if path exists             |
| `get_file_info`    | Get file/directory metadata      |
| `write_file`       | Write content to a file          |
| `create_directory` | Create a directory               |
| `delete_file`      | Delete a file                    |
| `delete_directory` | Delete a directory               |
| `move_file`        | Move or rename a file/directory  |
| `copy_file`        | Copy a file or directory         |
| `search_files`     | Search for files by glob pattern |
