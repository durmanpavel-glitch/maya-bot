import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import google.generativeai as genai
from flask import Flask
from threading import Thread

# 1. ПОЛУЧЕНИЕ КЛЮЧЕЙ ИЗ RENDER
TOKEN = os.environ.get('TELEGRAM_TOKEN')
API_KEY = os.environ.get('GEMINI_API_KEY')

# 2. НАСТРОЙКА GEMINI AI
genai.configure(api_key=API_KEY)
# Используем самую стабильную модель
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. ИНИЦИАЛИЗАЦИЯ БОТА
bot = Bot(token=TOKEN)
dp = Dispatcher()
app = Flask(__name__)

# Веб-сервер для Render (чтобы не засыпал)
@app.route('/')
def home():
    return "Maya is Online ✨"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

# 4. ЛОГИКА ОТВЕТОВ МАЙИ
async def ask_maya(question):
    try:
        # Промпт, задающий характер Майи
        prompt = f"Ты — Майя, мудрый ИИ-проводник. Твой тон спокойный и поддерживающий. Ответь на вопрос: {question}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Ошибка ИИ: {e}")
        return "Я настраиваю внутренние частоты. Попробуй задать вопрос чуть позже. 🙏"

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Здравствуй. Я Майя, твой проводник в мир осознанности. О чем ты хочешь поговорить?")

@dp.message()
async def handle_message(message: types.Message):
    # Показываем, что Майя "печатает"
    await bot.send_chat_action(message.chat.id, "typing")
    answer = await ask_maya(message.text)
    await message.answer(answer)

# 5. ЗАПУСК
async def main():
    Thread(target=run_flask).start()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
