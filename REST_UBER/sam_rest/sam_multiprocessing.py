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


mp_logger = multiprocessing.log_to_stderr()

def multiprocessing_setup():
    """
    Create the ProcessPoolExecutor object with the max number of concurrent workers equal to the number of cores of the
    machine running this script.
    :return: ProcessPoolExecutor object reference
    """
    nproc = multiprocessing.cpu_count()  # Get number of processors available on machine
    print "max_workers=%s" % nproc
    return Pool(max_workers = nproc)  # Set number of workers to equal the number of processors available on machine


class SamModelCaller(object):
    def __init__(self, name_temp, number_of_rows_list=None, no_of_processes=16):
        """
        Constructor for SamModelCaller class.
        :param name_temp: string
        :param number_of_rows_list: list
        :param no_of_processes: int
        """

        self.sam_bin_path = os.path.join(curr_path, 'bin')
        self.name_temp = name_temp
        self.number_of_rows_list = number_of_rows_list
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

        if self.number_of_rows_list is None \
                or type(self.number_of_rows_list) is not 'list':
            self.number_of_rows_list = self.split_csv()

        testing_sections = [308, 308, 308, 308, 308, 308, 308, 308, 308, 308, 308, 308, 308, 308, 308, 330]  # Temporary for testing
        for x in range(self.no_of_processes):  # Loop over all the 'no_of_processes' to fill the process pool
            pool.submit(
                # subprocess.Popen, "sleep 3"  # Testing
                daily_conc_callable,
                self.sam_bin_path,           # Absolute path to the SAM bin folder
                self.name_temp,              # Temporary path name for this SuperPRZM run
                self.two_digit(x),           # Section number, as two digits, of this set of HUCs for the SuperPRZM run
                # testing_sections[x]
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
            self.sam_bin_path, 'EcoRecipes_huc12', 'recipe_combos2012', 'huc12_outlets_metric.csv'
        ))

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


def daily_conc_callable(sam_bin_path, name_temp, section, array_size=320):
    # return subprocess.Popen(args).wait()  # Identical to subprocess.call()
    # return subprocess.Popen(args, stdout=subprocess.PIPE).communicate()  # Print FORTRAN output to STDOUT...not used anymore; terrible performance

    #return superprzm.runmain.run(sam_bin_path, name_temp, section, array_size)  # Run SuperPRZM as DLL

    import sam_callable

    try:
        sam_callable.run(sam_bin_path, name_temp, section, int(array_size))
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
    name_temp = sys.argv[1]
    try:  # 'number_of_rows_list' is an optional command line argument that is calculated if not given (split_csv() called)
        number_of_rows_list = sys.argv[2]
        # if isinstance(self.number_of_rows_list, str):
        number_of_rows_list = create_number_of_rows_list(number_of_rows_list)
        for item in number_of_rows_list:
            int(item)
    except ValueError:  # If the string is none int
        number_of_rows_list = None
    except IndexError:  # If the command-line argument is not supplied
        number_of_rows_list = None
    try:  # 'no_of_processes' is an optional command line argument that defaults to 16 if not given
        no_of_processes = int(sys.argv[3])
        sam = SamModelCaller(name_temp, number_of_rows_list, no_of_processes)
    except:
        sam = SamModelCaller(name_temp, number_of_rows_list)

    sam.sam_multiprocessing()

if __name__ == "__main__":
    # Create Process Pool
    pool = multiprocessing_setup()
    main()
    sys.exit()
