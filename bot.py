import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import openai

# Загружаем токены из .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Промпт для ChatGPT
def build_prompt(name):
    return f"""Ты — таинственный Оракул AI. Создай мистическое пророчество для человека по имени {name}. Используй структуру:
1. Вступление (1–2 строки)
2. Прошлое
3. Настоящее
4. Будущее
5. Тайное предупреждение
6. Символ (образ, число или цвет)

Стиль: эзотерика, загадочность, поэтичность, как будто говорит дух. Язык — русский.
"""

# Генерация текста от ChatGPT
async def generate_oracle_reply(name):
    prompt = build_prompt(name)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=1.1,
        max_tokens=600
    )
    return response.choices[0].message.content.strip()

# Обработка сообщений от пользователей
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    if not user_input:
        await update.message.reply_text("Пожалуйста, пришли имя для расклада.")
        return

    await update.message.reply_text("🔮 Оракул размышляет...")

    try:
        oracle_text = await generate_oracle_reply(user_input)
        await update.message.reply_text(oracle_text)
    except Exception as e:
        await update.message.reply_text("Что-то пошло не так с пророчеством...")
        print(f"Ошибка: {e}")

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет. Отправь своё имя, и Оракул заговорит...")

# Запуск бота
def main():
    print("✅ Код до запуска дойдён")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
