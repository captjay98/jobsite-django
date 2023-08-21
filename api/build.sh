!/usr/bin/bash
# exit on error
# set -o errexit


apt update -y && apt upgrade -y && apt install -y --no-install-recommends binutils libheif-dev libheif1 libproj-dev gdal-bin libgdal-dev python3-gdal

ldconfig
echo "FOUND THE DIRECTORY"
find / -name libheif.so.1

echo $LD_LIBRARY_PATH
echo "DIDN'T FIND THE FIlEPATH"

LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/
export LD_LIBRARY_PATH 
echo $LD_LIBRARY_PATH
echo "FOUND THE FILEPATH"
pip install --global-option=build_ext --global-option="-I/usr/include/gdal" GDAL==`gdal-config --version`


# pip install -r requirements.txt
# python manage.py collectstatic --no-input

# python manage.py makemigrations core
# python manage.py migrate core

# python manage.py makemigrations users
# python manage.py migrate users

# python manage.py makemigrations seekers
# python manage.py migrate seekers

# python manage.py makemigrations employers
# python manage.py migrate employers

# python manage.py makemigrations
# python manage.py migrate

