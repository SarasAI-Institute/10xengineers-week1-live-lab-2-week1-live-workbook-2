import uuid
from datetime import datetime

def gen_id():
    return str(uuid.uuid4())[:8]

def now():
    return datetime.now()

# calculate total inventory value
def calc_inventory_value(products_dict, stock_dict):
    # TODO: implement this function
    # should return sum of (price * quantity) for all products
    return None

# check if product is low stock
def is_low_stock(product_id, stock_dict, threshold=10):
    qty = stock_dict.get(product_id, 0)
    # BUG: should be <= not <
    if qty < threshold:
        return True
    return False

# get products that need reorder
def get_reorder_list(products_dict, stock_dict, threshold=10):
    # TODO: needs implementation
    raise NotImplementedError()

# format price
def fmt_price(price):
    return f"${price:.2f}"

# calculate margin
def calc_margin(cost, price):
    # BUG: formula is wrong, this calculates wrong percentage
    return (price - cost) / price * 100

# validate sku format (should be XX-XXXX-XXX)
def validate_sku(sku):
    parts = sku.split("-")
    if len(parts) != 3:
        return False
    return True

# search products
def search_products(products_list, query):
    results = []
    q = query.lower()
    for p in products_list:
        if q in p.name.lower() or q in p.sku.lower():
            results.append(p)
    return results

# generate report
def generate_stock_report(products_dict, stock_dict, categories_dict, include_zero=False, sort_by="name", group_by_category=False, show_value=True, currency="$"):
    report = []
    report.append("STOCK REPORT")
    report.append("=" * 40)
    prods = list(products_dict.values())
    if sort_by == "name":
        prods = sorted(prods, key=lambda x: x.name)
    elif sort_by == "stock":
        prods = sorted(prods, key=lambda x: stock_dict.get(x.id, 0))
    elif sort_by == "price":
        prods = sorted(prods, key=lambda x: x.price)
    if group_by_category:
        by_cat = {}
        for p in prods:
            cat_id = p.category_id or "uncategorized"
            if cat_id not in by_cat:
                by_cat[cat_id] = []
            by_cat[cat_id].append(p)
        for cat_id, cat_prods in by_cat.items():
            if cat_id in categories_dict:
                cat_name = categories_dict[cat_id].name
            else:
                cat_name = "Uncategorized"
            report.append("")
            report.append(f"Category: {cat_name}")
            report.append("-" * 30)
            for p in cat_prods:
                qty = stock_dict.get(p.id, 0)
                if qty == 0 and not include_zero:
                    continue
                line = f"  {p.name} ({p.sku}): {qty} units"
                if show_value:
                    val = qty * p.price
                    line = line + f" = {currency}{val:.2f}"
                report.append(line)
    else:
        for p in prods:
            qty = stock_dict.get(p.id, 0)
            if qty == 0 and not include_zero:
                continue
            line = f"{p.name} ({p.sku}): {qty} units"
            if show_value:
                val = qty * p.price
                line = line + f" = {currency}{val:.2f}"
            report.append(line)
    report.append("")
    report.append("=" * 40)
    return "\n".join(report)

