# 🛒 Flask Products (DynamoDB + S3) — Matt Edition

Clean, minimal store UI + REST API. Flask app stores products in DynamoDB and (optionally) uploads images to S3. Deployed behind NGINX via Terraform.

## 📁 Project Structure
```
flask-app-for-terraform-workshop/
  app.py                 # Registers blueprints
  services.py            # AWS clients (DynamoDB/S3) & env config
  routes/
    create.py            # POST /products
    get.py               # GET /, /form, /products
    update.py            # PUT/PATCH /products/<product_id>
    delete.py            # DELETE /products/<product_id>
  templates/
    index.html           # Minimal UI (Inter font, fetch API)
  static/
    styles.css           # 7‑Eleven inspired theme
  requirements.txt
```

* Used Flask Blueprints for modular routing (create/get/update/delete).

## 🔧 Environment
- `AWS_REGION` (e.g. `sa-east-1`)
- `DYNAMODB_TABLE_NAME` (e.g. `matt-products-table`)
- `S3_BUCKET_NAME` (e.g. `matt-product-images`, optional for images)

Ensure your AWS creds can access DynamoDB (and S3 if using images).

## 🚀 Run Locally
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

export AWS_REGION=sa-east-1
export DYNAMODB_TABLE_NAME=matt-products-table
export S3_BUCKET_NAME=matt-product-images   # optional

python app.py
```

Open UI: `http://localhost:5000/`  (form + product list)

## 🌐 Endpoints
- GET `/` and `/form` — UI
- GET `/products` — list
- POST `/products` — create (JSON or multipart)
- PUT/PATCH `/products/<product_id>` — update
- DELETE `/products/<product_id>` — delete

### Create (JSON)
```bash
curl -X POST http://localhost:5000/products \
  -H 'Content-Type: application/json' \
  -d '{
    "product_name":"Wireless Headphones",
    "price":99.99,
    "brand_name":"AudioTech",
    "quantity_available":50
  }'
```

### Create (multipart with image)
```bash
curl -X POST http://localhost:5000/products \
  -F 'product_name=Camera' \
  -F 'price=299.99' \
  -F 'brand_name=PhotoCo' \
  -F 'quantity_available=5' \
  -F 'image=@/path/to/image.jpg'
```

### Update
```bash
curl -X PATCH http://localhost:5000/products/<product_id> \
  -H 'Content-Type: application/json' \
  -d '{"price": 79.99, "quantity_available": 8}'
```

### Delete
```bash
curl -X DELETE http://localhost:5000/products/<product_id>
```

## ☁️ Deploy with Terraform (NGINX proxy) 
This app is deployed by the `terraform-practice` [https://github.com/mattenarle10/terraform-practice.git] repo (user_data installs Python, clones this repo from `locals.flask_github_repo`, starts Flask, and sets NGINX to proxy `/:80 -> 127.0.0.1:5000`).

Quick redeploy of instance:
```bash
cd ../terraform-practice
terraform taint aws_instance.web
terraform apply
```

Open public IP from Terraform output:
```bash
open "http://$(terraform output -raw ubuntu_instance_public_ip)/"
```

## 📝 Notes
- S3 bucket names must be globally unique and lowercase.
- If you see the NGINX default page, wait 60–90s or restart NGINX/Flask.
- UI uses a minimal theme; adjust `static/styles.css` as you like. ✅

### References
- Flask Blueprints: https://flask.palletsprojects.com/en/latest/blueprints/
- Terraform config linkage: see `terraform-practice/locals.tf` and `main.tf` (user_data)