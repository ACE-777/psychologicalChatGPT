CREATE DATABASE chat;

CREATE TABLE chat.users_info
(
    user_id Nullable(Int32),
    tags Nullable(String)
) ENGINE = Memory;
-- ENGINE = MergeTre on disk

CREATE TABLE chat.job (
  request Nullable(String),
  response Nullable(String)
) ENGINE = Memory;

CREATE TABLE chat.useful_links
(
    fields Nullable(VARCHAR),
    job_services Nullable(VARCHAR),
    forums Nullable(VARCHAR),
    useful_links_about_making_CV Nullable(VARCHAR)
) ENGINE = Memory;

CREATE TABLE chat.users_points
(
    user_id Nullable(Int),
    users_points Nullable(Int)
) ENGINE = Memory;

INSERT INTO chat.useful_links (fields, job_services, forums, useful_links_about_making_CV) VALUES (null, 'https://hh.ru/', null, null);

INSERT INTO chat.useful_links (fields, job_services, forums, useful_links_about_making_CV) VALUES (null, 'https://www.behance.net/joblist', null, null);

INSERT INTO chat.useful_links (fields, job_services, forums, useful_links_about_making_CV) VALUES (null, 'https://dribbble.com/jobs', null, null);

INSERT INTO chat.useful_links (fields, job_services, forums, useful_links_about_making_CV) VALUES (null, 'https://designjobs.aiga.org/', null, null);

INSERT INTO chat.useful_links (fields, job_services, forums, useful_links_about_making_CV) VALUES (null, 'https://www.simplyhired.com/', null, null);

INSERT INTO chat.useful_links (fields, job_services, forums, useful_links_about_making_CV) VALUES (null, 'https://www.linkedin.com/jobs/', null, null);

INSERT INTO chat.useful_links (fields, job_services, forums, useful_links_about_making_CV) VALUES (null, 'https://www.indeed.com/', null, null);

INSERT INTO chat.useful_links (fields, job_services, forums, useful_links_about_making_CV) VALUES (null, 'https://www.glassdoor.com/index.htm', null, null);

INSERT INTO chat.useful_links (fields, job_services, forums, useful_links_about_making_CV) VALUES ('C++', 'https://hh.ru/', null, null);
