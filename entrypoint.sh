#!/usr/bin/env bash

cd elevator-sys/backend
gunicorn ElevatorSystemService:server