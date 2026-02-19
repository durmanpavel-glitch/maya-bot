async def ask_maya(question):
    try:
        # Проверка наличия ключа в логах (для отладки)
        if not API_KEY:
            return "Ошибка: Ключ API не найден в настройках Render."
            
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"Ты — Майя, мудрый ИИ-проводник. Ответь на вопрос: {question}"
        response = model.generate_content(prompt)
        
        if response and response.text:
            return response.text
        else:
            return "Мои мысли сейчас туманны. Спроси иначе, пожалуйста."
            
    except Exception as e:
        print(f"ОШИБКА GEMINI: {e}")
        return f"Я настраиваю частоты. (Техническая деталь: {str(e)[:50]}...)"
