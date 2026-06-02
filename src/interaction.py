"""Interaction handler for user input"""
from PyQt5.QtWidgets import QMenu
from PyQt5.QtCore import Qt


class InteractionHandler:
    """Handles user interactions"""
    
    def __init__(self, window):
        self.window = window
    
    def show_context_menu(self, pos):
        """Show right-click context menu"""
        menu = QMenu(self.window)
        
        # Menu items
        action_info = menu.addAction("📖 Show Info")
        action_info.triggered.connect(self.show_info)
        
        action_settings = menu.addAction("⚙️ Settings")
        action_settings.triggered.connect(self.show_settings)
        
        menu.addSeparator()
        
        action_toggle_night = menu.addAction("🌙 Night Mode")
        action_toggle_night.triggered.connect(self.toggle_night_mode)
        
        action_toggle_sound = menu.addAction("🔊 Sound")
        action_toggle_sound.triggered.connect(self.toggle_sound)
        
        menu.addSeparator()
        
        action_exit = menu.addAction("❌ Exit")
        action_exit.triggered.connect(self.exit_app)
        
        menu.exec_(pos)
    
    def show_info(self):
        """Show character information"""
        print("Oliver - Star Scholar Owl v0.1.0")
        print("A delightful Windows desktop pet")
    
    def show_settings(self):
        """Show settings dialog"""
        print("Settings dialog - TODO")
    
    def toggle_night_mode(self):
        """Toggle night mode"""
        print("Night mode toggled - TODO")
    
    def toggle_sound(self):
        """Toggle sound"""
        print("Sound toggled - TODO")
    
    def exit_app(self):
        """Exit application"""
        self.window.close()
