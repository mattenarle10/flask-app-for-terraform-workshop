from flask import Blueprint, jsonify
from services import table

bp = Blueprint("delete", __name__)


@bp.route("/products/<product_id>", methods=["DELETE"])
def delete_product(product_id: str):
    try:
        table.delete_item(Key={"product_id": product_id})
        return jsonify({"message": "Product deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


