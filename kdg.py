import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
import pathlib
import textwrap
import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
GOOGLE_API_KEY='apikey'

genai.configure(api_key=GOOGLE_API_KEY)

for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)

model = genai.GenerativeModel('gemini-pro')

def generate_kitchen_description (menu):
  text = "Generate a description of kitchen that offers {menu}"
  response = model.generate_content(text)
  return response.text


class KitchenDescriptionApp(QWidget):
  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):
    self.setWindowTitle('Kitchen Description Generator')

    # Layout
    layout = QVBoxLayout()
    self.setLayout(layout)

    # Menu input
    self.menu_label = QLabel("Enter menu items separated by commas:")
    self.menu_input = QTextEdit()
    layout.addWidget(self.menu_label)
    layout.addWidget(self.menu_input)

    # Generate button
    self.generate_button = QPushButton("Generate Description")
    self.generate_button.clicked.connect(self.generate_description)
    layout.addWidget(self.generate_button)

    # Description output
    self.description_label = QLabel("")
    layout.addWidget(self.description_label)

    # Show the app
    self.show()

  def generate_description(self):
    menu = self.menu_input.toPlainText().strip()
    if menu:
      description = generate_kitchen_description(menu)
      self.description_label.setText(description)
    else:
      self.description_label.setText("Please enter menu items.")

if __name__ == '__main__':
  app = QApplication(sys.argv)
  # Configure API key
  genai.configure(api_key=GOOGLE_API_KEY)
  model = genai.GenerativeModel('gemini-pro')

  # Create and run the app
  window = KitchenDescriptionApp()
  sys.exit(app.exec_())
