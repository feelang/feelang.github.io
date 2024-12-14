---
layout: single
title: Build Python into a Binary File
categories: programming
tags:
    - Python
---

If you want to build your **Wafu CMS** project into a binary file, it’s important to structure the project in a way that’s clean, maintainable, and compatible with tools like PyInstaller. Here's a recommended project structure for your binary-focused Python project:

## 1. Project Structure

```
wafu_cms/
├── wafu_cms/               # Main package directory
│   ├── __init__.py         # Marks the directory as a Python package
│   ├── cli.py              # CLI entry point for your app
│   ├── core.py             # Core logic and functionality
│   ├── utils.py            # Helper functions (optional)
│   └── data/               # Static resources (e.g., templates, config files)
│       └── sample.txt      # Example of a resource file
├── tests/                  # Test cases for your app
│   ├── test_core.py        # Tests for core logic
│   └── test_cli.py         # Tests for CLI functionality
├── dist/                   # Output directory for binaries (created by PyInstaller)
├── build/                  # Temporary build files (created by PyInstaller)
├── wafu_cms.spec           # PyInstaller spec file (auto-generated)
├── setup.py                # Optional: For packaging as a Python package
├── requirements.txt        # Dependencies for your project
├── README.md               # Project description
└── LICENSE                 # License file
```

## 2. Explanation of Each Component

### `wafu_cms/` (Main Package)

This is your app's main directory where all logic is implemented.

- **`cli.py`**:
  Contains the CLI entry point. For example:
  ```python
  import argparse
  from wafu_cms.core import process_articles

  def main():
      parser = argparse.ArgumentParser(description="Wafu CMS: A Japanese content manager.")
      parser.add_argument("--source", help="Source directory of articles", required=True)
      parser.add_argument("--output", help="Output directory for formatted content", required=True)
      args = parser.parse_args()

      process_articles(args.source, args.output)

  if __name__ == "__main__":
      main()
  ```

- **`core.py`**:
  Implements the main logic of your app (e.g., formatting articles, handling data).
  ```python
  def process_articles(source_dir, output_dir):
      print(f"Processing articles from {source_dir} to {output_dir}...")
      # Your logic here
  ```

- **`data/`**:
  Stores static resources (e.g., templates, configurations) that your app might use.

### `tests/`

Contains unit tests for your project, ensuring reliability during development. Use tools like `pytest` to write and run your tests.

## 3. Writing a PyInstaller-Compatible Script

The **entry point** for your binary is the `cli.py` file, and PyInstaller needs this script as input. The `main()` function in `cli.py` will serve as the app’s starting point.

Example Command for PyInstaller:
```bash
pyinstaller --onefile --name wafu wafu_cms/cli.py
```

## 4. Including Static Resources in the Binary

If your app requires static files (e.g., templates, configurations), you must explicitly include them when building the binary.

### Update `cli.py` or `core.py` to Use `pkg_resources`

Use `pkg_resources` to access files within your package:

```python
import pkg_resources

def get_sample_data():
    data_path = pkg_resources.resource_filename("wafu_cms", "data/sample.txt")
    with open(data_path, "r") as f:
        return f.read()
```

### Pass Static Files to PyInstaller

Add `--add-data` when running PyInstaller:

```bash
pyinstaller --onefile --name wafu --add-data "wafu_cms/data:./data" wafu_cms/cli.py
```

## 5. Output Binaries

- The binary will be placed in the `dist/` directory (e.g., `dist/wafu`).
- Move the binary to a directory in your `$PATH` for global usage:
  ```bash
  mv dist/wafu /usr/local/bin
  ```

## 6. Project Dependencies

List dependencies in `requirements.txt` so they can be easily installed during development:
```
argparse
pkg_resources
```

Install them locally for development:
```bash
python3 -m pip install -r requirements.txt
```

## 7. Example Directory After Build

After building with PyInstaller, your project might look like this:

```
wafu_cms/
├── dist/                   # Contains the binary file (`wafu`)
│   └── wafu
├── build/                  # Temporary build files (can be ignored)
├── wafu_cms/               # Main package directory
│   ├── __init__.py
│   ├── cli.py
│   ├── core.py
│   ├── utils.py
│   └── data/
│       └── sample.txt
├── wafu_cms.spec           # PyInstaller spec file
├── setup.py
├── requirements.txt
├── README.md
└── LICENSE
```

This structure is clean, modular, and optimized for maintainability and binary builds.
