Projeto de Observabilidade: Flask + OpenTelemetry + Prometheus + Grafana

Aprendendo um pouco sobre métricas, logs e traces, replicando elas em Prometheus e criando dashboard no Grafana.

Este projeto serve como um laboratório prático para entender como implementar a stack de observabilidade moderna em uma aplicação Python (Flask) utilizando o ecossistema OpenTelemetry e ferramentas do Cloud Native (Prometheus e Grafana) rodando em Docker.

🚀 Tecnologias Utilizadas

Python / Flask: Aplicação web base a ser monitorizada.

OpenTelemetry: Padrão open-source para instrumentação de código e geração de telemetria (Métricas, Logs, Traces).

OpenTelemetry Collector: Recebe, processa e exporta os dados da aplicação.

Prometheus: Banco de dados de séries temporais (TSDB) que coleta (scrape) as métricas do Collector.

Grafana: Plataforma de visualização para criar dashboards interativos.

Docker: Containerização dos serviços de infraestrutura.

📋 Pré-requisitos

Para rodar este projeto na sua máquina, vai precisar de:

Python 3.x instalado.

Docker e Docker Compose (ou Docker Desktop se estiver usando Windows/WSL2).

Git.

🛠️ Como Executar o Projeto

Siga os passos abaixo para subir toda a infraestrutura e a aplicação.

1. Preparar o Ambiente Python

Clone o repositório e crie um ambiente virtual para instalar as dependências:

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências da aplicação e do OpenTelemetry
pip install Flask opentelemetry-distro opentelemetry-instrumentation-flask


2. Subir o OpenTelemetry Collector (Docker)

Crie um arquivo /tmp/otel-collector-config.yaml com a configuração do OTel (exportando no modo debug e prometheus). Depois, rode o container:

docker run -d -p 4317:4317 -p 4318:4318 -p 8889:8889 \
  --name otel-collector \
  -v /tmp/otel-collector-config.yaml:/etc/otel-collector-config.yaml \
  otel/opentelemetry-collector:latest \
  --config=/etc/otel-collector-config.yaml


3. Subir o Prometheus (Docker)

Crie um arquivo /tmp/prometheus.yml apontando para o target host.docker.internal:8889. Em seguida, inicie o Prometheus:

docker run -d -p 9090:9090 \
  --name prometheus \
  --add-host=host.docker.internal:host-gateway \
  -v /tmp/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus


(Nota: A flag --add-host é essencial no WSL2/Linux para que o Docker acesse o localhost da sua máquina).

4. Subir o Grafana (Docker)

Inicie o Grafana para criar os dashboards:

docker run -d -p 3000:3000 \
  --name grafana \
  --add-host=host.docker.internal:host-gateway \
  grafana/grafana


5. Iniciar a Aplicação Flask com Instrumentação

Com toda a infraestrutura rodando, inicie sua aplicação injetando o OpenTelemetry de forma automática:

opentelemetry-instrument \
  --traces_exporter otlp \
  --metrics_exporter otlp \
  --logs_exporter otlp \
  flask run -p 8080


🌐 Acessando as Interfaces

Após iniciar tudo, gere algum tráfego acessando a sua aplicação:

Aplicação Flask: http://127.0.0.1:8080/rolldice (Atualize algumas vezes para gerar dados)

Em seguida, visualize os dados nas seguintes ferramentas:

Prometheus: http://localhost:9090

Dica de busca (PromQL): Use rate(http_server_duration_milliseconds_count[1m]) para ver a taxa de requisições.

Grafana: http://localhost:3000

Credenciais padrão: admin / admin

Configuração do Data Source: Adicione o Prometheus com a URL http://host.docker.internal:9090.

