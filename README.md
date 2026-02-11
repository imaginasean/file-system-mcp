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

By default the server uses STDIO transport. For HTTP/SSE deployment, see [FastMCP deployment docs](https://gofastmcp.com/deployment).

## Cursor Configuration

Add to your Cursor MCP settings (e.g. `~/.cursor/mcp.json` or Cursor Settings → MCP):

```json
{
  "mcpServers": {
    "file-system": {
      "command": "/path/to/file-system-mcp/.venv/bin/python",
      "args": ["/path/to/file-system-mcp/server.py"]
    }
  }
}
```

Or with system Python:
```json
{
  "mcpServers": {
    "file-system": {
      "command": "python",
      "args": ["/path/to/file-system-mcp/server.py"]
    }
  }
}
```

Or with `uv`:
```json
{
  "mcpServers": {
    "file-system": {
      "command": "uv",
      "args": ["run", "python", "/path/to/file-system-mcp/server.py"]
    }
  }
}
```

## Tools

| Tool | Description |
|------|-------------|
| `read_file` | Read file contents |
| `list_directory` | List directory contents |
| `file_exists` | Check if path exists |
| `get_file_info` | Get file/directory metadata |
| `write_file` | Write content to a file |
| `create_directory` | Create a directory |
| `delete_file` | Delete a file |
| `delete_directory` | Delete a directory |
| `move_file` | Move or rename a file/directory |
| `copy_file` | Copy a file or directory |
| `search_files` | Search for files by glob pattern |
