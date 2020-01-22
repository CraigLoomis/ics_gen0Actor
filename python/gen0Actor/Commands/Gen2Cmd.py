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
                                                 types.Enum('bias', 'dark', 'arc', 'flat', 'object'),
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
        hdr['GARBAGE'] = True

        hdrString = base64.b64encode(hdr.tostring().encode('latin-1')).decode('latin-1')
        cmd.inform('header=%s' % (repr(hdrString)))
        cmd.finish()
