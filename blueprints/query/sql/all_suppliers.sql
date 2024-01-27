SELECT
    ROW_NUMBER() over (ORDER BY s_id) as 'N п/п',
    s_id as 'Уникальный номер',
    s_name as 'Название',
    phone_number as 'Номер телефона',
    city as 'Город',
    bank_name as 'Банк',
    bank_acc as 'Расчетный счёт',
    contract_date as 'Дата заключения контракта',
    term_time as 'Срок действия'
FROM
    supplier