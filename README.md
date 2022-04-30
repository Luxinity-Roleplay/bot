# Luxinity Discord Server Bots / UCP System

[![Discord server](https://img.shields.io/discord/812150001089118210?label=Join%20our%20Discord%20Server%21)](https://discord.gg/U7nXFpDrXd) [![Build Production](https://img.shields.io/github/workflow/status/Luxinity-Roleplay/Luxinity-UCP/Build%20Production/master)](https://github.com/Luxinity-Roleplay/Luxinity-UCP/actions/workflows/build.yml) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Luxinity Roleplay Discord Server Bots & UCP System written in `dis-snek` (python)

#### Note:

Tidak disarankan untuk menjalankan monorepo ini secara langsung tanpa merubah codingan apapun (walaupun monorepo ini sudah Production Ready) karena monorepo ini telah didesign khusus hanya untuk Luxinity Roleplay. Repository ini dibuat publik hanya untuk media belajar/referensi.

## Testing/Workflows

### Docker

Monorepo ini sudah _Docker Ready_, anda hanya tinggal meng-pull container nya. Cek selengkapnya di [halaman ini!](https://github.com/Luxinity-Roleplay/Luxinity-UCP/pkgs/container/luxinity-ucp)

- Pastikan Docker anda sudah terinstall versi terbaru!
- Anda hanya butuh menjalankan command:

```bash
docker-compose up --detach
```

### Manual Install

- Download dan install Python versi terbaru (usahakan yg terbaru, jangan yang jadul)

**WAJIB PAKE `virtualenv`, Please check python docs for more info!**

```md
saya anggap kalian sudah setup "virtualenv"
```

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

Copyright ©️2022 Clemie McCartney ([mclemie#0001](https://discord.com/users/351150966948757504)). Licensed to Luxinity Roleplay.
