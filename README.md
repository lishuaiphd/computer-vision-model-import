# Overview
This project implements a web app where users upload a photo/scan of a hand-drawn software/system/process diagram. The app extracts shapes, arrows, and text, builds a structured graph, and exports a JSON file representing the graphical elements.

The pipeline uses robust classical Computer Vision (OpenCV) plus OCR (Tesseract). An optional neural segmentation model scaffold is included for improved results (PyTorch).

# Setup

1. Install Tesseract.

* Linux: `sudo apt install tesseract-ocr`
* MacOS: `brew install tesseract`
* Windows: install from the internet and add to PATH. 

2. Install all required packages.

`pip install -r requirements.txt`

# Usage

* Linux/MacOS: `bash run.sh`
* Windows: `run_windows.bat`

Open http://127.0.0.1:5000