from tkinter import messagebox

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# Configuração do URL do banco de dados
DATABASE_URL = 'mysql+mysqlconnector://root:@localhost/avalia_projeto'

try:
    # Criação do engine para conectar ao banco
    engine = create_engine(DATABASE_URL, echo=True)

    # Criação de uma session para gerenciar as operações no banco
    SessionLocal = scoped_session(sessionmaker(bind=engine))

    # Base para os models
    Base = declarative_base()

except SQLAlchemyError as sqla_error:
    messagebox.showerror(
        'Erro ao conectar ao banco de dados',
        f'Erro ao conectar ao banco de dados: Detalhes: {sqla_error}',
    )
