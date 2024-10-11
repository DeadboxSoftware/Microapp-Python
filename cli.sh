RED='\033[0;31m'
NC='\033[0m' # No Color
BGreen='\033[1;32m'

source ".env"

if [ -z "$1" ]; then
    printf """${BGreen}cli.sh                 
    ${RED}
--------
Database:
* migrate => Migrates database
* seed => Migrates database
--------
Users:
newuser => --password --email
-------- 
Misc:
* env => Creates env from defaults
    """
fi

if [ "$1" == "env" ]; then
	cp example.env .env
	cp app/.env.example app/.env
elif [ -n "$1" ]; then
    docker exec "$APP_NAME" python cli.py "$@"
fi
