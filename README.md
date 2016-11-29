# proj1

apt-get install git

git clone https://github.com/noris7012/proj1.git

apt-get update

apt-get install python-pip

pip install Django==1.8.5

python manage.py migrate

apt-get install python-dev

pip install uwsgi

mkdir -p /etc/uwsgi/sites

apt-get install nginx

file : /etc/uwsgi/sites/proj1.ini

file : /etc/init/uwsgi.conf

file : /etc/nginx/sites-available/proj1

ln -s /etc/nginx/sites-available/proj1 /etc/nginx/sites-enabled/

rm /etc/nginx/sites-enabled/default

chmod 755 /root

service nginx configtest

service nginx restart

service uwsgi start

python==2.7.12



https://github.com/zkyz/NanumBarunGothic-webfont
