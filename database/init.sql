CREATE TABLE Comparison(
    comparison_id SERIAL PRIMARY KEY,
    date TIMESTAMP
);

CREATE TABLE Comparison_Mapping_Table (
    comparison_id INT,
    result_id INT
);

Create TABLE Optimization_Method(
    optimization_id SERIAL PRIMARY KEY,
    name TEXT
);

create table Library (
    library_id SERIAL PRIMARY KEY,
    name Text,
    version Text
);


Create TABLE Dataset(
    dataset_id SERIAL PRIMARY KEY,
    name TEXT,
    location TEXT
);


CREATE TABLE Model_Configuration (
  configuration_id SERIAL PRIMARY KEY,
  optimization_id INT,
  datatype_id INT,
  epoch INT,
  training_rate FLOAT,
  CONSTRAINT fk_optimization
      FOREIGN KEY(optimization_id) 
	    REFERENCES Optimization_Method(optimization_id)
);

Create TABLE LayerType (
  layer_type_id SERIAL PRIMARY KEY,
  layer_type TEXT
);

CREATE TABLE Parameter ( 
  parameter_id SERIAL PRIMARY KEY,
  parameter_name TEXT,
  parameter_type TEXT,
  layer_id INT,
  np_array_bytes BYTEA,
  CONSTRAINT fk_layer 
     FOREIGN KEY(layer_id) 
	REFERENCES LayerType(layer_type_id) 

);



CREATE TABLE Model (
    model_id SERIAL PRIMARY KEY,
    library_id INT,
    configuration_id INT,
    name TEXT,
    model_file bytea,
    model_type TEXT,
    CONSTRAINT fk_library
      FOREIGN KEY(library_id) 
	    REFERENCES library(library_id),
    CONSTRAINT fk_configuration
      FOREIGN KEY(configuration_id) 
	    REFERENCES Model_Configuration(configuration_id)

);


Create TABLE Layer (
  layer_id SERIAL PRIMARY KEY,
  layer_name TEXT,
  layer_type INT,
  layer_index INT,
  model_id INT,
  parameters INT[],
  CONSTRAINT fk_model
     FOREIGN KEY(model_id) 
	REFERENCES Model (model_id),
  CONSTRAINT fk_layer 
     FOREIGN KEY(layer_type) 
	REFERENCES LayerType(layer_type_id) 
);


CREATE TABLE Layer_Parameter (
  layer_id INT references Layer,
  parameter_id INT references Parameter,
  primary key (layer_id,parameter_id)
);




CREATE TABLE Result (
    result_id SERIAL PRIMARY KEY,
    model_id INT,
    dataset_id INT,
    startdate TIMESTAMP,
    enddate TIMESTAMP,
    ResultType INT,
    TP INT[],
    FP INT[],
    TN INT[],
    FN INT[],
    train_acc FLOAT[],
    train_loss FLOAT[],
    valid_acc FLOAT[],
    valid_loss FLOAT[],
    test_acc FLOAT[],
    test_loss FLOAT[],
    CONSTRAINT fk_model
      FOREIGN KEY(model_id) 
	    REFERENCES Model(model_id),
    CONSTRAINT fk_dataset
      FOREIGN KEY(dataset_id) 
	    REFERENCES Dataset(dataset_id)
);

CREATE TABLE MetricType (
	metric_type_id SERIAL PRIMARY KEY,
	Name TEXT
);

CREATE TABLE Metric_Result(
  metric_result_id SERIAL PRIMARY KEY,
  metric_type_id INT,
  result FLOAT,
  CONSTRAINT fk_metric_type
      FOREIGN KEY(metric_type_id) 
	    REFERENCES MetricType(metric_type_id)
);

CREATE TABLE ResultType (
    resulttype_id SERIAL PRIMARY KEY,
    NAME TEXT
);

Create Table DataType (
    datatype_id SERIAL PRIMARY KEY,
    Name TEXT
);

Insert into Library (Name, Version) Values('AutoKeras','1.0.x');
Insert into Optimization_Method(Name) Values('None');
Insert into Optimization_Method(Name) Values('SGD');
Insert into Optimization_Method(Name) Values('RMSprop');
Insert into Optimization_Method(Name) Values('Adam');
Insert into Optimization_Method(Name) Values('Adadelta');
Insert into Optimization_Method(Name) Values('Adagrad');
Insert into Optimization_Method(Name) Values('Adamax');
Insert into Optimization_Method(Name) Values('Nadam');
Insert into Optimization_Method(Name) Values('Ftrl');
Insert into ResultType(Name) Values ('Classification');
Insert into ResultType(Name) Values ('Regression');
Insert into DataType(Name) Values('Image');
Insert into DataType(Name) Values('Text');
Insert into DataType(Name) Values('Structured Data');
