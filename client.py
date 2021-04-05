import sys

from twisted import logger
from twisted.internet import defer
from twisted.internet import task

from wsjsonrpc import factory

logobserver = logger.textFileLogObserver(sys.stdout) #(Type: Function)Create a FileLogObserver(Type: Class Log observer that writes to a file-like object) that emits text to a specified (writable) file-like object
logger.globalLogPublisher.addObserver(logobserver) #The LogPublisher that all Logger instances that are not otherwise parameterized will point to by default. (type: LogPublisher)
log = logger.Logger() #A Logger emits log messages to an observer. You should instantiate it as a class or module attribute

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

    log.debug("result: {}".format(result))
    yield result

task.react(main)
