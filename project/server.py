from flask import Flask, render_template, redirect, url_for
import asyncio
import logging
from typing import Union, Literal
from project.config import (LOGS_FILE_PATH,
                            DEFAULT_LOGS_FILE,
                            SERVER_HOST,
                            SERVER_PORT)
import os


class Server:
    def __init__(self,
                 path_to_logs_file: str,
                 host: Union[str, None] = None,
                 port: Union[int, None] = None,
                 debug: bool = True):
        """
        Parameters
        ----------
        path_to_logs_file : str
            Путь до лог-файла.
        host : int
            Хост сервера.
        port : int
            Порт сервера.
        debug : bool
            Режим работы сервера.
        """
        self.script_file_name = "script/clear_cache.py"
        self.logs_file = path_to_logs_file
        self.logs_format = "%(asctime)s %(levelname)s %(message)s"
        # Определяем настройки для логирования событий.
        logging.basicConfig(level=logging.INFO, filename=self.logs_file, format=self.logs_format)
        logging.basicConfig(level=logging.WARNING, filename=self.logs_file, format=self.logs_format)
        # Параметры сервера.
        self.host = host
        self.port = port
        self.debug = debug
        # Инициализируем и сразу запускаем сервер.
        self.app = Flask(__name__)
        self.run()
        self.app.run(host=self.host, port=self.port, debug=self.debug)

    async def run_script_async(self) -> Literal["1", "0"]:
        """ Корутина для запуска исполняемого скрипта. """
        process = await asyncio.create_subprocess_exec(
            "python", self.script_file_name,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        # Запускаем исполнения скрипта в цикле событий.
        stdout, _ = await process.communicate()
        # По завершению работы скрипта принимаем байт строку с ответом о статусе исполнения.
        stdout = stdout.decode("utf-8").strip()
        return stdout

    def run(self):
        """ Функция инициализирует обработчики событий. """

        @self.app.route("/")
        def index():
            """ Функция рендерит страницу index.html """
            return render_template("index.html")

        @self.app.route("/run-script")
        async def run_script():
            """ Корутина. Асинхронно запускает исполняемый скрипт.
                В зависимости от того, как будет выполнен скрипт, производит редирект
                на страницы /done_page и /failed_page """
            response = await self.run_script_async()
            if response == "1":
                return redirect(url_for("done_page"))
            else:
                return redirect(url_for("failed_page"))

        @self.app.route("/done_page")
        def done_page():
            """ Функция рендерит страницу done_page.html """
            return render_template("done_page.html")

        @self.app.route("/failed_page")
        def failed_page():
            """ Функция рендерит страницу failed_page.html """
            return render_template("failed_page.html")


if __name__ == "__main__":
    # Определяем файл для логирования состояний сервера.
    logs_file = LOGS_FILE_PATH if os.path.exists(LOGS_FILE_PATH) else DEFAULT_LOGS_FILE
    debug_mode = True
    app = Server(
        path_to_logs_file=logs_file,
        host=SERVER_HOST,
        port=SERVER_PORT,
        debug=debug_mode
    )
