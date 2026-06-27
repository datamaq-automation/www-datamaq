# Datamaq

 **FastAPI Jinja2 SSR** (SEO First).

## Quick Start

1. `pip install -r requirements.txt`
2. `./run.sh`

## Tests

El repositorio incluye un hook `pre-push` que ejecuta los tests automáticamente:

```bash
ln -s ../../scripts/pre-push.sh .git/hooks/pre-push
```

Para correr los tests manualmente:

```bash
export PYTHONPATH=$PYTHONPATH:.
pytest --cov=src --cov-report=term-missing tests/
```

## Despliegue

El despliegue actual es **manual** mediante `scripts/deploy-server.sh`. Requiere completar `scripts/.env.deploy` a partir de `scripts/.env.deploy.example`.

Ver la guía completa en [`docs/CD.md`](docs/CD.md).

## CI/CD

GitHub Actions está planificado pero aún no implementado. El roadmap de tareas está en [`docs/TODO.md`](docs/TODO.md).

## Documentación clave

- [Estrategia SEO](docs/seo_strategy.md)
- [Arquitectura y macros](docs/architecture.md)
- [Guía de despliegue](docs/CD.md)
- [Tareas pendientes](docs/TODO.md)
- [Guía de estilo](GEMINI.md)
