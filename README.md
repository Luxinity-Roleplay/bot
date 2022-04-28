# Luxinity Discord Server Bots
Luxinity discord server bots written in python

## Installation

- Download dan install Python versi terbaru (usahakan yg terbaru, jgn yg jadul)

**WAJIB PAKE `virtualenv`, Please check python docs for more info!**
**saya anggap kalian sudah setup `virtualenv`*

- Install dependencies package nya menggunakan perintah ini
```bash
pip install -r ".\requirements.txt"
```

- sebelum menjalankan kode ini, buatlah satu file `.env` di folder root dan isi filenya menggunakan contoh berikut
```env
BOT_TOKEN="masukkan bot token anda disini, ambil di https://discord.com/developers/applications"
DATABASE_HOST="masukkan mysql database host kamu disini"
DATABASE_USER="masukkan username mysql kamu disini"
DATABASE_PASSWORD="masukkan password mysql kamu disini"
DATABASE_NAME="masukkan nama mysql database kamu disini"
IP="ip server kamu, support domain dan ip"
PORT="port server samp kamu"
```

- anda sudah siap menjalankan botnya. untuk menjalankan botnya, gunakan perintah ini
```bash
py main.py
```

## License
Seluruh source code ini menggunakan lisensi GNU GPL 2.0, Mohon mencantumkan Copyright notice saat anda menggunakan code ini!

Copyright, ©️2022 Clemie McCartney ([mclemie#0001](https://discord.com/users/351150966948757504)).
