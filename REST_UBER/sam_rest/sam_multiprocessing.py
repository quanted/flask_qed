__author__ = 'jflaisha'

from functools import partial
from concurrent.futures import ProcessPoolExecutor as Pool
import multiprocessing, logging, sys, os, numpy as np

try:
    import superprzm  #  Import superprzm.dll / .so
    _dll_loaded = True
except ImportError, e:
    logging.exception(e)
    _dll_loaded = False

curr_path = os.path.abspath(os.path.dirname(__file__))

class SamModelCaller(object):
    def __init__(self, sam_bin_path, name_temp, number_of_rows_list, no_of_processes=16):

        if _dll_loaded:

            self.sam_bin_path = os.path.join(curr_path, 'bin')
            self.sam_bin_path = sam_bin_path
            self.name_temp = name_temp
            self.number_of_rows_list = number_of_rows_list
            self.no_of_processes = no_of_processes

            self.multiprocessing_setup()


    def multiprocessing_setup(self):
        self.nproc = multiprocessing.cpu_count()  # Get number of processors available on machine
        print "max_workers=%s" % self.nproc
        self.pool = Pool(max_workers = self.nproc)  # Set number of workers to equal the number of processors available on machin


    def sam_multiprocessing(self):

        testing_sections = [308, 308, 308, 308, 308, 308, 308, 308, 308, 308, 308, 308, 308, 308, 308, 330]
        for x in range(self.no_of_processes):  # Loop over all the 'no_of_processes' to fill the process pool
            self.pool.submit(
                self.daily_conc_callable,
                self.name_temp,              # Temporary path name for this SuperPRZM run
                self.two_digit(x),           # Section number, as two digits, of this set of HUCs for the SuperPRZM run
                testing_sections[x]
                #number_of_rows_list[x]  # Number of 'rows'/HUC12s for this section of HUCs for the SuperPRZM run
            ).add_done_callback(
                partial(self.callback_daily)
            )

        # Destroy the Pool object which hosts the processes when the pending Futures objects are finished,
        # but do not wait until all Futures are done to have this function return
        self.pool.shutdown(wait=False)


    def daily_conc_callable(self, name_temp, section, array_size=320):
        # return subprocess.Popen(args).wait()  # Identical to subprocess.call()
        # return subprocess.Popen(args, stdout=subprocess.PIPE).communicate()  # Print FORTRAN output to STDOUT...not used anymore; terrible performance

        return superprzm.runmain.run(self.sam_bin_path, name_temp, section, array_size)  # Run SuperPRZM as DLL

    def callback_daily(future):
        print type(future.result())

    def two_digit(self, x):
        """
        Convert "1" to "01", etc., up to 9.  Value of x has 1 added to it; therefore, a zero-based sequence is expected.
        :param x: int
        :return: String, two digit representation of x + 1 if x < 9
        """
        if x < 9:
            number_string = "0" + str(x + 1)
        else:
            number_string = str(x + 1)

        return number_string


def main():
    # Get command line arguments
    sam_bin_path = sys.argv[1]
    name_temp = sys.argv[2]
    number_of_rows_list = sys.argv[3]
    # 'no_of_processes' is an optional command line argument that defaults to 16 if not given
    try:
        no_of_processes = sys.argv[4]
        sam = SamModelCaller(sam_bin_path, name_temp, number_of_rows_list, no_of_processes)
    except:
        sam = SamModelCaller(sam_bin_path, name_temp, number_of_rows_list)

    sam.sam_multiprocessing()

if __name__ == "__main__":
    main()
