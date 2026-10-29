
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

import re

# ============================================================
# TOKEN
# ============================================================

TOKEN = "8609299532:AAFgJDCJm0FPCNp9tWH9r-R1_qPuk08TMgI"

# ============================================================
# ПОДОЗРИТЕЛЬНЫЕ НОМЕРА
# ============================================================

SUSPICIOUS_NUMBERS = [
    "+77145123456",
    "+77145987654",
    "+77272727272",
    "+77001234567",
    "+7 701 234 5678",
    "+380501234567",
    "+375291234567",
    "+447911123456",
    "+1-800-555-0199",
    "unknown",
    "private number",
    "скрытый номер",
    "спам",
    "fraud",
    "scam"
]


# ============================================================
# МАРКЕРЫ МОШЕННИЧЕСТВА
# ============================================================

SCAM_MARKERS = {

    # КРИТИЧЕСКИЕ
    "код из смс": 45,
    "код подтверждения": 45,
    "безопасный счет": 45,
    "резервный счет": 45,
    "введите код": 45,
    "ввести код": 45,
    "сообщите пароль": 50,
    "сообщить пароль": 50,
    "подмена сотрудника банка": 42,
    "сотрудник банка": 18,
    "представитель банка": 20,
    "оператор банка": 20,
    "нажмите ссылку": 42,
    "ссылка для входа": 42,
    "ссылка для подтверждения": 42,
    "подтвердите вход": 38,
    "подтвердить вход": 38,
    "подтвердите оплату": 34,
    "подтвердить оплату": 34,
    "подтвердите перевод": 34,
    "подтвердить перевод": 34,
    "ошибка безопасности": 30,
    "временная блокировка": 30,
    "карта заблокирована": 35,
    "карту заблокировали": 35,
    "аккаунт заблокирован": 35,
    "восстановить доступ": 32,
    "подтвердите личность": 32,
    "проверка личности": 32,
    "необходимо подтвердить": 30,
    "подтвердить личность": 32,

    # СРЕДНИЕ
    "служба безопасности": 24,
    "оформить кредит": 22,
    "переведите деньги": 22,
    "перевод на карту": 30,
    "оплатите штраф": 30,
    "наложенный платеж": 22,
    "предоплата": 22,
    "ваша карта": 18,
    "ваш счет": 18,
    "попытка несанкционированного доступа": 30,
    "несанкционированная операция": 30,
    "внимание! аккаунт": 28,
    "позвоните по номеру": 18,
    "звонок с незнакомого номера": 18,
    "срочно свяжитесь": 18,
    "немедленно свяжитесь": 18,
    "заблокировали карту": 28,
    "ошибка в системе": 20,
    "временно приостановлена": 22,
    "ваша учетная запись": 20,
    "проверка безопасности": 22,
    "подозрительная активность": 20,

    # СЛАБЫЕ
    "срочно": 14,
    "немедленно": 14,
    "прямо сейчас": 14,
    "сегодня срочно": 18,
    "без задержек": 12,
    "только сейчас": 12,
    "выиграли": 14,
    "приз": 14,
    "подарок": 16,
    "выигрыш": 16,
    "лотерея": 16,
    "подтвердите": 16,
    "ваш аккаунт": 14,
    "перевод средств": 18,
    "подозрительный звонок": 16,
    "неверный код": 18,
    "click the link": 28,
    "confirm your account": 28,
    "urgent action required": 22,
    "verify your account": 24,
    "bank security": 18,
    "transaction blocked": 24,
    "suspicious activity": 20
}

# ============================================================
# АНАЛИЗ ТЕКСТА
# ============================================================

def analyze_text(text):

    text_lower = text.lower()

    risk = 0
    found = []

    for marker, weight in SCAM_MARKERS.items():

        if marker in text_lower:
            risk += weight
            found.append(marker)

    risk = min(risk, 100)

    if risk >= 35:
        level = "🔴 ВЫСОКИЙ РИСК"

    elif risk >= 10:
        level = "🟡 СРЕДНИЙ РИСК"

    else:
        level = "🟢 НИЗКИЙ РИСК"

    return {
        "risk": risk,
        "level": level,
        "found": found
    }

# ============================================================
# /start
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "👶 Ребенок",
                callback_data="child"
            ),

            InlineKeyboardButton(
                "🧑 Молодежь",
                callback_data="youth"
            )
        ],

        [
            InlineKeyboardButton(
                "👵 Пенсионер",
                callback_data="elderly"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "🛡 Добро пожаловать в BarysGuard!\n\n"
        "Я — ИИ помощник против онлайн-мошенничества.\n\n"
        "📌 Возможности:\n"
        "• Анализ сообщений\n"
        "• Проверка номеров\n"
        "• Объяснение угроз простым языком\n"
        "• Обучение распознаванию мошенников\n\n"
        "👇 Выберите режим:"
    )

    await update.message.reply_text(
        text,
        reply_markup=reply_markup
    )

# ============================================================
# ВЫБОР РЕЖИМА
# ============================================================

async def choose_group(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    group = query.data

    context.user_data["group"] = group

    if group == "child":

        text = (
            "👶 Детский режим активирован!\n\n"
            "Я буду объяснять всё простыми словами."
        )

    elif group == "elderly":

        text = (
            "👵 Режим для пенсионеров активирован!\n\n"
            "Я буду показывать крупные и понятные подсказки."
        )

    else:

        text = (
            "🧑 Молодежный режим активирован!\n\n"
            "Я покажу признаки социальной инженерии."
        )

    await query.edit_message_text(text)

# ============================================================
# /phone
# ============================================================

async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["waiting_phone"] = True

    await update.message.reply_text(
        "📞 Отправьте номер телефона для проверки.\n\n"
        "Пример:\n"
        "+77145123456"
    )

# ============================================================
# /help_elder
# ============================================================

async def help_elder(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "👵 ПАМЯТКА\n\n"
        "❌ Не сообщайте коды из СМС\n"
        "❌ Не переводите деньги незнакомцам\n"
        "❌ Не верьте безопасным счетам\n\n"
        "✅ При сомнении звоните родственникам."
    )

    await update.message.reply_text(text)

# ============================================================
# /train
# ============================================================

async def train(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "🚨 Это мошенник",
                callback_data="answer_scam"
            ),

            InlineKeyboardButton(
                "✅ Это безопасно",
                callback_data="answer_safe"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "📞 СЦЕНАРИЙ\n\n"
        "Здравствуйте.\n"
        "Это служба безопасности банка.\n"
        "На ваше имя пытаются оформить кредит.\n"
        "Срочно сообщите код из СМС."
    )

    await update.message.reply_text(
        text,
        reply_markup=reply_markup
    )

# ============================================================
# TRAIN ANSWER
# ============================================================

async def train_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    if query.data == "answer_scam":

        text = (
            "✅ Верно!\n\n"
            "Настоящий банк никогда не просит "
            "код из СМС."
        )

    else:

        text = (
            "❌ Неверно.\n\n"
            "Это классическая схема "
            "социальной инженерии."
        )

    await query.edit_message_text(text)

# ============================================================
# ГЛАВНЫЙ ОБРАБОТЧИК
# ============================================================

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    # ========================================================
    # ПРОВЕРКА НОМЕРА
    # ========================================================

    if context.user_data.get("waiting_phone"):

        phone = text.strip()

        risk = 0
        reason = "Номер выглядит безопасно"

        if phone in SUSPICIOUS_NUMBERS:

            risk = 95

            reason = (
                "Номер уже встречался "
                "в мошеннических схемах"
            )

        elif re.match(r"\+77145\d+", phone):

            risk = 70

            reason = (
                "Номер похож на поддельный "
                "VoIP номер Алматы"
            )

        if risk >= 50:

            response = (
                "🔴 ПОДОЗРИТЕЛЬНЫЙ НОМЕР\n\n"
                f"📊 Риск: {risk}%\n\n"
                f"📌 Причина:\n{reason}"
            )

        else:

            response = (
                "🟢 Номер не вызывает "
                "серьезных подозрений."
            )

        await update.message.reply_text(response)

        context.user_data["waiting_phone"] = False

        return

    # ========================================================
    # АНАЛИЗ ТЕКСТА
    # ========================================================

    result = analyze_text(text)

    response = (
        f"{result['level']}\n\n"
        f"📊 Вероятность скама: {result['risk']}%\n\n"
    )

    if result["found"]:

        response += "⚠ Обнаружены признаки:\n"

        for item in result["found"]:
            response += f"• {item}\n"

        response += "\n"

    group = context.user_data.get("group", "youth")

    if group == "child":

        response += (
            "🎮 Никому нельзя давать коды из СМС.\n"
            "Это как пароль от аккаунта."
        )

    elif group == "elderly":

        response += (
            "👵 Настоящий банк никогда не просит:\n"
            "• код из СМС\n"
            "• перевести деньги\n"
            "• назвать пароль"
        )

    else:

        response += (
            "🚨 Возможна схема социальной инженерии.\n"
            "Рекомендуется прекратить диалог."
        )

    if result["risk"] >= 60:

        response += (
            "\n\n📱 Уведомление доверенному лицу "
            "готово к отправке."
        )


    await update.message.reply_text(response)

# ============================================================
# ЗАПУСК
# ============================================================

app = ApplicationBuilder().token(TOKEN).build()

# команды

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("phone", phone))
app.add_handler(CommandHandler("train", train))
app.add_handler(CommandHandler("help_elder", help_elder))

# callback кнопки

app.add_handler(
    CallbackQueryHandler(
        choose_group,
        pattern="^(child|youth|elderly)$"
    )
)

app.add_handler(
    CallbackQueryHandler(
        train_answer,
        pattern="^answer_"
    )
)

# сообщения

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        analyze
    )
)

print("🚀 BarysGuard запущен!")

app.run_polling()

