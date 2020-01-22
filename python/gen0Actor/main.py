#!/usr/bin/env python3

import actorcore.Actor

import SeqPath

class OurActor(actorcore.Actor.Actor):
    def __init__(self, name,
                 productName=None, configFile=None,
                 modelNames=(),
                 debugLevel=30):

        """ Setup an Actor instance. See help for actorcore.Actor for details. """
        
        # This sets up the connections to/from the hub, the logger, and the twisted reactor.
        #
        actorcore.Actor.Actor.__init__(self, name, 
                                       productName=productName, 
                                       configFile=configFile,
                                       modelNames=modelNames)

        baseTemplate = '%(filePrefix)%(seqno)08d'
        site = 'A'
        self.fileMgr = SeqPath.NightFilenameGen('/data/mcs',
                                                filePrefix='PF%sC' % (site),
                                                filePattern="%s.fits" % (baseTemplate))

#
# To work
def main():
    theActor = OurActor('gen2', productName='gen0Actor')
    theActor.run()

if __name__ == '__main__':
    main()