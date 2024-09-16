git pull
git add .
git commit -m "%*"
git push
ssh zwogli\zwogli@35.234.78.80 "cd /home/mathiaskohler91/projects/videoflix-backend/ && git pull"
ssh zwogli\zwogli@35.234.78.80 "sudo supervisorctl restart videoflix_gunicorn"
ssh zwogli\zwogli@35.234.78.80 "sudo systemctl reload nginx"
