#!/bin/bash

python3 -m pytest tests/ -v --cov=services --cov=models --cov=enums --cov=exceptions --cov-report=term-missing