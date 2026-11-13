# Análise de sistemas — Biblioteca em Python

## Análise de sistemas

## Sistema de gerenciamento de biblioteca

O projeto é um controle de biblioteca pelo terminal. A proposta é cadastrar livros e usuários, registrar quem está com cada exemplar e consultar o que está disponível. As operações ficam em um menu que se repete até a escolha da opção 0.

## 1. Escopo e participação

O atendente é a pessoa que opera o programa. O usuário da biblioteca é a pessoa cadastrada para pegar livros emprestados; nesta versão, ela não acessa o sistema diretamente. Cada livro cadastrado representa um exemplar físico, com um ID próprio.

## 2. Requisitos funcionais

RF01 — Adicionar livros. Cadastrar título e autor, gerar um ID único e iniciar o exemplar como disponível.

RF02 — Remover livros. Excluir um exemplar pelo ID, desde que ele não esteja emprestado.

RF03 — Listar o acervo. Exibir ID, título, autor e situação de todos os exemplares.

RF04 — Registrar usuários. Cadastrar o nome de uma pessoa e gerar um ID único.

RF05 — Listar usuários. Exibir ID, nome e IDs dos livros emprestados a cada pessoa.

RF06 — Registrar empréstimos. Relacionar um exemplar disponível a um usuário cadastrado e atualizar sua disponibilidade.

RF07 — Consultar empréstimos. Mostrar os empréstimos ativos, com IDs, título e nome da pessoa responsável.

RF08 — Registrar devoluções. Encerrar o empréstimo e tornar o exemplar disponível novamente.

RF09 — Consultar disponibilidade. Oferecer listas separadas de exemplares disponíveis e emprestados.

RF10 — Encerrar o programa. Manter o menu em repetição e sair quando o atendente digitar 0.

## 3. Requisitos não funcionais

RNF01 — Usabilidade. Apresentar menu numerado e mensagens em português. Informar quando não houver registros e explicar erros de entrada sem encerrar a sessão.

RNF02 — Integridade. Validar campos obrigatórios e a existência dos IDs antes de alterar os registros. Não permitir dois empréstimos ativos para o mesmo exemplar nem remoção de exemplar emprestado.

RNF03 — Privacidade e segurança. Solicitar apenas o nome da pessoa, sem documentos ou dados sensíveis. Esta versão é local, sem login ou controle de acesso, e deve ser usada para o exercício com dados fictícios.

RNF04 — Desempenho. Atender ao uso individual com um acervo pequeno em memória. A busca por ID percorre uma lista, com custo O(n). Não há meta de tempo medida nem teste de carga nesta entrega.

RNF05 — Manutenção. Separar as operações em funções com nomes claros e docstrings. Manter as regras separadas da leitura de entradas e da impressão de mensagens.

RNF06 — Compatibilidade. Executar em terminal com Python 3.10 ou superior e sem dependências externas de execução. Usar pytest apenas para os testes.

RNF07 — Armazenamento. Utilizar listas e dicionários em memória durante a sessão e avisar que os dados serão apagados ao sair. Persistência em banco ou arquivo fica fora do escopo.

## 4. Regras do sistema

Um exemplar pode ter somente um empréstimo ativo. Uma pessoa pode pegar mais de um exemplar; não foi definido limite nesta atividade. Títulos e nomes iguais são permitidos porque a identificação é feita pelo ID.

Título, autor e nome não podem ficar vazios. Os IDs gerados são inteiros positivos e não são reutilizados após uma remoção. O menu recusa IDs digitados como texto ou números não positivos.

A devolução é feita pelo ID do livro. Ela remove o empréstimo ativo, retira o ID da lista da pessoa e libera o exemplar. Não há histórico de empréstimos encerrados, reservas, multas ou prazos nesta versão.

## 5. Estrutura e funcionamento

O estado da biblioteca é um dicionário com três listas: livros, usuarios e emprestimos. Ele também guarda os contadores proximo_livro e proximo_usuario.

Livro: id (inteiro), titulo (texto), autor (texto) e disponivel (booleano).

Usuário: id (inteiro), nome (texto) e livros_emprestados (lista de IDs de livros).

Empréstimo: livro_id e usuario_id (inteiros que ligam os cadastros).

As funções recebem o dicionário da biblioteca como argumento. Isso permite criar um estado novo para cada teste e evita depender de listas globais. O arquivo biblioteca.py reúne as funções para manter a entrega simples.

## 6. Fluxo principal e exceções

O programa cria a biblioteca vazia e entra no laço while True. A função executar_opcao() lê os dados necessários e chama a operação escolhida. Ao digitar 0, o break encerra o laço.

As regras usam ValueError para indicar uma entrada inválida ou uma operação não permitida. O menu captura esse erro e mostra uma mensagem. Também encerra de forma controlada quando recebe fim de entrada ou Ctrl+C.

Exemplo: o atendente cadastra um livro e uma pessoa, registra o empréstimo pelos IDs e consulta a lista de empréstimos. Depois, registra a devolução e confirma que o livro voltou à lista de disponíveis.

## 7. Testes e versionamento

Foram executados 24 testes automatizados com pytest, todos aprovados. Eles cobrem cadastros, campos vazios, IDs inexistentes, filtros de disponibilidade, empréstimo duplicado, bloqueio de remoção, devolução, IDs após remoção e o fluxo pelo menu.

Execução: python3 -m pytest -q. Os testes usam dados fictícios, uma fixture para criar estados independentes e monkeypatch para simular entradas do terminal.

O repositório Git local tem commits por etapa e branches de gerenciamento, testes e documentação, integradas à main. O projeto está publicado em github.com/MarkusEagle39/biblioteca-python. O mesmo endereço está no arquivo meu_projeto_github.txt.

## 8. Casos de uso

O diagrama mostra o atendente e as operações disponíveis no menu. As linhas indicam quais ações ele pode executar; não representam a ordem das etapas.
