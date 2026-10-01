-- Runs once when the Postgres volume is first created.
CREATE EXTENSION IF NOT EXISTS vector;
CREATE DATABASE medspace_test;
\c medspace_test
CREATE EXTENSION IF NOT EXISTS vector;
