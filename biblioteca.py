"""Biblioteca de terminal com listas e dicionários; os dados duram uma sessão."""


def criar_biblioteca():
    """Cria um estado independente, útil também para isolar os testes."""
    return {"livros": [], "usuarios": [], "emprestimos": [],
            "proximo_livro": 1, "proximo_usuario": 1}


def validar_texto(texto, campo):
    """Remove espaços das pontas e recusa campos em branco."""
    if not isinstance(texto, str) or not texto.strip():
        raise ValueError(f"Preencha o campo {campo}.")
    return texto.strip()


def buscar_por_id(registros, identificador, tipo):
    """Localiza um registro ou informa que o ID não existe."""
    for registro in registros:
        if registro["id"] == identificador:
            return registro
    raise ValueError(f"{tipo} não encontrado: ID {identificador}.")


def adicionar_livro(biblioteca, titulo, autor):
    """Cadastra um exemplar com ID único e disponibilidade inicial."""
    titulo = validar_texto(titulo, "título")
    autor = validar_texto(autor, "autor")
    livro = {"id": biblioteca["proximo_livro"], "titulo": titulo,
             "autor": autor, "disponivel": True}
    biblioteca["livros"].append(livro)
    biblioteca["proximo_livro"] += 1
    return livro


def remover_livro(biblioteca, livro_id):
    """Remove apenas exemplares que estão disponíveis."""
    livro = buscar_por_id(biblioteca["livros"], livro_id, "Livro")
    if not livro["disponivel"]:
        raise ValueError("Devolva o livro antes de removê-lo.")
    biblioteca["livros"].remove(livro)


def listar_livros(biblioteca, disponivel=None):
    """Lista o acervo; True filtra disponíveis e False, emprestados."""
    return [livro.copy() for livro in biblioteca["livros"]
            if disponivel is None or livro["disponivel"] == disponivel]


def registrar_usuario(biblioteca, nome):
    """Registra uma pessoa; nomes iguais podem ter IDs diferentes."""
    nome = validar_texto(nome, "nome")
    usuario = {"id": biblioteca["proximo_usuario"], "nome": nome,
               "livros_emprestados": []}
    biblioteca["usuarios"].append(usuario)
    biblioteca["proximo_usuario"] += 1
    return usuario


def listar_usuarios(biblioteca):
    """Retorna cópias para consultar usuários sem alterar seus cadastros."""
    return [{**usuario, "livros_emprestados": usuario["livros_emprestados"].copy()}
            for usuario in biblioteca["usuarios"]]


def registrar_emprestimo(biblioteca, livro_id, usuario_id):
    """Valida os dois cadastros antes de modificar os dados."""
    livro = buscar_por_id(biblioteca["livros"], livro_id, "Livro")
    usuario = buscar_por_id(biblioteca["usuarios"], usuario_id, "Usuário")
    if not livro["disponivel"]:
        raise ValueError("Este livro já está emprestado.")
    biblioteca["emprestimos"].append({"livro_id": livro_id,
                                      "usuario_id": usuario_id})
    livro["disponivel"] = False
    usuario["livros_emprestados"].append(livro_id)


def consultar_emprestimos(biblioteca):
    """Relaciona os empréstimos ativos aos títulos e nomes cadastrados."""
    resultado = []
    for emprestimo in biblioteca["emprestimos"]:
        livro = buscar_por_id(biblioteca["livros"], emprestimo["livro_id"], "Livro")
        usuario = buscar_por_id(biblioteca["usuarios"], emprestimo["usuario_id"], "Usuário")
        resultado.append({**emprestimo, "titulo": livro["titulo"],
                          "nome": usuario["nome"]})
    return resultado


def devolver_livro(biblioteca, livro_id):
    """Encerra o empréstimo ativo e libera o exemplar para outra pessoa."""
    livro = buscar_por_id(biblioteca["livros"], livro_id, "Livro")
    if livro["disponivel"]:
        raise ValueError("Este livro não está emprestado.")
    for emprestimo in biblioteca["emprestimos"]:
        if emprestimo["livro_id"] == livro_id:
            usuario = buscar_por_id(biblioteca["usuarios"],
                                    emprestimo["usuario_id"], "Usuário")
            usuario["livros_emprestados"].remove(livro_id)
            biblioteca["emprestimos"].remove(emprestimo)
            livro["disponivel"] = True
            return


def ler_id(mensagem):
    """Converte a entrada do terminal e aceita somente IDs positivos."""
    try:
        identificador = int(input(mensagem))
    except ValueError:
        raise ValueError("Digite um ID numérico inteiro.") from None
    if identificador <= 0:
        raise ValueError("O ID deve ser maior que zero.")
    return identificador


def mostrar_livros(livros):
    """Exibe uma lista de livros com a situação de cada exemplar."""
    if not livros:
        print("Nenhum livro encontrado.")
    for livro in livros:
        situacao = "Disponível" if livro["disponivel"] else "Emprestado"
        print(f'{livro["id"]} | {livro["titulo"]} | {livro["autor"]} | {situacao}')


def executar_opcao(biblioteca, opcao):
    """Cuida da entrada e saída; as regras ficam nas funções acima."""
    if opcao == "1":
        livro = adicionar_livro(biblioteca, input("Título: "), input("Autor: "))
        print(f'Livro cadastrado com ID {livro["id"]}.')
    elif opcao == "2":
        remover_livro(biblioteca, ler_id("ID do livro: "))
        print("Livro removido.")
    elif opcao == "3":
        mostrar_livros(listar_livros(biblioteca))
    elif opcao == "4":
        usuario = registrar_usuario(biblioteca, input("Nome: "))
        print(f'Usuário cadastrado com ID {usuario["id"]}.')
    elif opcao == "5":
        usuarios = listar_usuarios(biblioteca)
        if not usuarios:
            print("Nenhum usuário cadastrado.")
        for usuario in usuarios:
            print(f'{usuario["id"]} | {usuario["nome"]} | '
                  f'IDs dos livros emprestados: {usuario["livros_emprestados"]}')
    elif opcao == "6":
        registrar_emprestimo(biblioteca, ler_id("ID do livro: "),
                            ler_id("ID do usuário: "))
        print("Empréstimo registrado.")
    elif opcao == "7":
        emprestimos = consultar_emprestimos(biblioteca)
        if not emprestimos:
            print("Nenhum empréstimo ativo.")
        for item in emprestimos:
            print(f'Livro {item["livro_id"]}: {item["titulo"]} | '
                  f'Usuário {item["usuario_id"]}: {item["nome"]}')
    elif opcao == "8":
        devolver_livro(biblioteca, ler_id("ID do livro: "))
        print("Devolução registrada.")
    elif opcao == "9":
        mostrar_livros(listar_livros(biblioteca, disponivel=True))
    elif opcao == "10":
        mostrar_livros(listar_livros(biblioteca, disponivel=False))
    else:
        print("Opção inválida. Escolha uma opção do menu.")


MENU = """
=== BIBLIOTECA ===
1 - Adicionar livro
2 - Remover livro
3 - Listar todo o acervo
4 - Registrar usuário
5 - Listar usuários
6 - Registrar empréstimo
7 - Consultar empréstimos ativos
8 - Devolver livro
9 - Listar livros disponíveis
10 - Listar livros emprestados
0 - Sair
"""


def main():
    """Mantém o menu aberto e trata entradas inválidas sem encerrar a sessão."""
    biblioteca = criar_biblioteca()
    print("Os dados ficam na memória e serão apagados ao sair.")
    while True:
        try:
            print(MENU)
            opcao = input("Escolha uma opção: ").strip()
            if opcao == "0":
                print("Programa encerrado. Até mais!")
                break
            executar_opcao(biblioteca, opcao)
        except ValueError as erro:
            print(f"Não foi possível concluir: {erro}")
        except (EOFError, KeyboardInterrupt):
            print("\nPrograma encerrado.")
            break


if __name__ == "__main__":
    main()
