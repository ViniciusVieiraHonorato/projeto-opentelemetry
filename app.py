import logging
from random import randint
from flask import Flask, request
from opentelemetry import metrics, trace

# Adquira um rastreador (Traces)
tracer = trace.get_tracer("diceroller.tracer")

# Adquira um medidor (Metrics)
meter = metrics.get_meter("diceroller.meter")

# Cria um instrumento contador para fazer medições
roll_counter = meter.create_counter(
    "dice.rolls",
    description="O número de jogadas por valor de jogada",
)

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route("/rolldice")
def roll_dice():
    # Cria um novo span para a operação
    with tracer.start_as_current_span("roll") as roll_span:
        player = request.args.get("player", default=None, type=str)
        result = str(roll())

        # Adiciona atributo ao span do trace
        roll_span.set_attribute("roll.value", result)

        # Adiciona 1 ao contador da métrica
        roll_counter.add(1, {"roll.value": result})

        if player:
            logger.warning("%s esta jogando os dados: %s", player, result)
        else:
            logger.warning("Jogador anonimo esta jogando os dados: %s", result)

        return result


def roll():
    return randint(1, 6)
