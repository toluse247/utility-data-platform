COPY regions FROM '/docker-entrypoint-initdb.d/regions.csv' DELIMITER ',' CSV HEADER;
COPY districts FROM '/docker-entrypoint-initdb.d/districts.csv' DELIMITER ',' CSV HEADER;
COPY service_units FROM '/docker-entrypoint-initdb.d/service_units.csv' DELIMITER ',' CSV HEADER;
COPY feeders FROM '/docker-entrypoint-initdb.d/feeders.csv' DELIMITER ',' CSV HEADER;
COPY transformers FROM '/docker-entrypoint-initdb.d/transformers.csv' DELIMITER ',' CSV HEADER;
COPY sales_reps FROM '/docker-entrypoint-initdb.d/sales_reps.csv' DELIMITER ',' CSV HEADER;
COPY band_tariff FROM '/docker-entrypoint-initdb.d/band_tariff.csv' DELIMITER ',' CSV HEADER;
