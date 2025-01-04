echo -e "import datetime\nwith open('./log.txt', 'a') as f:\n    f.write(f\"{datetime.datetime.now().ctime()}:INFO: INSTALL.SH\\\x0a\")" | python3
sudo cp keypan.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl start keypan.service
sudo systemctl enable keypan.service