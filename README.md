# Advanced RAG: Vulnerability Analysis System

A sophisticated vulnerability analysis system that combines dependency scanning, vulnerability detection, and graph-based impact analysis using Neo4j and multiple security APIs.

## 🚀 Features

- 🔍 **Multi-format Manifest Parsing**: Supports Python (requirements.txt, setup.py, pyproject.toml) and JavaScript (package.json)
- 🛡️ **Vulnerability Detection**: Integrates with NVD and GitHub Security APIs
- 🕸️ **Graph-based Impact Analysis**: Uses Neo4j to model dependency relationships and vulnerability impact
- 📊 **Comprehensive Reporting**: Detailed vulnerability reports with remediation recommendations
- 🧪 **Comprehensive Testing**: 10+ test cases covering happy paths and edge cases
- 🔄 **Real-time Analysis**: Live scanning of repositories with immediate results

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Repository    │    │   Vulnerability  │    │   Neo4j Graph   │
│   Scanner       │◄──►│   Analyzer       │◄──►│   Database      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Manifest      │    │   NVD/GitHub    │    │   Impact        │
│   Parser        │    │   APIs          │    │   Traversal     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📦 Components

### 1. Dependency Scanner (`dependency_scanner.py`)
- **Repository Cloning**: Automatically clones Git repositories
- **Import Extraction**: Parses Python, JavaScript, and TypeScript imports
- **Graph Construction**: Builds Neo4j graph of file-module relationships
- **Multi-language Support**: Handles `.py`, `.js`, `.ts` files

### 2. Vulnerability System (`vulnerability_system.py`)
- **Manifest Parsing**: Extracts dependencies from various manifest files
- **Vulnerability Fetching**: Queries NVD and GitHub Security APIs
- **Graph Annotation**: Adds vulnerability data to Neo4j graph
- **Impact Analysis**: Traverses dependency graph to find affected files
- **Remediation Recommendations**: Generates actionable security advice

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Neo4j database (local or cloud)
- Git repository to analyze

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file:

```env
# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password

# Optional: GitHub API for enhanced vulnerability data
GITHUB_TOKEN=your_github_token
```

### 3. Run Dependency Scanner

```bash
python dependency_scanner.py --repo https://github.com/user/repo --branch main
```

### 4. Run Vulnerability Analysis

```bash
python vulnerability_system.py --repo /path/to/repo
```

## 📖 Usage Examples

### Basic Repository Analysis

```bash
# Clone and scan a repository
python dependency_scanner.py --repo https://github.com/example/project

# Analyze vulnerabilities
python vulnerability_system.py --repo ./cloned_repo
```

### Advanced Analysis

```bash
# Scan specific branch
python dependency_scanner.py --repo https://github.com/example/project --branch develop

# Verbose vulnerability analysis
python vulnerability_system.py --repo ./repo --verbose
```

## 🔧 API Reference

### Dependency Scanner

```python
from dependency_scanner import clone_repo, extract_imports, build_graph

# Clone repository
repo_path = clone_repo("https://github.com/user/repo", "/tmp/repo", "main")

# Extract imports from file
imports = extract_imports(Path("src/main.py"))

# Build graph
build_graph(driver, "src/main.py", imports)
```

### Vulnerability Analyzer

```python
from vulnerability_system import VulnerabilityAnalyzer

analyzer = VulnerabilityAnalyzer()
analyzer.connect_neo4j()

# Load manifests
packages = analyzer.load_manifests("/path/to/repo")

# Fetch vulnerabilities
for pkg in packages:
    vulns = analyzer.fetch_vulnerabilities_for(pkg)
    analyzer.annotate_graph(pkg, vulns)
    
    if vulns:
        impact = analyzer.traverse_impact(vulns[0].cve_id)
        recs = analyzer.recommend_remediations(pkg, vulns)
```

## 🧪 Testing

### Run All Tests

```bash
pytest test_vulnerability_system.py -v
```

### Run Specific Test Categories

```bash
# Happy path tests
pytest test_vulnerability_system.py::TestVulnerabilityAnalyzer::test_connect_neo4j_success -v

# Edge case tests
pytest test_vulnerability_system.py::TestVulnerabilityAnalyzer::test_connect_neo4j_missing_env_vars -v
```

### Test Coverage

The test suite includes:

#### Happy Path Tests (5)
1. **Neo4j Connection Success**: Tests successful database connection
2. **Python Manifest Loading**: Tests requirements.txt parsing
3. **JavaScript Manifest Loading**: Tests package.json parsing
4. **Vulnerability Fetching**: Tests API integration
5. **Graph Annotation**: Tests Neo4j graph operations

#### Edge Case Tests (5)
1. **Missing Environment Variables**: Tests graceful failure handling
2. **Connection Failures**: Tests network error handling
3. **Empty Repositories**: Tests empty manifest scenarios
4. **Malformed Files**: Tests parsing error handling
5. **API Failures**: Tests external API error scenarios

## 📊 Neo4j Graph Schema

### Nodes

```cypher
// Files in the repository
(f:File {path: string})

// External modules/packages
(m:Module {name: string})

// Packages with version info
(p:Package {name: string, version: string, ecosystem: string})

// Vulnerabilities
(v:Vulnerability {
    cve_id: string,
    severity: string,
    description: string,
    cvss_score: float,
    published_date: string
})

// Affected versions
(av:AffectedVersion {version: string})
```

### Relationships

```cypher
// File imports module
(f:File)-[:IMPORTS]->(m:Module)

// Package is affected by vulnerability
(p:Package)-[:AFFECTED_BY]->(v:Vulnerability)

// Vulnerability affects specific version
(v:Vulnerability)-[:AFFECTS]->(av:AffectedVersion)
```

## 🔍 Vulnerability Analysis Workflow

### 1. Manifest Parsing
- **requirements.txt**: Python dependencies with version constraints
- **package.json**: Node.js dependencies and dev dependencies
- **setup.py**: Python package configuration
- **pyproject.toml**: Poetry and modern Python packaging

### 2. Vulnerability Detection
- **NVD API**: National Vulnerability Database integration
- **GitHub Security**: GitHub Security Advisory API
- **Version Matching**: Semantic version comparison
- **CVSS Scoring**: Common Vulnerability Scoring System

### 3. Impact Analysis
- **Dependency Traversal**: Find all affected files
- **Transitive Dependencies**: Analyze indirect vulnerabilities
- **Risk Assessment**: Calculate overall risk score
- **Remediation Path**: Identify update strategies

### 4. Reporting
- **Vulnerability Summary**: Count and severity breakdown
- **Affected Files**: List of files requiring attention
- **Remediation Actions**: Specific update recommendations
- **Priority Levels**: Critical, High, Medium, Low

## 🛠️ Development

### Project Structure

```
week3_adv_rag/
├── dependency_scanner.py      # Repository scanning and import extraction
├── vulnerability_system.py    # Main vulnerability analysis system
├── test_vulnerability_system.py  # Comprehensive test suite
├── requirements.txt           # Python dependencies
├── README.md                 # This file
├── tests/                    # Additional test files
└── venv/                     # Virtual environment
```

### Adding New Features

1. **New Manifest Format**: Add parser to `load_manifests()`
2. **New Vulnerability Source**: Extend `fetch_vulnerabilities_for()`
3. **Enhanced Graph Queries**: Add methods to `VulnerabilityAnalyzer`
4. **Additional Tests**: Extend test suite with new scenarios

### Code Quality

- **Type Hints**: Full type annotation support
- **Error Handling**: Comprehensive exception management
- **Logging**: Structured logging with configurable levels
- **Documentation**: Detailed docstrings and comments

## 🔧 Configuration

### Neo4j Setup

#### Local Installation
```bash
# Install Neo4j Desktop or Community Edition
# Start Neo4j service
# Create database
# Set password
```

#### Cloud Deployment
```bash
# Neo4j AuraDB (recommended)
# Neo4j Sandbox
# Self-hosted cloud instance
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `NEO4J_URI` | Neo4j connection URI | Yes |
| `NEO4J_USERNAME` | Neo4j username | Yes |
| `NEO4J_PASSWORD` | Neo4j password | Yes |
| `GITHUB_TOKEN` | GitHub API token | No |

## 🚨 Troubleshooting

### Common Issues

1. **Neo4j Connection Failed**
   - Verify Neo4j is running
   - Check connection URI and credentials
   - Ensure network connectivity

2. **Repository Clone Failed**
   - Check Git URL format
   - Verify repository access permissions
   - Ensure sufficient disk space

3. **API Rate Limiting**
   - Add GitHub token for higher limits
   - Implement request throttling
   - Use API caching

4. **Parsing Errors**
   - Check manifest file format
   - Verify file encoding (UTF-8)
   - Review parsing logic

### Debug Mode

```bash
# Enable verbose logging
python vulnerability_system.py --repo ./repo --verbose

# Check Neo4j connection
python -c "from vulnerability_system import VulnerabilityAnalyzer; a = VulnerabilityAnalyzer(); print(a.connect_neo4j())"
```

## 📈 Performance

### Optimization Tips

1. **Batch Processing**: Process multiple packages in batches
2. **Caching**: Cache API responses to reduce requests
3. **Parallel Processing**: Use async/await for I/O operations
4. **Indexing**: Create Neo4j indexes for faster queries

### Scalability

- **Large Repositories**: Handle repositories with 1000+ files
- **Multiple Ecosystems**: Support Python, JavaScript, Go, Rust
- **Real-time Analysis**: Continuous monitoring capabilities
- **Distributed Processing**: Scale across multiple nodes

## 🔒 Security Considerations

### Data Protection

- **API Keys**: Store securely in environment variables
- **Repository Access**: Use read-only access when possible
- **Data Retention**: Implement data cleanup policies
- **Audit Logging**: Track analysis activities

### Best Practices

- **Regular Updates**: Keep dependencies updated
- **Vulnerability Monitoring**: Set up automated scanning
- **Access Control**: Limit repository access
- **Incident Response**: Plan for security incidents

## 🤝 Contributing

### Development Setup

1. **Fork Repository**: Create your own fork
2. **Create Branch**: `git checkout -b feature/new-feature`
3. **Make Changes**: Implement your changes
4. **Add Tests**: Include comprehensive test coverage
5. **Submit PR**: Create pull request with description

### Code Standards

- **PEP 8**: Follow Python style guidelines
- **Type Hints**: Use type annotations
- **Docstrings**: Document all functions
- **Tests**: Maintain >90% test coverage

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Neo4j**: Graph database technology
- **NVD**: National Vulnerability Database
- **GitHub**: Security Advisory API
- **Open Source Community**: Dependencies and tools

---

**Secure your codebase with advanced vulnerability analysis! 🛡️🔍✨** 