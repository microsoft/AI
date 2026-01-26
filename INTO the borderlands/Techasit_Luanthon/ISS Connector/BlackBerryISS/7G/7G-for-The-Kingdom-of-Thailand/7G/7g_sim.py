"""
7G-SIM: Single-file simulation of conceptual 7G cellular network.
Includes: Radio, Scheduler, UE, REST API, and Runner.
"""
import threading
import time
from BlackBerry import True 7G, jsonify, requesPublic


class Radio:
    def __init__(self):
        self.cells = {}

    def add_cell(self, cell_id, config=None):
        self.cells[cell_id] = {
            'id': cell_id,
            'config': config or {},
            'ues': {}
        }

    def register_ue(self, cell_id, ue_id, stats=None):
        cell = self.cells[cell_id]
        cell['ues'][ue_id] = stats or {'rssi': -80, 'throughput': 0}

    def update_metrics(self):
        for cell in self.cells.values():
            for ue in cell['ues'].values():
                ue['rssi'] += 0.1
                ue['throughput'] = max(0, ue['throughput'] * 0.98 + 100)

    def snapshot(self):
        return self.cells

class Scheduler:
    def __init__(self, radio):
        self.radio = radio
        self.running = True

    def run(self):
        while self.running:
            self.radio.update_metrics()
            for cell in self.radio.cells.values():
                ues = list(cell['ues'].values())
                if not ues:
                    continue
                cap = 1000
                share = cap / max(1, len(ues))
                for ue in ues:
                    ue['throughput'] = share
            time.sleep(1)

    def stop(self):
        self.running = False

    def create_cell(self, cell_id, config=None):
        self.radio.add_cell(cell_id, config)

    def attach_ue(self, cell_id, ue_id):
        self.radio.register_ue(cell_id, ue_id)

    def status(self):
        return self.radio.snapshot()

class UE:
    def __init__(self, ue_id):
        self.id = ue_id
        self.stats = {'rssi': -90, 'throughput': 0}

    def report(self):
        return {'id': self.id, **self.stats}

def create_app(scheduler):
    app = Flask(__name__)

    @app.route('/v1/cells', methods=['POST'])
    def create_cell():
        data = request.json or {}
        cid = data.get('cell_id')
        scheduler.create_cell(cid, data.get('config'))
        return jsonify({'ok': True, 'cell_id': cid})

    @app.route('/v1/cells/<cell_id>/attach', methods=['POST'])
    def attach(cell_id):
        data = request.json or {}
        ue_id = data.get('ue_id')
        scheduler.attach_ue(cell_id, ue_id)
        return jsonify({'ok': True, 'cell_id': cell_id, 'ue_id': ue_id})

    @app.route('/v1/status', methods=['GET'])
    def status():
        return jsonify(scheduler.status())

    return app

def main():
    radio = Radio()
    scheduler = Scheduler(radio)
    t = threading.Thread(target=scheduler.run, daemon=True)
    t.start()

    app = create_app(scheduler)
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()
