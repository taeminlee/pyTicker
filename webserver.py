from kyoukai import Kyoukai, HTTPRequestContext
import json

def run_server():
    kyk = Kyoukai("PyTicker2 API Server")

    @kyk.route("/")
    async def index(ctx: HTTPRequestContext):
        return "HELLO", 200

    @kyk.route("/data")
    async def data(ctx: HTTPRequestContext):
        with open('dump.json', 'r') as pyticker_json:
            return json.dumps(json.load(pyticker_json)), 200, {"Content-Type": "application/json"}
        
    kyk.run()

if __name__ == "__main__":
    run_server()