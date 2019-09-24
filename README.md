**SputnikIDE** - это веб-интерфейс для работы с моделью малого космического аппарата.


Для управления платой необходимо поключиться к ней через ssh: \
ip: 192.168.42.1 \
Логин: pi

Подгатовка к установке:
```
sudo apt-get update
sudo apt-get install python3
sudo apt-get install python3-pip
sudo apt-get install git
sudo apt-get install unzip
```

Установка:
```
cd ~
git clone https://github.com/andrey99429/Sputnik_IDE.git
cd Sputnik_IDE
sudo ./installserver
./runserver
```

Для автозапуска сервера необходимо изменить файл автозапуска:
```
sudo nano /etc/rc.local
```
Внутри файла прописать:
```
sudo -u pi /home/pi/Sputnik_IDE/runserver &
```

Для обновления системы:
```
cd ~/Sputnik_IDE
git pull
```

В системе есть адмиристратор. Логин и пароль совпадают с логином и паролем пользователя платы.
Панель администратора находиться по адресу: admin/

В системе есть пользователь: \
Логин: user \
Пароль: sputnik
