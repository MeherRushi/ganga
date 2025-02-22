

from GangaCore.testlib.GangaUnitTest import GangaUnitTest


class TestSavannah13406(GangaUnitTest):

    def test_Savannah13406(self):
        #from GangaCore.GPI import config
        #config['Configuration']['autoGenerateJobWorkspace'] = True

        import os

        from GangaCore.GPI import Job, jobs
        jobs.remove()
        j = Job()
        j.submit()  # Needed in order to create the workspace
        self.assertTrue(os.path.exists(j.inputdir + '/../..'))
        jobs.remove()
        # Check is repository/Local or repository/Remote still exists
        self.assertTrue(os.path.exists(os.path.abspath(j.inputdir + '/../..')))
