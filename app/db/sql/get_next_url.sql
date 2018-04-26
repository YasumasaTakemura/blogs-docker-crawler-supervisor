SELECT
    path
FROM
    @table
WHERE
    crawled = FALSE
ORDER BY
    created_at
LIMIT 1
