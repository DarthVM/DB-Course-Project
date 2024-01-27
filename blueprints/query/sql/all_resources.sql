SELECT
    ROW_NUMBER() over (ORDER BY r_id) as 'N п/п',
    p_name as 'Название',
    amount as 'Количество',
    m_unit as 'Ед. изм.',
    price as 'Цена',
    update_date as 'Дата последнего изменения'
FROM
    resources
        LEFT JOIN product_info
ON
    product_info.p_id = resources.product


