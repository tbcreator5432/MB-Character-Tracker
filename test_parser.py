#!/usr/bin/env python3
"""
Test script for MB Character Tracker

This script tests the parser functionality without requiring the GUI.
"""

from mb_parser import MBSaveParser


def test_parser():
    """Test the parser with the sample save file."""
    print("=" * 60)
    print("MB Character Tracker - Parser Test")
    print("=" * 60)
    
    parser = MBSaveParser()
    
    # Test with sample save file
    print("\nParsing sample.sav...")
    try:
        data = parser.parse('sample.sav')
        
        print("\n" + "=" * 60)
        print("CHARACTER INFORMATION")
        print("=" * 60)
        print(f"Name:   {data['name']}")
        print(f"Level:  {data['level']}")
        print(f"Renown: {data['renown']}")
        print(f"Gold:   {data['gold']}")
        
        print("\n" + "=" * 60)
        print("SKILLS")
        print("=" * 60)
        for skill, value in data['skills'].items():
            print(f"{skill:25s}: {value}")
        
        print("\n" + "=" * 60)
        print("WEAPON PROFICIENCIES")
        print("=" * 60)
        for prof, value in data['proficiencies'].items():
            print(f"{prof:15s}: {value}")
        
        print("\n" + "=" * 60)
        print("EQUIPMENT")
        print("=" * 60)
        if data['equipment']:
            for item in data['equipment']:
                print(f"\n{item['slot']}:")
                print(f"  Name: {item['name']}")
                if item['stats']:
                    print(f"  Stats: {item['stats']}")
        else:
            print("No equipment found")
        
        print("\n" + "=" * 60)
        print("FACTION RELATIONS")
        print("=" * 60)
        for faction, relation in data['faction_relations'].items():
            print(f"{faction:30s}: {relation:+4d}")
        
        print("\n" + "=" * 60)
        print("Test completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError during parsing: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = test_parser()
    exit(0 if success else 1)
