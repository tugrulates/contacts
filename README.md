# A template Python project (**template-python**)

[![CI](https://github.com/tugrulates/template-python-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/tugrulates/template-python-cli/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/tugrulates/template-python/branch/main/graph/badge.svg?token=RLPSDZQHII)](https://codecov.io/gh/tugrulates/template-python)
[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](https://github.com/python/mypy)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![License - MIT](https://img.shields.io/badge/license-MIT-9400d3.svg)](https://spdx.org/licenses/)

This project contains sample code for a Python CLI app. It attempts to create a Python development environment that is simple but allows a fast development cycle to produce high-quality code. This is inspired by the _“Boring Python”_ posts [^1][^2] by [James Bennett](https://www.b-list.org/).

[^1]: [Boring Python: dependency management](https://www.b-list.org/weblog/2022/may/13/boring-python-dependencies/)
[^2]: [Boring Python: code quality](https://www.b-list.org/weblog/2022/dec/19/boring-python-code-quality/)

## ✨ Features

The following libraries and frameworks are configured and working out of the box.

-   [hatch](https://github.com/pypa/hatch) (MIT License): Project and dependency management.
-   [flake8](https://github.com/PyCQA/flake8) (MIT License): Code linter, with several plugins configured.
-   [black](https://github.com/psf/black) (MIT License): Code style formatter.
-   [isort](https://github.com/PyCQA/isort) (MIT License): Import organizer.
-   [mypy](https://github.com/python/mypy) (MIT License): Static typing.
-   [bandit](https://github.com/PyCQA/bandit) (Apache License): Security linter.
-   [pytest](https://github.com/pytest-dev/pytest) (MIT License): Tests.
-   [pytest-cov](https://github.com/pytest-dev/pytest-cov) (MIT License): Test coverage.
-   [pre-commit](https://github.com/pre-commit/pre-commit) (MIT License): Git hooks for sanity checks.
-   [typer](https://github.com/tiangolo/typer) (MIT License): Library for parsing CLI arguments and storing configuration.
-   [GitHub Actions](https://github.com/features/actions): Continuous integration.
-   [GitHub Dependabot](https://github.com/features/security): Automated dependency updates.
-   [EditorConfig](https://editorconfig.org/): Generic editor config.
-   Some niceties for [VS Code](https://code.visualstudio.com/) (see below).

## ⚙️ Setup

Do either of the following.

-   **Use this template** button on GitHub to create a new project
-   **Open in a codespace** button on GitHub to start playing with the project
-   Download, copy, or clone the project

### Visual Studio Code

You can skip this section if you prefer an editor that is not VSCode.

The fastest route to productivity will come from opening this project remotely in a [Dev Container](https://containers.dev/). The only requirement is [Docker Desktop](https://www.docker.com/products/docker-desktop/). Everything else will be automatically installed into the Dev Container. A Docker account is not needed. If you open the project locally, VSCode will prompt to open inside the configured Dev Container.

Once the container is ready, the project will be buildable, lintable, and testable. Linting and formatting will be automatically done as you save. Check the _Problems_ tab for lint issues. Test cases will be automatically discovered in the _Testing_ tab. You can run all the tests or start debugging from here.

If running locally instead, you will need Python3 with [hatch](https://github.com/pypa/hatch) (`pip install hatch`). In this scenario, it might be worthwhile to do the point VSCode to the Python interpreter of the dev environment in the project (`hatch run dev:python -c "import sys;print(sys.executable)"`).

### Other editors

Skip this section if you are using Dev Containers or Codespaces.

All following setup is optional. They are meant to increase life-of-quality during development.

-   To run 'hatch' commands (see below):

```shell
pip install hatch
```

-   Install and enable commit hooks for git

```shell
pip install pre-commit && pre-commit install-hooks
```

## 💻 Development cycle

-   Run your CLI app

```shell
hatch run my-cli --help
```

-   Run lint checks

```shell
hatch run dev:lint
```

-   Run all tests

```shell
hatch run test:test
```

-   Run pre-commit checks on all files

```shell
pre-commit run --all-files
```

Check out the example app code to get accustomed to the setup. You will need to change any name that starts with “my”, like _my description_.

## 🤖 Continuous integration

There is a robust CI pipeline already setup. It contains the following jobs.

-   **lint**: Checks that all lint checkers are happy and pre-commit would succeed.
-   **test**: Checks that all unit tests are passing on Linux, Mac, and Windows, with different Python versions.
-   **coverage**: Checks that code coverage is above 80%. Optionally, uploads coverage to [Codecov](https://codecov.io).
-   **build**: Checks that a wheel is buildable and runs standard smoke tests against it.

Make sure your integration flow includes pull requests. Merge PRs only when the CI is successful, and you will have a good integration setup. Commit to main directly, and you will become a sad developer.

## 📦 Dependency management

All dependencies are pinned to a specific version. Dependabot will send occasional pull requests to update dependencies to available versions. Merge them only when CI is passing.

This is not a strict implementation of reproducible builds, since indirect dependencies are not locked to specific versions. If an indirect dependency has a new version that is incompatible with our app, it might break our integration. This will be remedied with a lock file once _hatch_ supports locking dependencies.

## 👋 Help and contributions

I hope you will find this template useful. You can create an issue if you have a question, or if something is not working right for you. PRs are welcome if you would like to fix or add anything.

## 🚩 Roadmap

The project scaffolds a basic CLI application. You can build upon this for your own, or you can also strip the CLI parts altogether to build a different type of Python package. Actual templatign a la [Cookiecuter](https://www.cookiecutter.io/) could be useful.

This project does not yet include an end-to-end test. It would be an improvement to automatically download CI artifacts from the main branch and run tests against them.
