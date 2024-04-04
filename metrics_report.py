import os
import time
import psutil
import platform
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do E-mail
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')

# Função para enviar e-mail
def send_email(subject, body):
    msg = MIMEMultipart('alternative')
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject

    # Corpo do e-mail em formato HTML
    html_body = f"""
    <html>
    <body>
        <table border="0" cellspacing="0" cellpadding="10" style="border-collapse: collapse;">
            <tr>
                <td style="vertical-align: top;">
                    <table border="1" cellspacing="0" cellpadding="10" style="border-collapse: collapse;">
                        <tr>
                            <th colspan="2" style="background-color: #FDEBD0;">Uso do Sistema</th>
                        </tr>
                        <tr>
                            <td>Processador | System</td>
                            <td>{platform.processor()} | {platform.system()}</td>
                        </tr>
                        <tr>
                            <td>Quantidade de Memória</td>
                            <td>{round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB</td>
                        </tr>
                        <tr>
                            <td>Uso de CPU</td>
                            <td>{psutil.cpu_percent():.2f}%</td>
                        </tr>
                        <tr>
                            <td>Uso de Memória</td>
                            <td>{psutil.virtual_memory().percent:.2f}%</td>
                        </tr>
                        <tr>
                            <td>Uso de Disco</td>
                            <td>{psutil.disk_usage('/').percent:.2f}%</td>
                        </tr>
                        <tr>
                            <td>Conexões de Rede</td>
                            <td>{len(psutil.net_connections())}</td>
                        </tr>
                    </table>
                </td>
                <td style="vertical-align: top;">
                    <table border="1" cellspacing="0" cellpadding="10" style="border-collapse: collapse;">
                        <tr>
                            <th colspan="4" style="background-color: #FADBD8;">Processos em execução (Top 5)</th>
                        </tr>
                        <tr>
                            <th>PID</th>
                            <th>Nome</th>
                            <th>Uso de CPU</th>
                            <th>Uso de Memória</th>
                        </tr>
                        {"".join([f"<tr><td>{proc['pid']}</td><td>{proc['name']}</td><td>{proc['cpu_percent']:.2f}%</td><td>{proc['memory_percent']:.2f}%</td></tr>" for proc in get_top_5_processes()])}
                    </table>
                </td>
            </tr>
            <tr>
                <td style="vertical-align: top;">
                    <table border="1" cellspacing="0" cellpadding="10" style="border-collapse: collapse;">
                        <tr>
                            <th colspan="2" style="background-color: #D5DBDB;">E/S de Disco</th>
                        </tr>
                        <tr>
                            <td>Leituras</td>
                            <td>{psutil.disk_io_counters().read_count}</td>
                        </tr>
                        <tr>
                            <td>Escritas</td>
                            <td>{psutil.disk_io_counters().write_count}</td>
                        </tr>
                        <tr>
                            <td>Bytes lidos</td>
                            <td>{psutil.disk_io_counters().read_bytes}</td>
                        </tr>
                        <tr>
                            <td>Bytes escritos</td>
                            <td>{psutil.disk_io_counters().write_bytes}</td>
                        </tr>
                        <tr>
                            <td>Tempo de leitura</td>
                            <td>{psutil.disk_io_counters().read_time} ms</td>
                        </tr>
                        <tr>
                            <td>Tempo de escrita</td>
                            <td>{psutil.disk_io_counters().write_time} ms</td>
                        </tr>
                    </table>
                </td>
                <td style="vertical-align: top;">
                    <table border="1" cellspacing="0" cellpadding="10" style="border-collapse: collapse;">
                        <tr>
                            <th colspan="2" style="background-color: #D1F2EB;">E/S de Rede</th>
                        </tr>
                        <tr>
                            <td>Bytes enviados</td>
                            <td>{psutil.net_io_counters().bytes_sent}</td>
                        </tr>
                        <tr>
                            <td>Bytes recebidos</td>
                            <td>{psutil.net_io_counters().bytes_recv}</td>
                        </tr>
                        <tr>
                            <td>Pacotes enviados</td>
                            <td>{psutil.net_io_counters().packets_sent}</td>
                        </tr>
                        <tr>
                            <td>Pacotes recebidos</td>
                            <td>{psutil.net_io_counters().packets_recv}</td>
                        </tr>
                        <tr>
                            <td>Erros na entrada</td>
                            <td>{psutil.net_io_counters().errin}</td>
                        </tr>
                        <tr>
                            <td>Erros na saída</td>
                            <td>{psutil.net_io_counters().errout}</td>
                        </tr>
                        <tr>
                            <td>Pacotes descartados na entrada</td>
                            <td>{psutil.net_io_counters().dropin}</td>
                        </tr>
                        <tr>
                            <td>Pacotes descartados na saída</td>
                            <td>{psutil.net_io_counters().dropout}</td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

    # Adicionar o corpo HTML ao e-mail
    msg.attach(MIMEText(html_body, 'html'))

    # Enviar e-mail
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

# Função para obter os 5 processos que mais consomem recursos
def get_top_5_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        processes.append({
            'pid': proc.info['pid'],
            'name': proc.info['name'],
            'cpu_percent': proc.info['cpu_percent'],
            'memory_percent': proc.info['memory_percent']
        })
    processes.sort(key=lambda x: x['memory_percent'], reverse=True)
    return processes[:5]

# Função para coletar e enviar métricas
def send_hourly_report():
    while True:
        # Enviar e-mail com o relatório
        send_email("Relatório de Métricas", "")

        # Aguardar uma hora antes de enviar o próximo relatório
        time.sleep(3600)  # 3600 segundos = 1 hora

if __name__ == "__main__":
    send_hourly_report()
