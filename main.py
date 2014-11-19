#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import uuid

from datetime import datetime

import tornado
import tornado.ioloop
import tornado.options
from tornado.log import app_log
from tornado.web import RequestHandler

from tornado import gen, web

class MeatSpaceBaseHandler(RequestHandler):
    '''
    Base request handler for the meatspace tracker
    '''
    @property
    def event_store(self):
        return self.settings['event_store']

class RegistrationHandler(MeatSpaceBaseHandler):
    @gen.coroutine
    def post(self):
        self.write(self.request.arguments)

class EventIDHandler(MeatSpaceBaseHandler):
    @gen.coroutine
    def get(self):
        ip = self.request.remote_ip
        app_log.debug(ip)
        self.write(self.event_store.get_event_id(ip))


class DummyEventStore():
    '''
    DummyEventStore is an initial mock of what we'd want to capture for events.

    TODO: Cull events after expiration time
    TODO: Declare a valid range for an event
    '''

    def __init__(self):
        self.store = {}

    def get_event_id(self, ip):

        if ip not in self.store:
            creation = datetime.utcnow()
            event_id = uuid.uuid5(uuid.NAMESPACE_DNS, ip + str(creation))

            self.store[ip] = {}
            self.store[ip]["created"] = creation
            self.store[ip]["event_id"] = event_id

        return str(self.store[ip]["event_id"])


def main():
    tornado.options.define('port', default=0xbeef, # 48879
        help="port for the main server to listen on"
    )

    static_path = os.path.join(os.path.dirname(__file__), "static")
    template_path = os.path.join(os.path.dirname(__file__), "templates")
   
    tornado.options.parse_command_line()
    opts = tornado.options.options 

    handlers = [
        ("/api/events/", EventIDHandler),
        ("/api/events/register", RegistrationHandler),
    ]

    ioloop = tornado.ioloop.IOLoop().instance()

    settings = dict(
        static_path=static_path,
        cookie_secret=uuid.uuid4(),
        #TODO: Set this back to True
        xsrf_cookies=False,
        debug=True,
        autoescape=None,
        template_path=template_path,
        event_store=DummyEventStore(),
    )

    app_log.info("Listening on {}".format(opts.port))
    application = tornado.web.Application(handlers, **settings)
    application.listen(opts.port)
    ioloop.start()

if __name__ == "__main__":
    main()
