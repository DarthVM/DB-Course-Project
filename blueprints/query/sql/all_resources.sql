SELECT
    ROW_NUMBER() over (ORDER BY r_id) as 'N �/�',
    p_name as '��������',
    amount as '����������',
    m_unit as '��. ���.',
    price as '����',
    update_date as '���� ���������� ���������'
FROM
    resources
        LEFT JOIN product_info
ON
    product_info.p_id = resources.product


