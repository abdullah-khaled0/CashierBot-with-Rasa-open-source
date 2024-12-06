@echo off
start cmd /k "rasa run actions"
timeout 14
start cmd /k "rasa run --enable-api"
timeout 14
start cmd /k "uvicorn backend.main:app --reload"
