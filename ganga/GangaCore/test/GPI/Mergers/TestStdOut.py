

import os
import tempfile

from GangaCore.testlib.GangaUnitTest import GangaUnitTest
from GangaCore.testlib.monitoring import run_until_completed


class TestStdOut(GangaUnitTest):
    def setUp(self):
        super(TestStdOut, self).setUp()
        from GangaCore.GPI import (Executable, File, Job, Local, LocalFile,
                                   config)
        from GangaTest.Framework.utils import write_file

        config['Mergers']['associate'] = {'stdout': 'RootMerger'}

        self.jobslice = []
        self.file_name = 'id_echo.sh'

        for i in range(2):

            j = Job(application=Executable(), backend=Local())

            scriptString = '''
            #!/bin/sh
            echo "Output from job $1." > out.txt
            echo "Output from job $2." > out2.txt
            '''

            # write string to tmpfile
            tmpdir = tempfile.mktemp()
            os.mkdir(tmpdir)
            fileName = os.path.join(tmpdir, self.file_name)

            write_file(fileName, scriptString)

            j.application.exe = 'sh'
            j.application.args = [File(fileName), str(j.id), str(j.id * 10)]
            j.outputfiles = [LocalFile('out.txt'), LocalFile('out2.txt')]
            self.jobslice.append(j)

    def runJobSlice(self):
        for j in self.jobslice:
            j.submit()
            assert run_until_completed(j, timeout=60), 'Timeout on job submission: job is still not finished'

    def testCanSetStdOutMerge(self):
        from GangaCore.GPI import SmartMerger
        from GangaCore.GPIDev.Adapters.IPostProcessor import \
            PostProcessException

        self.runJobSlice()

        tmpdir = tempfile.mktemp()
        os.mkdir(tmpdir)

        sm = SmartMerger()
        sm.files = ['stdout']
        try:
            assert not sm.merge(self.jobslice, tmpdir)
        except PostProcessException:
            pass
