"""
Mount & Blade Save File Parser

This module provides functionality to parse Mount & Blade .sav files
and extract player character data including stats, skills, equipment, and relations.
"""

import struct
import io


class MBSaveParser:
    """Parser for Mount & Blade save files."""
    
    def __init__(self, filepath=None):
        self.filepath = filepath
        self.character_data = {}
        
    def parse_string(self, file):
        """Parse a length-prefixed string from the save file."""
        try:
            length = struct.unpack('<I', file.read(4))[0]
            if length > 0 and length < 10000:  # Reasonable string length
                return file.read(length).decode('utf-8', errors='ignore').rstrip('\x00')
        except:
            pass
        return ""
    
    def parse_integer(self, file):
        """Parse a 32-bit integer from the save file."""
        try:
            return struct.unpack('<I', file.read(4))[0]
        except:
            return 0
    
    def parse_float(self, file):
        """Parse a 32-bit float from the save file."""
        try:
            return struct.unpack('<f', file.read(4))[0]
        except:
            return 0.0
    
    def parse(self, filepath):
        """
        Parse a Mount & Blade save file and extract character data.
        
        Args:
            filepath: Path to the .sav file
            
        Returns:
            Dictionary containing parsed character data
        """
        self.filepath = filepath
        self.character_data = {
            'name': 'Unknown',
            'level': 1,
            'renown': 0,
            'gold': 0,
            'skills': {},
            'proficiencies': {},
            'equipment': [],
            'faction_relations': {}
        }
        
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
                
            # Try to extract character information
            self._extract_character_info(data)
            self._extract_skills(data)
            self._extract_proficiencies(data)
            self._extract_equipment(data)
            self._extract_faction_relations(data)
            
        except Exception as e:
            print(f"Error parsing save file: {e}")
            
        return self.character_data
    
    def _extract_character_info(self, data):
        """Extract basic character information."""
        # Try to find character name - typically stored early in the file
        try:
            # Look for patterns that might indicate character data
            # Mount & Blade stores player name in various locations
            for i in range(0, min(5000, len(data) - 100), 4):
                # Check for string length indicator
                if i + 4 < len(data):
                    length = struct.unpack('<I', data[i:i+4])[0]
                    if 3 < length < 50:  # Reasonable name length
                        try:
                            name = data[i+4:i+4+length].decode('utf-8', errors='ignore').rstrip('\x00')
                            # Check if it looks like a valid name
                            if name and name.isprintable() and not any(c in name for c in ['/', '\\', '\n', '\r']):
                                if len(name) > 3 and ' ' not in name[:3]:  # Basic validation
                                    self.character_data['name'] = name
                                    break
                        except:
                            continue
            
            # Extract level - typically stored as integer
            # This is a simplified approach - actual format varies by M&B version
            if len(data) > 1000:
                # Look for level values (typically 1-60 range)
                for i in range(100, min(2000, len(data) - 4), 4):
                    val = struct.unpack('<I', data[i:i+4])[0]
                    if 1 <= val <= 60:
                        self.character_data['level'] = val
                        break
            
            # Extract renown and gold - stored as integers
            for i in range(100, min(5000, len(data) - 4), 4):
                val = struct.unpack('<I', data[i:i+4])[0]
                # Renown typically ranges from 0 to several thousand
                if 0 <= val <= 10000 and self.character_data['renown'] == 0:
                    self.character_data['renown'] = val
                # Gold can be much higher
                if 0 <= val <= 1000000 and self.character_data['gold'] == 0:
                    self.character_data['gold'] = val
                    
        except Exception as e:
            print(f"Error extracting character info: {e}")
    
    def _extract_skills(self, data):
        """Extract character skills."""
        # Mount & Blade skills: Ironflesh, Power Strike, Power Throw, etc.
        skill_names = [
            "Ironflesh", "Power Strike", "Power Throw", "Power Draw",
            "Weapon Master", "Shield", "Athletics", "Riding",
            "Horse Archery", "Looting", "Trainer", "Tracking",
            "Tactics", "Path-finding", "Spotting", "Inventory Management",
            "Wound Treatment", "Surgery", "First Aid", "Engineer",
            "Persuasion", "Prisoner Management", "Leadership", "Trade"
        ]
        
        try:
            # Initialize all skills to 0
            for skill_name in skill_names:
                self.character_data['skills'][skill_name] = 0
            
            # Try to find skill values (typically 0-10 range)
            skill_count = 0
            for i in range(1000, min(10000, len(data) - 4), 4):
                if skill_count >= len(skill_names):
                    break
                val = struct.unpack('<I', data[i:i+4])[0]
                if 0 <= val <= 10:
                    self.character_data['skills'][skill_names[skill_count]] = val
                    skill_count += 1
                    
        except Exception as e:
            print(f"Error extracting skills: {e}")
    
    def _extract_proficiencies(self, data):
        """Extract weapon proficiencies."""
        proficiency_names = [
            "One Handed", "Two Handed", "Polearm",
            "Archery", "Crossbow", "Throwing"
        ]
        
        try:
            # Initialize all proficiencies to 0
            for prof_name in proficiency_names:
                self.character_data['proficiencies'][prof_name] = 0
            
            # Proficiencies typically range from 0 to 500+
            prof_count = 0
            for i in range(2000, min(15000, len(data) - 4), 4):
                if prof_count >= len(proficiency_names):
                    break
                val = struct.unpack('<I', data[i:i+4])[0]
                if 0 <= val <= 700:
                    self.character_data['proficiencies'][proficiency_names[prof_count]] = val
                    prof_count += 1
                    
        except Exception as e:
            print(f"Error extracting proficiencies: {e}")
    
    def _extract_equipment(self, data):
        """Extract equipped items and their stats."""
        # Equipment slots: Head, Body, Legs, Hands, Weapon1-4
        equipment_slots = [
            "Head", "Body", "Legs", "Hands",
            "Weapon 1", "Weapon 2", "Weapon 3", "Weapon 4"
        ]
        
        try:
            # Look for item names and stats
            # This is simplified - actual format is complex
            item_names = []
            
            # Try to find text strings that might be item names
            for i in range(5000, min(50000, len(data) - 100), 4):
                if len(item_names) >= len(equipment_slots):
                    break
                    
                try:
                    length = struct.unpack('<I', data[i:i+4])[0]
                    if 5 < length < 50:
                        item_name = data[i+4:i+4+length].decode('utf-8', errors='ignore').rstrip('\x00')
                        if item_name and item_name.isprintable():
                            # Look for stats nearby (damage, armor, etc.)
                            stats = {}
                            for j in range(i+4+length, min(i+4+length+100, len(data) - 4), 4):
                                stat_val = struct.unpack('<I', data[j:j+4])[0]
                                if 1 <= stat_val <= 100:  # Reasonable stat range
                                    if 'armor' not in stats:
                                        stats['armor'] = stat_val
                                    elif 'damage' not in stats:
                                        stats['damage'] = stat_val
                                    break
                            
                            self.character_data['equipment'].append({
                                'slot': equipment_slots[len(item_names)] if len(item_names) < len(equipment_slots) else f"Item {len(item_names)}",
                                'name': item_name,
                                'stats': stats
                            })
                            item_names.append(item_name)
                except:
                    continue
                    
        except Exception as e:
            print(f"Error extracting equipment: {e}")
    
    def _extract_faction_relations(self, data):
        """Extract relations with factions."""
        faction_names = [
            "Swadia", "Vaegirs", "Khergits", "Nords", "Rhodoks",
            "Sarranids", "Kingdom of Swadia", "Kingdom of Vaegirs",
            "Kingdom of Nords", "Kingdom of Rhodoks", "Khergit Khanate",
            "Sarranid Sultanate"
        ]
        
        try:
            # Relations typically range from -100 to +100
            for faction in faction_names:
                self.character_data['faction_relations'][faction] = 0
            
            # Try to find relation values
            relation_count = 0
            for i in range(10000, min(30000, len(data) - 4), 4):
                if relation_count >= len(faction_names):
                    break
                val = struct.unpack('<i', data[i:i+4])[0]  # signed integer
                if -100 <= val <= 100:
                    faction = list(self.character_data['faction_relations'].keys())[relation_count]
                    self.character_data['faction_relations'][faction] = val
                    relation_count += 1
                    
        except Exception as e:
            print(f"Error extracting faction relations: {e}")
    
    def get_character_name(self):
        """Get the character name."""
        return self.character_data.get('name', 'Unknown')
    
    def get_level(self):
        """Get the character level."""
        return self.character_data.get('level', 1)
    
    def get_renown(self):
        """Get the character renown."""
        return self.character_data.get('renown', 0)
    
    def get_gold(self):
        """Get the character gold."""
        return self.character_data.get('gold', 0)
    
    def get_skills(self):
        """Get the character skills."""
        return self.character_data.get('skills', {})
    
    def get_proficiencies(self):
        """Get the weapon proficiencies."""
        return self.character_data.get('proficiencies', {})
    
    def get_equipment(self):
        """Get the equipped items."""
        return self.character_data.get('equipment', [])
    
    def get_faction_relations(self):
        """Get faction relations."""
        return self.character_data.get('faction_relations', {})
