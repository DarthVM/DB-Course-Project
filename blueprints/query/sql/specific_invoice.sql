SELECT
    in_id as '����� ���������',
    date as '����',
    s_name as '���������'
FROM
    invoice LEFT JOIN supplier
ON
    s_id = supplier
where
    in_id = '$invoice'