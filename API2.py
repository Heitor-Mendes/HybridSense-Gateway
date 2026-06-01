from flask import Flask, request, jsonify

app = Flask(__name__)

sensors = []
next_id = 1


@app.route("/sensor/add", methods=["POST"])
def add_sensor():
    global next_id

    data = request.json

    sensor = {
        "id": next_id,
        "nome": data["nome"],
        "endereco": hex(next_id),
        "tensao": data["tensao"],
        "protocolo": data["protocolo"]
    }

    sensors.append(sensor)
    next_id += 1

    print("Sensor adicionado:", sensor)

    return jsonify({"status": "ok", "sensor": sensor})


@app.route("/sensor/list", methods=["GET"])
def list_sensor():
    return jsonify(sensors)


@app.route("/sensor/remove", methods=["POST"])
def remove_sensor():
    sid = int(request.json["id"])

    global sensors
    sensors = [s for s in sensors if s["id"] != sid]

    return jsonify({"status": "removido"})


@app.route("/simular", methods=["POST"])
def simular():
    sensor_id = request.json["id"]

    print(f"Simulação iniciada sensor {sensor_id}")

    return jsonify({"status": "simulação iniciada"})


@app.route("/processar", methods=["POST"])
def processar():

    # simulação fake (senoide)
    import math

    data = {
        "t": list(range(100)),
        "y": [math.sin(x * 0.1) for x in range(100)]
    }

    return jsonify(data)


if __name__ == "__main__":
    app.run(port=5000)