# Contributing to COVID-19 Economic Impact Analysis

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/covid_economic_analysis.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit and push
7. Create a Pull Request

## Development Setup

```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v
```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise
- Add comments for complex logic

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Run tests with: `pytest tests/ -v`
- Aim for good test coverage

## API Development

When adding new API endpoints:

1. Add the endpoint to `src/api.py`
2. Include proper error handling
3. Add tests in `tests/test_api.py`
4. Update `API_DOCUMENTATION.md`
5. Add examples to `examples/api_usage_example.py`

## Documentation

- Update README.md for major changes
- Update API_DOCUMENTATION.md for API changes
- Add entries to CHANGELOG.md
- Include code comments and docstrings

## Pull Request Process

1. Update documentation as needed
2. Add tests for new functionality
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Provide clear PR description
6. Link related issues

## Commit Messages

Use clear, descriptive commit messages:

```
feat: Add new correlation endpoint to API
fix: Resolve database connection issue
docs: Update API documentation
test: Add tests for economic data endpoint
refactor: Improve data processing performance
```

## Areas for Contribution

### High Priority
- Additional data sources integration
- Performance optimizations
- Enhanced error handling
- More comprehensive tests
- API rate limiting
- Authentication system

### Medium Priority
- Additional visualization types
- Export functionality
- Data caching
- API versioning
- Internationalization

### Documentation
- Tutorial videos
- More code examples
- Architecture diagrams
- Performance benchmarks

## Bug Reports

When reporting bugs, include:

- Python version
- Operating system
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages/logs
- Screenshots (if applicable)

## Feature Requests

For feature requests, provide:

- Clear description
- Use case/motivation
- Proposed implementation (optional)
- Examples (if applicable)

## Questions?

- Open an issue for questions
- Check existing issues first
- Be respectful and constructive

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Assume good intentions
- Help others learn and grow

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- CHANGELOG.md

Thank you for contributing! 🎉
