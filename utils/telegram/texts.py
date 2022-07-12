from utils.telegram.tools import Text


class LanguageIsSet(Text):
    en = 'Your language is set to 🇺🇸 English'
    fa = 'زبان شما روی 🇮🇷 فارسی تنظیم شد'


class LinkYourLinkedIn(Text):

    en = ("To use this bot, I need to know you on Linkedin.\n"
          "To do so, please copy the code below and send it to me on Linkedin.\n\n"
          "Your Code is:\n"
          "`%code%`\n\n"
          "This code is valid for 5 minutes.")

    fa = ("برای استفاده از ربات، باید لینکدین خود را با اکانت تلگرامتان همگام سازی کنید.\n"
          "بدین منظور لطفا کد زیر را کپی کرده و برای من در لینکدین ارسال کنید\n\n"
          "کد شما:\n"
          "`%code%`\n\n"
          "اعتبار این کد 5 دقیقه است")


class LinkedinLinked(Text):

    en = ("✅ Your Linkedin account has been added successfully.\n\n"
          "To download media, simply \"Share\" desired posts to my Linkedin Account")

    fa = ("✅ اکانت لینکدین شما با موفقیت همگام سازی شد\n\n"
          "برای دانلود مدیا، تنها کافی است پست مورد نظرتان را برای اکانت لینکدین من \"Share\" کنید")


class MediaCaption(Text):

    en = "Author: %author%"
    fa = "دریافت شده از: %author%"
