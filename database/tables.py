from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    Text,
    String,
    ForeignKey,
    LargeBinary
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector  # Import the Vector type from pgvector
Base = declarative_base()

class Model(Base):
    __tablename__ = 'model'
    
    model_id = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(Text, nullable=True)
    library = Column(Text, nullable=True)
    graph = Column(JSONB, nullable=True)
    average_weight_embedding = Column(Vector(256), nullable=True)
    
    # One-to-many: one model has many layers.
    layers = relationship("Layer", back_populates="model", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Model(model_id={self.model_id}, model_name={self.model_name}, library={self.library})>"


class Layer(Base):
    __tablename__ = 'layer'
    
    layer_id = Column(Integer, primary_key=True, autoincrement=True)
    layer_name = Column(Text, nullable=True)
    model_id = Column(Integer, ForeignKey("model.model_id"), nullable=False)
    known_type = Column(String, nullable=True)
    attributes = Column(JSONB, nullable=True)
    
    # Relationships: each layer belongs to a model and can have many parameters.
    model = relationship("Model", back_populates="layers")
    parameters = relationship("Parameter", back_populates="layer", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Layer(layer_id={self.layer_id}, layer_name={self.layer_name}, model_id={self.model_id})>"


class Parameter(Base):
    __tablename__ = 'parameter'
    
    parameter_id = Column(BigInteger, primary_key=True, autoincrement=True)
    parameter_name = Column(String, nullable=True)
    layer_id = Column(Integer, ForeignKey("layer.layer_id"), nullable=False)
    shape = Column(Text, nullable=True) 
    weight_embedding = Column(Vector(256), nullable=True)

    # Relationships: each parameter belongs to a layer and can have interpolated parameters.
    layer = relationship("Layer", back_populates="parameters")
    #interpolated_parameters = relationship(
    #    "InterpolatedParametersVector",
    #    back_populates="parameter",
    #    cascade="all, delete-orphan"
    #)
    
    def __repr__(self):
        return f"<Parameter(parameter_id={self.parameter_id}, parameter_name={self.parameter_name})>"

class Paper(Base):
    __tablename__ = 'paper'

    paper_id = Column(BigInteger, primary_key=True, autoincrement=True)
    paper_name = Column(String, nullable=True)
    contents = Column(LargeBinary, nullable=True)

    def __repr__(self):
        return f"<Paper(paper_id={paper_id}, paper_name={paper_name})>"


class Paper_Model(Base):
    __tablename__ = "paper_model"
    paper_model_id = Column(BigInteger, primary_key=True, autoincrement=True)
    paper_id = Column(Integer)
    model_id = Column(Integer)

    def __repr__(self):
        return f"<Paper_Model(paper_model_id={paper_model_id}, paper_id={paper_id}, model_id={model_id} )>"

#class InterpolatedParametersVector(Base):
#    __tablename__ = 'interpolated_parameters_vector'
#    
#    interpolated_parameter_id = Column(BigInteger, primary_key=True, autoincrement=True)
#    # Use the pgvector Vector type with 256 dimensions
#    weight_embedding = Column(Vector(256), nullable=True)
#    parameter_id = Column(BigInteger, ForeignKey("parameter.parameter_id"), nullable=False)
    
    # Relationship: each interpolated parameter vector is linked to one parameter.
#    parameter = relationship("Parameter", back_populates="interpolated_parameters")
    
#    def __repr__(self):
#        return f"<InterpolatedParametersVector(interpolated_parameter_id={self.interpolated_parameter_id})>"

