CREATE DATABASE chat;

CREATE TABLE chat.job (
  request Nullable(String),
  response Nullable(String)
) ENGINE = Memory;
-- ENGINE = MergeTre on disk