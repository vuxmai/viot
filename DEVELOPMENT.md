# Development Guide

This guide will help you set up your development environment for the Viot project.

## Development localhost with domain

To avoid some problems with cookies that need a subdomain, we will use a custom local domain `viot.local`.

You need to add this domain to your local hosts file:
```
127.0.0.1 api.viot.local
127.0.0.1 flower
127.0.0.1 mailpit
127.0.0.1 emqx
```

## Pre-commit and code linting
This project uses [pre-commit](https://pre-commit.com/) for code linting and formatting.
When you commit, pre-commit hooks will be run automatically. It ensures that code is consistent across the project.

You can find the pre-commit configuration in the `.pre-commit-config.yaml` file at the root of the project.

### Install pre-commit
To install globally you should follow the [official pre-commit installation guide](https://pre-commit.com/#install).

After installation, you can install the pre-commit hooks in the repository with:
```
pre-commit install
```

Now when you commit, pre-commit hooks will be run automatically.

If you want to run pre-commit manually, you can use:
```
pre-commit run --all-files
```

## Backend
For more information about the backend, please refer to the [Viot README.md](viot/README.md) file.
