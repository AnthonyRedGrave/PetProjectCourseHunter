web: uvicorn fastapi_core.main:app --host=0.0.0.0 --port=${PORT:-8008}
admin: python3 -m admin.app
release: alembic upgrade head