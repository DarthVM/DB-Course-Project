SELECT
    ROW_NUMBER() over (ORDER BY rc_id) as 'N ο/ο',
    DAY(work_date) as 'Δενό',
    rc_sum as 'Ρσμμΰ'
FROM
    report_costs
WHERE report='$report'

