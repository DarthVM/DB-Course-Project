SELECT
    ROW_NUMBER() over (ORDER BY inl_id) as 'N �/�',
    p_name as '�����',
    amount as '����������',
    m_unit as '��. ���.',
    price as '���� (� ������)'
FROM
    invoice_list
    JOIN invoice
ON
    inl_id=in_id
LEFT JOIN product_info
ON
    p_id=invoice_list.product
WHERE inl_id='$invoice'