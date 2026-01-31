from fastapi import FastAPI, HTTPException
from typing import List, Optional
from app.models import Product, ProductCreate, Category, CategoryCreate, StockMovement, StockAdjust
from app.storage import products, categories, stock, movements
from app.utils import gen_id, now, is_low_stock

app = FastAPI()

# products

@app.get("/products")
def list_products(category_id: Optional[str] = None, low_stock: bool = False):
    prods = list(products.values())
    if category_id:
        prods = [p for p in prods if p.category_id == category_id]
    if low_stock:
        prods = [p for p in prods if is_low_stock(p.id, stock)]
    return prods

@app.get("/products/{product_id}")
def get_product(product_id: str):
    # TODO: implement
    pass

@app.post("/products")
def create_product(data: ProductCreate):
    p = Product(
        id=gen_id(),
        name=data.name,
        sku=data.sku,
        price=data.price,
        category_id=data.category_id,
        created_at=now()
    )
    products[p.id] = p
    stock[p.id] = 0
    return p

@app.delete("/products/{product_id}")
def delete_product(product_id: str):
    if product_id not in products:
        raise HTTPException(404)
    del products[product_id]
    # BUG: doesn't delete from stock dict
    return {"deleted": True}

# categories

@app.get("/categories")
def list_categories():
    return list(categories.values())

@app.post("/categories")
def create_category(data: CategoryCreate):
    c = Category(id=gen_id(), name=data.name, description=data.description)
    categories[c.id] = c
    return c

# stock

@app.get("/stock/{product_id}")
def get_stock(product_id: str):
    if product_id not in products:
        raise HTTPException(404)
    return {"product_id": product_id, "quantity": stock.get(product_id, 0)}

@app.post("/stock/{product_id}/adjust")
def adjust_stock(product_id: str, data: StockAdjust):
    if product_id not in products:
        raise HTTPException(404)
    current = stock.get(product_id, 0)
    new_qty = current + data.quantity
    if new_qty < 0:
        raise HTTPException(400, "cannot have negative stock")
    stock[product_id] = new_qty
    mv = StockMovement(
        id=gen_id(),
        product_id=product_id,
        quantity=data.quantity,
        reason=data.reason,
        timestamp=now()
    )
    movements[mv.id] = mv
    return {"product_id": product_id, "previous": current, "new": new_qty}

@app.get("/stock/{product_id}/history")
def stock_history(product_id: str):
    # TODO: implement - should return all movements for this product
    raise NotImplementedError()

@app.get("/report")
def get_report():
    # TODO: use generate_stock_report from utils
    return None

