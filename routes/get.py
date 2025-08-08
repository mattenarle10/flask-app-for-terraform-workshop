from flask import Blueprint, jsonify, render_template
from ..services import table

bp = Blueprint("get", __name__)


@bp.route("/", methods=["GET"])
def home_ui():
    return render_template("index.html")


@bp.route("/form", methods=["GET"])
def product_form():
    return render_template("index.html")


@bp.route("/products", methods=["GET"])
def get_products():
    try:
        response = table.scan()
        products = response.get("Items", [])
        sorted_products = sorted(products, key=lambda x: x.get("created_at", ""))
        return jsonify(sorted_products), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


