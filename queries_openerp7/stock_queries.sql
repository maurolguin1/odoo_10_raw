-- Stock picking selection general selection
SELECT * FROM stock_picking;

--Stock picking specified
SELECT id, origin, partner_id, backorder_id, name, note, sale_id, inv, partner_parent  FROM stock_picking LIMIT 100;

-- Stock partial picking general selection
SELECT * FROM stock_partial_picking;

-- Stock partial picking specific selection
SELECT id, picking_id,  FROM stock_partial_picking;

SELECT * FROM shipping_shippingregister;

-- Stock move here there are qty_expected
SELECT * FROM stock_move;
SELECT id, origin, name, product_uos_qty, product_uom, product_qty,  qty_expected,  product_uos, partner_id,  product_id, picking_id, state, sale_line_id, purchase_line_id FROM stock_move;

SELECT * FROM product_uom;

-- Here in moment of purchase
SELECT * FROM purchase_order_line;

SELECT id, product_uom,  product_qty, product_id, order_id, name, state, sale_order_line_id
FROM purchase_order_line WHERE product_id = 95833;