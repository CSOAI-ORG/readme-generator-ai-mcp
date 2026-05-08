<div align="center">

# Readme Generator Ai MCP

**MCP server for readme generator ai mcp operations**

[![PyPI](https://img.shields.io/pypi/v/meok-readme-generator-ai-mcp)](https://pypi.org/project/meok-readme-generator-ai-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

Readme Generator Ai MCP provides AI-powered tools via the Model Context Protocol (MCP).

## Tools

| Tool | Description |
|------|-------------|
| `generate_readme` | Generate a complete README.md from project metadata including sections for insta |
| `analyze_project` | Analyze project structure from a file list to recommend README sections and dete |
| `suggest_sections` | Suggest appropriate README sections based on project type and capabilities. |
| `generate_badges` | Generate shield.io badge markdown for a GitHub repository. |

## Installation

```bash
pip install meok-readme-generator-ai-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "readme-generator-ai": {
      "command": "python",
      "args": ["-m", "meok_readme_generator_ai_mcp.server"]
    }
  }
}
```

## Usage with FastMCP

```python
from mcp.server.fastmcp import FastMCP

# This server exposes 4 tool(s) via MCP
# See server.py for full implementation
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
