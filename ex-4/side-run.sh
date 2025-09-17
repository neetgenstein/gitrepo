sudo apt update
sudo apt install apache2
cd /var/www/html
sudo apt install gedit

cat > "/var/www/html/index.html" <<EOF
<!DOCTYPE html>
<html>
<head>
    <title>Vanakkam</title>
</head>
<body>
    <h1>This is me running my servers</h1>
    <p>I am cool.</p>
</body>
</html>
EOF
