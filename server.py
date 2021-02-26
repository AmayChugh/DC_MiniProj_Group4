import sys
from twisted import logger
from twisted.internet import reactor
from wsjsonrpc import factory

logobserver = logger.textFileLogObserver(sys.stdout)
logger.globalLogPublisher.addObserver(logobserver)
def _sum(protocol, x, y):
    return x + y
def _diff(protocol, x, y):
    return x - y
def _mult(protocol, x, y):
    return x * y
def _division(protocol, x, y):
    return x / y
if __name__ == "__main__":

    factory = factory.JsonRpcWebSocketServerFactory(u"ws://127.0.0.1:8095/wsjsonrpc")
    factory.registerMethod("math.sum", _sum)
    factory.registerMethod("math.sub", _diff)
    factory.registerMethod("math.mult", _mult)
    factory.registerMethod("math.division", _division)
    reactor.listenTCP(8095, factory)
    reactor.run()
