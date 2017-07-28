update res_users set password = 'admin' WHERE id = 1;

SELECT id, name, price_subtotal  FROM purchase_order_line;

SELECT id, name  FROM sale_order;

SELECT id, name,  product_id FROM purchase_order;

SELECT * FROM grid_order_form_wizard;

SELECT  p.price, pt.standard_price, pt.list_price
FROM product_product p, product_template pt;

SELECT pp.id, rp.name, pp.price, pp.min_quantity  from pricelist_partnerinfo pp LEFT JOIN res_partner rp ON pp.suppinfo_id = rp.id WHERE pric;

SELECT * FROM res_partner;

SELECT ps.id as "ps_id", pp.id as "pp_id", pp.suppinfo_id as "pp_suppinfo_id", pp.price as "pp_price" FROM product_supplierinfo ps LEFT JOIN pricelist_partnerinfo pp ON ps.id = pp.suppinfo_id;


SELECT * FROM product_supplierinfo;

SELECT pp.id as "pp_id", ps.product_id as "ps_product_id", pp.name as "pp_name"
FROM product_product pp
  LEFT JOIN product_template pt
  ON pp.id = pt.id
LEFT JOIN product_supplierinfo ps
  ON pp.id = ps.product_id;

SELECT pt.id as "pt_id", pt.name as "pt_name", ps.product_id as "ps_product_id", pp.name as "pp_name", ps.id as "ps_id", pl.suppinfo_id as "pl_suppinfo_id", pt.standard_price as "pt_std_price",  pl.price as "pl_price"
FROM product_template pt
  LEFT JOIN product_supplierinfo ps ON pt.id = ps.product_id
  LEFT JOIN pricelist_partnerinfo pl ON ps.id = pl.suppinfo_id
  LEFT JOIN product_product pp ON pt.id = pp.product_tmpl_id
                                  WHERE pt.id= 120;
