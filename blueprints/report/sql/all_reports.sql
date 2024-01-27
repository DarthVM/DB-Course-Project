SELECT
    rep_id,
    rep_type,
    MONTHNAME(start_date) as month,
    YEAR(start_date) as year
FROM
    report