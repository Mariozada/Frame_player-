#!/usr/bin/env python3
"""
GIF Frame Player
A simple application to play GIF files frame by frame with controls for stepping forward and backward.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os

try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False


class GIFFramePlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("GIF Frame Player")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")
        
        # Initialize variables
        self.gif_frames = []
        self.current_frame = 0
        self.gif_path = None
        self.photo_images = []
        
        self.setup_ui()
        
        # Setup drag and drop after UI is ready
        if DND_AVAILABLE:
            self.setup_drag_drop()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # File selection frame
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Button(file_frame, text="Open GIF", command=self.open_gif).grid(row=0, column=0, padx=(0, 10))
        self.file_label = ttk.Label(file_frame, text="No file selected", foreground="gray")
        self.file_label.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Image display frame
        self.image_frame = ttk.Frame(main_frame, relief="sunken", borderwidth=2)
        self.image_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.image_frame.columnconfigure(0, weight=1)
        self.image_frame.rowconfigure(0, weight=1)
        
        # Image label
        if DND_AVAILABLE:
            instruction_text = "Open a GIF file to start\nor drag & drop a GIF here"
        else:
            instruction_text = "Open a GIF file to start"
            
        self.image_label = ttk.Label(self.image_frame, text=instruction_text, 
                                   font=("Arial", 14), foreground="gray", anchor="center", justify="center")
        self.image_label.grid(row=0, column=0, padx=20, pady=20)
        
        # Control frame
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E))
        control_frame.columnconfigure(1, weight=1)
        
        # Navigation buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        self.prev_button = ttk.Button(button_frame, text="◀ Previous", 
                                    command=self.previous_frame, state="disabled")
        self.prev_button.grid(row=0, column=0, padx=(0, 10))
        
        self.next_button = ttk.Button(button_frame, text="Next ▶", 
                                    command=self.next_frame, state="disabled")
        self.next_button.grid(row=0, column=1, padx=(10, 0))
        
        # Frame info
        info_frame = ttk.Frame(control_frame)
        info_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E))
        info_frame.columnconfigure(1, weight=1)
        
        ttk.Label(info_frame, text="Frame:").grid(row=0, column=0, sticky=tk.W)
        self.frame_info = ttk.Label(info_frame, text="0 / 0", font=("Arial", 12, "bold"))
        self.frame_info.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        # Progress bar
        self.progress_var = tk.IntVar()
        self.progress_bar = ttk.Scale(info_frame, from_=0, to=100, orient="horizontal",
                                    variable=self.progress_var, command=self.on_progress_change)
        self.progress_bar.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        self.progress_bar.configure(state="disabled")
        
        # Keyboard bindings
        self.root.bind('<Left>', lambda e: self.previous_frame())
        self.root.bind('<Right>', lambda e: self.next_frame())
        self.root.bind('<Control-o>', lambda e: self.open_gif())
        self.root.focus_set()
        
    def setup_drag_drop(self):
        """Setup drag and drop functionality using tkinterdnd2"""
        # Register the main window and image frame for file drops
        self.root.drop_target_register(DND_FILES)
        self.image_frame.drop_target_register(DND_FILES)
        
        # Bind the drop event
        self.root.dnd_bind('<<Drop>>', self.on_drop)
        self.image_frame.dnd_bind('<<Drop>>', self.on_drop)
        
    def on_drop(self, event):
        """Handle file drop events"""
        try:
            # Get the dropped files
            files = event.data
            
            # Handle string format (most common)
            if isinstance(files, str):
                # Split multiple files if they're space-separated
                file_list = []
                
                # Handle paths with spaces (enclosed in braces)
                import re
                if '{' in files and '}' in files:
                    # Extract paths from braces
                    matches = re.findall(r'\{([^}]+)\}', files)
                    file_list.extend(matches)
                else:
                    # Simple space-separated paths
                    file_list = files.split()
            else:
                file_list = files if isinstance(files, list) else [files]
            
            # Process the first GIF file found
            gif_found = False
            for file_path in file_list:
                # Clean up the file path
                file_path = file_path.strip().strip('{}').strip('"\'')
                
                # Check if it's a GIF file and exists
                if file_path.lower().endswith('.gif') and os.path.exists(file_path):
                    try:
                        self.load_gif(file_path)
                        gif_found = True
                        break
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to load dropped GIF file:\n{str(e)}")
                        return
            
            if not gif_found:
                messagebox.showwarning("Invalid File", "Please drop a valid GIF file (.gif)")
                
        except Exception as e:
            messagebox.showerror("Drop Error", f"Error processing dropped file:\n{str(e)}")
        
        return 'break'  # Prevent further processing
        
    def open_gif(self):
        """Open and load a GIF file"""
        file_path = filedialog.askopenfilename(
            title="Select a GIF file",
            filetypes=[("GIF files", "*.gif"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.load_gif(file_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load GIF file:\n{str(e)}")
    
    def load_gif(self, file_path):
        """Load GIF frames from file"""
        self.gif_path = file_path
        self.gif_frames = []
        self.photo_images = []
        
        # Open the GIF file
        gif = Image.open(file_path)
        
        # Extract all frames
        try:
            frame_count = 0
            while True:
                # Convert frame to RGB if it's in palette mode
                if gif.mode in ('P', 'PA'):
                    frame = gif.convert('RGBA')
                else:
                    frame = gif.copy()
                
                self.gif_frames.append(frame)
                frame_count += 1
                gif.seek(frame_count)
        except EOFError:
            pass  # End of frames
        
        if not self.gif_frames:
            raise ValueError("No frames found in the GIF file")
        
        # Update UI
        filename = os.path.basename(file_path)
        self.file_label.configure(text=f"Loaded: {filename} ({len(self.gif_frames)} frames)")
        
        # Enable controls
        self.prev_button.configure(state="normal")
        self.next_button.configure(state="normal")
        self.progress_bar.configure(state="normal", to=len(self.gif_frames)-1)
        
        # Show first frame
        self.current_frame = 0
        self.display_frame()
        self.update_frame_info()
        
    def display_frame(self):
        """Display the current frame"""
        if not self.gif_frames:
            return
        
        frame = self.gif_frames[self.current_frame]
        
        # Resize frame to fit the display area while maintaining aspect ratio
        display_width = 600
        display_height = 400
        
        # Calculate scaling factor
        width_ratio = display_width / frame.width
        height_ratio = display_height / frame.height
        scale_factor = min(width_ratio, height_ratio)
        
        new_width = int(frame.width * scale_factor)
        new_height = int(frame.height * scale_factor)
        
        # Resize the frame
        resized_frame = frame.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(resized_frame)
        
        # Update the label
        self.image_label.configure(image=photo, text="")
        self.image_label.image = photo  # Keep a reference to prevent garbage collection
        
    def previous_frame(self):
        """Go to the previous frame"""
        if not self.gif_frames:
            return
        
        if self.current_frame > 0:
            self.current_frame -= 1
        else:
            self.current_frame = len(self.gif_frames) - 1  # Loop to last frame
        
        self.display_frame()
        self.update_frame_info()
        
    def next_frame(self):
        """Go to the next frame"""
        if not self.gif_frames:
            return
        
        if self.current_frame < len(self.gif_frames) - 1:
            self.current_frame += 1
        else:
            self.current_frame = 0  # Loop to first frame
        
        self.display_frame()
        self.update_frame_info()
        
    def update_frame_info(self):
        """Update frame information display"""
        if self.gif_frames:
            self.frame_info.configure(text=f"{self.current_frame + 1} / {len(self.gif_frames)}")
            self.progress_var.set(self.current_frame)
        else:
            self.frame_info.configure(text="0 / 0")
            self.progress_var.set(0)
    
    def on_progress_change(self, value):
        """Handle progress bar changes"""
        if not self.gif_frames:
            return
        
        new_frame = int(float(value))
        if new_frame != self.current_frame:
            self.current_frame = new_frame
            self.display_frame()
            self.update_frame_info()


def main():
    """Main function to run the application"""
    # Create root window with drag and drop support if available
    if DND_AVAILABLE:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
        
    app = GIFFramePlayer(root)
    
    # Center the window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()
