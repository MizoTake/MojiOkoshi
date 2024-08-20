#!/bin/bash

PROJECT_DIR=$(pwd)

pyinstaller --onefile --distpath "$PROJECT_DIR/dist" --workpath "$PROJECT_DIR/build" --specpath "$PROJECT_DIR/spec" main.py

if [ $? -eq 0 ]; then
    echo "Build completed successfully."
    echo "The executable can be found in the dist/ directory."
else
    echo "Build failed."
    exit 1
fi
