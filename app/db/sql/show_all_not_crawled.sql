SELECT
    *
FROM
    @table
WHERE
    crawled = FALSE
ORDER BY
    created_at
