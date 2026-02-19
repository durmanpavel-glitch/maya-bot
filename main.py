import os, asyncio
import google.generativeai as genai
from flask import Flask
from threading import Thread
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties

# Веб-сервер для "будильника"
app = Flask('')
@app.route('/')
def home(): return "Maya is Online ✨"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# Настройки ИИ
TOKEN = os.environ.get('TELEGRAM_TOKEN')
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

async def ask_maya(text):
    try:
        prompt = f"Ты — Майя, мудрый проводник в мир энергопрактик. Твой тон спокойный. Ответь ученику: {text}"
        response = model.generate_content(prompt)
        return response.text if response.text else "Я погружена в тишину. Попробуй еще раз."
    except Exception as e:
        return "Я настраиваю частоты. Подыши глубоко и напиши мне снова."

@dp.message(F.text)
async def handle_message(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    answer = await ask_maya(message.text)
    await message.answer(f"{answer}\n\n<i>— Твой проводник, Майя ✨</i>")

async def main():
    Thread(target=run).start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
