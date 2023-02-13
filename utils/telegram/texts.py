from utils.telegram.tools import Text


class LanguageIsSet(Text):
    en = "Your language is set to 🇺🇸 English"
    fa = "زبان شما روی 🇮🇷 فارسی تنظیم شد"


class LinkYourLinkedIn(Text):

    en = (
        "🖇 To use this bot, I need to know you on Linkedin.\n"
        "👉 To do so, please copy the code below and send it to me on Linkedin.\n\n"
        "Your code is:\n"
        "`%code%`\n\n"
        "⏳ This code is valid for 30 minutes.\n\n"
        "➖➖➖➖\n"
        "🔅 Please consider; to send a message, you need to *connect* with me first. "
        "And then send /start again to get a new code.\n\n"
        "▫️ **Downloadin will accept all connect invites, automatically every 15 minutes.** \n"
        "▫️ This is a one-time process, so don't worry about it."
    )

    fa = (
        "🖇 برای استفاده از ربات، باید لینکدین خود را با اکانت تلگرامتان همگام سازی کنید.\n"
        "👈 بدین منظور لطفا کد زیر را کپی کرده و برای من در لینکدین ارسال کنید\n\n"
        "🔹 کد شما:\n"
        "`%code%`\n\n"
        "⏳ اعتبار این کد 30 دقیقه است\n\n"
        "➖➖➖➖\n"
        "🔅 لطفا توجه داشته باشید؛ برای ارسال پیام، ابتدا باید با اکانت لینکدین من *connect* شوید "
        "و پس از تایید، مجددا برای دریافت کد /start را ارسال کنید.\n\n"
        "▫️ **ربات DownloadIn تمامی درخواست های کانکت را، هر 15 دقیقه یکبار بصورت خودکار قبول می کند.**\n"
        "▫️ این پروسه تنها برای اولین پیام ضروری است، بنابراین نگران نباشید."
    )


class LinkedinAlreadyLinked(Text):

    en = (
        "🖇 You already linked your Linkedin account.\n"
        "🔅 To download images, documents and videos, *share* desired posts with me on Linkedin.\n"
    )

    fa = (
        "🖇 اکانت لینکدین شما همگام سازی شده است.\n"
        "🔅 برای دریافت تصاویر، فایل ها و ویدیوهای موجود در پست ها، پست موردنظر خود"
        " را با من در لینکدین *share* کنید.\n"
    )


class LinkedinLinked(Text):

    en = (
        "✅ Your Linkedin account has been added successfully.\n\n"
        'To download media, simply "Share" desired posts to my Linkedin account'
    )

    fa = (
        "✅ اکانت لینکدین شما با موفقیت همگام سازی شد\n\n"
        'برای دانلود مدیا، تنها کافی است پست مورد نظرتان را برای اکانت لینکدین من "Share" کنید'
    )


class MediaCaption(Text):

    en = "📥 Author: %author%"
    fa = "📥 دریافت شده از: %author%"


class MediaIsNotDownloadable(Text):

    en = (
        "🛑 Uploading media in telegram failed, here is the link to your requested media:\n\n"
        "%link%\n\n "
        "You can download it directly"
    )

    fa = (
        "🛑 آپلود فایل در تلگرام ناموفق بود، این لینک فایل درخواستی شما است:\n\n"
        "%link%\n\n"
        "می توانید آن را مستقیما دانلود کنید"
    )
