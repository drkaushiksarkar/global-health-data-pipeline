# Global Health Data Pipeline

Scalable ETL pipeline for ingesting, normalizing, and serving 150+ global health data sources with automated quality checks.

## Architecture

```
global-health-data-pipeline/
  src/           # Core modules
  tests/         # Unit and integration tests
  config/        # Configuration files
  docs/          # Documentation
```

## Modules

- **etl_orchestrator**: Core etl orchestrator functionality
- **data_normalizer**: Core data normalizer functionality
- **source_connector**: Core source connector functionality
- **quality_checker**: Core quality checker functionality
- **schema_mapper**: Core schema mapper functionality

## Quick Start

```bash
pip install -r requirements.txt
python -m global_health_data_pipeline.main
```

## Testing

```bash
pytest tests/ -v
```

## License

MIT License - see LICENSE for details.
