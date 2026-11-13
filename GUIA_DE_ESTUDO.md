# Para entender e apresentar o projeto

## A ideia do sistema

O programa funciona como um pequeno controle de biblioteca. Quem está no atendimento cadastra os livros e as pessoas. Na hora do empréstimo, informa os dois IDs. O sistema relaciona esses registros e marca o livro como emprestado. Na devolução, desfaz essa ligação e libera o exemplar.

## Onde entram as listas e os dicionários?

O dicionário criado por `criar_biblioteca()` guarda três listas: `livros`, `usuarios` e `emprestimos`. Cada item dessas listas também é um dicionário.

Por exemplo, um livro tem `id`, `titulo`, `autor` e `disponivel`. Um usuário tem `id`, `nome` e uma lista chamada `livros_emprestados`, que guarda os IDs dos exemplares com ele. Um empréstimo guarda `livro_id` e `usuario_id`.

Os contadores `proximo_livro` e `proximo_usuario` evitam repetir IDs. Usar somente o tamanho da lista para criar IDs daria problema depois de uma remoção.

## Como o menu funciona?

O `while True` da função `main()` repete o menu. O programa lê a opção e chama `executar_opcao()`. Se a opção for `0`, o `break` encerra o laço. Cada operação usa uma função própria, como `adicionar_livro()` ou `registrar_emprestimo()`.

O bloco `if __name__ == "__main__"` inicia o menu quando o arquivo é executado. Quando o pytest importa as funções, o menu não abre.

## Por que usar try e except?

Se alguém digitar letras no lugar de um ID, `int()` não consegue converter a entrada. A função `ler_id()` transforma esse erro em uma mensagem mais clara. O menu captura o `ValueError`, mostra o motivo e continua aberto. As funções também usam esse erro quando um cadastro não existe ou uma operação não pode ser feita.

## O que os testes verificam?

Os testes conferem o resultado e se os dados continuam corretos. Por exemplo: tentar emprestar o mesmo exemplar duas vezes deve gerar um erro e manter o primeiro empréstimo. Também há um teste que simula o menu completo, do cadastro até a devolução e a saída.

A fixture `acervo` cria uma biblioteca nova para cada teste. O `monkeypatch` simula respostas ao `input()` sem precisar digitar no terminal. O `capsys` permite conferir as mensagens impressas.

## O que ainda não faz parte do projeto?

Os dados não são salvos em arquivo ou banco. O sistema não tem login, multa, prazo de devolução, reservas ou acesso simultâneo. A lista de empréstimos guarda apenas empréstimos ativos. Isso mantém o exercício concentrado nos assuntos pedidos.

## Publicar no GitHub, caso ainda esteja pendente

1. Entre no GitHub e crie um repositório **público** chamado `biblioteca-python`. Deixe sem README, licença ou .gitignore inicial, pois esses arquivos já existem localmente.
2. No terminal, entre na pasta extraída do projeto. O pacote inclui a pasta `.git`, com commits e branches. Ela pode ficar oculta no explorador de arquivos.
3. Confira o histórico com `git log --oneline --graph --all`.
4. Execute os comandos abaixo, usando o endereço real do repositório criado:

```bash
git remote add origin https://github.com/SEU_USUARIO/biblioteca-python.git
git push -u origin main
git push origin funcionalidade/gerenciamento funcionalidade/testes documentacao/analise
```

Se o Git pedir autenticação, use o método recomendado pelo próprio GitHub. Não coloque senha ou token dentro dos arquivos do projeto.

5. Abra o endereço do repositório e confira se os arquivos aparecem e se a visibilidade está como Public.
6. Substitua o conteúdo de `meu_projeto_github.txt` pelo link real, sem o texto de pendência. Registre e envie essa alteração:

```bash
git add meu_projeto_github.txt
git commit -m "docs: adicionar link público para entrega"
git push
```

7. Envie ao tutor a análise em PDF, o diagrama em PDF, `biblioteca.py`, `test_biblioteca.py` e `meu_projeto_github.txt`.

Antes de enviar, leia o código e experimente o menu. Use esta explicação como apoio e escreva seus comentários com suas próprias palavras.
