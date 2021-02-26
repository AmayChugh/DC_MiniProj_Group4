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

    df = None
    with protocol.batchContext() as batch:
        batch.request("math.sub", [5, 2])
        batch.request("math.sub", [2, 3])
        batch.request("math.sub", [3, 4])
        batch.request("math.sub", [4, 5])
        df = batch.deferredList(consumeErrors=1)

    result = yield df

    log.debug("difference result: {}".format(result))
    yield result

task.react(main)
