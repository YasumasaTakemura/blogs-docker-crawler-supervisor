INSERT INTO @table (
    path
    ,crawled
    ,stored
    ,crawled_at
    ,created_at
    ,updated_at
)
SELECT
    tmp.path
    ,tmp.crawled
    ,tmp.stored
    ,NULL
    ,'@timestamp'
    ,'@timestamp'
FROM
    (
      VALUES
        @values
    ) tmp (
      path
      ,crawled
      ,stored
    )
LEFT JOIN
    @table
    ON tmp.path = @table.path
WHERE
    @table.path IS NULL;