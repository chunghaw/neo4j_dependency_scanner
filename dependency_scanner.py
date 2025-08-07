#!/usr/bin/env python3
"""
dependency_scanner.py

Scan a GitHub repo for Python, JavaScript, and TypeScript imports and build a Neo4j
graph where:
  (f:File)-[:IMPORTS]->(m:Module)
"""

import os
import sys
import argparse
import tempfile
import ast
import re
from pathlib import Path
from git import Repo
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI      = os.getenv("NEO4J_URI")
NEO4J_USER     = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# Regex to catch JS/TS imports: `import x from 'module'` or `require('module')`
JS_IMPORT_RE = re.compile(r"""(?:import\s.+\sfrom\s|require\()\s*['"](?P<mod>[^'"]+)['"]""")

def clone_repo(git_url: str, clone_to: str, branch: str):
    repo = Repo.clone_from(git_url, clone_to)
    if branch and branch in repo.branches:
        repo.git.checkout(branch)
    return Path(repo.working_dir)

def extract_python_imports(py_path: Path):
    mods = set()
    try:
        tree = ast.parse(py_path.read_text(encoding="utf-8"))
    except Exception:
        return mods
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                mods.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            mods.add(node.module.split(".")[0])
    return mods

def extract_js_imports(js_path: Path):
    mods = set()
    text = js_path.read_text(encoding="utf-8")
    for m in JS_IMPORT_RE.finditer(text):
        name = m.group("mod").split("/")[0]  # only top-level package
        # skip relative imports
        if not name.startswith("."):
            mods.add(name)
    return mods

def extract_imports(file_path: Path):
    """Dispatch based on file extension."""
    if file_path.suffix in {".py"}:
        return extract_python_imports(file_path)
    if file_path.suffix in {".js", ".ts"}:
        return extract_js_imports(file_path)
    return set()

def build_graph(driver, file_node: str, imports: set):
    """
    1) Create uniqueness constraints (one-time ops)
    2) MERGE the File node
    3) MERGE each Module and the IMPORTS relationship
    """
    with driver.session() as sess:
        # ensure uniqueness
        sess.run("CREATE CONSTRAINT IF NOT EXISTS FOR (f:File) REQUIRE f.path IS UNIQUE")
        sess.run("CREATE CONSTRAINT IF NOT EXISTS FOR (m:Module) REQUIRE m.name IS UNIQUE")

        # merge file
        sess.run("MERGE (f:File {path: $path})", {"path": file_node})
        # merge modules + relationships
        for mod in sorted(imports):
            sess.run(
                """
                MERGE (m:Module {name: $mod})
                MERGE (f:File   {path: $path})
                MERGE (f)-[:IMPORTS]->(m)
                """,
                {"mod": mod, "path": file_node}
            )

def main():
    p = argparse.ArgumentParser(description="Scan a git repo into Neo4j")
    p.add_argument("--repo",   required=True, help="Git URL")
    p.add_argument("--branch", default="main", help="Branch to checkout")
    args = p.parse_args()

    # 1) Clone & checkout
    tmpdir  = tempfile.mkdtemp(prefix="dep_scan_")
    repo_dir = clone_repo(args.repo, tmpdir, args.branch)
    print(f"Cloned {args.repo} → {repo_dir}")

    # 2) Connect to Neo4j
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    # 3) Walk code files
    for path in repo_dir.rglob("*"):
        if path.suffix in {".py", ".js", ".ts"}:
            rel = str(path.relative_to(repo_dir))
            imps = extract_imports(path)
            print(f"{rel}: imports {imps}")
            build_graph(driver, rel, imps)

    driver.close()
    print("Done.")

if __name__ == "__main__":
    main()