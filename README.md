# Readme Generator Ai

> By [MEOK AI Labs](https://meok.ai) — MEOK AI Labs — Generate README.md files from project analysis.

Generate README.md files from project analysis. — MEOK AI Labs.

## Installation

```bash
pip install readme-generator-ai-mcp
```

## Usage

```bash
# Run standalone
python server.py

# Or via MCP
mcp install readme-generator-ai-mcp
```

## Tools

### `generate_readme`
Generate a complete README.md from project metadata including sections for install, usage, API, and contributing.

**Parameters:**
- `project_name` (str)
- `description` (str)
- `language` (str)
- `features` (str)
- `author` (str)
- `license_type` (str)

### `analyze_project`
Analyze project structure from a file list to recommend README sections and detect project type.

**Parameters:**
- `file_list` (str)
- `language` (str)

### `suggest_sections`
Suggest appropriate README sections based on project type and capabilities.

**Parameters:**
- `project_type` (str)
- `has_api` (bool)
- `has_cli` (bool)
- `has_docker` (bool)

### `generate_badges`
Generate shield.io badge markdown for a GitHub repository.

**Parameters:**
- `owner` (str)
- `repo` (str)
- `badges` (str)
- `license_type` (str)
- `version` (str)


## Authentication

Free tier: 15 calls/day. Upgrade at [meok.ai/pricing](https://meok.ai/pricing) for unlimited access.

## Links

- **Website**: [meok.ai](https://meok.ai)
- **GitHub**: [CSOAI-ORG/readme-generator-ai-mcp](https://github.com/CSOAI-ORG/readme-generator-ai-mcp)
- **PyPI**: [pypi.org/project/readme-generator-ai-mcp](https://pypi.org/project/readme-generator-ai-mcp/)

## License

MIT — MEOK AI Labs
