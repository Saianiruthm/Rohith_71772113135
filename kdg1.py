import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QTextEdit
from PyQt5.QtCore import Qt
from main import identify_cuisine_diet, generate_kitchen_description_auto_main_cuisine_random
import pandas as pd

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Menu Analyzer")
        
        # Load CSV file, prepare data
        self.df = pd.read_csv("recipes.csv", usecols=['Unnamed: 0', 'recipe_name', 'ingredients', 'cuisine_path'])
        self.df.columns = ['ID', 'Recipe Name', 'Ingredients', 'Cuisine Path']
        split_df = self.df['Cuisine Path'].apply(lambda x: pd.Series(x.split('/')))
        split_df.columns = [f'Cuisine Path_{i}' for i in range(split_df.shape[1])]
        self.df = pd.concat([self.df, split_df], axis=1)
        self.df.drop('Cuisine Path', axis=1, inplace=True)
        
        self.menu_input = QTextEdit()
        self.menu_input.setPlaceholderText("Enter menu items separated by commas")
        
        self.menu_button = QPushButton("Analyze Menu")
        self.menu_button.clicked.connect(self.analyze_menu)
        
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        
        layout = QVBoxLayout()
        layout.addWidget(self.menu_input)
        layout.addWidget(self.menu_button)
        layout.addWidget(self.result_label)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
    def analyze_menu(self):
        menu = self.menu_input.toPlainText().strip().split(",")  # Get menu items from input and split by comma
        
        cuisine_dict = identify_cuisine_diet(menu, self.df)
        main_cuisine_description_random = generate_kitchen_description_auto_main_cuisine_random(cuisine_dict)
        
        self.result_label.setText(main_cuisine_description_random)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
