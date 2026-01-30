# Contributing to Financial Time Series Analytics Platform

First off, thank you for considering contributing to this project! It's people like you that make this platform better for everyone.

## 🤝 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** (code snippets, screenshots, etc.)
- **Describe the behavior you observed and what you expected**
- **Include your environment details** (OS, Python version, Docker version)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful**
- **List any alternative solutions** you've considered

### Your First Code Contribution

Unsure where to begin? You can start by looking through `beginner` and `help-wanted` issues:

- **Beginner issues** - issues that should only require a few lines of code
- **Help wanted issues** - issues that may be more involved

### Pull Requests

1. **Fork the repo** and create your branch from `main`
2. **Follow the coding standards** below
3. **Test your changes** thoroughly
4. **Update documentation** if you're changing functionality
5. **Ensure the test suite passes**
6. **Make sure your code lints** without errors
7. **Issue the pull request**

## 💻 Development Setup

1. **Clone your fork**
```bash
git clone https://github.com/your-username/architecture-fullstack.git
cd architecture-fullstack
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create a branch**
```bash
git checkout -b feature/your-feature-name
```

## 📝 Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and modular
- Maximum line length: 100 characters (flexible for readability)

### Code Structure

```python
def example_function(param1, param2):
    """
    Brief description of what the function does.
    
    Args:
        param1 (type): Description of param1
        param2 (type): Description of param2
    
    Returns:
        type: Description of return value
    """
    # Implementation
    pass
```

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- First line should be 50 characters or less
- Reference issues and pull requests liberally

Examples:
```
Add LSTM forecasting model
Fix date range filtering bug (#123)
Update documentation for Docker deployment
Refactor data loading pipeline
```

## 🧪 Testing

- Write tests for new features
- Ensure all existing tests pass
- Test your changes with different stock tickers
- Test in both local and Docker environments

```bash
# Run the app locally
streamlit run main.py

# Test Docker build
docker-compose up --build
```

## 📚 Documentation

- Update the README.md if you change functionality
- Add docstrings to all new functions and classes
- Update ARCHITECTURE.md for architectural changes
- Include code examples where helpful

## 🎨 Adding New Features

### New Visualizations

1. Add your visualization function in `main.py` or create a new module
2. Use the existing `COLOR_PALETTE` for consistency
3. Make it configurable through Streamlit widgets
4. Add a section in the dashboard with clear labels

### New Models

1. Create a new class or function in an appropriate module
2. Follow the pattern established by existing models
3. Add model selection in the Streamlit sidebar
4. Include diagnostic plots and metrics
5. Document model parameters and usage

### New Data Sources

1. Add data fetching logic to `datamover.py` or create new module
2. Ensure data format is consistent with existing sources
3. Add error handling for API failures
4. Update documentation with API requirements

## 🐛 Issue Labels

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Documentation improvements
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention is needed
- `question` - Further information is requested

## 🔍 Code Review Process

1. Maintainers will review your PR within 48-72 hours
2. Address any requested changes
3. Once approved, maintainers will merge your PR
4. Your contribution will be acknowledged in the README

## 📜 Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior

- Trolling, insulting/derogatory comments
- Personal or political attacks
- Public or private harassment
- Publishing others' private information
- Other conduct which could reasonably be considered inappropriate

## 📧 Getting Help

- Open an issue for questions about the codebase
- Check existing documentation first
- Be patient - maintainers volunteer their time

## 🎉 Recognition

Contributors will be acknowledged in:
- The README.md file
- Release notes
- Project documentation

Thank you for contributing! 🙌

