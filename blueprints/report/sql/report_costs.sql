SELECT
    ROW_NUMBER() over (ORDER BY rc_id) as 'N �/�',
    DAY(work_date) as '����',
    rc_sum as '�����'
FROM
    report_costs
WHERE report='$report'

