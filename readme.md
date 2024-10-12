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

## Discord Oauth Setup

- Login to https://discord.com/developers
- Create a new application
- Take note of your Client Secret & Client ID and add to .env file
- Change your callback to the correct location ie http://localhost:8000/callback