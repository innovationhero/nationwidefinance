git add .
git commit -a -m "$1"
git push
ssh admin@dev.webiken.net "cd ~/nationwidefinance/;git pull"
