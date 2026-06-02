# Oliver - Star Scholar Owl 🦉

A delightful Windows desktop pet application featuring Oliver, a star scholar owl with rich animations and interactive capabilities.

## Features

✨ **Rich Character Design**
- Detailed owl character with unique visual style
- Multiple animation states (idle, thinking, surprised, confused, etc.)
- Dynamic particle effects and visual feedback

🎬 **Smooth Animations**
- 60 FPS animation system
- State-based animation manager
- Easing functions for natural motion

🖱️ **Interactive Gameplay**
- Mouse hover and click interactions
- Drag-and-drop repositioning
- Context menu with options

🎨 **Visual Polish**
- Custom color palette
- Ambient particle system
- Time-based visual effects (day/night modes)

## Requirements

- Python 3.9+
- PyQt5 5.15.0+
- Windows 10/11

## Installation

```bash
# Clone the repository
git clone https://github.com/yanghuajun336/oliver-desktop-pet.git
cd oliver-desktop-pet

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m src.main
```

## Project Structure

```
oliver-desktop-pet/
├── src/
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration and constants
│   ├── window.py            # Main window class
│   ├── renderer.py          # Rendering engine
│   ├── character.py         # Character class and state management
│   ├── animator.py          # Animation system (coming soon)
│   ├── interaction.py       # User interaction handler
│   ├── particles.py         # Particle system (coming soon)
│   ├── audio.py             # Audio management (coming soon)
│   ├── assets/
│   │   ├── sprites/         # Character sprites and assets
│   │   ├── sounds/          # Sound effects
│   │   └── fonts/           # Custom fonts
│   └── utils/
│       ├── geometry.py      # Geometric calculations
│       ├── color_utils.py   # Color manipulation
│       ├── math_helpers.py  # Mathematical utilities
│       └── time_utils.py    # Time utilities
├── requirements.txt
└── README.md
```

## Development Status

- [x] Project structure and configuration
- [x] Main window and event loop
- [x] Character class and state management
- [x] Basic rendering pipeline
- [ ] Detailed character drawing
- [ ] Animation system
- [ ] Particle effects
- [ ] Audio system
- [ ] Advanced interactions
- [ ] Packaging as EXE

## Architecture

### Character Animation System
- State-based character management
- Frame-by-frame animation updates
- Easing functions for smooth motion
- Support for parallel animations

### Rendering Pipeline
1. Clear canvas
2. Draw background particles
3. Draw body and main character elements
4. Draw wings and secondary elements
5. Draw head and facial features
6. Draw accessories
7. Draw foreground effects and UI

## Configuration

Edit `src/config.py` to customize:
- Color palette
- Animation timings
- Character dimensions
- Particle system parameters
- Window properties
- Audio settings

## Controls

- **Left Click**: Interact with Oliver (triggers random action)
- **Right Click**: Open context menu
- **Drag**: Move Oliver around the screen

## Menu Options

- 📖 Show Info - Display character information
- ⚙️ Settings - Open settings dialog
- 🌙 Night Mode - Toggle night mode
- 🔊 Sound - Toggle sound effects
- ❌ Exit - Close the application

## License

MIT License

## Author

Yang Huajun (@yanghuajun336)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
