#!/usr/bin/env python3
"""Generate README.md files from project analysis. — MEOK AI Labs."""

import sys, os
sys.path.insert(0, os.path.expanduser('~/clawd/meok-labs-engine/shared'))
from auth_middleware import check_access

import json, os, re, hashlib
from datetime import datetime, timezone
from typing import Optional
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

FREE_DAILY_LIMIT = 30
_usage = defaultdict(list)
def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now-t).total_seconds() < 86400]
    if len(_usage[c]) >= FREE_DAILY_LIMIT: return json.dumps({"error": "Limit/day. Upgrade: meok.ai"})
    _usage[c].append(now); return None

mcp = FastMCP("readme-generator-ai", instructions="MEOK AI Labs — Generate README.md files from project analysis.")

LANGUAGE_CONFIGS = {
    "python": {"pkg_file": "requirements.txt", "test_cmd": "pytest", "install": "pip install -r requirements.txt"},
    "javascript": {"pkg_file": "package.json", "test_cmd": "npm test", "install": "npm install"},
    "typescript": {"pkg_file": "package.json", "test_cmd": "npm test", "install": "npm install"},
    "rust": {"pkg_file": "Cargo.toml", "test_cmd": "cargo test", "install": "cargo build"},
    "go": {"pkg_file": "go.mod", "test_cmd": "go test ./...", "install": "go mod download"},
    "java": {"pkg_file": "pom.xml", "test_cmd": "mvn test", "install": "mvn install"},
    "ruby": {"pkg_file": "Gemfile", "test_cmd": "bundle exec rspec", "install": "bundle install"},
}

SECTION_TEMPLATES = {
    "installation": "## Installation\n\n```bash\n{install_cmd}\n```",
    "usage": "## Usage\n\n```{lang}\n# Example usage\n{usage_example}\n```",
    "api": "## API Reference\n\n{api_docs}",
    "contributing": "## Contributing\n\n1. Fork the repository\n2. Create a feature branch (`git checkout -b feature/amazing`)\n3. Commit changes (`git commit -m 'Add amazing feature'`)\n4. Push to branch (`git push origin feature/amazing`)\n5. Open a Pull Request",
    "license": "## License\n\nThis project is licensed under the {license} License — see [LICENSE](LICENSE) for details.",
    "testing": "## Testing\n\n```bash\n{test_cmd}\n```",
    "changelog": "## Changelog\n\nSee [CHANGELOG.md](CHANGELOG.md) for release history.",
    "support": "## Support\n\nFor questions and support, please open an issue on GitHub.",
}

BADGE_TEMPLATES = {
    "license": "[![License: {license}](https://img.shields.io/badge/License-{license}-blue.svg)]({license_url})",
    "version": "[![Version](https://img.shields.io/badge/version-{version}-green.svg)]()",
    "build": "[![Build Status](https://img.shields.io/github/actions/workflow/status/{owner}/{repo}/ci.yml)](https://github.com/{owner}/{repo}/actions)",
    "coverage": "[![Coverage](https://img.shields.io/codecov/c/github/{owner}/{repo})](https://codecov.io/gh/{owner}/{repo})",
    "python": "[![Python](https://img.shields.io/badge/python-{version}-blue.svg)](https://python.org)",
    "node": "[![Node](https://img.shields.io/badge/node-%3E%3D{version}-green.svg)](https://nodejs.org)",
    "npm": "[![npm](https://img.shields.io/npm/v/{package}.svg)](https://npmjs.com/package/{package})",
    "pypi": "[![PyPI](https://img.shields.io/pypi/v/{package}.svg)](https://pypi.org/project/{package})",
    "downloads": "[![Downloads](https://img.shields.io/npm/dm/{package}.svg)](https://npmjs.com/package/{package})",
    "stars": "[![Stars](https://img.shields.io/github/stars/{owner}/{repo}.svg)](https://github.com/{owner}/{repo})",
}


@mcp.tool()
def generate_readme(project_name: str, description: str, language: str = "python",
                    features: str = "", author: str = "", license_type: str = "MIT",
                    api_key: str = "") -> str:
    """Generate a complete README.md from project metadata including sections for install, usage, API, and contributing."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    lang_cfg = LANGUAGE_CONFIGS.get(language.lower(), LANGUAGE_CONFIGS["python"])
    feature_list = [f.strip() for f in features.split(",") if f.strip()] if features else []

    sections = [f"# {project_name}\n", f"> {description}\n"]
    if feature_list:
        sections.append("## Features\n")
        for feat in feature_list:
            sections.append(f"- {feat}")
        sections.append("")
    sections.append(SECTION_TEMPLATES["installation"].format(install_cmd=lang_cfg["install"]))
    sections.append("")
    sections.append(SECTION_TEMPLATES["usage"].format(lang=language, usage_example=f"import {project_name.lower().replace('-', '_')}"))
    sections.append("")
    sections.append(SECTION_TEMPLATES["testing"].format(test_cmd=lang_cfg["test_cmd"]))
    sections.append("")
    sections.append(SECTION_TEMPLATES["contributing"])
    sections.append("")
    sections.append(SECTION_TEMPLATES["license"].format(license=license_type))
    if author:
        sections.append(f"\n## Author\n\n**{author}**")

    readme_content = "\n".join(sections)
    word_count = len(readme_content.split())
    return {
        "project": project_name,
        "language": language,
        "sections": ["header", "features", "installation", "usage", "testing", "contributing", "license"],
        "word_count": word_count,
        "readme": readme_content,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool()
def analyze_project(file_list: str, language: str = "python", api_key: str = "") -> str:
    """Analyze project structure from a file list to recommend README sections and detect project type."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    files = [f.strip() for f in file_list.split(",") if f.strip()]
    analysis = {"total_files": len(files), "detected_types": [], "recommended_sections": ["installation", "usage"]}

    extensions = defaultdict(int)
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext:
            extensions[ext] += 1

    if any("test" in f.lower() or "spec" in f.lower() for f in files):
        analysis["detected_types"].append("has_tests")
        analysis["recommended_sections"].append("testing")
    if any(f.lower() in ("dockerfile", "docker-compose.yml", "docker-compose.yaml") for f in files):
        analysis["detected_types"].append("dockerized")
        analysis["recommended_sections"].append("docker")
    if any(f.lower().endswith((".yml", ".yaml")) and "ci" in f.lower() for f in files):
        analysis["detected_types"].append("ci_cd")
        analysis["recommended_sections"].append("ci_cd")
    if any(f.lower() == "setup.py" or f.lower() == "pyproject.toml" for f in files):
        analysis["detected_types"].append("python_package")
        analysis["recommended_sections"].append("api")
    if any(f.lower() == "package.json" for f in files):
        analysis["detected_types"].append("node_package")
    if any(f.lower().endswith((".env.example", ".env.template")) for f in files):
        analysis["recommended_sections"].append("configuration")

    analysis["recommended_sections"].extend(["contributing", "license"])
    analysis["file_extensions"] = dict(extensions)
    analysis["timestamp"] = datetime.now(timezone.utc).isoformat()
    return analysis


@mcp.tool()
def suggest_sections(project_type: str, has_api: bool = False, has_cli: bool = False,
                     has_docker: bool = False, api_key: str = "") -> str:
    """Suggest appropriate README sections based on project type and capabilities."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    base_sections = ["header", "description", "installation", "usage", "contributing", "license"]
    extra = []
    ptype = project_type.lower()

    if ptype in ("library", "package", "sdk"):
        extra.extend(["api", "examples", "changelog"])
    elif ptype in ("cli", "tool"):
        extra.extend(["commands", "examples", "configuration"])
    elif ptype in ("web", "webapp", "api"):
        extra.extend(["endpoints", "authentication", "deployment"])
    elif ptype in ("data", "ml", "ai"):
        extra.extend(["dataset", "model", "training", "evaluation"])

    if has_api:
        extra.append("api_reference")
    if has_cli:
        extra.append("cli_reference")
    if has_docker:
        extra.extend(["docker", "docker_compose"])

    all_sections = base_sections + [s for s in extra if s not in base_sections]
    templates = {s: SECTION_TEMPLATES.get(s, f"## {s.replace('_', ' ').title()}\n\nTODO: Add content") for s in all_sections}
    return {
        "project_type": project_type,
        "sections": all_sections,
        "total": len(all_sections),
        "templates": templates,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool()
def generate_badges(owner: str, repo: str, badges: str = "license,version,build",
                    license_type: str = "MIT", version: str = "1.0.0", api_key: str = "") -> str:
    """Generate shield.io badge markdown for a GitHub repository."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    requested = [b.strip().lower() for b in badges.split(",") if b.strip()]
    generated = []
    license_urls = {"MIT": "https://opensource.org/licenses/MIT", "Apache-2.0": "https://opensource.org/licenses/Apache-2.0",
                    "GPL-3.0": "https://www.gnu.org/licenses/gpl-3.0", "BSD-3": "https://opensource.org/licenses/BSD-3-Clause"}

    for badge in requested:
        tmpl = BADGE_TEMPLATES.get(badge)
        if tmpl:
            try:
                md = tmpl.format(owner=owner, repo=repo, license=license_type,
                                 license_url=license_urls.get(license_type, "#"),
                                 version=version, package=repo)
                generated.append({"name": badge, "markdown": md})
            except KeyError:
                generated.append({"name": badge, "markdown": f"<!-- Badge '{badge}' needs additional params -->"})
        else:
            generated.append({"name": badge, "error": f"Unknown badge type: {badge}",
                              "available": list(BADGE_TEMPLATES.keys())})

    badge_line = " ".join(b["markdown"] for b in generated if "markdown" in b)
    return {
        "owner": owner,
        "repo": repo,
        "badges": generated,
        "badge_line": badge_line,
        "total_generated": len([b for b in generated if "error" not in b]),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    mcp.run()
