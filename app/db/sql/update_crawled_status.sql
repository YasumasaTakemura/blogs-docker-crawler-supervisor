UPDATE @table
  SET crawled = TRUE
  ,SET crawled_at = @timestamp
  ,SET update_at = @timestamp
WHERE path = '@path'