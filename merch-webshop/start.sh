nohup python3 flask_app.py > /dev/null 2>&1 &
pgrep -f "flask_app.py"
echo "Running"
