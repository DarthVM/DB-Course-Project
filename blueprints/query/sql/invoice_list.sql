SELECT
    ROW_NUMBER() over (ORDER BY inl_id) as 'N п/п',
    p_name as 'Товар',
    amount as 'Количество',
    m_unit as 'Ед. Изм.',
    price as 'Цена (в рублях)'
FROM
    invoice_list
    JOIN invoice
ON
    inl_id=in_id
LEFT JOIN product_info
ON
    p_id=invoice_list.product
WHERE inl_id='$invoice'