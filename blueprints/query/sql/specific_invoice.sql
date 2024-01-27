SELECT
    in_id as 'Номер накладной',
    date as 'Дата',
    s_name as 'Поставщик'
FROM
    invoice LEFT JOIN supplier
ON
    s_id = supplier
where
    in_id = '$invoice'