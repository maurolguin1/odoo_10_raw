UPDATE res_users SET password = 'admin'
WHERE id = 1;

SELECT id, product_id FROM product_template;

select id from account_move_line where partner_id = 1445;

-- Jeff Queries
select invoice_id, name, price_unit, quantity from account_invoice_line where invoice_id in (select invoice_id from account_move_line);

-- My queries
select partner_id, count(invoice_id) invoice_total from account_invoice_line GROUP BY partner_id
ORDER BY invoice_total DESC;

-- invoice with more lines
SELECT name FROM res_partner WHERE id = 16748;
SELECT invoice_id, partner_id, sum(invoice_id) as invoice_sum FROM account_invoice_line
GROUP BY invoice_id, partner_id
ORDER BY invoice_sum DESC;

SELECT invoice_id, partner_id, name, product_id, price_unit, quantity, price_total FROM account_invoice_line WHERE invoice_id = 37;

SELECT * FROM res_partner WHERE customer IS TRUE and id = 1445;

-- _display_lines_sql_q1_receivable_and_payable(self, partners, date_start, date_end) # Q1
SELECT m.name AS move_id, l.partner_id, l.date, l.name,
                                l.ref, l.blocked, l.currency_id, l.company_id, ail.name AS product_name,
            CASE WHEN (l.currency_id is not null AND l.amount_currency > 0.0)
                THEN sum(l.amount_currency)
                ELSE sum(l.debit)
            END as debit,
            CASE WHEN (l.currency_id is not null AND l.amount_currency < 0.0)
                THEN sum(l.amount_currency * (-1))
                ELSE sum(l.credit)
            END as credit,
            CASE WHEN l.date_maturity is null
                THEN l.date
                ELSE l.date_maturity
            END as date_maturity
            FROM account_move_line l
            JOIN account_account_type at ON (at.id = l.user_type_id)
            JOIN account_move m ON (l.move_id = m.id)
            JOIN account_invoice_line ail ON ail.invoice_id = l.invoice_id
            JOIN res_partner rp ON rp.id = l.partner_id
            WHERE l.partner_id IN ('1445') AND (at.type = 'payable' OR at.type = 'receivable')
                                AND '2017-01-01' < l.date AND l.date <= '2017-10-17'
                                AND rp.customer IS TRUE
            GROUP BY l.partner_id, m.name, l.date, l.date_maturity, l.name,
                                l.ref, l.blocked, l.currency_id,
                                l.amount_currency, l.company_id, ail.name;

-- _display_lines_sql_q2_receivable_and_payable(self, company_id)
SELECT Q1.partner_id, move_id, date, date_maturity, Q1.name, ref,
                            debit, credit, debit-credit as amount, blocked, product_name,
            COALESCE(Q1.currency_id, c.currency_id) AS currency_id
            FROM (SELECT m.name AS move_id, l.partner_id, l.date, l.name,
                                l.ref, l.blocked, l.currency_id, l.company_id, ail.name AS product_name,
            CASE WHEN (l.currency_id is not null AND l.amount_currency > 0.0)
                THEN sum(l.amount_currency)
                ELSE sum(l.debit)
            END as debit,
            CASE WHEN (l.currency_id is not null AND l.amount_currency < 0.0)
                THEN sum(l.amount_currency * (-1))
                ELSE sum(l.credit)
            END as credit,
            CASE WHEN l.date_maturity is null
                THEN l.date
                ELSE l.date_maturity
            END as date_maturity
            FROM account_move_line l
            JOIN account_account_type at ON (at.id = l.user_type_id)
            JOIN account_move m ON (l.move_id = m.id)
            JOIN account_invoice_line ail ON ail.invoice_id = l.invoice_id
            WHERE l.partner_id IN ('1445') AND (at.type = 'payable' OR at.type = 'receivable')
                                AND '2017-01-01' < l.date AND l.date <= '2017-10-17'
            GROUP BY l.partner_id, m.name, l.date, l.date_maturity, l.name,
                                l.ref, l.blocked, l.currency_id,
                                l.amount_currency, l.company_id, ail.name) AS Q1
            JOIN res_company c ON (c.id = Q1.company_id)
            WHERE c.id = '3';


