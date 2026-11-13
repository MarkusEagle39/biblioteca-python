# Biblioteca em Python

Repositório público: https://github.com/MarkusEagle39/biblioteca-python

Este projeto organiza livros, usuários e empréstimos pelo terminal. A ideia é praticar funções, listas, dicionários e testes em Python com um exemplo de biblioteca.

## Como executar

Com Python 3.10 ou mais recente, abra o terminal na pasta do projeto:

```bash
python3 biblioteca.py
```

No Windows, o comando pode ser `python biblioteca.py`.

O menu fica aberto até você digitar `0`. Os dados ficam apenas na memória: ao fechar o programa, os cadastros são perdidos. Cada cadastro de livro representa um exemplar. Dois exemplares do mesmo título recebem IDs diferentes.

## O que dá para fazer

- Adicionar e remover livros.
- Listar o acervo e filtrar livros disponíveis ou emprestados.
- Registrar e listar usuários.
- Registrar empréstimos e consultar quem está com cada livro.
- Registrar devoluções.

Um livro emprestado não pode ser removido nem emprestado novamente antes da devolução. O programa também verifica campos vazios, IDs inexistentes e opções inválidas.

## Como testar

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m pytest -q
```

O programa não precisa de bibliotecas externas para funcionar. O pytest é necessário somente para os testes.

## Um exemplo para experimentar

1. Digite `1` e cadastre o livro *Dom Casmurro*, de Machado de Assis.
2. Digite `4` e cadastre uma pessoa fictícia, como Ana.
3. Digite `6` e informe o ID do livro e o ID da pessoa.
4. Digite `7` e confira o empréstimo.
5. Digite `8` e informe o ID do livro para devolver.
6. Digite `0` para sair.

## Organização

- `biblioteca.py`: regras da biblioteca e menu, separados em funções.
- `test_biblioteca.py`: testes automatizados.
- `docs/analise_sistemas.pdf`: requisitos, estrutura dos dados e regras.
- `docs/diagrama_casos_uso.pdf`: diagrama dos casos de uso.
- `GUIA_DE_ESTUDO.md`: explicação do código e roteiro de entrega.
- `meu_projeto_github.txt`: link público para entrega.

## Versionamento

O histórico local foi dividido em etapas de implementação. As branches de funcionalidades foram mantidas para mostrar o desenvolvimento. Para consultar:

```bash
git log --oneline --graph --all
git branch
```

Se a publicação ainda estiver pendente, veja o roteiro em `GUIA_DE_ESTUDO.md`. Não envie o arquivo de link ao tutor antes de confirmar que o repositório está público e que o endereço abre.
