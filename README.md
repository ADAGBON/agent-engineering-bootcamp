# My Project

This is a Python project created with `uv` package manager.

## Setup

1. Create and activate virtual environment:
```bash
python -m uv venv
.\.venv\Scripts\activate  # On Windows
source .venv/bin/activate  # On Unix/MacOS
```

2. Install dependencies:
```bash
python -m uv pip install -r requirements.txt
```

## Project Structure

```
my_project/
├── .venv/              # Virtual environment
├── src/               # Source code
│   └── __init__.py
├── tests/             # Test files
│   └── __init__.py
├── requirements.txt   # Project dependencies
└── README.md         # Project documentation
``` 