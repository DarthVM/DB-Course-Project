SELECT
    ROW_NUMBER() over (ORDER BY p_id) as 'N �/�',
    p_id as '���������� �����',
    p_name as '��������',
    m_unit as '������� ���������',
    product_info.`group` as '������ �������'
FROM
    product_info

