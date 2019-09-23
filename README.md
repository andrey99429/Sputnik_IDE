**SputnikIDE** - это веб-интерфейс для работы с моделью малого космического аппарата.


Для управления платой необходимо поключиться к ней через ssh: \
ip: 192.168.42.1 \
Логин: pi \

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
./installserver
./runserver
```

В системе есть пользователь по умолчанию: \
Логин: \
Пароль:
