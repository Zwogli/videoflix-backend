git pull
git add .
git commit -m "%*"
git push
ssh mathi@35.234.78.80 "cd /home/mathiaskohler91/projects/videoflix-backend/ && git pull"
ssh mathi@35.234.78.80 "sudo supervisorctl restart videoflix_gunicorn"
ssh mathi@35.234.78.80 "sudo supervisorctl restart videoflix-rq-worker"
ssh mathi@35.234.78.80 "sudo /usr/sbin/nginx -s reload"

