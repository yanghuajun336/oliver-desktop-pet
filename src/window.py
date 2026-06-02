"""Main application window"""
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, QRect, QPoint
from PyQt5.QtGui import QPainter, QColor, QBrush
from src.config import WINDOW, ANIMATION, COLOR_PALETTE
from src.renderer import Renderer
from src.character import Character
from src.interaction import InteractionHandler


class OliverWindow(QWidget):
    """Main window for Oliver desktop pet"""
    
    def __init__(self):
        super().__init__()
        self.init_window()
        self.setup_ui()
        self.setup_timers()
        self.setup_interactions()
        
    def init_window(self):
        """Initialize window properties"""
        self.setWindowTitle("Oliver - Star Scholar Owl")
        self.setGeometry(
            100, 100,
            WINDOW['width'],
            WINDOW['height']
        )
        
        # Window flags
        if WINDOW['frameless']:
            self.setWindowFlags(Qt.FramelessWindowHint)
        if WINDOW['always_on_top']:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        
        # Transparency
        if WINDOW['transparent_background']:
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.setStyleSheet("background-color: transparent;")
        
        self.setCursor(Qt.ArrowCursor)
    
    def setup_ui(self):
        """Setup UI components"""
        self.character = Character()
        self.renderer = Renderer(self)
        
    def setup_timers(self):
        """Setup animation timers"""
        self.frame_timer = QTimer()
        self.frame_timer.timeout.connect(self.update_frame)
        frame_interval = int(1000 / ANIMATION['fps'])
        self.frame_timer.start(frame_interval)
        
    def setup_interactions(self):
        """Setup interaction handler"""
        self.interaction_handler = InteractionHandler(self)
        
    def update_frame(self):
        """Update frame and trigger repaint"""
        self.character.update(1.0 / ANIMATION['fps'])
        self.update()  # Trigger paintEvent
    
    def paintEvent(self, event):
        """Paint event handler"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        # Draw background (transparent or semi-transparent)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 0))
        
        # Draw character
        self.renderer.render(painter, self.character)
        
        painter.end()
    
    def mousePressEvent(self, event):
        """Handle mouse press"""
        if event.button() == Qt.LeftButton:
            self.drag_start = event.pos()
        elif event.button() == Qt.RightButton:
            self.interaction_handler.show_context_menu(event.globalPos())
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging"""
        if hasattr(self, 'drag_start') and self.drag_start is not None:
            delta = event.pos() - self.drag_start
            new_pos = self.pos() + delta
            self.move(new_pos)
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        self.drag_start = None
