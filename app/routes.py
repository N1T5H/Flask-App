from flask import Blueprint, request, jsonify
from .models import Quote, db
from .metrics import QUOTE_COUNTER

quote_bp = Blueprint('quote', __name__)

@quote_bp.route('/quote', methods=['GET'])
def get_quote():
    quote = Quote.query.order_by(db.func.random()).first()
    QUOTE_COUNTER.inc()
    return jsonify({'quote': quote.text}) if quote else jsonify({'message': 'No quotes found.'}), 200

@quote_bp.route('/quote', methods=['POST'])
def add_quote():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Quote text is required'}), 400

    new_quote = Quote(text=data['text'])
    db.session.add(new_quote)
    db.session.commit()
    return jsonify({'message': 'Quote added successfully'}), 201
