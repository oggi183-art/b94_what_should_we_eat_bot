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
    "🥩 До гарніру": [
        "Котлети",
        "Курка смажена з грибами в вершковому соусі",
        "Фрикадельки в вершковому соусі з грибами",
        "Фрикадельки в томатному соусі",
        "Битки",
        "Брізоль",
        "Курячі стегна печені",
        "Сосиски/сардельки",
        "Курячий рулет",
        "Котлети по-київськи",
        "Томлена яловичина",
        "Філе лосося запечене/на грилі",
    ],
    "🍝 Основні страви": [
        "Паста вершкова з креветками",
        "Паста з фетою та куркою",
        "Паста з куркою (а-ля Карбонара)",
        "Гостра паста з телятиною/куркою/креветками",
        "Фунчоза з телятиною/куркою/креветками",
        "М'ясо по-французськи",
        "Фаршировані перці",
        "Голубці",
        "Курка ціла печена",
        "Жульєн у картопляному кошику (кіш)",
        "Пельмені",
        "Вареники з зажаркою",
        "Піцца",
        "Паста болоньєзе",
        "Зрази",
        "Сосиски в лаваші",
        "Хот-доги",
        "Сосиски в тісті",
        "Міні-піцци",
        "Піцца-бони",
    ],
}

GARNISH_KEY = "🍚 Гарніри"
SIDE_KEY = "🥩 До гарніру"

# ===== КЛАВІАТУРИ =====
def main_keyboard():
    keyboard = [[InlineKeyboardButton(cat, callback_data=f"cat:{cat}")] for cat in MENU]
    keyboard.append([InlineKeyboardButton("🎲 Рандомна страва (будь-яка)", callback_data="random_all")])
    keyboard.append([InlineKeyboardButton("🍽️ Рандомний гарнір + до нього", callback_data="random_pair")])
    return InlineKeyboardMarkup(keyboard)

def category_keyboard(category):
    rows = [[InlineKeyboardButton("🎲 Рандомна з цієї категорії", callback_data=f"rand:{category}")]]
    if category == GARNISH_KEY:
        rows.append([InlineKeyboardButton("🍽️ Рандомний гарнір + до нього", callback_data="random_pair")])
    rows.append([InlineKeyboardButton("⬅️ Назад до меню", callback_data="back")])
    return InlineKeyboardMarkup(rows)

def random_result_keyboard(category=None):
    rows = [[InlineKeyboardButton("🔄 Ще раз!", callback_data=f"rand:{category}" if category else "random_all")]]
    if category == GARNISH_KEY:
        rows.append([InlineKeyboardButton("🍽️ З підбором до гарніру", callback_data="random_pair")])
    if category:
        rows.append([InlineKeyboardButton("⬅️ До категорії", callback_data=f"cat:{category}")])
    rows.append([InlineKeyboardButton("🏠 Головне меню", callback_data="back")])
    return InlineKeyboardMarkup(rows)

def pair_result_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Інший варіант!", callback_data="random_pair")],
        [InlineKeyboardButton("🏠 Головне меню", callback_data="back")],
    ])

# ===== ХЕНДЛЕРИ =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👩‍🍳 Привіт! Це наш особистий кулінарний помічник 💕\n\n"
        "Обери категорію, щоб побачити страви,\nабо натисни 🎲 для випадкового вибору:",
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

    elif data == "random_pair":
        garnish = random.choice(MENU[GARNISH_KEY])
        side = random.choice(MENU[SIDE_KEY])
        await query.edit_message_text(
            f"🍽️ Рандомний варіант вечері:\n\n"
            f"🍚 *Гарнір:* {garnish}\n"
            f"🥩 *До нього:* {side}\n\n"
            f"Смачного вам обом! 💕",
            parse_mode="Markdown",
            reply_markup=pair_result_keyboard()
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
