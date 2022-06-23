# Luxinity-UCP

[![Discord server](https://img.shields.io/discord/812150001089118210?label=Join%20our%20Discord%20Server%21)](https://discord.gg/U7nXFpDrXd) [![Build Production](https://img.shields.io/github/workflow/status/Luxinity-Roleplay/Luxinity-UCP/Build%20Production/master)](https://github.com/Luxinity-Roleplay/Luxinity-UCP/actions/workflows/build.yml) [![pre-commit](https://img.shields.io/github/workflow/status/Luxinity-Roleplay/Luxinity-UCP/precommit-action?label=pre-commit)](https://github.com/Luxinity-Roleplay/Luxinity-UCP/actions/workflows/pre-commit.yml) [![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Luxinity-Roleplay/Luxinity-UCP/master.svg)](https://results.pre-commit.ci/latest/github/Luxinity-Roleplay/Luxinity-UCP/master) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Luxinity Roleplay Discord Server Bots & UCP System made with [NAFF](https://github.com/Discord-Snake-Pit/NAFF).

Kunjungi [panduan resmi NAFF](https://naff.readthedocs.io/Guides/01%20Getting%20Started/) untuk memulai.

#### Note:

Tidak disarankan untuk menjalankan repository ini secara langsung tanpa merubah codingan apapun (walaupun repository ini sudah Production Ready) karena repository ini telah didesign khusus hanya untuk Luxinity Roleplay. Repository ini dibuat publik hanya untuk media belajar/referensi.

## Menjalankan Aplikasi

Ada beberapa cara untuk menjalankan aplikasi ini.

### Docker

Repository ini sudah _Docker Ready_, anda hanya tinggal meng-pull container nya. Cek selengkapnya di [halaman ini!](https://github.com/Luxinity-Roleplay/Luxinity-UCP/pkgs/container/luxinity-ucp)

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
PROJECT_NAME="Luxinity-UCP"
LOAD_DEBUG_COMMANDS=true # untuk production ready, ganti value ini ke false
DISCORD_TOKEN="masukkan bot token anda disini, ambil di https://discord.com/developers/applications"
DATABASE_HOST="masukkan mysql database host kamu disini"
DATABASE_USER="masukkan username mysql kamu disini"
DATABASE_PASSWORD="masukkan password mysql kamu disini"
DATABASE_NAME="masukkan nama mysql database kamu disini"
IP="ip server kamu, support domain dan ip"
PORT="port server samp kamu"
GITHUB_TOKEN="github personal access token kamu untuk meng-akses gist dan repository server"
GIST_ID="read-this-channel readme gist id"
GIST_ID2="ucp-manager readme gist id"
```

- anda sudah siap menjalankan botnya. untuk menjalankan botnya, gunakan perintah ini

```bash
py main.py
```

## Informasi Tambahan
Kami sudah siapkan konfigurasi [pre-commit](https://pre-commit.com) bawaan untuk merapihkan kodingan kalian.

Sangat direkomendasikan untuk menggunakan tool ini dengan menjalankan perintah berikut:

1) `pip install pre-commit`
2) `pre-commit install`

## License

Seluruh source code ini menggunakan lisensi GNU GPL 2.0, Mohon mencantumkan Copyright notice saat anda menggunakan code ini!

Copyright ©️2022 Clemie McCartney ([clemie#0001](https://discord.com/users/351150966948757504)). Licensed to Luxinity Roleplay.
