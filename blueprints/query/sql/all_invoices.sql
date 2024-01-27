SELECT
    ROW_NUMBER() over (ORDER BY in_id) as 'N п/п',
    in_id as 'Номер накладной',
    date as 'Дата',
    s_name as 'Поставщик'
FROM
    invoice LEFT JOIN supplier
ON
    s_id = supplier