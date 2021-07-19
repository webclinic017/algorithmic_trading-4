import queue
from loguru import logger
from market.market import Market
from holdings.portfolio import Portfolio, Transaction


class EventHandler:
    def __init__(self,
                 market: Market,
                 pf: Portfolio):
        self.event_queue = queue.Queue()
        self.market = market
        self.pf = pf

    def put_event(self,
                  event):
        self.event_queue.put(event)

    def get_event(self):
        return self.event_queue.get()

    def is_empty(self):
        return self.event_queue.empty()

    def handle_event(self,
                     verbose=False):
        e = self.get_event()
        if e.type == 'MARKET':
            self.pf.update_all_market_values(date=e.date,
                                             market_data=self.market)
            if verbose:
                logger.info(e.details)

        elif e.type == 'TRANSACTION':
            self.pf.transact_security(trans=e.trans)
            if verbose:
                logger.info(e.details)