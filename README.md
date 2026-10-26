# Nexora ERP

Sistema de console em Python para gerenciar os **materiais e custos** de um negócio de sublimação (canecas, camisetas e outros produtos personalizados).

É um projeto pessoal em desenvolvimento: nasceu para deixar de calcular à mão quanto custa produzir cada peça e quanto vale a pena cobrar por ela.

## O que ele faz?

- Cadastra materiais (papel de sublimação, tintas, bases brancas, embalagens...) com a quantidade e o custo pago.
- Calcula o custo por unidade de cada material.
- Consulta, atualiza, desativa e reativa materiais (sem apagá-los, para não perder o histórico).
- Valida os dados: não aceita quantidades inválidas nem materiais duplicados (sem diferenciar maiúsculas de minúsculas).
- Guarda o dinheiro em centavos para evitar erros de arredondamento e o exibe em reais (R$).

## Em desenvolvimento

- Fichas de custo: lista de materiais que cada produto consome e seu custo total.
- Margem de lucro e preço de venda sugerido.
- Testes automáticos.

## Como executar

Você precisa do Python 3. Não há dependências externas.

```bash
git clone https://github.com/albertoh88/Nexora-ERP.git
cd Nexora-ERP
python main.py
```

Na primeira execução, o banco de dados local `database/nexora.db` (SQLite) é criado. Esse arquivo não é enviado ao repositório.

> Se você estiver atualizando de uma versão anterior, o esquema do banco de dados pode ter mudado. Nesse caso, apague o `database/nexora.db` para que ele seja criado novamente.

## Estrutura do projeto

```
Nexora-ERP/
├── main.py            # Menus de console
├── services/          # Regras de negócio e validações
├── repositories/      # Consultas SQL
├── database/          # Conexão e esquema (schema.sql)
└── .github/workflows/ # Versionamento automático
```

O código é separado em camadas: o menu não fala diretamente com o banco de dados; ele passa pelos serviços, e estes pelos repositórios.

## Versionamento

As versões seguem o [SemVer](https://semver.org/lang/pt-BR/) e são publicadas como tags quando as mudanças são integradas à `main`. Enquanto a versão for `0.x`, o projeto ainda está em construção e pode mudar sem aviso.

## Licença

[MIT](LICENSE)