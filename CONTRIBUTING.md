# Contributing to poly402

Thank you for your interest in contributing to poly402! This document provides guidelines for contributing to the project.

## Development Setup

1. Fork the repository on GitHub
2. Clone your fork locally:
```bash
git clone https://github.com/yourusername/poly402.git
cd poly402
```

3. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install development dependencies:
```bash
pip install -r requirements.txt
pip install -e .
npm install
```

5. Create a branch for your changes:
```bash
git checkout -b feature/your-feature-name
```

## Code Standards

### Python

- Follow PEP 8 style guide
- Use type hints where applicable
- Write docstrings for all public functions and classes
- Keep functions focused and single-purpose

Format code with black:
```bash
black src/
```

Lint with flake8:
```bash
flake8 src/
```

Type check with mypy:
```bash
mypy src/
```

### TypeScript

- Follow standard TypeScript conventions
- Use ESLint for linting
- Write JSDoc comments for public APIs

## Testing

Run Python tests:
```bash
pytest tests/
```

Run TypeScript tests:
```bash
npm test
```

## Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update documentation in the `docs/` directory
3. Add tests for new functionality
4. Ensure all tests pass
5. Update the CHANGELOG (if exists)
6. Submit pull request with clear description of changes

## Commit Message Guidelines

- Use clear, descriptive commit messages
- Start with a verb in present tense (e.g., "Add", "Fix", "Update")
- Reference issue numbers where applicable

Examples:
```
Add support for batch trading
Fix balance check for Polygon network
Update README with installation instructions
```

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Respect differing opinions and experiences

## Questions?

Open an issue on GitHub or join our Discord community.

## License

By contributing to poly402, you agree that your contributions will be licensed under the MIT License.
