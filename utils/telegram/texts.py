from utils.telegram.tools import Text


class LanguageIsSet(Text):
    en = 'Your language is set to 🇺🇸 English'
    fa = 'زبان شما روی 🇮🇷 فارسی تنظیم شد'


class LinkYourLinkedIn(Text):

    en = ("🖇 To use this bot, I need to know you on Linkedin.\n"
          "👉 To do so, please copy the code below and send it to me on Linkedin.\n\n"
          "Your Code is:\n"
          "`%code%`\n\n"
          "⏳ This code is valid for 5 minutes.\n\n"
          "🔅 Please consider that if you don't have Linkedin premium, you need to *connect* with me first. "
          "And then send /start again to get a new code.\n"
          "This is a one-time process, so don't worry about it. We will accept your request as soon as we can.")

    fa = ("🖇 برای استفاده از ربات، باید لینکدین خود را با اکانت تلگرامتان همگام سازی کنید.\n"
          "👈 بدین منظور لطفا کد زیر را کپی کرده و برای من در لینکدین ارسال کنید\n\n"
          "🔹 کد شما:\n"
          "`%code%`\n\n"
          "⏳ اعتبار این کد 5 دقیقه است\n\n"
          "🔅 لطفا توجه داشته باشید اگر اکانت پرمیوم لینکدین ندارید، ابتدا باید با اکانت لینکدین من *connect* شوید. "
          "و پس از تایید، مجددا برای دریافت کد /start را ارسال کنید.\n"
          "این پروسه تنها برای اولین پیام ضروری است، بنابراین نگران نباشید. "
          "ما درخواست شما را در سریعترین زمان ممکن تایید خواهیم کرد"
          )


class LinkedinAlreadyLinked(Text):

    en = ("🖇 You already linked your Linkedin account.\n"
          "🔅 To download images, documents and videos, *share* desired posts with me on Linkedin.\n")

    fa = ("🖇 اکانت لینکدین شما همگام سازی شده است.\n"
          "🔅 برای دریافت تصاویر، فایل ها و ویدیوهای موجود در پست ها، پست موردنظر خود"
          " را با من در لینکدین *share* کنید.\n")


class LinkedinLinked(Text):

    en = ("✅ Your Linkedin account has been added successfully.\n\n"
          "To download media, simply \"Share\" desired posts to my Linkedin Account")

    fa = ("✅ اکانت لینکدین شما با موفقیت همگام سازی شد\n\n"
          "برای دانلود مدیا، تنها کافی است پست مورد نظرتان را برای اکانت لینکدین من \"Share\" کنید")


class MediaCaption(Text):

    en = "Author: %author%"
    fa = "دریافت شده از: %author%"
