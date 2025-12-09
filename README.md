# QR Code Generator

A Python GUI application that generates QR codes from text or URLs.

## Description

This project is a desktop application built with Python and Tkinter that allows users to:
- Enter any text or URL
- Generate a QR code with customizable settings
- Preview the QR code in the application
- Save the QR code as PNG or JPG

## Features

- **Customizable Error Correction**: Choose from 4 levels (Low, Medium, Quartile, High)
- **Adjustable Size**: Slider to control QR code dimensions
- **Live Preview**: See the QR code before saving
- **Export Options**: Save as PNG or JPG format


## Usage

Run the application:
```bash
python qr_code_generator.py
```

1. Enter your text or URL in the input field
2. Adjust error correction and size settings
3. Click "Generate QR Code"
4. Click "Save Image" to export the QR code

## Requirements

- Python 3.x
- Pillow
- qrcode

## Project Structure

```
qr-code-generator/
├── qr_code_generator.py    # Main application code
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── screenshot.png         # Application screenshot
```

## Code Structure

The project uses two classes with inheritance:

- **QRCodeGenerator**: Base class that handles QR code generation and saving
- **QRCodeApp**: Inherits from QRCodeGenerator and adds the GUI interface

## Author

Joseph Carruthers
