#!/usr/bin/env bash

SQL_FILE="$1"

if [ ! -f "$SQL_FILE" ]; then
    echo "SQL file not found: $SQL_FILE"
    exit 1
fi

set -a
source .env
set +a

cat "$SQL_FILE" | podman exec -i \
-e ASE_USER="$ASE_USER" \
-e ASE_PASSWORD="$ASE_PASSWORD" \
-e ASE_DATABASE="$ASE_DATABASE" \
-e ASE_SERVER="$ASE_SERVER" \
ase16 bash -c \
'source /opt/sybase/SYBASE.sh &&
 export DSQUERY="$ASE_SERVER" &&
 isql -U "$ASE_USER" -P "$ASE_PASSWORD" -D "$ASE_DATABASE"' \