SELECT
    ROW_NUMBER() over (ORDER BY in_id) as 'N �/�',
    in_id as '����� ���������',
    date as '����',
    s_name as '���������'
FROM
    invoice LEFT JOIN supplier
ON
    s_id = supplier