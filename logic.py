from database import load_database, save_database

# حافظه موقت برای نگهداری وضعیت مکالمه کاربران (مثل روند ورود ادمین)
user_states = {}

def Reply(message_data):
    """
    تابع اصلی پردازش پیام‌ها و اجرای منطق ربات (کاربران و ادمین‌ها)
    """
    try:
        chat_id = message_data.get("chat_id")
        text = message_data.get("text", "").strip()
        
        if not chat_id:
            return "خطا در دریافت شناسه کاربر."

        db = load_database()
        
        # ثبت کاربر در لیست کاربران
        if chat_id not in db["users"]:
            db["users"].append(chat_id)
            save_database(db)

        current_state = user_states.get(chat_id, "NORMAL")

        # ۱. خروج از حالت ادمین یا لغو
        if text == "بازگشت به منوی اصلی":
            user_states[chat_id] = "NORMAL"
            return "به منوی اصلی بازگشتید."

        # ۲. روند ورود به منوی ادمین
        if text == "منوی ادمین" and current_state == "NORMAL":
            user_states[chat_id] = "WAITING_NAME"
            return "لطفاً نام ادمین خود را وارد کنید:"

        if current_state == "WAITING_NAME":
            # بررسی نام ادمین
            valid_admin = False
            for admin in db["admins"]:
                if text == admin["name"]:
                    valid_admin = True
                    break
            
            if valid_admin:
                user_states[chat_id] = "WAITING_PASS"
                return "نام تایید شد. لطفاً کد رمز ورود را وارد کنید:"
            else:
                user_states[chat_id] = "NORMAL"
                return "نام وارد شده معتبر نیست. به منوی اصلی بازگشتید."

        if current_state == "WAITING_PASS":
            # بررسی رمز ادمین (آخرین نام ذخیره شده یا چک کردن در لیست)
            # برای سادگی، رمز را با ادمین ثبت شده مطابقت می‌دهیم
            admin_obj = db["admins"][0] # ادمین اصلی
            if text == admin_obj["passcode"]:
                user_states[chat_id] = "ADMIN_PANEL"
                return (
                    "✅ ورود موفقیت‌آمیز به منوی ادمین!\n\n"
                    "گزینه‌های مدیریت:\n"
                    "- ویرایش نام ربات\n"
                    "- ویرایش درباره ما\n"
                    "- تنظیم دریافت کانال\n"
                    "- مشاهده نظرات\n"
                    "- ارسال همگانی\n"
                    "(کافی است دستور مورد نظر را ارسال کنید)"
                )
            else:
                user_states[chat_id] = "NORMAL"
                return "کد رمز اشتباه است. دسترسی رد شد."

        # ۳. مدیریت پنل ادمین (اگر کاربر در حالت ادمین باشد)
        if current_state == "ADMIN_PANEL":
            if text == "ویرایش درباره ما":
                user_states[chat_id] = "EDIT_ABOUT"
                return "متن جدید «درباره ما» را بفرستید:"
            elif text == "مشاهده نظرات":
                feedbacks = db.get("feedback", [])
                if not feedbacks:
                    return "هنوز نظری ثبت نشده است."
                return "نظرات کاربران:\n\n" + "\n---\n".join(feedbacks)
            elif text == "تنظیم دریافت کانال":
                user_states[chat_id] = "EDIT_CHANNEL"
                return "متن یا لینک جدید کانال را ارسال کنید:"
            else:
                return f"دستور ادمین دریافت شد: {text}\n(برای خروج 'بازگشت به منوی اصلی' را بفرستید)"

        # ثبت متن درباره ما
        if current_state == "EDIT_ABOUT":
            db["settings"]["about"] = text
            save_database(db)
            user_states[chat_id] = "ADMIN_PANEL"
            return "✅ متن «درباره ما» با موفقیت بروز شد."

        # ثبت لینک کانال
        if current_state == "EDIT_CHANNEL":
            db["settings"]["channel_text"] = text
            save_database(db)
            user_states[chat_id] = "ADMIN_PANEL"
            return "✅ تنظیمات کانال با موفقیت بروز شد."

        # ۴. منوی مخاطبین (کاربران عادی)
        if text == "/start":
            settings = db.get("settings", {})
            welcome_msg = (
                "به ربات اختصاصی تیم IRAN NARRATIVE خوش آمدید 🌹\n"
                "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:"
            )
            return welcome_msg

        elif text == "ℹ️ درباره ما":
            return db.get("settings", {}).get("about", "توضیحی ثبت نشده است.")

        elif text == "📢 دریافت کانال":
            return db.get("settings", {}).get("channel_text", "کانالی ثبت نشده است.")

        elif text == "📩 ارسال نظرات":
            user_states[chat_id] = "WAITING_FEEDBACK"
            return "لطفاً نظر، پیشنهاد یا انتقاد خود را بنویسید و ارسال کنید:"

        elif current_state == "WAITING_FEEDBACK":
            db.setdefault("feedback", []).append(f"کابر {chat_id}: {text}")
            save_database(db)
            user_states[chat_id] = "NORMAL"
            return "✅ نظر شما با موفقیت به دست تیم ادمین رسید. سپاس از همراهی شما!"

        elif text == "📂 مشاهده پست‌ها":
            posts = db.get("posts", [])
            if not posts:
                return "فعلاً پستی منتشر نشده است."
            return "پست‌های اخیر:\n\n" + "\n\n".join(posts)

        elif text == "🛠 پشتیبانی":
            return "برای ارتباط با پشتیبانی تیم، به آیدی ادمین پیام دهید."

        else:
            return f"دستور نامعتبر. پیام شما دریافت شد: {text}"

    except Exception as e:
        return f"خطا در پردازش: {str(e)}"
      
