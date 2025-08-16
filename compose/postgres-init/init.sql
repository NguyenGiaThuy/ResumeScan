-- Create additional databases
/*
CREATE DATABASE IF NOT EXISTS appdb;
CREATE DATABASE IF NOT EXISTS langgraph_db;
*/

--
\connect postgres
SELECT 'CREATE DATABASE appdb'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'appdb')\gexec


SELECT 'CREATE DATABASE langgraph_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'langgraph_db')\gexec


\connect langgraph_db
CREATE TABLE IF NOT EXISTS qna_resume (
    ids UUID PRIMARY KEY,
    urls TEXT NOT NULL,
    qa JSONB,
    livecode JSONB
);

-- Grant permissions (optional)
GRANT ALL PRIVILEGES ON DATABASE appdb TO postgres;
GRANT ALL PRIVILEGES ON DATABASE langgraph_db TO postgres;

