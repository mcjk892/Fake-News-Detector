import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from researcher import researcher
from models import db, SearchHistory
import os

app = Flask(__name__)
CORS(app)

# Database Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'history.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    input_text = data.get('input', '')
    
    if not input_text:
        return jsonify({"error": "No input provided"}), 400
    
    result = researcher.analyze(input_text)
    
    # Save to History
    try:
        new_history = SearchHistory(
            input_text=input_text,
            verdict=result.get('verdict', 'Unknown')
        )
        db.session.add(new_history)
        db.session.commit()
    except Exception as e:
        print(f"Error saving history: {e}")
        
    return jsonify(result)

@app.route('/history', methods=['GET'])
def get_history():
    history = SearchHistory.query.order_by(SearchHistory.timestamp.desc()).limit(20).all()
    return jsonify([h.to_dict() for h in history])

@app.route('/history/delete', methods=['POST'])
def delete_history():
    try:
        db.session.query(SearchHistory).delete()
        db.session.commit()
        return jsonify({"message": "History deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
