from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QLineEdit, QBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt 
import sys 

class Window(QWidget):
    def __init__(self):
        super().__init__()
        layout = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        self.setWindowTitle("NYSE Software")
        self.setLayout(layout)

        title = QLabel("WELCOME")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        user = QLabel("Username")
        layout.addWidget(user)

        self.input1 = QLineEdit()
        layout.addWidget(self.input1)

        pwd = QLabel("Password")
        layout.addWidget(pwd)

        self.input2 = QLineEdit()
        self.input2.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.input2)

        button1 = QPushButton("Register")
        layout.addWidget(button1)

        button2 = QPushButton("Login")
        button2.clicked.connect(self.login)
        layout.addWidget(button2)

    def login(self):
        if self.input1.text() == "Claflin" and self.input2.text() == "123456":
            QMessageBox.information(self, "Success", "Login successful")
            # Open new window
            self.open_new_window()
        else:
           QMessageBox.warning(self, "Error", "Invalid username or password")

    def open_new_window(self):
        self.new_window = NewWindow()
        self.new_window.show()

class NewWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Home Page")
        layout = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.setLayout(layout)
        
        label = QLabel("NYSE Software")
        layout.addWidget(label)
        
        # Add buttons for navigation
        buttons_layout = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        
        home_button = QPushButton("Home")
        home_button.clicked.connect(self.go_to_home)
        buttons_layout.addWidget(home_button)
        
        profile_button = QPushButton("Profile")
        profile_button.clicked.connect(self.go_to_profile)
        buttons_layout.addWidget(profile_button)
        
        stock_button = QPushButton("Stocks")
        stock_button.clicked.connect(self.go_to_stock)
        buttons_layout.addWidget(stock_button)
        
        portfolio_button = QPushButton("Portfolio")
        portfolio_button.clicked.connect(self.go_to_portfolio)
        buttons_layout.addWidget(portfolio_button)

        layout.addLayout(buttons_layout)

        button = QPushButton("Logout")
        button.clicked.connect(self.logout)
        layout.addWidget(button)

    def logout(self):
        # Close the current window (home page)
        self.close()
        # Open the login window again
        login_window.show() # type: ignore

    def go_to_home(self):
        QMessageBox.information(self, "Navigation", "Already on the Home Page")

    def go_to_profile(self):
        self.profile_window = ProfileWindow()
        self.profile_window.show()

    def go_to_stock(self):
        self.stock_window = StockWindow()
        self.stock_window.show()

    def go_to_portfolio(self):
        self.portfolio_window = PortfolioWindow()
        self.portfolio_window.show()

class ProfileWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Profile")
        layout = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.setLayout(layout)
        
        label = QLabel("Profile")
        layout.addWidget(label)
        
        # Add text boxes
        layout.addWidget(QLabel("First Name:"))
        layout.addWidget(QLabel("Last Name:"))
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(QLabel("Number:"))
        
        button = QPushButton("Save")
        layout.addWidget(button)

class StockWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stocks")
        layout = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.setLayout(layout)
        
        label = QLabel("Stocks")
        layout.addWidget(label)
        
        # Add text boxes
        layout.addWidget(QLabel("Stock Name:"))
        layout.addWidget(QLineEdit())
        layout.addWidget(QLabel("Quantity:"))
        layout.addWidget(QLabel("Price:"))
        
        button = QPushButton("Search")
        layout.addWidget(button)

class PortfolioWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Portfolio")
        layout = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.setLayout(layout)
        
        label = QLabel("Portfolio")
        layout.addWidget(label)
        
        # Add text boxes
        layout.addWidget(QLabel("Stock Name:"))
        layout.addWidget(QLineEdit())
        layout.addWidget(QLabel("Quantity:"))
        layout.addWidget(QLabel("Current Price:"))
        
        
        button = QPushButton("Search")
        layout.addWidget(button)

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
