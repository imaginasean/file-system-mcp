"""
File System MCP Server

Exposes file system operations as MCP tools for LLM applications.
"""

from pathlib import Path

from fastmcp import FastMCP

mcp = FastMCP(
    "File System",
    instructions="Tools for reading, writing, and managing files and directories.",
)


# ---------------------------------------------------------------------------
# Read operations
# ---------------------------------------------------------------------------


@mcp.tool
def read_file(path: str, encoding: str = "utf-8") -> str:
    """
    Read the contents of a file.

    Args:
        path: Path to the file (absolute or relative).
        encoding: Text encoding (default: utf-8).

    Returns:
        The file contents as a string.
    """
    p = Path(path).expanduser().resolve()
    if not p.exists():
        return f"Error: File not found: {path}"
    if not p.is_file():
        return f"Error: Not a file: {path}"
    try:
        return p.read_text(encoding=encoding)
    except Exception as e:
        return f"Error reading file: {e}"


@mcp.tool
def list_directory(path: str = ".") -> str:
    """
    List contents of a directory.

    Args:
        path: Path to the directory (default: current directory).

    Returns:
        List of files and subdirectories with basic metadata.
    """
    p = Path(path).expanduser().resolve()
    if not p.exists():
        return f"Error: Directory not found: {path}"
    if not p.is_dir():
        return f"Error: Not a directory: {path}"
    try:
        entries = []
        for item in sorted(p.iterdir()):
            kind = "dir" if item.is_dir() else "file"
            size = item.stat().st_size if item.is_file() else "-"
            entries.append(f"  {item.name}\t({kind}, {size})")
        return "\n".join(entries) if entries else "(empty directory)"
    except Exception as e:
        return f"Error listing directory: {e}"


@mcp.tool
def file_exists(path: str) -> bool:
    """
    Check if a file or directory exists at the given path.

    Args:
        path: Path to check.

    Returns:
        True if the path exists, False otherwise.
    """
    return Path(path).expanduser().resolve().exists()


@mcp.tool
def get_file_info(path: str) -> str:
    """
    Get metadata about a file or directory (size, modified time, type).

    Args:
        path: Path to the file or directory.

    Returns:
        Metadata string with size, mtime, and type.
    """
    import datetime

    p = Path(path).expanduser().resolve()
    if not p.exists():
        return f"Error: Path not found: {path}"
    try:
        stat = p.stat()
        mtime = datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()
        kind = "directory" if p.is_dir() else "file"
        size = stat.st_size if p.is_file() else "-"
        return f"Path: {p}\nType: {kind}\nSize: {size}\nModified: {mtime}"
    except Exception as e:
        return f"Error: {e}"


# ---------------------------------------------------------------------------
# Write operations
# ---------------------------------------------------------------------------


@mcp.tool
def write_file(path: str, content: str, append: bool = False) -> str:
    """
    Write content to a file. Creates the file and parent directories if needed.

    Args:
        path: Path to the file.
        content: Content to write.
        append: If True, append to existing file instead of overwriting.

    Returns:
        Success or error message.
    """
    p = Path(path).expanduser().resolve()
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        mode = "a" if append else "w"
        p.write_text(content, encoding="utf-8")
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing file: {e}"


@mcp.tool
def create_directory(path: str, parents: bool = True) -> str:
    """
    Create a directory. Creates parent directories if parents=True.

    Args:
        path: Path to the directory to create.
        parents: If True, create parent directories as needed.

    Returns:
        Success or error message.
    """
    p = Path(path).expanduser().resolve()
    try:
        p.mkdir(parents=parents, exist_ok=True)
        return f"Successfully created directory: {path}"
    except Exception as e:
        return f"Error creating directory: {e}"


# ---------------------------------------------------------------------------
# Modify / Delete operations
# ---------------------------------------------------------------------------


@mcp.tool
def delete_file(path: str) -> str:
    """
    Delete a file.

    Args:
        path: Path to the file to delete.

    Returns:
        Success or error message.
    """
    p = Path(path).expanduser().resolve()
    if not p.exists():
        return f"Error: File not found: {path}"
    if not p.is_file():
        return f"Error: Not a file (use delete_directory for directories): {path}"
    try:
        p.unlink()
        return f"Successfully deleted: {path}"
    except Exception as e:
        return f"Error deleting file: {e}"


@mcp.tool
def delete_directory(path: str, recursive: bool = False) -> str:
    """
    Delete a directory.

    Args:
        path: Path to the directory to delete.
        recursive: If True, delete directory and all contents.

    Returns:
        Success or error message.
    """
    import shutil

    p = Path(path).expanduser().resolve()
    if not p.exists():
        return f"Error: Directory not found: {path}"
    if not p.is_dir():
        return f"Error: Not a directory: {path}"
    try:
        if recursive:
            shutil.rmtree(p)
        else:
            p.rmdir()
        return f"Successfully deleted directory: {path}"
    except Exception as e:
        return f"Error deleting directory: {e}"


@mcp.tool
def move_file(source: str, destination: str) -> str:
    """
    Move or rename a file or directory.

    Args:
        source: Path to the file or directory to move.
        destination: Destination path.

    Returns:
        Success or error message.
    """
    src = Path(source).expanduser().resolve()
    dest = Path(destination).expanduser().resolve()
    if not src.exists():
        return f"Error: Source not found: {source}"
    try:
        src.rename(dest)
        return f"Successfully moved {source} to {destination}"
    except Exception as e:
        return f"Error moving: {e}"


@mcp.tool
def copy_file(source: str, destination: str) -> str:
    """
    Copy a file or directory to a new location.

    Args:
        source: Path to the file or directory to copy.
        destination: Destination path.

    Returns:
        Success or error message.
    """
    import shutil

    src = Path(source).expanduser().resolve()
    dest = Path(destination).expanduser().resolve()
    if not src.exists():
        return f"Error: Source not found: {source}"
    try:
        if src.is_dir():
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest)
        return f"Successfully copied {source} to {destination}"
    except Exception as e:
        return f"Error copying: {e}"


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------


@mcp.tool
def search_files(
    directory: str = ".",
    pattern: str = "*",
    recursive: bool = False,
) -> str:
    """
    Search for files matching a glob pattern in a directory.

    Args:
        directory: Directory to search in.
        pattern: Glob pattern (e.g. "*.py", "**/test_*").
        recursive: If True, search subdirectories.

    Returns:
        Newline-separated list of matching file paths.
    """
    p = Path(directory).expanduser().resolve()
    if not p.exists():
        return f"Error: Directory not found: {directory}"
    if not p.is_dir():
        return f"Error: Not a directory: {directory}"
    try:
        if recursive:
            matches = list(p.rglob(pattern))
        else:
            matches = list(p.glob(pattern))
        # Filter to files only
        files = [m for m in matches if m.is_file()]
        return "\n".join(str(f) for f in sorted(files)) if files else "(no matches)"
    except Exception as e:
        return f"Error searching: {e}"


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8010,
        path="/mcp",
    )
