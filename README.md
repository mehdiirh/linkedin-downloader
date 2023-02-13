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
Soon...

## # Add A New Language
To add a new language to bot, edit [texts.py](utils/telegram/texts.py) and add your new language
texts using its ISO formatted name like "en" or "fa".

Then edit [keyboards.py](utils/telegram/keyboards.py) and add new language buttons in SET_LANG and SET_LANG_CONVERSATION
buttons. also don't forget to edit their data
( `set_lang::en`, `set_lang_conv::en` ) and replace `en` with your language ISO.