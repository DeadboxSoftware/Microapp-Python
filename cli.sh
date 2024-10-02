RED='\033[0;31m'
NC='\033[0m' # No Color
BGreen='\033[1;32m'


if [ -z "$1" ]; then
    printf """${BGreen}cli.sh                 
    ${RED}
--------
Database:
* migrate => Migrates database
-------- 
Misc:
* env => Creates env from defaults
    """
fi

if [ "$1" == "env" ]; then
	cp example.env .env
	# cp app/example.env app/.env
elif [ -n "$1" ]; then
    docker exec "fastapi_app" python cli.py "$@"
fi
