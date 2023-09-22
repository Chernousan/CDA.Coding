-- URL has size 2083 (according https://support.microsoft.com/en-au/topic/maximum-url-length-is-2-083-characters-in-internet-explorer-174e7c8a-6666-f4e0-6fd6-908b53c12246)
-- Title has size 500 (according good sense)
CREATE TABLE IF NOT EXISTS estate (
    title VARCHAR(500),
    url VARCHAR(2083)
);