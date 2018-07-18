#!/usr/bin/env bash

ROOT=$(pwd)

command -v python >/dev/null 2>&1 || { echo >&2 "Python no esta instalado. Instale una version mayor ó igual a la 2.7\nAbortando...\n"; exit 1; }

function check_python_version()
{
    PYTHON_VERSION="$(python -c 'import sys;version_arr = sys.version_info[:]; sys.stdout.write(str(version_arr[0]) + "." + str(version_arr[1]))')"
    if [[ "$PYTHON_VERSION" =~ [2-9].[7-9][0-9]*|[3-9].[0-9]* ]]; then
        echo "La version python cumple con la version minima"
    else
        echo "La version de Python minima requerida es 2.7\nPor favor, actualice a una version mas reciente.\nAbortando..."
        exit 1
    fi
}

check_python_version

python2.7 setup.py py2app
PROGRAM_DIRECTORY="$ROOT/dist/Sync Select Files.app"

if [ -d "$PROGRAM_DIRECTORY" ]; then
    cp -R "${PROGRAM_DIRECTORY}" "/Applications"
    echo "Programa instalado correctamente."
else
    echo "Ocurrio un error al buscar el programa instalado."
fi

EXECUTABLE_STRING='
open /Applications/Sync\ Select\ Files.app
'

EXECUTABLE_DIR='/usr/local/bin/ssf'

if [ -r ${EXECUTABLE_DIR} ]; then
    echo '\nNo se puede crear el ejecutable, ya existe un programa con el mismo nombre.'
    echo 'Abortando...\n'
    exit 1
fi

echo ${EXECUTABLE_STRING} > ${EXECUTABLE_DIR}
chmod 755 ${EXECUTABLE_DIR}

