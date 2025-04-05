# app.py
from flask import Flask, render_template
import main  # Import file chứa game của bạn

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Render giao diện chính của game

@app.route('/run_game')
def run_game():
    main.run_game()  # Gọi hàm chạy game trong main.py
    return "Game is running"  # Trả về thông báo khi game đang chạy

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
