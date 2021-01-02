# chmod +x open_apps.sh
# ./open_apps.sh

gnome-terminal -- sh -c 'cd Proxy; flask run; exec bash'
gnome-terminal -- sh -c 'cd UserManager; flask run; exec bash'
gnome-terminal -- sh -c 'cd Videos; flask run; exec bash'
gnome-terminal -- sh -c 'cd Qa; flask run; exec bash'
gnome-terminal -- sh -c 'cd Stats; flask run; exec bash'
gnome-terminal -- sh -c 'cd Logs; flask run; exec bash'
