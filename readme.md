## CLI
```
--------
Database:
* migrate => Migrates database
-------- 
Misc:
* env => Creates env from defaults
    """
```

## Migration
```
docker exec -it deadbox_app bash &&
alembic init migrations
alembic revision --autogenerate -m "Initial migration" # Create new migration
alembic upgrade head # Command for applying migration
alembic upgrade head --sql # Outputs SQL table for updating ect
```