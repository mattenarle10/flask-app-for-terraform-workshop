from flask import Blueprint, request, jsonify
from decimal import Decimal
from ..services import table

bp = Blueprint("update", __name__)


@bp.route("/products/<product_id>", methods=["PUT", "PATCH"])
def update_product(product_id: str):
    try:
        data = request.get_json(force=True, silent=True) or {}
        update_expressions = []
        expr_attr_values = {}
        expr_attr_names = {}

        def set_field(field: str, value):
            expr_attr_names[f"#{field}"] = field
            expr_attr_values[f":{field}"] = value
            update_expressions.append(f"#{field} = :{field}")

        if "product_name" in data:
            set_field("product_name", data["product_name"])
        if "price" in data:
            set_field("price", Decimal(str(data["price"])))
        if "brand_name" in data:
            set_field("brand_name", data["brand_name"])
        if "quantity_available" in data:
            set_field("quantity_available", int(data["quantity_available"]))

        if not update_expressions:
            return jsonify({"error": "No updatable fields provided"}), 400

        table.update_item(
            Key={"product_id": product_id},
            UpdateExpression="SET " + ", ".join(update_expressions),
            ExpressionAttributeNames=expr_attr_names,
            ExpressionAttributeValues=expr_attr_values,
            ReturnValues="ALL_NEW",
        )

        return jsonify({"message": "Product updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


