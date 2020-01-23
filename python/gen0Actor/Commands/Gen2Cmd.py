import base64

import opscore.protocols.keys as keys
import opscore.protocols.types as types
from opscore.utility.qstr import qstr

import astropy.io.fits as pyfits


class Gen2Cmd(object):

    def __init__(self, actor):
        # This lets us access the rest of the actor.
        self.actor = actor

        # Declare the commands we implement. When the actor is started
        # these are registered with the parser, which will call the
        # associated methods when matched. The callbacks will be
        # passed a single argument, the parsed and typed command.
        #
        self.vocab = [
            ('getVisit', '', self.getVisit),
            ('getFitsCards', '<frameId> <expTime> <expType>', self.getFitsCards),
        ]

        # Define typed command arguments for the above commands.
        self.keys = keys.KeysDictionary("core_core", (1, 1),
                                        keys.Key("expType",
                                                 types.Enum('bias', 'dark', 'arc', 'flat',
                                                            'object', 'acquisition'),
                                                 help='exposure type for FITS header'),
                                        keys.Key("expTime", types.Float(),
                                                 help='exposure time'),
                                        keys.Key("frameId", types.String(),
                                                 help='Gen2 frame ID'),
                                        )

    def getVisit(self, cmd):
        visit = self.actor.fileMgr.consumeNextSeqno()
        cmd.finish(f'visit={visit}')

    def getFitsCards(self, cmd):
        """ Query for all TSC and observatory FITS cards. """

        cmdKeys = cmd.cmd.keywords
        frameId = cmdKeys['frameId'].values[0]
        expTime = cmdKeys['expTime'].values[0]
        expType = cmdKeys['expType'].values[0]

        hdr = pyfits.Header()

        hdr['W_GEN2ID'] = 'dummy'
        hdr.set('FRAMEID', frameId, "Image ID")
        if frameId.startswith('PFS'):
            try:
                framenum = frameId[4:]
                visit = int(framenum[:6], base=10)
            except:
                visit = 0
            hdr.set('EXP-ID', '%sE%06d00' % (frameId[:3], visit),
                    "Exposure/visit ID")
            hdr.set('W_VISIT', visit, 'PFS visit')

        # exposure time
        hdr.set('EXPTIME',float(expTime), "[sec] Total integration time of the frame")
        hdr.set('DATA-TYP', expType.upper(), "Subaru-style exp. type")

        hdrString = base64.b64encode(hdr.tostring().encode('latin-1')).decode('latin-1')
        cmd.inform('header=%s' % (repr(hdrString)))
        cmd.finish()
