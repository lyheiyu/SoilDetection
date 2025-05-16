--! Previous: -
--! Hash: sha1:8f3adf5418f6a8a1c4065f1972d9ef18bb98a2ca

-- Enter migration here

-- DROP SCHEMA IF EXISTS core;
DROP SCHEMA IF EXISTS core CASCADE;
DROP TABLE IF EXISTS core.project CASCADE;
DROP TABLE IF EXISTS core.project_related CASCADE;
DROP TABLE IF EXISTS core.site CASCADE;
DROP TABLE IF EXISTS core.site_project CASCADE;
DROP SCHEMA IF EXISTS core;
CREATE SCHEMA core;
COMMENT ON SCHEMA core IS 'Core entities and relations from the ISO-28258 domain model';
