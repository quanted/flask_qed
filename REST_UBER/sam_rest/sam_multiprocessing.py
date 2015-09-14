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
    nproc = multiprocessing.cpu_count()  # Get number of processors available on machine
    print "max_workers=%s" % nproc
    return Pool(max_workers = nproc)  # Set number of workers to equal the number of processors available on machine


class SamModelCaller(object):
    def __init__(self, name_temp, number_of_rows_list, no_of_processes=16):

        # if _dll_loaded:

        self.sam_bin_path = os.path.join(curr_path, 'bin')
        self.name_temp = name_temp
        self.number_of_rows_list = number_of_rows_list
        self.no_of_processes = no_of_processes


    def sam_multiprocessing(self):

        # global pool
        # if pool is None:
        #     pool = multiprocessing_setup()

        try:
            if pool is None:
                pass
        except NameError:
            pool = multiprocessing_setup()

        testing_sections = [308, 308, 308, 308, 308, 308, 308, 308, 308, 308, 308, 308, 308, 308, 308, 330]
        for x in range(self.no_of_processes):  # Loop over all the 'no_of_processes' to fill the process pool
            pool.submit(
                daily_conc_callable,
                self.sam_bin_path,
                self.name_temp,              # Temporary path name for this SuperPRZM run
                self.two_digit(x),           # Section number, as two digits, of this set of HUCs for the SuperPRZM run
                # testing_sections[x]
                self.number_of_rows_list[x]  # Number of 'rows'/HUC12s for this section of HUCs for the SuperPRZM run
            ).add_done_callback(
                callback_daily
                #partial(callback_daily, self.two_digit(x))
            )

        # Destroy the Pool object which hosts the processes when the pending Futures objects are finished,
        # but do not wait until all Futures are done to have this function return
        pool.shutdown(wait=False)  # Non-blocking
        #pool.shutdown()  # Blocking


    def split_csv(self, number, name_temp):
        """
        Load master CSV for SuperPRZM run as Pandas DataFrame and slice it
        based on the number of Futures objects created to execute it.
        (Currently Fortran is set to accept only a 1 char digit; therefore,
        the max number here is 9)
        :param number: int (1 - 9)
        :param curr_path: String; absolute path to this module
        :return: None
        """

        print "number = ", number
        import pandas as pd
        df = pd.read_csv(os.path.join(
            self.sam_bin_path, 'EcoRecipes_huc12', 'recipe_combos2012', 'huc12_outlets_metric.csv'
        ))

        if number > 99:
            number = 99
        if number < 1:
            number = 1

        try:
            rows_per_sect = df.shape[0] / number
            print rows_per_sect
            print type(rows_per_sect)
        except:
            number = 1
            rows_per_sect = df.shape[0] / number

        os.makedirs(os.path.join(self.sam_bin_path, name_temp, 'EcoRecipes_huc12', 'recipe_combos2012'))

        number_of_rows_list = []
        i = 1
        while i <= number:
            if i == 1:
                print 1
                # First slice
                df_slice = df[:rows_per_sect]
            elif i == number:
                print str(i) + " (last)"
                # End slice: slice to the end of the DataFrame
                df_slice = df[((i - 1) * rows_per_sect):]
            else:
                print i
                # Middle slices (not first or last)
                df_slice = df[((i - 1) * rows_per_sect):i * rows_per_sect]

            number_of_rows_list.append(len(df_slice))  # Save the number of rows for each CSV to be passed to SuperPRZM
            df_slice.to_csv(os.path.join(
                self.sam_bin_path, name_temp, 'EcoRecipes_huc12', 'recipe_combos2012', 'huc12_outlets_metric_' + self.two_digit(i - 1) + '.csv'
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
        sam_callable.run(sam_bin_path, name_temp, section, array_size)
    except Exception, e:
        mp_logger.exception(e)


def callback_daily(section, future):
    print "Section: ", section
    # print future.result()


def main():

    # Get command line arguments
    name_temp = sys.argv[1]
    number_of_rows_list = sys.argv[2]
    # 'no_of_processes' is an optional command line argument that defaults to 16 if not given
    try:
        no_of_processes = sys.argv[3]
        sam = SamModelCaller(name_temp, number_of_rows_list, no_of_processes)
    except:
        sam = SamModelCaller(name_temp, number_of_rows_list)

    sam.sam_multiprocessing()

if __name__ == "__main__":
    # Create Process Pool
    pool = multiprocessing_setup()
    main()
    sys.exit()
