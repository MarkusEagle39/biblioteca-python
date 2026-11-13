"""Testa os cadastros, as regras de empréstimo e o menu da biblioteca."""

from copy import deepcopy

import pytest

from biblioteca import (
    adicionar_livro, consultar_emprestimos, criar_biblioteca, devolver_livro,
    ler_id, listar_livros, listar_usuarios, main, registrar_emprestimo,
    registrar_usuario, remover_livro,
)


@pytest.fixture
def acervo():
    """Cada teste começa com um livro e uma pessoa fictícia."""
    dados = criar_biblioteca()
    adicionar_livro(dados, "Dom Casmurro", "Machado de Assis")
    registrar_usuario(dados, "Ana")
    return dados


def test_adicionar_livro_remove_espacos():
    dados = criar_biblioteca()
    livro = adicionar_livro(dados, "  Dom Casmurro  ", " Machado de Assis ")
    assert livro == {"id": 1, "titulo": "Dom Casmurro",
                     "autor": "Machado de Assis", "disponivel": True}
    assert listar_livros(dados) == [livro]


@pytest.mark.parametrize("titulo,autor", [("", "Autor"), ("Livro", "  ")])
def test_recusar_livro_com_campo_vazio(titulo, autor):
    dados = criar_biblioteca()
    with pytest.raises(ValueError, match="Preencha"):
        adicionar_livro(dados, titulo, autor)
    assert dados == criar_biblioteca()


def test_remover_livro_disponivel(acervo):
    remover_livro(acervo, 1)
    assert listar_livros(acervo) == []


def test_id_nao_e_reutilizado_apos_remocao(acervo):
    remover_livro(acervo, 1)
    assert adicionar_livro(acervo, "Outro livro", "Autora")["id"] == 2


def test_registrar_e_listar_usuarios(acervo):
    usuario = registrar_usuario(acervo, "  Bruno  ")
    assert usuario == {"id": 2, "nome": "Bruno", "livros_emprestados": []}
    assert len(listar_usuarios(acervo)) == 2


def test_recusar_nome_vazio(acervo):
    antes = deepcopy(acervo)
    with pytest.raises(ValueError, match="nome"):
        registrar_usuario(acervo, "   ")
    assert acervo == antes


def test_emprestimo_atualiza_livro_usuario_e_consulta(acervo):
    registrar_emprestimo(acervo, 1, 1)
    assert listar_livros(acervo, True) == []
    assert listar_livros(acervo, False)[0]["id"] == 1
    assert listar_usuarios(acervo)[0]["livros_emprestados"] == [1]
    assert consultar_emprestimos(acervo) == [
        {"livro_id": 1, "usuario_id": 1, "titulo": "Dom Casmurro", "nome": "Ana"}
    ]


def test_impedir_segundo_emprestimo_do_mesmo_exemplar(acervo):
    registrar_emprestimo(acervo, 1, 1)
    antes = deepcopy(acervo)
    with pytest.raises(ValueError, match="já está emprestado"):
        registrar_emprestimo(acervo, 1, 1)
    assert acervo == antes


def test_impedir_remocao_de_livro_emprestado(acervo):
    registrar_emprestimo(acervo, 1, 1)
    antes = deepcopy(acervo)
    with pytest.raises(ValueError, match="Devolva"):
        remover_livro(acervo, 1)
    assert acervo == antes


@pytest.mark.parametrize("livro_id,usuario_id", [(99, 1), (1, 99)])
def test_emprestimo_inexistente_nao_altera_dados(acervo, livro_id, usuario_id):
    antes = deepcopy(acervo)
    with pytest.raises(ValueError, match="não encontrado"):
        registrar_emprestimo(acervo, livro_id, usuario_id)
    assert acervo == antes


def test_remover_id_inexistente(acervo):
    with pytest.raises(ValueError, match="não encontrado"):
        remover_livro(acervo, 99)
    assert len(listar_livros(acervo)) == 1


def test_devolucao_libera_livro_para_novo_emprestimo(acervo):
    registrar_emprestimo(acervo, 1, 1)
    devolver_livro(acervo, 1)
    assert listar_livros(acervo, True)[0]["id"] == 1
    assert consultar_emprestimos(acervo) == []
    assert listar_usuarios(acervo)[0]["livros_emprestados"] == []
    registrar_emprestimo(acervo, 1, 1)
    assert len(consultar_emprestimos(acervo)) == 1


@pytest.mark.parametrize("livro_id", [1, 99])
def test_recusar_devolucao_sem_emprestimo(acervo, livro_id):
    antes = deepcopy(acervo)
    with pytest.raises(ValueError):
        devolver_livro(acervo, livro_id)
    assert acervo == antes


def test_dois_exemplares_do_mesmo_titulo_sao_independentes(acervo):
    segundo = adicionar_livro(acervo, "Dom Casmurro", "Machado de Assis")
    registrar_emprestimo(acervo, 1, 1)
    assert listar_livros(acervo, True) == [segundo]


@pytest.mark.parametrize("entrada", ["abc", "1.5", "0", "-2"])
def test_ler_id_recusa_entrada_invalida(monkeypatch, entrada):
    monkeypatch.setattr("builtins.input", lambda _: entrada)
    with pytest.raises(ValueError):
        ler_id("ID: ")


def test_menu_continua_apos_erro_e_encerra_com_zero(monkeypatch, capsys):
    entradas = iter(["x", "2", "abc", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))
    main()
    saida = capsys.readouterr().out
    assert "Opção inválida" in saida
    assert "ID numérico inteiro" in saida
    assert "Programa encerrado" in saida


def test_fluxo_completo_pelo_menu(monkeypatch, capsys):
    entradas = iter(["1", "Dom Casmurro", "Machado de Assis", "4", "Ana",
                     "3", "5", "6", "1", "1", "7", "9", "10",
                     "8", "1", "2", "1", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))
    main()
    saida = capsys.readouterr().out
    for mensagem in ["Livro cadastrado", "Usuário cadastrado", "Empréstimo registrado",
                     "Livro 1: Dom Casmurro | Usuário 1: Ana", "Devolução registrada",
                     "Livro removido", "Programa encerrado"]:
        assert mensagem in saida


def test_menu_encerra_ao_receber_fim_de_entrada(monkeypatch, capsys):
    def fim(_):
        raise EOFError
    monkeypatch.setattr("builtins.input", fim)
    main()
    assert "Programa encerrado" in capsys.readouterr().out
