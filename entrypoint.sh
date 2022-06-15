#!/usr/bin/env bash

cd elevator-sys
git pull main
cd backend
gunicorn ElevatorSystemService:server