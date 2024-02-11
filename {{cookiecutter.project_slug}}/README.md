# {{ cookiecutter.project_name }}

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/{{ cookiecutter.project_slug }}?style=flat-square)

{{ cookiecutter.project_description }}


## Development installation

```bash
cd /path/to/{{ cookiecutter.project_slug }}
python3 -m venv .venv
source .venv/bin/activate
poetry install
```

## Running

```bash
task build
task run
```

## Usage

```bash
flowctl apply -p workflows/
flowctl workflow run example_workflow
```

## Testing

```bash
task unit-tests
```

## Documentation

```bash
task build-docs
task run-docs
```