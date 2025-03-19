from flask import Flask, render_template, redirect, url_for
import asyncio
from typing import Union


class Server:
    def __init__(self,
                 host: Union[str, None] = None,
                 port: Union[int, None] = None,
                 debug: bool = True):
        self.script_file_name = "test.py"
        self.host = host
        self.port = port
        self.debug = debug
        self.app = Flask(__name__)
        self.run()
        self.app.run(host=self.host, port=self.port, debug=self.debug)

    async def run_script_async(self):
        process = await asyncio.create_subprocess_exec(
            "python", self.script_file_name,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        # Логирование результата работы скрипта для отладки
        if stdout:
            print(f"[stdout]\n{stdout.decode()}")
        if stderr:
            print(f"[stderr]\n{stderr.decode()}")

    def run(self):
        @self.app.route("/")
        def index():
            return render_template("index.html")

        @self.app.route("/run-script")
        async def run_script():
            # Асинхронно запускаем ваш Python-скрипт.
            await self.run_script_async()
            return redirect(url_for("done_page"))

        @self.app.route("/done_page")
        def done_page():
            return render_template("done_page.html")


if __name__ == "__main__":
    print(True)
    server_host = "0.0.0.0"
    server_port = 5000
    debug_mode = False
    app = Server(debug=debug_mode)
