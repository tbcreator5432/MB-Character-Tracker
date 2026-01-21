#!/usr/bin/env python3
"""
Sample save file generator for testing the MB Character Tracker.
Creates a dummy .sav file with sample data.
"""

import struct
import os


def create_sample_save():
    """Create a sample Mount & Blade save file for testing."""
    data = bytearray()
    
    # Add some header bytes
    data.extend(b'\x00' * 100)
    
    # Add character name
    name = "TestHero"
    data.extend(struct.pack('<I', len(name)))
    data.extend(name.encode('utf-8'))
    
    # Add padding
    data.extend(b'\x00' * 50)
    
    # Add level (e.g., 15)
    data.extend(struct.pack('<I', 15))
    
    # Add some padding
    data.extend(b'\x00' * 200)
    
    # Add renown (e.g., 250)
    data.extend(struct.pack('<I', 250))
    
    # Add padding
    data.extend(b'\x00' * 100)
    
    # Add gold (e.g., 5000)
    data.extend(struct.pack('<I', 5000))
    
    # Add padding before skills
    data.extend(b'\x00' * 500)
    
    # Add skills (24 skills, values 0-10)
    skills = [5, 3, 2, 4, 6, 3, 5, 4, 2, 1, 3, 4, 5, 2, 3, 4, 5, 3, 4, 2, 6, 3, 5, 4]
    for skill in skills:
        data.extend(struct.pack('<I', skill))
    
    # Add padding before proficiencies
    data.extend(b'\x00' * 500)
    
    # Add proficiencies (6 proficiencies)
    proficiencies = [150, 120, 100, 180, 90, 80]
    for prof in proficiencies:
        data.extend(struct.pack('<I', prof))
    
    # Add padding before equipment
    data.extend(b'\x00' * 1000)
    
    # Add equipment items
    items = [
        "Great Helm",
        "Coat of Plates",
        "Iron Greaves",
        "Mail Mittens",
        "Bastard Sword",
        "Knightly Heater Shield",
        "Heavy Crossbow",
        "Bolts"
    ]
    
    for item in items:
        data.extend(struct.pack('<I', len(item)))
        data.extend(item.encode('utf-8'))
        # Add some stats
        data.extend(struct.pack('<I', 45))  # armor or damage
        data.extend(b'\x00' * 50)
    
    # Add padding before faction relations
    data.extend(b'\x00' * 2000)
    
    # Add faction relations (-100 to +100)
    relations = [25, -15, 10, 30, -5, 0, 20, -10, 15, 5, -20, 8]
    for rel in relations:
        data.extend(struct.pack('<i', rel))
    
    # Add more padding
    data.extend(b'\x00' * 5000)
    
    return bytes(data)


if __name__ == "__main__":
    save_data = create_sample_save()
    
    with open('sample.sav', 'wb') as f:
        f.write(save_data)
    
    print("Sample save file created: sample.sav")
    print(f"File size: {len(save_data)} bytes")
