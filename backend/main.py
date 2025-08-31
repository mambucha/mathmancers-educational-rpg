from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import models, session
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import user, auth, battle, player

# --- ЛОГІКА ІНІЦІАЛІЗАЦІЇ ---
def init_db():
    db = session.SessionLocal()
    try:
        # Створюємо таблиці
        models.Base.metadata.create_all(bind=session.engine)

        # Створюємо ворогів, якщо їх немає
        if db.query(models.Enemy).count() == 0:
            print("Creating initial enemies...")
            enemies = [
                models.Enemy(name="Chaos Number", max_hp=50, math_topic="addition", resistance="algebra"),
                models.Enemy(name="Subtraction Sprite", max_hp=70, math_topic="subtraction", resistance="multiplication"),
                models.Enemy(name="Multiplication Minion", max_hp=100, math_topic="multiplication", vulnerability="subtraction"),
                models.Enemy(name="Geometric Gargoyle", max_hp=120, math_topic="geometry", vulnerability="geometry", resistance="addition"),
                models.Enemy(name="Algebraic Elemental", max_hp=150, math_topic="algebra", vulnerability="algebra", resistance="geometry"),
            ]
            db.add_all(enemies)
            db.commit()
            print("Initial enemies created.")
    finally:
        db.close()

# --- ЖИТТЄВИЙ ЦИКЛ ДОДАТКУ ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код, що виконується при старті
    print("Application startup...")
    init_db()
    yield
    # Код, що виконується при зупинці (якщо потрібно)
    print("Application shutdown...")

# Ініціалізуємо FastAPI з нашим життєвим циклом
app = FastAPI(lifespan=lifespan)

# --- MIDDLEWARE (CORS) ---
origins = [
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ПІДКЛЮЧЕННЯ РОУТЕРІВ ---
app.include_router(user.router, prefix="/api/v1", tags=["users"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(battle.router, prefix="/api/v1", tags=["battle"])
app.include_router(player.router, prefix="/api/v1", tags=["player"])

# --- КОРЕНЕВИЙ ЕНДПОІНТ ---
@app.get("/")
def read_root():
    return {"message": "Welcome to MathMancers Backend!"}