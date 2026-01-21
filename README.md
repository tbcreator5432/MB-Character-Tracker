# Mount & Blade Character Tracker

A desktop application with a tabbed UI for parsing and viewing Mount & Blade save files.

## Features

The application parses Mount & Blade `.sav` files and extracts:

- **Character Information**
  - Character name
  - Level
  - Renown
  - Gold

- **Skills**
  - All 24 character skills (Ironflesh, Power Strike, Athletics, etc.)

- **Weapon Proficiencies**
  - One Handed, Two Handed, Polearm, Archery, Crossbow, Throwing

- **Equipment**
  - Equipped items with their stats
  - Head, Body, Legs, Hands armor
  - Weapons (up to 4 weapon slots)

- **Faction Relations**
  - Relations with all major factions (Swadia, Vaegirs, Khergits, Nords, Rhodoks, Sarranids)

## Requirements

- Python 3.6 or higher
- tkinter (usually included with Python)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/tbcreator5432/MB-Character-Tracker.git
cd MB-Character-Tracker
```

2. Install dependencies (if any):
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

### Using the Application

1. Click **"Open Save File"** button or use **File > Open Save File** menu
2. Select a Mount & Blade `.sav` file
3. Browse through the tabs to view different aspects of your character:
   - **Character Info**: Basic character information
   - **Skills & Proficiencies**: View all skills and weapon proficiencies
   - **Equipment**: See equipped items and their stats
   - **Faction Relations**: Check your standing with each faction

## Testing

To create a sample save file for testing:
```bash
python create_sample_save.py
```

This will create a `sample.sav` file that you can load in the application.

## File Structure

```
MB-Character-Tracker/
├── main.py                  # Main application with GUI
├── mb_parser.py            # Mount & Blade save file parser
├── create_sample_save.py   # Utility to create sample save files
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## How It Works

The application uses a binary parser (`mb_parser.py`) to read Mount & Blade save files, which are stored in a proprietary binary format. The parser extracts character data by:

1. Reading binary structures from the `.sav` file
2. Parsing length-prefixed strings for character names and item names
3. Extracting integer values for stats, skills, and proficiencies
4. Building a structured data model for display

The GUI (`main.py`) is built with tkinter and provides a clean tabbed interface for viewing all extracted data.

## Compatibility

This parser is designed to work with Mount & Blade: Warband save files. The binary format may vary between different versions of the game.

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
