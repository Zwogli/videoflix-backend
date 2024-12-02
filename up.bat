git pull
git add .
git commit -m "%*"
git push
ssh mathi@34.159.49.18 "cd /home/mathiaskohler91/projects/videoflix-backend/ && git pull"
ssh mathi@34.159.49.18 "sudo supervisorctl restart videoflix_gunicorn"
ssh mathi@34.159.49.18 "sudo supervisorctl restart videoflix-rq-worker"
ssh mathi@34.159.49.18 "sudo /usr/sbin/nginx -s reload"