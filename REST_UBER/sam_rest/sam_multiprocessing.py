__author__ = 'jflaisha'

from functools import partial
from concurrent.futures import ProcessPoolExecutor as Pool
import multiprocessing, logging, sys, os, numpy as np
import sam_callable

try:
    import superprzm  # Import superprzm.dll / .so
    _dll_loaded = True
except ImportError, e:
    logging.exception(e)
    _dll_loaded = False

curr_path = os.path.abspath(os.path.dirname(__file__))

mp_logger = multiprocessing.log_to_stderr()

def multiprocessing_setup():
    """
    Create the ProcessPoolExecutor object with the max number of concurrent workers equal to the number of cores of the
    machine running this script.
    :return: ProcessPoolExecutor object reference
    """
    nproc = multiprocessing.cpu_count()  # Get number of processors available on machine
    if nproc > 16:  # Force 'nproc' to be 16
        nproc = 16
    try:
        host_name = os.uname()[1]
        if host_name == 'ord-uber-vm005':  # Force Server 5 to use 16 processes to avoid the memdump error when using a process pool with less max_workers than total number of processes
            nproc = 16
    except:
        pass
    print "max_workers=%s" % nproc
    return Pool(max_workers = nproc)  # Set number of workers to equal the number of processors available on machine


class SamModelCaller(object):
    def __init__(self, jid, name_temp, no_of_processes=16):
        """
        Constructor for SamModelCaller class.
        :param name_temp: string
        :param number_of_rows_list: list
        :param no_of_processes: int
        """

        self.sam_bin_path = os.path.join(curr_path, 'bin')
        print self.sam_bin_path
        self.jid = jid
        self.name_temp = name_temp
        self.no_of_processes = no_of_processes

    def sam_multiprocessing(self):
        """
        Submits jobs (SAM runs) to the worker pool.
        """

        try:
            import subprocess32 as subprocess    # Use subprocess32 for Linux (Python 3.2 backport)
        except ImportError:
            import subprocess

        try:  # Ensure that the ProcessPoolExecutor object has been instantiated
            if pool is None:
                pass  # 'pool' is already defined by multiprocessing_setup()
        except NameError:
            pool = multiprocessing_setup()

        # Split master HUC CSV into sections and return a list containing the number of rows in each section (sequentially)
        try:
            self.number_of_rows_list = self.split_csv()
        except:
            print "Split CSV failed"
            self.number_of_rows_list = [306, 306, 306, 306, 306, 306, 306, 306, 306, 306, 306, 306, 306, 306, 306, 320]

        for x in range(self.no_of_processes):  # Loop over all the 'no_of_processes' to fill the process
            pool.submit(
                daily_conc_callable,
                self.jid,                    # 'jid' of SAM run
                self.sam_bin_path,           # Absolute path to the SAM bin folder
                self.name_temp,              # Temporary path name for this SuperPRZM run
                self.two_digit(x),           # Section number, as two digits, of this set of HUCs for the SuperPRZM run
                self.number_of_rows_list[x]  # Number of 'rows'/HUC12s for this section of HUCs for the SuperPRZM run
            ).add_done_callback(
                partial(callback_daily, self.two_digit(x))
            )

        # Destroy the Pool object which hosts the processes when the pending Futures objects are finished,
        # but do not wait until all Futures are done to have this function return
        # pool.shutdown(wait=False)  # Non-blocking
        pool.shutdown()  # Blocking

    def split_csv(self):
        """
        Load master CSV for SuperPRZM run as Pandas DataFrame and slice it
        based on the number of Futures objects created to execute it.
        (Currently Fortran is set to accept only a 1 char digit; therefore,
        the max number here is 9)
        :param number: int (1 - 9)
        :param curr_path: String; absolute path to this module
        :return: list; list with length equal number of csv sections, where each index is number of rows in section
        """

        print "number = ", self.no_of_processes
        import pandas as pd
        df = pd.read_csv(os.path.join(
            self.sam_bin_path, 'EcoRecipes_huc12', 'recipe_combos2012', 'huc12_outlets_metric.csv'),
            dtype={'HUC_12': object, 'COMID': object}  # Set columns 'HUC_12' & 'COMID' to 'object' (~eq. to string)
        )                                              # This preserves any leading zeros present in the HUC12_IDs

        if self.no_of_processes > 99:
            self.no_of_processes = 99
        if self.no_of_processes < 1:
            self.no_of_processes = 1

        try:
            rows_per_sect = df.shape[0] / self.no_of_processes
            print rows_per_sect
            print type(rows_per_sect)
        except:
            self.no_of_processes = 1
            rows_per_sect = df.shape[0] / self.no_of_processes

        os.makedirs(os.path.join(self.sam_bin_path, self.name_temp, 'EcoRecipes_huc12', 'recipe_combos2012'))

        number_of_rows_list = []
        i = 1
        while i <= self.no_of_processes:
            if i == 1:
                print 1
                # First slice
                df_slice = df[:rows_per_sect]
            elif i == self.no_of_processes:
                print str(i) + " (last)"
                # End slice: slice to the end of the DataFrame
                df_slice = df[((i - 1) * rows_per_sect):]
            else:
                print i
                # Middle slices (not first or last)
                df_slice = df[((i - 1) * rows_per_sect):i * rows_per_sect]

            number_of_rows_list.append(len(df_slice))  # Save the number of rows for each CSV to be passed to SuperPRZM
            df_slice.to_csv(os.path.join(
                self.sam_bin_path, self.name_temp, 'EcoRecipes_huc12',
                'recipe_combos2012', 'huc12_outlets_metric_' + self.two_digit(i - 1) + '.csv'
            ), index=False)

            i += 1

        return number_of_rows_list

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


def daily_conc_callable(jid, sam_bin_path, name_temp, section, array_size=320):
    """

    :param jid:
    :param sam_bin_path:
    :param name_temp:
    :param section:
    :param array_size:
    :return:
    """

    #TODO: Remove these; left to show how it was previously done while testing callable
    # return subprocess.Popen(args).wait()  # Identical to subprocess.call()
    # return subprocess.Popen(args, stdout=subprocess.PIPE).communicate()  # Print FORTRAN output to STDOUT...not used anymore; terrible performance

    try:
        sam_callable.run(jid, sam_bin_path, name_temp, section, int(array_size))
    except Exception, e:
        mp_logger.exception(e)


def callback_daily(section, future):
    print "Section: ", section
    # print future.result()

def create_number_of_rows_list(list_string):
    return list_string.split()

def main():
    """
    When run from command line this script takes 1 mandatory arguments and 2 optional arguments.
    Mandatory arg: name_temp, string.  Random 6 character string for run to generate temporary run directory.
    Optional args: number_of_rows_list, list.  If using a dataset that has already been processed by the split_csv()
                       method, this is a list with a length equal to the number of csv sections created (which is equal
                       to the number of workers).  Each item in the list is the number of rows in that csv section,
                       sequentially, where index 0 is the 1st csv section.
                   no_of_processes, int.  Total number of processes that will be used to complete the run.  This is also
                       equal to the number of sections the csv will be dividing into and the length of the
                       number_of_rows_list optional argument.
    :return:
    """

    # Get command line arguments
    jid = sys.argv[1]
    name_temp = sys.argv[2]
    if len(sys.argv) == 4:  # 'no_of_processes' is an optional command line argument that defaults to 16 if not given
        no_of_processes = int(sys.argv[3])
        sam = SamModelCaller(jid, name_temp, no_of_processes)
    else:
        sam = SamModelCaller(jid, name_temp)

    sam.sam_multiprocessing()

if __name__ == "__main__":
    # Create Process Pool
    pool = multiprocessing_setup()
    main()
    sys.exit()