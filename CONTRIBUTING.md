# Contributing to Image Renamer

First off, thank you for considering contributing to Image Renamer! It's people like you that make it a great tool for everyone.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

- **Use a clear and descriptive title** for the issue to identify the problem.
- **Describe the exact steps which reproduce the problem** in as many details as possible.
- **Provide specific examples to demonstrate the steps**. Include links to files or GitHub projects, or copy/pasteable snippets, which you use in those examples.
- **Describe the behavior you observed after following the steps** and point out what exactly is the problem with that behavior.
- **Explain which behavior you expected to see instead and why.**
- **Include screenshots and animated GIFs** which show you following the described steps and clearly demonstrate the problem.
- **If the problem is related to performance or memory**, include a CPU profile capture with your report.
- **If the crash is related to a specific image file**, include it if possible or describe it in detail.

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion, including completely new features and minor improvements to existing functionality.

- **Use a clear and descriptive title** for the issue to identify the suggestion.
- **Provide a step-by-step description of the suggested enhancement** in as many details as possible.
- **Provide specific examples to demonstrate the steps**. Include copy/pasteable snippets which you use in those examples.
- **Describe the current behavior** and **explain which behavior you expected to see instead** and why.
- **Include screenshots and animated GIFs** which help you demonstrate the steps or point out the part which the suggestion is related to.
- **Explain why this enhancement would be useful** to most users.
- **Specify which version of Image Renamer you're using.**

### Pull Requests

- Fill in the required template
- Do not include issue numbers in the PR title
- Include screenshots and animated GIFs in your pull request whenever possible
- Follow the Python styleguide
- Include tests for new features
- Document new code
- End all files with a newline

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/larsniet/image-renamer.git
   cd image-renamer
   ```
3. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e .
   pip install -r requirements.txt
   ```

4. Run the tests to make sure everything works:
   ```bash
   pytest
   ```

5. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

6. Make your changes and add tests for your changes
7. Run the tests to make sure everything still works:
   ```bash
   pytest
   ```

8. Push your branch and create a pull request:
   ```bash
   git push origin feature/your-feature-name
   ```

## Style Guide

This project uses flake8 and isort for code formatting. Make sure your code adheres to these guidelines:

```bash
# Install development tools
pip install flake8 isort black

# Format your code
isort .
black .

# Check your code
flake8 .
```

## Testing

- Tests are written using pytest
- All new code should include tests
- Run the test suite with `pytest`
- Check code coverage with `pytest --cov=imagerenamer` 