# tbd
import os
from Preprocessing.utilities import NHDTable


def examine_navigator(region, navigator_path=r"..\bin\Preprocessed\Navigators\region_{}.npz"):
    from Tool.functions import Navigator

    # Initialize navigator object
    nav = Navigator(region, navigator_path)

    # Test navigator object
    reaches, times, warning = nav.upstream_watershed(5641230)
    print(reaches)
    print(times)

    print(reaches.size)

    print(warning)


def main():
    examine_navigator('07')

main()