import sys

from twisted import logger
from twisted.internet import defer
from twisted.internet import task

from wsjsonrpc import factory

logobserver = logger.textFileLogObserver(sys.stdout)
logger.globalLogPublisher.addObserver(logobserver)
log = logger.Logger()

@defer.inlineCallbacks
def main(reactor):

    protocol = yield factory.get_client(hostname="localhost", port=8095, path=u"wsjsonrpc")
    a = int(input())
    b = int(input())
    df = None
    with protocol.batchContext() as batch:
        batch.request("math.sum", [a, b])
        batch.request("math.sub", [a, b])
        batch.request("math.mult", [a, b])
        batch.request("math.division", [a, b])
        df = batch.deferredList(consumeErrors=1)

    result = yield df

    log.debug("sum result: {}".format(result))
    yield result

task.react(main)
