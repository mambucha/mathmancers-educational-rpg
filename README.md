# 🧙‍♂️ MathMancers: The Last Arithmancer

**Революційна освітня RPG-гра, яка перетворює математику на магічну пригоду**

[![Demo](https://img.shields.io/badge/Live%20Demo-Available-brightgreen)](your-demo-link)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Backend](https://img.shields.io/badge/Backend-FastAPI-009688)](backend/)
[![Frontend](https://img.shields.io/badge/Frontend-Vue.js%203-4FC08D)](frontend/)

## 🎯 Що це?

MathMancers - освітня гра де учні розв'язують математичні задачі через інтерактивні бої. Замість нудних прикладів - система адаптивного навчання з аналізом помилок та персоналізованими поясненнями.

### 📸 Скріншоти

![Battle Screen](docs/images/battle-screenshot.png)
![Algebra System](docs/images/progressive-algebra.png)

## ✨ Ключові особливості

- **🎮 Ігрофікація**: Математика як форма магії в RPG світі
- **🧠 Адаптивне навчання**: AI аналізує помилки та підбирає підхід
- **⚖️ Візуальні метафори**: Рівняння як магічні ваги, операції як заклинання
- **📊 Аналітика для батьків**: Детальні звіти про прогрес дитини
- **🏆 Система майстерності**: Прогрес через розуміння, не механічне запам'ятовування

## 🚀 Швидкий старт

### Вимоги
- Python 3.11+
- Node.js 18+
- PostgreSQL (або SQLite для dev)

### Запуск за 3 хвилини

1. **Клонування:**
```bash
git clone https://github.com/username/mathmancers-project.git
cd mathmancers-project

Backend:

bashcd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn main:app --reload

Frontend:

bashcd frontend
npm install
npm run dev

Відкрити: http://localhost:5173

🏗️ Архітектура

Backend: FastAPI + SQLAlchemy + PostgreSQL
Frontend: Vue.js 3 + TypeScript + Tailwind CSS
Бойова система: Прогресивна алгебра з системою аналізу помилок
AI: Детекція математичних заблуджень та персоналізовані пояснення