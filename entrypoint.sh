#!/usr/bin/env bash

cd elevator-sys
git pull main
cd backend
gunicorn -b 0.0.0.0:8000 ElevatorSystemService:server