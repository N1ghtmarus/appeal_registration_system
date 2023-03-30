import tornado.ioloop
import tornado.web
import os
from typing import NoReturn
import uuid
from tornado.options import define, options
import pika

import json


define("port", default=8888, help="run on the 8888", type=int)


def send_rabbitmq(msg:{} = {}) -> NoReturn:
    """
    Функция устанавливает соединение с RabbitMQ и
    посылает сообщение в очередь tornado_task
    """
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='tornado_task')
    channel.basic_publish(exchange='', routing_key='tornado_task', body=msg)
    print(" [x] The appeal sent!")
    connection.close()


class Application(tornado.web.Application):
    """
    Класс, представляющий веб-приложение Tornado.

    :param handlers: список кортежей, где каждый кортеж содержит URL-шаблон
    :type handlers: list
    :param settings: словарь настроек приложения
    :type settings: dict
    """
    def __init__(self):
        handlers = [
           (r"/", MainHandler),
           (r"/appeal", AppealHandler),
        ]
        settings = dict(
            title=u"Tornado backend",
            template_path=os.path.join(os.path.dirname(__file__), "../frontend"),
            # static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            cookie_secret=uuid.uuid4().int,
            debug=False,
        )
        super(Application, self).__init__(handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    """
    Обработчик запросов для главной страницы веб-приложения.
    """
    async def get(self) -> NoReturn:
        self.render("index.html", error_name=None)


class AppealHandler(tornado.web.RequestHandler):
    """
    Обработчик запросов для страницы
    отправки обращений в rabbitmq
    """
    def post(self) -> NoReturn:
        surname = self.get_argument("surname", default=None, strip=False)
        name = self.get_argument("name", default=None, strip=False)
        patronymic = self.get_argument("patronymic", default=None, strip=False)
        phone_number = self.get_argument("phone_number", default=None, strip=False)
        appeal_text = self.get_argument("appeal_text", default=None, strip=False)

        appeal_dict = dict()
        try:
            for el in ('surname', 'name', 'patronymic', 'phone_number', 'appeal_text'):
                appeal_dict[el] = locals()[el]
            send_rabbitmq(json.dumps(appeal_dict))
            self.render("index.html", error_name='Обращение отправлено!')
        except Exception as err:
            self.render("index.html", error_name="Невалидные данные. Попробуйте ещё раз")


def run_tornado():
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


run_tornado()
