"""
QR Code Generator


Author: Joseph Carruthers
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import qrcode
import io


class QRCodeGenerator:
    """
    generate QR codes with customizable options.
    
    Attributes:
        version (int): QR code version (1-40), controls size
        error_correction: Error correction level
        box_size (int): Size of each box in pixels
        border (int): Border size in boxes
    """
    
    # Error correction levels as class attribute
    ERROR_LEVELS = {
        'Low (7%)': qrcode.constants.ERROR_CORRECT_L,
        'Medium (15%)': qrcode.constants.ERROR_CORRECT_M,
        'Quartile (25%)': qrcode.constants.ERROR_CORRECT_Q,
        'High (30%)': qrcode.constants.ERROR_CORRECT_H
    }
    
    def __init__(self, box_size=10, border=4, error_correction='Medium (15%)'):
        """Initialize the QR code generator with default settings."""
        self.box_size = box_size
        self.border = border
        self.error_correction = self.ERROR_LEVELS.get(error_correction, 
                                                       qrcode.constants.ERROR_CORRECT_M)
        self.last_generated_image = None
    
    def generate(self, data, fill_color='black', back_color='white'):
        """
        Generate a QR code from the given data.
        
        Args:
            data (str): The text or URL to encode
            fill_color (str): Color of the QR code modules
            back_color (str): Background color
            
        Returns:
            PIL.Image: The generated QR code image
        """
        if not data.strip():
            raise ValueError("Please enter text or URL to generate QR code")
        
        qr = qrcode.QRCode(
            version=None,  # Auto-determine version
            error_correction=self.error_correction,
            box_size=self.box_size,
            border=self.border
        )
        
        qr.add_data(data)
        qr.make(fit=True)
        
        self.last_generated_image = qr.make_image(fill_color=fill_color, 
                                                   back_color=back_color)
        return self.last_generated_image
    
    def save(self, filepath):
        """
        Save the last generated QR code to a file.
        
        Args:
            filepath (str): Path to save the image
        """
        if self.last_generated_image is None:
            raise ValueError("No QR code generated yet")
        
        self.last_generated_image.save(filepath)


class QRCodeApp(QRCodeGenerator):
    """
    GUI Application for QR Code Generator.
    Inherits from QRCodeGenerator to add GUI functionality.
    """
    
    def __init__(self):
        """Initialize the GUI application."""
        super().__init__()
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("QR Code Generator")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 16, 'bold'))
        
        # Build the interface
        self._create_widgets()
        
    def _create_widgets(self):
        """Create and arrange all GUI widgets."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = ttk.Label(main_frame, text="QR Code Generator", 
                          style='Header.TLabel')
        header.pack(pady=(0, 20))
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Input", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(input_frame, text="Enter text or URL:").pack(anchor=tk.W)
        
        self.text_input = tk.Text(input_frame, height=3, width=50, 
                                  font=('Arial', 10))
        self.text_input.pack(fill=tk.X, pady=(5, 0))
        
        # Options section
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Error correction dropdown
        error_frame = ttk.Frame(options_frame)
        error_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(error_frame, text="Error Correction:").pack(side=tk.LEFT)
        
        self.error_var = tk.StringVar(value='Medium (15%)')
        error_dropdown = ttk.Combobox(error_frame, textvariable=self.error_var,
                                      values=list(self.ERROR_LEVELS.keys()),
                                      state='readonly', width=15)
        error_dropdown.pack(side=tk.RIGHT)
        
        # Size slider
        size_frame = ttk.Frame(options_frame)
        size_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(size_frame, text="Size:").pack(side=tk.LEFT)
        
        self.size_var = tk.IntVar(value=10)
        size_slider = ttk.Scale(size_frame, from_=5, to=20, 
                                variable=self.size_var, orient=tk.HORIZONTAL)
        size_slider.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        generate_btn = ttk.Button(button_frame, text="Generate QR Code",
                                  command=self._on_generate)
        generate_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        
        save_btn = ttk.Button(button_frame, text="Save Image",
                              command=self._on_save)
        save_btn.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(5, 0))
        
        # QR Code display area
        display_frame = ttk.LabelFrame(main_frame, text="Preview", padding="10")
        display_frame.pack(fill=tk.BOTH, expand=True)
        
        self.qr_label = ttk.Label(display_frame, text="QR code will appear here",
                                  anchor=tk.CENTER)
        self.qr_label.pack(expand=True)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var,
                               relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, pady=(10, 0))
    
    def _on_generate(self):
        """Handle generate button click."""
        data = self.text_input.get("1.0", tk.END).strip()
        
        if not data:
            messagebox.showwarning("Warning", "Please enter text or URL")
            return
        
        try:
            # Update generator settings
            self.box_size = self.size_var.get()
            self.error_correction = self.ERROR_LEVELS[self.error_var.get()]
            
            # Generate QR code
            qr_image = self.generate(data)
            
            # Convert to PhotoImage for display
            # Resize for preview (max 250x250)
            display_size = 250
            qr_image_resized = qr_image.get_image().resize(
                (display_size, display_size), 
                Image.Resampling.NEAREST
            )
            
            self.photo = ImageTk.PhotoImage(qr_image_resized)
            self.qr_label.configure(image=self.photo, text="")
            
            self.status_var.set(f"Generated QR code for: {data[:30]}...")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set("Error generating QR code")
    
    def _on_save(self):
        """Handle save button click."""
        if self.last_generated_image is None:
            messagebox.showwarning("Warning", 
                                   "Generate a QR code first before saving")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All files", "*.*")
            ],
            title="Save QR Code"
        )
        
        if filepath:
            try:
                self.save(filepath)
                self.status_var.set(f"Saved to: {filepath}")
                messagebox.showinfo("Success", f"QR code saved to:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")
    
    def run(self):
        """Start the application main loop."""
        self.root.mainloop()


# Main entry point
if __name__ == "__main__":
    app = QRCodeApp()
    app.run()
