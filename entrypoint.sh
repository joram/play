#!/bin/sh

cat > /etc/nginx/nginx.conf <<EOF
events {
  worker_connections 1024;
}
http {
  charset           utf-8;
  include           /etc/nginx/mime.types;
  server_tokens     off;
  gzip              on;
  gzip_vary         on;
  gzip_proxied      any;
  gzip_comp_level   6;
  gzip_buffers 16   8k;
  gzip_http_version 1.1;
  gzip_min_length   256;
  gzip_types        text/plain text/css application/json application/x-javascript
                    text/javascript application/javascript text/xml application/xml
                    application/xml+rss application/vnd.ms-fontobject
                    application/x-font-ttf font/opentype image/svg+xml
                    image/x-icon;
  server {
    listen 8000;
    server_name play.battlesnake.io;
    location /static/ {
      alias /static/;
    }
    location / {
      include uwsgi_params;
      proxy_pass          http://127.0.0.1:8080/;
      proxy_redirect      off;
      proxy_set_header    Host \$host;
      proxy_set_header    X-Forwarded-Host \$server_name;
      # For testing locally
      # proxy_set_header    X-Forwarded-Host 127.0.0.1:8000;
      proxy_set_header    X-Forwarded-Proto \$scheme;
    }
  }
}
EOF

cat > /etc/supervisord.conf <<EOF
[supervisord]
nodaemon = true

[program:nginx]
command = /usr/sbin/nginx -g 'daemon off;'
startsecs = 5
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0

[program:gunicorn]
command = /usr/bin/gunicorn wsgi:application --name play --workers 3 --bind 0.0.0.0:8080
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0
EOF

./manage.py migrate
./manage.py collectstatic --noinput

exec supervisord -c /etc/supervisord.conf
