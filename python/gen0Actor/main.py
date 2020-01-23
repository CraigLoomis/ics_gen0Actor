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
        self.gen2keys = dict(TELFOCUS=0.0,
                             INSROT=0.0,
                             AZIMUTH=0.0,
                             ALTITUDE=85.0)
        self.gen2keys['FOC-VAL'] = 0.0
        self.gen2keys['INST-PA'] = 0.0
        self.gen2keys['INR-STR'] = 0.0
        self.gen2keys['ADC-TYPE'] = 'POPT_2'
        self.gen2keys['ADC-STR'] = 0.0

        self.gen2keys['DOM-HUM'] = 30.0
        self.gen2keys['DOM-PRS'] = 450.0
        self.gen2keys['DOM-TMP'] = 10.0
        self.gen2keys['DOM-WND'] = 2.0
        self.gen2keys['OUT-HUM'] = 31.0
        self.gen2keys['OUT-PRS'] = 451.0
        self.gen2keys['OUT-TMP'] = 11.0
        self.gen2keys['OUT-WND'] = 3.0

    def _gen2ActorKeys(self, cmd, doGen2Refresh=False):
        """Generate all gen2 status keys.

        For this actor, this might get called from either the gen2 or the MHS sides.

        Bugs
        ---

        With the current Gen2 keyword table implementation, we do not
        correctly set invalid values to the right type. I think the
        entire mechanism will be changed.

        """

        def gk(name, cmd=cmd):
            return self.gen2keys[name]

        if doGen2Refresh:
            self.gen2.update_header_stat()
        cmd.inform(f'tel_focus={gk("TELFOCUS")},{gk("FOC-VAL")}')
        cmd.inform(f'tel_axes={gk("AZIMUTH")},{gk("ALTITUDE")}')
        cmd.inform(f'tel_rot={gk("INST-PA")},{gk("INR-STR")}')
        cmd.inform(f'tel_adc={gk("ADC-TYPE")},{gk("ADC-STR")}')
        cmd.inform(f'dome_env={gk("DOM-HUM")},{gk("DOM-PRS")},{gk("DOM-TMP")},{gk("DOM-WND")}')
        cmd.inform(f'outside_env={gk("OUT-HUM")},{gk("OUT-PRS")},{gk("OUT-TMP")},{gk("OUT-WND")}')

# To work
def main():
    theActor = OurActor('gen2', productName='gen0Actor')
    theActor.run()

if __name__ == '__main__':
    main()
