# Tasks

## Bugs to Fix

- [ ] `is_low_stock()` in utils.py uses `<` instead of `<=` for threshold comparison
- [ ] `calc_margin()` in utils.py has wrong formula (divides by price instead of cost)
- [ ] `delete_product()` in api.py doesn't clean up the stock dictionary when deleting a product

## TODOs

- [ ] Implement `get_product()` function in api.py (currently just passes)
- [ ] Implement `stock_history()` endpoint in api.py (currently raises NotImplementedError)
- [ ] Implement `get_report()` endpoint in api.py to use `generate_stock_report` from utils
- [ ] Implement `calc_inventory_value()` function in utils.py (should return sum of price * quantity)
- [ ] Implement `get_reorder_list()` function in utils.py (currently raises NotImplementedError)
