from flask import Flask
import os
import json
from decimal import Decimal
from routes.create import bp as create_bp
from routes.get import bp as get_bp
from routes.update import bp as update_bp
from routes.delete import bp as delete_bp

app = Flask(__name__)

# Enable Decimal -> float serialization for JSON responses
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

app.json_encoder = DecimalEncoder

app.register_blueprint(get_bp)
app.register_blueprint(create_bp)
app.register_blueprint(update_bp)
app.register_blueprint(delete_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))