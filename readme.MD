# Relatório de Métricas

Este é um script Python para coletar métricas do sistema e enviá-las por e-mail em formato de relatório HTML. O relatório inclui informações sobre o uso do sistema, processos em execução, E/S de disco e E/S de rede.

Adicione mais recursos da biblíoteca `psutil` e `platform` conforme sua necessidade!

## Requisitos

- Python 3.x
- Bibliotecas Python:
  - psutil
  - smtplib
  - email
  - dotenv

## Configuração

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   ```
2. Instale as dependências:
`pip install -r requirements.txt`

3. Configure as variáveis de ambiente:
Crie um arquivo .env na raiz do projeto com as seguintes variáveis:
    ```bash
    EMAIL_ADDRESS=seu-email@gmail.com
    EMAIL_PASSWORD=sua-senha-do-email
    RECIPIENT_EMAIL=email-do-destinatario@gmail.com
    ```
Substitua seu-email@gmail.com, sua-senha-do-email e email-do-destinatario@gmail.com pelas informações corretas.

## Uso
Execute o script Python: `python metrics_report.py`
Isso enviará um relatório de métricas por e-mail a cada hora.
![Exemplo do relatório](https://i.imgur.com/jyinWlL.png)

## Personalização
Você pode personalizar o conteúdo e o estilo do relatório HTML editando o script `metrics_report.py`.

## Contribuição

Contribuições são bem-vindas! Se você encontrar algum problema ou tiver sugestões de melhorias, sinta-se à vontade para abrir uma [issue](https://github.com/Solvezera/metrics_report/issues) ou enviar um [pull request](https://github.com/metrics_report/passmanager/pulls).

## Licença

Este projeto é licenciado sob a [MIT License](https://opensource.org/licenses/MIT).