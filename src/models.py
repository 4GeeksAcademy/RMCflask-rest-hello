import os
import sys
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er
from datetime import datetime, timezone

Base = declarative_base()
db = SQLAlchemy()

class Usuario(Base):
    __tablename__ = 'usuario'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(40), nullable=False, unique=True)
    password = Column(String(40), nullable=False)
    full_name = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    created = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    favoritos = relationship('Favorito', backref='usuario', lazy='select')

class Planeta(Base):
    __tablename__ = 'planeta'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    diameter = Column(String(100), nullable=False)
    rotation_period = Column(String(100), nullable=False)
    orbital_period = Column(String(100), nullable=False)
    gravity = Column(String(100), nullable=False)
    population = Column(String(100), nullable=False)
    climate = Column(String(100), nullable=False)
    terrain = Column(String(100), nullable=False)
    surface_water = Column(String(100), nullable=False)
    created = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    edited = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    favoritos = relationship('Favorito', backref='planeta', lazy='select')

class Vehiculo(Base):
    __tablename__ = 'vehiculo'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    vehicle_class = Column(String(100), nullable=False)
    manufacturer = Column(String(100), nullable=False)
    length = Column(String(100), nullable=False)
    cost_in_credits = Column(String(100), nullable=False)
    crew = Column(String(100), nullable=False)
    max_atmosphering_speed = Column(String(100), nullable=False)
    cargo_capacity = Column(String(100), nullable=False)
    consumables = Column(String(100), nullable=False)
    url = Column(String(200), nullable=False)
    created = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    edited = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    favoritos = relationship('Favorito', backref='vehiculo', lazy='select')

class Persona(Base):
    __tablename__ = 'persona'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    birth_year = Column(String(100), nullable=False)
    eye_color = Column(String(100), nullable=False)
    gender = Column(String(100), nullable=False)
    hair_color = Column(String(100), nullable=False)
    height = Column(String(20), nullable=False)
    mass = Column(String(40), nullable=False)
    skin_color = Column(String(20), nullable=False)
    homeworld = Column(String(40), nullable=False)
    url = Column(String(100), nullable=False)
    created = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    edited = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    favoritos = relationship('Favorito', backref='persona', lazy='select')

class Favorito(Base):
    __tablename__ = 'favorito'
    
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id', ondelete='CASCADE'), nullable=False)
    persona_id = Column(Integer, ForeignKey('persona.id', ondelete='CASCADE'), nullable=True)
    vehiculo_id = Column(Integer, ForeignKey('vehiculo.id', ondelete='CASCADE'), nullable=True)
    planeta_id = Column(Integer, ForeignKey('planeta.id', ondelete='CASCADE'), nullable=True)

# Generar el diagrama del esquema de la base de datos
render_er(Base, 'diagram.png')
