# Fortune migration to ES tool


Create index:

```
PYTHONPATH=. python -m elastic.app \
    --create test20 \
    --mapping data/fortune-mapping.json
```

Populate index with data:

```
PYTHONPATH=. python -m elastic.app \
    --populate test20
```

