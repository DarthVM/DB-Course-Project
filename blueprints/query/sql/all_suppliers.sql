SELECT
    ROW_NUMBER() over (ORDER BY s_id) as 'N �/�',
    s_id as '���������� �����',
    s_name as '��������',
    phone_number as '����� ��������',
    city as '�����',
    bank_name as '����',
    bank_acc as '��������� ����',
    contract_date as '���� ���������� ���������',
    term_time as '���� ��������'
FROM
    supplier