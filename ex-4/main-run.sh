sudo apt update
sudo apt install nginx
cd /etc/nginx
sudo apt install gedit

echo "First VM IP: $1"
echo "Second VM IP: $2"

cat >> /etc/nginx/nginx.conf <<EOF
http {
    upstream backend {
        server $1;   #vm1
        server $2;   #vm2
    }
}
EOF

cd sites-available

SOURCE_DEFAULT="~/gitrepo/ex-4/default"
TARGET_DEFAULT="/etc/nginx/sites-available/default"
cat "$SOURCE_FILE" > "$TARGET_FILE"

systemctl restart nginx