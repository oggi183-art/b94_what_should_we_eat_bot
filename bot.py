import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ===== МЕНЮ =====
MENU = {
    "🌅 Сніданки": [
        "Авокадо-тост з яйцем пашот",
        "Авокадо-тост з лососем",
        "Омлет з помідорами, сиром та ковбаскою",
        "Яєшня",
        "Круасани з яйцем, сиром та огірком",
        "Сирники",
        "Тост з тунцем",
    ],
    "🍲 Супи": [
        "Борщ",
        "Гострий сирний суп з курочкою/ковбасками",
        "Сирний крем-суп",
        "Грибний крем-суп",
        "Бульйон чистий",
        "Бульйон з куркою, яйцем та вермішеллю",
    ],
    "🥗 Салати": [
        "Огірок-помідор-цибуля",
        "Огірок-редиска",
        "Пекінка з куркою",
        "Цезар",
        "Груша з лососем",
    ],
    "🍚 Гарніри": [
        "Гречка",
        "Картопля печена",
        "Картопля смажена",
        "Картопляне пюре",
        "Спагетті",
        "Макарони",
        "Батат-фрі",
        "Картопляний гратен",
        "Млинці",
        "Тушкована картопля з овочами",
        "Спаржа смажена",
        "Ньоккі",
        "Деруни",
    ],
    "🍖 Основні страви": [
        "Котлети",
        "Паста вершкова з креветками",
        "Паста з фетою та куркою",
        "Паста з куркою (а-ля Карбонара)",
        "Гостра паста з телятиною/куркою/креветками",
        "Курка смажена з грибами в вершковому соусі",
        "Фунчоза з телятиною/куркою/креветками",
        "М'ясо по-французськи",
        "Фаршировані перці",
        "Голубці",
        "Курка ціла печена",
        "Фрикадельки в вершковому соусі з грибами",
        "Фрикадельки в томатному соусі",
        "Жульєн у картопляному кошику",
        "Пельмені",
        "Вареники з зажаркою",
        "Піцца",
        "Битки",
        "Брізоль",
        "Паста болоньєзе",
        "Зрази",
        "Курячі стегна печені",
        "Сосиски/сардельки",
        "Сосиски в лаваші",
        "Курячий рулет",
        "Хот-доги",
        "Сосиски в тісті",
        "Котлети по-київськи",
        "Томлена яловичина",
        "Міні-піцци",
        "Піцца-бони",
        "Філе лосося запечене/на грилі",
    ],
}

# ===== КЛАВІАТУРИ =====
def main_keyboard():
    keyboard = [[InlineKeyboardButton(cat, callback_data=f"cat:{cat}")] for cat in MENU]
    keyboard.append([InlineKeyboardButton("🎲 Рандомна страва (будь-яка)", callback_data="random_all")])
    return InlineKeyboardMarkup(keyboard)

def category_keyboard(category):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎲 Рандомна з цієї категорії", callback_data=f"rand:{category}")],
        [InlineKeyboardButton("⬅️ Назад до меню", callback_data="back")],
    ])

def random_result_keyboard(category=None):
    rows = [[InlineKeyboardButton("🔄 Ще раз!", callback_data=f"rand:{category}" if category else "random_all")]]
    if category:
        rows.append([InlineKeyboardButton("⬅️ До категорії", callback_data=f"cat:{category}")])
    rows.append([InlineKeyboardButton("🏠 Головне меню", callback_data="back")])
    return InlineKeyboardMarkup(rows)

# ===== ХЕНДЛЕРИ =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👩‍🍳 Привіт! Це наш особистий кулінарний помічник 💕\n\n"
        "Обери категорію, щоб побачити страви, або натисни 🎲 для випадкового вибору:",
        reply_markup=main_keyboard()
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back":
        await query.edit_message_text(
            "👩‍🍳 Обери категорію або натисни 🎲 для випадкової страви:",
            reply_markup=main_keyboard()
        )

    elif data == "random_all":
        all_dishes = [dish for dishes in MENU.values() for dish in dishes]
        dish = random.choice(all_dishes)
        await query.edit_message_text(
            f"🎲 Сьогодні пропоную:\n\n✨ *{dish}*\n\nСмачного вам обом! 💕",
            parse_mode="Markdown",
            reply_markup=random_result_keyboard()
        )

    elif data.startswith("cat:"):
        category = data[4:]
        if category in MENU:
            dishes_text = "\n".join(f"• {d}" for d in MENU[category])
            await query.edit_message_text(
                f"{category}\n\n{dishes_text}",
                reply_markup=category_keyboard(category)
            )

    elif data.startswith("rand:"):
        category = data[5:]
        if category in MENU:
            dish = random.choice(MENU[category])
            await query.edit_message_text(
                f"🎲 Рандомна страва з *{category}*:\n\n✨ *{dish}*\n\nСмачного вам обом! 💕",
                parse_mode="Markdown",
                reply_markup=random_result_keyboard(category)
            )

# ===== ЗАПУСК =====
def main():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise ValueError("Не знайдено BOT_TOKEN! Перевір змінні середовища.")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    print("✅ Бот запущено!")
    app.run_polling()

if __name__ == "__main__":
    main()
