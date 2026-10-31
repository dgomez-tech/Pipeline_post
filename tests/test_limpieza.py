"""Tests para el módulo de limpieza."""
import pandas as pd
import pytest
from src.limpieza import limpiar_posts, merge_usuarios_posts

@pytest.fixture
def df_posts_raw():
    return pd.DataFrame({
        'post_id': [1, 2, 3, 4, 5],
        'user_id': [101, 102, 103, 104, 105],
        'title': ['Post 1', 'Post 2', 'Post 3', 'Post 4', 'Post 5'],
        'body': ['Body 1', 'Body 2', 'Body 3', 'Body 4', 'Body 5'],
        'autor_nombre': ['Alice', 'Bob', 'Charlie', None, 'Eve'],
        'autor_ciudad': ['City A', 'City B', None, 'City D', 'City E'],
        'autor_empresa': ['Company A', 'Company B', 'Company C', 'Company D', 'Company E']
    })

def test_limpiar_normaliza_titulos(df_posts_raw):
    result = limpiar_posts(df_posts_raw)
    assert result['title'].tolist() == ['Post 1', 'Post 2', 'Post 3', 'Post 4', 'Post 5']

def test_limpiar_ciudad_nula_es_desconocida(df_posts_raw):
    result = limpiar_posts(df_posts_raw)
    assert 'Desconocida' in result['autor_ciudad'].values

def test_limpiar_crea_body_length(df_posts_raw):
    result = limpiar_posts(df_posts_raw)
    assert 'body_length' in result.columns
    assert (result['body_length'] > 0).all()

def test_limpiar_sin_duplicados(df_posts_raw):
    df = pd.DataFrame({
        'post_id': [1, 1, 2],
        'user_id': [1, 1, 2],
        'title': ['A', 'A duplicado', 'B'],
        'body': ['x', 'x', 'y'],
        'autor_nombre': ['Ana', 'Ana', 'Carlos'],
        'autor_ciudad': ['Madrid', 'Madrid', 'Barcelona'],
        'autor_empresa': ['X', 'X', 'Y']
    })
    resultado = limpiar_posts(df)
    assert len(resultado) == 2