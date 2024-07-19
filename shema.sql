CREATE TABLE test (
	id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	kind varchar NOT NULL,
	name varchar NOT NULL,
	version varchar NOT NULL,
	description varchar,
	state varchar NOT NULL,
	json json NOT NULL
)