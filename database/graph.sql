CREATE EXTENSION vector;

create TABLE dataset (dataset_id bigserial primary key,
datsaet_name text,
source text
);

CREATE TABLE paper (
  paper_id bigserial PRIMARY KEY,
  paper_name Text,
  contents bytea -- may be better a filepath
);

CREATE TABLE model (
  model_id bigserial PRIMARY KEY,
  model_name Text,
  library Text,
  average_weight_embedding vector(256),
  graph jsonb
);

CREATE TABLE paper_model (
   paper_model_id serial,
   paper_id serial,
   model_id serial
);

CREATE TABLE layer (
  layer_id SERIAL PRIMARY KEY,
  layer_name Text,
  known_type Text,
  model_id SERIAL,
  attributes jsonb, 
  CONSTRAINT fk_model_id
      FOREIGN KEY(model_id)
            REFERENCES model(model_id)


);

CREATE TABLE parameter ( parameter_id bigserial PRIMARY KEY, 
	parameter_name Text,
  layer_id SERIAL,
	shape text,
	weight_embedding vector(256),
        CONSTRAINT fk_layer_id
           FOREIGN KEY(layer_id)
		REFERENCES layer(layer_id)
);

CREATE TABLE neural_network_output (
  output_id bigserial primary key,
  dataset_id serial,
  average_output vector(2048),
  average_steelette_output vector(3),
  CONSTRAINT fk_dataset_id 
  FOREIGN KEY(dataset_id) 
  REFERENCES dataset(dataset_id)
);



--CREATE TABLE interpolated_parameters_vector( interpolated_parameter_id bigserial primary key,
--	weight_embedding vector(256),
--	parameter_id serial,
--	CONSTRAINT fk_parameter_id	
--		FOREIGN KEY(parameter_id)
--			REFERENCES parameter(parameter_id)
--);




commit;
