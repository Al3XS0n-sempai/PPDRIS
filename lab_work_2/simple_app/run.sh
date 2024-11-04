#!/bin/bash

cd /app
nohup /venv/bin/uvicorn app:app --host 127.0.0.1 --port 8000 --reload &
