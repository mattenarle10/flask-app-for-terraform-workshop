from flask import Blueprint, request, jsonify
from decimal import Decimal
import uuid
from datetime import datetime
import os
from services import table, s3, bucket_name, region

bp = Blueprint("create", __name__)


@bp.route("/products", methods=["POST"])
def create_product():
    try:
        if request.is_json:
            data = request.get_json()
            image = None
        else:
            data = request.form.to_dict()
            image = request.files.get("image")

        required_fields = [
            "product_name",
            "price",
            "brand_name",
            "quantity_available",
        ]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        product_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()

        image_url = None
        if image and image.filename and s3 and bucket_name:
            extension = os.path.splitext(image.filename)[1]
            s3_key = f"products/{product_id}{extension}"
            s3.upload_fileobj(
                image,
                bucket_name,
                s3_key,
                ExtraArgs={"ContentType": image.content_type},
            )
            image_url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{s3_key}"

        item = {
            "product_id": product_id,
            "product_name": data["product_name"],
            "price": Decimal(str(data["price"])),
            "brand_name": data["brand_name"],
            "quantity_available": int(data["quantity_available"]),
            "created_at": timestamp,
        }

        if image_url:
            item["image_url"] = image_url
            item["image_key"] = s3_key  # type: ignore[name-defined]

        table.put_item(Item=item)
        return (
            jsonify(
                {
                    "message": "Product created successfully",
                    "product_id": product_id,
                    "image_url": image_url,
                }
            ),
            201,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


