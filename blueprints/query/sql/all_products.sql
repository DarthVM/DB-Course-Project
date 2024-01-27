SELECT
    ROW_NUMBER() over (ORDER BY p_id) as 'N п/п',
    p_id as 'Уникальный номер',
    p_name as 'Название',
    m_unit as 'Единица измерения',
    product_info.`group` as 'Группа товаров'
FROM
    product_info

