.SUFFIXES: .exe .o .mod .f90 .f95 .f .f9x .res .rc .rcx

# Fortran preprocessor name: xcoco
# Options:
#    -x :: Read _xcoco.ini
#    -S :: supress final setfile message
# fpp = xcoco
# fpp_opts = -x -S
fpp =
fpp_opts =

# FC = lf95
FC = gfortran44

# Lf95 flags
# -dbl -- extend all single precision real items to double precision
# -in -- "Implicit None"
# -info -- variables declared and not used, other stuff
# -nchk -- no checks
# -nconcc -- turn off Fortran carriage control processing for console I/O.
# -pause -- pause after the program terminates
# -wo -- warn obsolescent f90
# -xref -- generate cross-reference information (stored in *.lst)
# XREF = -xref # -info
XREF = -g # -info

# Debug: Compile and link flags
DEBUGcf = -chk -g -pca -stchk -trace -w -winconsole

# OPTIMIZE: Compile and link flags
OPTIMIZEcf = -nap -nchk -ndal -ng -o1 -npca -ntrace -nsav -nstchk -nw

SRC_Path =
ModuleList = 

f95flags =
ldflags =

# [production options]
# f95flags = -in -zero $(XREF) #-info
f95flags = $(XREF)

# Rules:
.f90 :
        $(fpp) $(fpp_opts)  $@ $<


f90code = 	PesticideInputs.f90 \
			Variables.f90 \
			Utilities.f90 \
			Pesticide_Application_Module.f90 \
			Output.f90 \
			MthExceed.f90 \
			Transport.f90 \
			CheckForErrors.f90 \
			ThirtyDayAvg.f90 \
			AnnExceed.f90 \
			ReadScenarios.f90 \
			WaterBodyConc.f90 \
			MainPesticideCalculator.f90

targets : SuperPRZMpesticide.exe

SuperPRZMpesticide.exe : $(f90code) 
	$(FC) $(ldflags) -o $@ $(f90code)

# -ffixed-line-length-0
#End-of-File Makefile

clean:
	rm -f *.mod SuperPRZMpesticide.exe

