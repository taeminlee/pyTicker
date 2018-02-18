from kyoukai import Kyoukai, HTTPRequestContext
import json

def run_server():
    kyk = Kyoukai("example_app")

    @kyk.route("/")
    async def index(ctx: HTTPRequestContext):
        return "HELLO", 200

    @kyk.route("/data")
    async def data(ctx: HTTPRequestContext):
        with open('upbit.json', 'r') as upbit_json:
            return json.dumps(json.load(upbit_json)), 200, {"Content-Type": "application/json"}
        
    kyk.run()

if __name__ == "__main__":
    run_server()