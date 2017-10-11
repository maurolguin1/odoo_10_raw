UPDATE res_users SET password = 'admin'
WHERE id = 1;

SELECT id, product_id FROM product_template;

SELECT m.name AS move_id, l.partner_id, l.date, l.name,
                                l.ref, l.product_id, pt.name, l.blocked,  l.currency_id, l.company_id,
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
JOIN account_account_type at ON at.id = l.user_type_id
JOIN account_move m ON l.move_id = m.id
JOIN product_product p ON l.product_id = p.id
  JOIN product_template pt ON pt.id = p.product_tmpl_id
-- WHERE l.partner_id = 1445 AND at.type = 'receivable'
-- AND '2017-01-01' < l.date AND l.date <= '2017-10-10'
            GROUP BY l.partner_id, l.product_id, m.name, l.date, l.date_maturity, l.name,
                                l.ref, l.blocked, l.currency_id,
                                l.amount_currency, l.company_id, pt.name;


select id from account_move_line where partner_id = 1445;

select name, price_unit, quantity from account_invoice_line where invoice_id in (select invoice_id from account_move_line where id = 1273);


--_initial_balance_sql_q2_receivable_and_payable @params company_id
SELECT Q1.partner_id, debit-credit AS balance,
            COALESCE(Q1.currency_id, c.currency_id) AS currency_id
            FROM Q1
            JOIN res_company c ON (c.id = Q1.company_id)
            WHERE c.id = %s



-- _display_lines_sql_q1 @params partners, date_start, date_end
SELECT m.name AS move_id, l.partner_id, l.date, l.name,
                                l.ref, l.blocked, l.currency_id, l.company_id,
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
            WHERE l.partner_id IN (%s) AND at.type = 'receivable'
                                AND '%s' < l.date AND l.date <= '%s'
            GROUP BY l.partner_id, m.name, l.date, l.date_maturity, l.name,
                                l.ref, l.blocked, l.currency_id,
                                l.amount_currency, l.company_id

-- _display_lines_sql_q1_receivable_and_payable @params partners, date_start, date_end
SELECT m.name AS move_id, l.partner_id, l.date, l.name,
                                l.ref, l.blocked, l.currency_id, l.company_id,
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
            WHERE l.partner_id IN (%s) AND (at.type = 'payable' OR at.type = 'receivable')
                                AND '%s' < l.date AND l.date <= '%s'
            GROUP BY l.partner_id, m.name, l.date, l.date_maturity, l.name,
                                l.ref, l.blocked, l.currency_id,
                                l.amount_currency, l.company_id;

-- _display_lines_sql_q2




--_display_lines_sql_q2_receivable_and_payable @param company_id
SELECT Q1.partner_id, move_id, date, date_maturity, Q1.name, ref,
                            debit, credit, debit-credit as amount, blocked,
            COALESCE(Q1.currency_id, c.currency_id) AS currency_id
            FROM Q1
            JOIN res_company c ON (c.id = Q1.company_id)
            WHERE c.id = %s

--_get_account_display_lines_receivable_and_payable @params: company_id, partner_ids, date_start,date_end
