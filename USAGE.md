# Mount & Blade Character Tracker - Usage Guide

## Overview

MB Character Tracker is a desktop application that parses Mount & Blade save files (`.sav`) and displays character information in an easy-to-read tabbed interface.

## Installation

### Requirements
- Python 3.6 or higher
- tkinter (typically included with Python)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/tbcreator5432/MB-Character-Tracker.git
   cd MB-Character-Tracker
   ```

2. (Optional) Install any additional dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Starting the GUI
```bash
python main.py
```

This will open the main application window with a tabbed interface.

### Loading a Save File
1. Click the "Open Save File" button or use **File > Open Save File** from the menu
2. Navigate to your Mount & Blade save directory:
   - Windows: Usually in `Documents\Mount&Blade Warband\Characters\<character_name>\`
   - The file will have a `.sav` extension
3. Select the save file you want to analyze
4. The application will parse the file and display the data across multiple tabs

### Viewing Character Data

The application displays data in four main tabs:

#### 1. Character Info Tab
Displays basic character information:
- **Name**: Your character's name
- **Level**: Current character level
- **Renown**: Your character's renown value
- **Gold**: Amount of gold/denars

#### 2. Skills & Proficiencies Tab
Shows two columns:
- **Left side - Skills**: All 24 character skills with their current values (0-10)
  - Combat skills (Ironflesh, Power Strike, etc.)
  - Movement skills (Athletics, Riding, etc.)
  - Leadership skills (Leadership, Prisoner Management, etc.)
  - Support skills (Surgery, First Aid, etc.)

- **Right side - Weapon Proficiencies**: Six weapon type proficiencies (0-500+)
  - One Handed
  - Two Handed
  - Polearm
  - Archery
  - Crossbow
  - Throwing

#### 3. Equipment Tab
Displays equipped items with their stats:
- Helmet/Head armor
- Body armor
- Leg armor
- Hand armor/Gloves
- Weapons (up to 4 slots)
- Item statistics (armor values, damage, etc.)

#### 4. Faction Relations Tab
Shows your character's relationship with all major factions:
- Positive values (+) indicate friendly relations
- Negative values (-) indicate hostile relations
- Factions include: Swadia, Vaegirs, Khergits, Nords, Rhodoks, Sarranids

## Testing

### Using the Sample Save File
A sample save file is included for testing:

1. Create the sample save:
   ```bash
   python create_sample_save.py
   ```

2. This creates `sample.sav` with test data:
   - Character named "TestHero"
   - Level 15
   - 250 Renown
   - 5000 Gold
   - Various skill and proficiency values

3. Load `sample.sav` in the application to see how it displays data

### Command-Line Testing
You can test the parser without the GUI:

```bash
python test_parser.py
```

This runs the parser on `sample.sav` and displays all extracted data in the terminal.

## Troubleshooting

### "No file loaded" Message
- Make sure you've selected a valid `.sav` file
- Check that the file is not corrupted

### Parser Returns Zeros or Incorrect Data
- Mount & Blade save files use a proprietary binary format
- Different game versions (Warband, Original, Mods) may have slightly different formats
- The parser uses heuristics to locate data and may not work perfectly with all save files
- Equipment and faction relation parsing depends heavily on save file structure

### GUI Doesn't Start
- Ensure Python is installed correctly
- Check that tkinter is available: `python -c "import tkinter"`
- On Linux, you may need to install: `sudo apt-get install python3-tk`

## File Format Notes

Mount & Blade save files are binary files with:
- Length-prefixed strings for names and text
- 32-bit integers for stats, skills, and counters
- Complex structures for equipment, faction data, and party information

The parser uses pattern matching to locate:
1. Character name (length-prefixed string in early part of file)
2. Basic stats (consecutive integers in reasonable ranges)
3. Skills (24 consecutive values 0-10)
4. Proficiencies (6 consecutive values 0-700)
5. Equipment and faction data (more complex, location varies)

## Compatibility

- Tested with Mount & Blade: Warband save files
- May work with the original Mount & Blade
- Mod compatibility depends on how the mod modifies save structure
- Works on Windows, macOS, and Linux (with tkinter installed)

## Tips

1. **Backup your save files** before any operations
2. Save files are located in different directories depending on your game version
3. The parser is read-only and won't modify your save files
4. If data seems incorrect, it may be due to save file format variations
5. Use the sample save file to verify the application works on your system

## Advanced Usage

### Using the Parser Programmatically

You can use the parser in your own Python scripts:

```python
from mb_parser import MBSaveParser

# Create parser instance
parser = MBSaveParser()

# Parse a save file
data = parser.parse('path/to/save.sav')

# Access parsed data
print(f"Character: {data['name']}")
print(f"Level: {data['level']}")
print(f"Gold: {data['gold']}")

# Access skills
for skill, value in data['skills'].items():
    print(f"{skill}: {value}")
```

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Submit a pull request with improvements
- Check the README.md for general information

## License

This project is open source and available under the MIT License.
