#!/usr/bin/env bash

cd /backend
gunicorn ElevatorSystemService:app