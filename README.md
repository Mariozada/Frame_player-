# GIF Frame Player

A simple Python application for playing GIF files frame by frame with forward and backward navigation controls.

## Features

- Load and display GIF files
- **Drag & Drop Support**: Simply drag GIF files into the application window
- Step forward and backward through frames
- Progress bar for quick navigation to any frame
- Keyboard shortcuts (Left/Right arrows)
- Automatic frame resizing to fit display
- Frame counter display
- Loop through frames (wraps around at beginning/end)

## Requirements

- Python 3.6+
- Pillow (PIL) library
- tkinter (usually comes with Python)
- tkinterdnd2 (for drag & drop functionality)

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python gif_frame_player.py
```

### Controls

- **Drag & Drop**: Drag any GIF file into the application window to load it instantly
- **Open GIF**: Click the "Open GIF" button to load a GIF file
- **Previous Frame**: Click "◀ Previous" button or press Left arrow key
- **Next Frame**: Click "Next ▶" button or press Right arrow key
- **Progress Bar**: Drag the slider to jump to any frame
- **Keyboard Shortcuts**:
  - `Ctrl+O`: Open file dialog
  - `←` (Left Arrow): Previous frame
  - `→` (Right Arrow): Next frame

### Features

- **Frame Navigation**: Step through GIF frames one by one
- **Drag & Drop**: Instantly load GIF files by dragging them into the window
- **Loop Playback**: Automatically loops to the beginning when reaching the end
- **Frame Counter**: Shows current frame number and total frames
- **Responsive Display**: Frames are automatically resized to fit the window while maintaining aspect ratio
- **File Info**: Displays the loaded file name and frame count

## Example Usage

1. Run the application
2. **Drag & drop** a GIF file into the window OR click "Open GIF" to browse
3. Use the Previous/Next buttons or arrow keys to navigate through frames
4. Use the progress bar to jump to specific frames
5. Try the included `sample.gif` for testing

## Supported Formats

- GIF files (.gif)
- Both animated and static GIF images
- Palette and RGB color modes

## Technical Details

The application uses:
- **tkinter**: For the GUI interface
- **PIL (Pillow)**: For image processing and GIF frame extraction
- **tkinterdnd2**: For drag and drop functionality
- **Threading-safe design**: Handles GIF loading and display efficiently

## License

This project is open source and available under the MIT License.
