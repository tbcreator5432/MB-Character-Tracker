"""
Mount & Blade Character Tracker - Main Application

A desktop application with a tabbed UI for parsing and displaying
Mount & Blade .sav files with player character data.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from mb_parser import MBSaveParser


class MBCharacterTracker:
    """Main application window for MB Character Tracker."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Mount & Blade Character Tracker")
        self.root.geometry("800x600")
        
        self.parser = MBSaveParser()
        self.current_file = None
        
        self._create_menu()
        self._create_ui()
        
    def _create_menu(self):
        """Create the menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Save File...", command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def _create_ui(self):
        """Create the main UI with tabs."""
        # Top frame for file info
        self.top_frame = tk.Frame(self.root, bg="#f0f0f0", pady=10)
        self.top_frame.pack(side=tk.TOP, fill=tk.X)
        
        self.file_label = tk.Label(
            self.top_frame, 
            text="No file loaded. Use File > Open Save File to load a .sav file.",
            bg="#f0f0f0",
            font=("Arial", 10)
        )
        self.file_label.pack()
        
        # Button to open file
        self.open_button = tk.Button(
            self.top_frame,
            text="Open Save File",
            command=self.open_file,
            padx=20,
            pady=5
        )
        self.open_button.pack(pady=5)
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.character_tab = tk.Frame(self.notebook)
        self.skills_tab = tk.Frame(self.notebook)
        self.equipment_tab = tk.Frame(self.notebook)
        self.relations_tab = tk.Frame(self.notebook)
        
        self.notebook.add(self.character_tab, text="Character Info")
        self.notebook.add(self.skills_tab, text="Skills & Proficiencies")
        self.notebook.add(self.equipment_tab, text="Equipment")
        self.notebook.add(self.relations_tab, text="Faction Relations")
        
        # Initialize tabs
        self._init_character_tab()
        self._init_skills_tab()
        self._init_equipment_tab()
        self._init_relations_tab()
    
    def _init_character_tab(self):
        """Initialize the Character Info tab."""
        # Create a frame for better layout
        frame = tk.Frame(self.character_tab, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = tk.Label(frame, text="Character Information", font=("Arial", 16, "bold"))
        title.pack(pady=(0, 20))
        
        # Character info fields
        info_frame = tk.Frame(frame)
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        # Name
        tk.Label(info_frame, text="Name:", font=("Arial", 12, "bold"), anchor='w').grid(row=0, column=0, sticky='w', pady=5)
        self.name_label = tk.Label(info_frame, text="-", font=("Arial", 12), anchor='w')
        self.name_label.grid(row=0, column=1, sticky='w', padx=(10, 0), pady=5)
        
        # Level
        tk.Label(info_frame, text="Level:", font=("Arial", 12, "bold"), anchor='w').grid(row=1, column=0, sticky='w', pady=5)
        self.level_label = tk.Label(info_frame, text="-", font=("Arial", 12), anchor='w')
        self.level_label.grid(row=1, column=1, sticky='w', padx=(10, 0), pady=5)
        
        # Renown
        tk.Label(info_frame, text="Renown:", font=("Arial", 12, "bold"), anchor='w').grid(row=2, column=0, sticky='w', pady=5)
        self.renown_label = tk.Label(info_frame, text="-", font=("Arial", 12), anchor='w')
        self.renown_label.grid(row=2, column=1, sticky='w', padx=(10, 0), pady=5)
        
        # Gold
        tk.Label(info_frame, text="Gold:", font=("Arial", 12, "bold"), anchor='w').grid(row=3, column=0, sticky='w', pady=5)
        self.gold_label = tk.Label(info_frame, text="-", font=("Arial", 12), anchor='w')
        self.gold_label.grid(row=3, column=1, sticky='w', padx=(10, 0), pady=5)
    
    def _init_skills_tab(self):
        """Initialize the Skills & Proficiencies tab."""
        # Create main container
        container = tk.Frame(self.skills_tab)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side - Skills
        skills_frame = tk.LabelFrame(container, text="Skills", font=("Arial", 12, "bold"), padx=10, pady=10)
        skills_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 5))
        
        # Create scrollable frame for skills
        skills_canvas = tk.Canvas(skills_frame)
        skills_scrollbar = ttk.Scrollbar(skills_frame, orient="vertical", command=skills_canvas.yview)
        self.skills_inner_frame = tk.Frame(skills_canvas)
        
        self.skills_inner_frame.bind(
            "<Configure>",
            lambda e: skills_canvas.configure(scrollregion=skills_canvas.bbox("all"))
        )
        
        skills_canvas.create_window((0, 0), window=self.skills_inner_frame, anchor="nw")
        skills_canvas.configure(yscrollcommand=skills_scrollbar.set)
        
        skills_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        skills_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Right side - Proficiencies
        prof_frame = tk.LabelFrame(container, text="Weapon Proficiencies", font=("Arial", 12, "bold"), padx=10, pady=10)
        prof_frame.grid(row=0, column=1, sticky='nsew', padx=(5, 0))
        
        self.prof_inner_frame = tk.Frame(prof_frame)
        self.prof_inner_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
    
    def _init_equipment_tab(self):
        """Initialize the Equipment tab."""
        frame = tk.Frame(self.equipment_tab, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = tk.Label(frame, text="Equipped Items", font=("Arial", 16, "bold"))
        title.pack(pady=(0, 10))
        
        # Create treeview for equipment
        columns = ("Slot", "Item Name", "Stats")
        self.equipment_tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        # Define headings
        self.equipment_tree.heading("Slot", text="Slot")
        self.equipment_tree.heading("Item Name", text="Item Name")
        self.equipment_tree.heading("Stats", text="Stats")
        
        # Define column widths
        self.equipment_tree.column("Slot", width=150)
        self.equipment_tree.column("Item Name", width=300)
        self.equipment_tree.column("Stats", width=250)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.equipment_tree.yview)
        self.equipment_tree.configure(yscroll=scrollbar.set)
        
        self.equipment_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def _init_relations_tab(self):
        """Initialize the Faction Relations tab."""
        frame = tk.Frame(self.relations_tab, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = tk.Label(frame, text="Faction Relations", font=("Arial", 16, "bold"))
        title.pack(pady=(0, 10))
        
        # Create treeview for relations
        columns = ("Faction", "Relation")
        self.relations_tree = ttk.Treeview(frame, columns=columns, show='headings', height=20)
        
        # Define headings
        self.relations_tree.heading("Faction", text="Faction")
        self.relations_tree.heading("Relation", text="Relation")
        
        # Define column widths
        self.relations_tree.column("Faction", width=400)
        self.relations_tree.column("Relation", width=300)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.relations_tree.yview)
        self.relations_tree.configure(yscroll=scrollbar.set)
        
        self.relations_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def open_file(self):
        """Open a .sav file and parse it."""
        filename = filedialog.askopenfilename(
            title="Select Mount & Blade Save File",
            filetypes=[("Save Files", "*.sav"), ("All Files", "*.*")]
        )
        
        if filename:
            try:
                self.current_file = filename
                self.file_label.config(text=f"Loaded: {os.path.basename(filename)}")
                
                # Parse the file
                self.parser.parse(filename)
                
                # Update all displays
                self.update_display()
                
                messagebox.showinfo("Success", "Save file loaded successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load save file:\n{str(e)}")
    
    def update_display(self):
        """Update all UI elements with parsed data."""
        self.update_character_tab()
        self.update_skills_tab()
        self.update_equipment_tab()
        self.update_relations_tab()
    
    def update_character_tab(self):
        """Update the Character Info tab with parsed data."""
        self.name_label.config(text=self.parser.get_character_name())
        self.level_label.config(text=str(self.parser.get_level()))
        self.renown_label.config(text=str(self.parser.get_renown()))
        self.gold_label.config(text=str(self.parser.get_gold()))
    
    def update_skills_tab(self):
        """Update the Skills & Proficiencies tab with parsed data."""
        # Clear existing widgets
        for widget in self.skills_inner_frame.winfo_children():
            widget.destroy()
        for widget in self.prof_inner_frame.winfo_children():
            widget.destroy()
        
        # Add skills
        skills = self.parser.get_skills()
        for i, (skill_name, skill_value) in enumerate(skills.items()):
            tk.Label(
                self.skills_inner_frame,
                text=f"{skill_name}:",
                font=("Arial", 10),
                anchor='w'
            ).grid(row=i, column=0, sticky='w', pady=2)
            
            tk.Label(
                self.skills_inner_frame,
                text=str(skill_value),
                font=("Arial", 10, "bold"),
                anchor='w'
            ).grid(row=i, column=1, sticky='w', padx=(10, 0), pady=2)
        
        # Add proficiencies
        proficiencies = self.parser.get_proficiencies()
        for i, (prof_name, prof_value) in enumerate(proficiencies.items()):
            tk.Label(
                self.prof_inner_frame,
                text=f"{prof_name}:",
                font=("Arial", 10),
                anchor='w'
            ).grid(row=i, column=0, sticky='w', pady=2)
            
            tk.Label(
                self.prof_inner_frame,
                text=str(prof_value),
                font=("Arial", 10, "bold"),
                anchor='w'
            ).grid(row=i, column=1, sticky='w', padx=(10, 0), pady=2)
    
    def update_equipment_tab(self):
        """Update the Equipment tab with parsed data."""
        # Clear existing items
        for item in self.equipment_tree.get_children():
            self.equipment_tree.delete(item)
        
        # Add equipment
        equipment = self.parser.get_equipment()
        for item in equipment:
            slot = item.get('slot', 'Unknown')
            name = item.get('name', 'Empty')
            stats = item.get('stats', {})
            
            # Format stats string
            stats_str = ", ".join([f"{k}: {v}" for k, v in stats.items()])
            if not stats_str:
                stats_str = "No stats"
            
            self.equipment_tree.insert('', tk.END, values=(slot, name, stats_str))
    
    def update_relations_tab(self):
        """Update the Faction Relations tab with parsed data."""
        # Clear existing items
        for item in self.relations_tree.get_children():
            self.relations_tree.delete(item)
        
        # Add faction relations
        relations = self.parser.get_faction_relations()
        for faction, relation in relations.items():
            # Color code based on relation value
            relation_text = f"{relation:+d}"  # Format with + or - sign
            self.relations_tree.insert('', tk.END, values=(faction, relation_text))
    
    def show_about(self):
        """Show the About dialog."""
        about_text = """Mount & Blade Character Tracker
        
Version 1.0

A desktop application for parsing and viewing
Mount & Blade save files.

Features:
- Character information (name, level, renown, gold)
- Skills and proficiencies
- Equipment and item stats
- Faction relations
"""
        messagebox.showinfo("About", about_text)


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = MBCharacterTracker(root)
    root.mainloop()


if __name__ == "__main__":
    main()
