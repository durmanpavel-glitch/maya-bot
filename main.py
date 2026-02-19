import os
import asyncio
from flask import Flask
from threading import Thread
from google import genai
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties

# --- СЕРВЕР ДЛЯ RENDER ---
app = Flask('')
@app.route('/')
def home(): return "Майя: Энергия в потоке. ✨"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
def keep_alive():
    t = Thread(target=run); t.daemon = True; t.start()

# --- КОНФИГУРАЦИЯ ---
TOKEN = os.environ.get('TELEGRAM_TOKEN')
API_KEY = os.environ.get('GEMINI_API_KEY')

client = genai.Client(api_key=API_KEY)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()
user_history = {}

async def ask_maya(user_id, user_input):
    if user_id not in user_history: user_history[user_id] = []
    system_role = "Ты — Майя, эксперт в энергопрактиках. Твой тон мудрый и спокойный."
    history_context = "\n".join(user_history[user_id][-6:])
    full_prompt = f"{system_role}\n\nИстория ученика:\n{history_context}\n\nЗапрос: {user_input}"

    for model_id in ["gemini-2.0-flash", "gemini-1.5-flash-8b"]:
        try:
            response = client.models.generate_content(model=model_id, contents=full_prompt)
            if response.text:
                user_history[user_id].append(f"У: {user_input}")
                user_history[user_id].append(f"М: {response.text[:100]}")
                return response.text
        except: continue
    return "Я настраиваю связь. Подыши глубоко."

@dp.message(F.text)
async def handle_text(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    answer = await ask_maya(message.from_user.id, message.text)
    await message.answer(f"{answer}\n\n<i>— Майя ✨</i>")

async def main():
    keep_alive()
    print("💎 МАЙЯ В ЭФИРЕ.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
