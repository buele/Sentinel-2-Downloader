export PYTHONPATH=/usr/downloader
echo "HELLO MY WORLD"
#python3.4 -m unittest discover --verbose
python3.4 src/downloader_manager/init.py
nohup supervisord -c /usr/downloader/src/downloader_manager/config/supervisord.conf   &

sleep infinity