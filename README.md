![Let's Download !](./banner.png "DownloadIn")

<div align="center">
    <h1> Linkedin Downloader Bot </h1>
</div>

<div align="center">
    <strong>Telegram-LinkedIn based bot to download media from LinkedIn and receive them within Telegram</strong>
</div>

<br>

<div align="center">
  <a href="https://github.com/python/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black">
  </a>
</div>

<hr>

## # Install With Docker
Soon...

## # Manual Install

You need `mysql` installed and running on your machine. 

#### - Create a python virtual environment ( `venv` ) and activate it
```bash
python3 -m venv venv
source venv/bin/activate
```
#### - Install requirements
```bash
pip install -r requirement.txt
```

#### - Create a copy of settings.py.sample
```bash
cp settings.py.sample settings.py
```

#### - Edit `settings.py` and fill up the required information ( you can find the help table of `settings.py` below )
#### - Run the app
```bash
python main.py
```

## # Help table of `settings.py`

| Key            | Description                                                                                      |
|----------------|--------------------------------------------------------------------------------------------------|
| **# DATABASE** |                                                                                                  |
| USER           | MySQL database username                                                                          |
| PASS           | MySQL database password                                                                          |
| HOST           | MySQL database host                                                                              |
| **# LINKEDIN** |                                                                                                  |
| USER           | LinkedIn account username                                                                        |
| PASS           | LinkedIn account password                                                                        |
| **# TELEGRAM** | ( [How to get a Telegram API_ID and API_HASH?](https://core.telegram.org/api/obtaining_api_id) ) |
| API_ID         | Telegram api id                                                                                  |
| API_HASH       | Telegram api id                                                                                  |
| TOKEN          | Telegram bot token                                                                               |

## # Add A New Language
To add a new language to bot, edit [texts.py](utils/telegram/texts.py) and add your new language
texts using its ISO formatted name like "en" or "fa".

Then edit [keyboards.py](utils/telegram/keyboards.py) and add new language buttons in SET_LANG and SET_LANG_CONVERSATION
buttons. also don't forget to edit their data
( `set_lang::en`, `set_lang_conv::en` ) and replace `en` with your language ISO.