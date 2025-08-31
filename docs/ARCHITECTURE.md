# Архітектура MathMancers

## Загальна схема
- Backend: FastAPI + SQLAlchemy + PostgreSQL
- Frontend: Vue.js 3 + TypeScript + Pinia
- Комунікація: REST API + JWT авторизація

## Backend компоненти
- `app/api/` - REST endpoints
- `app/services/` - бізнес-логіка
- `app/db/` - моделі та база даних
- `app/schemas/` - Pydantic валідація

## Frontend компоненти  
- `components/` - переіспользовувані компоненти
- `views/` - сторінки програми
- `stores/` - Pinia stores для стану
- `services/` - API клієнти

## Ключові архітектурні рішення
- Розділення frontend/backend для незалежної розробки
- Модульна структура для легкого масштабування
- Адаптивна система навчання через services layer

mathmancers-project/
├── README.md                    # 🔥 ГОЛОВНИЙ ФАЙЛ - опис проекту
├── PROJECT_OVERVIEW.md          # Технічна документація з артефакту
├── SETUP.md                     # Інструкції запуску
├── CONTRIBUTING.md              # Для розробників
├── LICENSE                      # MIT або Apache 2.0
├── .gitignore                   # Ігнорувати конфіденційні файли
├── docs/                        # Документація
│   ├── ARCHITECTURE.md          # Архітектура системи
│   ├── PEDAGOGY.md             # Педагогічна концепція  
│   ├── API.md                  # Документація API
│   └── DEPLOYMENT.md           # Розгортання
├── backend/
│   ├── README.md               # Специфіка backend
│   ├── requirements.txt        # Python залежності
│   ├── app/
│   └── tests/                  # Тести (створіть базові)
└── frontend/
    ├── README.md               # Специфіка frontend
    ├── package.json
    ├── src/
    └── tests/                  # Тести