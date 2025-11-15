# Contributing to Bolt Task Automation

Thank you for your interest in contributing to Bolt! We welcome contributions from the community and are pleased to have you join us in making Bolt better.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Test-Driven Development](#test-driven-development)
- [Making Changes](#making-changes)
- [Testing Requirements](#testing-requirements)
- [Coding Standards](#coding-standards)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Documentation](#documentation)
- [Community](#community)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment. We are committed to providing a welcoming experience for everyone, regardless of background or identity.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/bolt.git
   cd bolt
   ```
3. **Add the upstream repository**:
   ```bash
   git remote add upstream https://github.com/abantos/bolt.git
   ```

## Development Setup

Bolt uses [uv](https://docs.astral.sh/uv/) for dependency management. Follow these steps to set up your development environment:

1. **Install uv** (if not already installed):
   
   Follow the installation instructions for your operating system at: https://docs.astral.sh/uv/getting-started/installation/

2. **Sync dependencies**:
   ```bash
   uv sync
   ```

3. **Verify your setup** by running the tests:
   ```bash
   uv run bolt ut
   ```

### Development Dependencies

The project includes several development dependencies:
- **pytest**: Test framework
- **pytest-cov**: Code coverage plugin
- **assertpy**: Fluent assertion library
- **conttest**: Continuous testing
- **sphinx**: Documentation generator
- **coverage**: Code coverage measurement

## Test-Driven Development

**Bolt follows a Test-Driven Development (TDD) approach.** This means:

### TDD Workflow

1. **Write a failing test first** - Before implementing any feature or fix:
   - Write a test that describes the expected behavior
   - Run the test and confirm it fails (red phase)

2. **Write the minimum code to pass** - Implement just enough code to make the test pass:
   - Focus on making the test green, not on perfection
   - Avoid over-engineering at this stage

3. **Refactor** - Improve the code while keeping tests green:
   - Clean up duplication
   - Improve naming and structure
   - Ensure all tests still pass

### TDD Benefits in Bolt

- **Better design**: Tests first leads to more modular, testable code
- **Living documentation**: Tests serve as examples of how to use the code
- **Confidence**: Comprehensive test coverage enables safe refactoring
- **Fewer bugs**: Issues are caught early in development

### Example TDD Cycle

```python
# 1. Write a failing test (RED)
def test_task_executes_with_config():
    config = {"param": "value"}
    task = MyNewTask()
    result = task(config)
    assert result.success is True

# 2. Write minimal code to pass (GREEN)
class MyNewTask(Task):
    def execute(self):
        return Result(success=True)

# 3. Refactor (REFACTOR)
# Clean up, add error handling, improve names, etc.
```

## Making Changes

### Branch Naming

Create a descriptive branch for your changes:

```bash
git checkout -b feature/add-new-task-type
git checkout -b fix/issue-123-config-parsing
git checkout -b docs/improve-getting-started
```

Use prefixes:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test improvements

### Before You Code

1. **Check existing issues** - Search for related issues or discussions
2. **Open an issue** for major changes - Discuss your approach before investing significant time
3. **Keep changes focused** - One feature or fix per pull request
4. **Update from upstream** regularly:
   ```bash
   git fetch upstream
   git rebase upstream/master
   ```

## Testing Requirements

### Unit Test Requirements

**All code contributions MUST include unit tests.** Pull requests without appropriate tests will not be merged.

#### Test Coverage Standards

- **Minimum coverage**: 75% (enforced by CI)
- **Target coverage**: 85% or higher
- **New code**: Must have 100% coverage for new modules/features
- **Bug fixes**: Must include a test that reproduces the bug

#### Writing Unit Tests

Tests are located in the `test/` directory and use `pytest` and `assertpy`:

```python
import unittest
from assertpy import assert_that
from bolt.api import Task

class TestMyFeature(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.config = {"param": "value"}
        
    def test_feature_does_something(self):
        """Test should have a descriptive name and docstring"""
        # Arrange
        task = MyTask()
        
        # Act
        result = task(self.config)
        
        # Assert
        assert_that(result).is_not_none()
        assert_that(result.success).is_true()
        
    def test_feature_handles_error_condition(self):
        """Test error cases and edge conditions"""
        with self.assertRaises(RequiredConfigurationError):
            task = MyTask()
            task({})  # Missing required config
```

#### Test Organization

- Mirror the source code structure in `test/`
- Name test files as `test_<module>.py`
- Group related tests in test classes
- Use descriptive test names that explain the behavior being tested

#### Running Tests

```bash
# Run all unit tests
uv run bolt ut

# Run tests with coverage report
uv run bolt lcov

# Run continuous testing (watches for changes)
uv run bolt ct

# Run specific test file
uv run pytest test/test_api.py

# Run specific test
uv run pytest test/test_api.py::TestTask::test_specific_behavior
```

### Test Quality Guidelines

- **Test one thing** - Each test should verify a single behavior
- **Use AAA pattern** - Arrange, Act, Assert
- **Independent tests** - Tests should not depend on each other
- **Fast tests** - Unit tests should run quickly
- **Readable tests** - Use clear names and avoid complex logic in tests
- **Test edge cases** - Include boundary conditions and error scenarios

## Coding Standards

### Python Style Guide

- Follow **PEP 8** style guidelines
- Use **4 spaces** for indentation (no tabs)
- Maximum line length: **79 characters** (PEP 8 standard)
- Use meaningful variable and function names

### Code Quality

- Write **clear, self-documenting code**
- Add **docstrings** for modules, classes, and public methods
- Keep functions **small and focused** (Single Responsibility Principle)
- Avoid **premature optimization**
- Handle **errors gracefully** with appropriate exceptions

### Documentation Strings

```python
def register_task(name, dependencies=None):
    """Register a task with optional dependencies.
    
    Args:
        name (str): The name of the task to register.
        dependencies (list, optional): List of task names this task depends on.
        
    Returns:
        bool: True if registration was successful.
        
    Raises:
        TaskRegistrationError: If a task with the same name already exists.
        
    Example:
        >>> register_task('build', ['clean', 'compile'])
        True
    """
```

## Commit Messages

Write clear and meaningful commit messages:

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `style`: Code style changes (formatting, no logic change)
- `chore`: Maintenance tasks

### Examples

```
feat(tasks): add support for async task execution

Implement AsyncTask base class that allows tasks to run
asynchronously using Python's asyncio library.

Closes #123
```

```
fix(config): handle missing optional parameters correctly

Previously, optional parameters would raise an error if not
provided in config. Now they properly default to None.

Fixes #456
```

## Pull Request Process

### Before Submitting

1. **Write tests first** (TDD approach)
2. **Ensure all tests pass**: `uv run bolt ut`
3. **Check code coverage**: `uv run bolt lcov`
4. **Update documentation** if needed
5. **Run the build locally**: Check that documentation builds successfully
6. **Rebase on latest master**: `git rebase upstream/master`

### Submitting Your PR

1. **Push your branch** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request** on GitHub

3. **Fill out the PR template** completely:
   - Provide a clear summary of changes
   - Reference related issues
   - Describe how you tested the changes
   - Note any breaking changes

4. **Respond to feedback** - Be open to suggestions and iterate on your changes

### PR Review Process

- **CI must pass** - All automated checks must be green
- **Code coverage** must meet minimum thresholds (75%)
- **At least one approval** from a maintainer is required
- **All conversations resolved** before merging

### What Happens After Submission

1. Automated tests run via GitHub Actions
2. Code coverage is calculated and reported
3. Maintainers review your code
4. You may be asked to make changes
5. Once approved, a maintainer will merge your PR

## Reporting Bugs

### Before Reporting

- **Search existing issues** to avoid duplicates
- **Test with the latest version** of Bolt
- **Verify it's not a configuration issue**

### Bug Report Template

```markdown
**Description**
A clear description of the bug.

**Steps to Reproduce**
1. Step one
2. Step two
3. Step three

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- Bolt version: 
- Python version:
- OS:

**Additional Context**
Any other relevant information.
```

## Suggesting Enhancements

We welcome feature suggestions! Please:

1. **Check existing issues** for similar proposals
2. **Open a new issue** with the `enhancement` label
3. **Describe the use case** - Why is this needed?
4. **Propose a solution** - How might it work?
5. **Consider alternatives** - Are there other approaches?

## Documentation

Documentation is as important as code. Please update documentation when:

- Adding new features
- Changing existing behavior
- Fixing bugs that were caused by misleading docs

### Documentation Location

- **User documentation**: `docs/source/`
- **API documentation**: Docstrings in source code
- **README**: High-level overview and quick start
- **CONTRIBUTING**: This file

### Building Documentation Locally

```bash
uv run sphinx-build -M html docs/source docs/build
```

View the built documentation at `docs/build/html/index.html`.

## Community

### Getting Help

- **Documentation**: https://bolt-task-automation.readthedocs.io
- **GitHub Issues**: For bug reports and feature requests
- **Discussions**: For questions and general discussion

### Recognition

All contributors are recognized in our release notes and commit history. Thank you for helping make Bolt better!

## Questions?

Don't hesitate to ask questions! Open an issue with the `question` label, or reach out to the maintainers.

---

**Thank you for contributing to Bolt Task Automation!** 🚀