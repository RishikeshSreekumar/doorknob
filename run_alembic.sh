#!/bin/bash
cd backend
alembic revision --autogenerate -m "Initial migration"
