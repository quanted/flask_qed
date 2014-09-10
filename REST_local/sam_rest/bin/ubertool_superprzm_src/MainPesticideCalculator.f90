program PesticideCalculator
   use Variables !, ONLY: appdate, appnumrec, napps, appMethod, appDepth, koc, Soil_HalfLife, cropdesired,totalApplied, &
                       !Scenario_Path, recipe_name, RecipePath,DwRecipepath,EcoRecipepath,area,pesticide_applied, &
                       !Hydropath,DwHydropath,EcoHydropath,Flowpath,EcoFlowpath,DwFlowpath,Outpath,DwROutPath,DwFOutPath,EcoOutPath,&
                       !eco_or_dw,Scenario_Path,appMass,Number_crop_ids, ndates, start_count, startjul, endjul, DwRecipepath, &
                       !num_records,juliandates,sdates,totalarea,Total_Runoff, dailyApplied, crop, mukey, &
                       !Total_Runoff_Mass,degradation_aqueous,degradation_sorbed,objID,dummy,xarea,vol,flow  
   use transport
   use pesticide_application_module
   use output
   use ReadScenarioFiles
   use WaterBodyConc
   use AnnExceed
   use MthExceed
   use ThirtyDayAvgConc
   use Utilities
   
   implicit none
   character(len=100) :: inputFile         !Watershed Recipe input file
   character(len=100) :: inputFileHydro    !Watershed Hydrology input file
   character(len=100) :: inputFileFlow     !Flow Volumes input file
   
   real               :: t1,t2
   integer            :: count1, count2
   !integer            :: crop           !Crop Number that is read from the file name
   integer            :: start, last, lastm    !index used to locate crop number in file name 
   integer            :: io_status, ieof, ierror, status
   character(len=100) :: filename, scenariofilename
   integer            :: random_int, random  !For random # generation of CDL years - mmf 7/2014

   integer :: i,count,fullcount,j,k,kk,t,tk

   character(len=256) :: message   
   logical :: hydro_only
   
   integer:: badscenario
   integer :: count_rate

   character(len=100) :: filename_jon
   character(len=100) :: sam_input_file
   logical :: have_file

   
   sam_input_file = "SAM.inp"
   write(*,9200) trim(sam_input_file)
   9200 format ("##### sam_input_file---", ">>", a, "<<")
   call cpu_time (t1)  
   call SYSTEM_CLOCK(count1)

   !Read Chemical Inputs and get Scenario Files
     !Read inputFile and eco_or_dw from SAM.inp (created by SAMv1.vb)
   open (UNIT=39, FILE=sam_input_file,IOSTAT=ierror, STATUS = 'OLD')
   
   !open (UNIT=39, FILE=trim(adjustl("..\..\SAM.inp")),IOSTAT=ierror, STATUS = 'OLD')
   read(39,*,IOSTAT=io_status) eco_or_dw     !Line 1; old- inputFile,
   write (*, 9300) "eco_or_dw", Trim(eco_or_dw)
   9300 Format ("-------", a, ">>", a ,"<<")

   !call get_command_argument(1,inputFile)  !files.txt for eco and dw
   !call get_command_argument(2, eco_or_dw) 
         
   

   
   !THESE CHEMICAL/RECIPE PROPERTIES ARE ENTERED IN GUI & READ IN FROM "SAM.inp"
   read (39,*) start_count                    !Line 2; num_record of simulation start date, since 1/1/1948
   read (39,*) startjul                       !Line 3; Simulation Start Julian date
   read (39,*) endjul                         !Line 4; Simulation End Julian date
   read (39,*) ndates                         !Line 5; Total # days in simulation
   read (39,*) (juliandates(i), i=1,ndates)   !Line 6; Julian dates of simulation days
   read (39,*) (sdates(i), i=1,ndates)        !Line 7; Actual date strings
   read (39,*)                                !Line 8; Chemical name
   read (39,*) Number_crop_ids                !Line 9; Total # crops
   read (39,*) cropdesired(1:Number_crop_ids) !Line 10; Crop IDs
   read (39,*) Koc                            !Line 11; Koc, read as mL/g
   read (39,*) Soil_HalfLife                  !Line 12; Soil half life
   read (39,*) napps                          !Line 13; Total # applications
   read (39,*) (appnumrec(i),i=1,napps)       !Line 14; Application num_record
   read (39,*) (appdate(i), i=1,napps)        !Line 15; Application dates (Julian format)
   read (39,*) (appmass(i), i=1,napps)        !Line 16; Mass of each application (read as kg/ha, coverted to kg/m2 below)
   read (39,*) (appMethod(i), i=1,napps)      !Line 17; Application method (1=ground,...)
   read (39,*) outputtype                     !Line 18; Output type (1=ToxExd,2=30dMax,3=Daily)
   read (39,*) toxthreshold                   !Line 19; Output tox threshold level (30d or ann)
   read (39,*) toxthrestype                   !Line 20; Output tox thres type (1=30d,2=ann)
   read (39,*) outputformat                   !Line 21; Output format (1=table,2=map)
   read (39,*) DwRecipepath                   !Line 22; Path to DwRecipes
   filename_jon = "Bad_Scenarios.txt"
   filename_jon = trim(DwRecipepath)//filename_jon
   write (*,9100)  Trim(filename_jon)
   9100 format ("##### filename_jon---", ">>", a, "<<")

   !call randomf(1,5,random)
   !random_int = random
   open (unit=97, file="recipe.txt")
   write (97,*) trim(adjustl(recipePath))
   print *, trim(adjustl(recipePath))
   open(UNIT=61, FILE=filename_jon)
   !open(UNIT=61, FILE=trim(adjustl(recipePath))//trim("Bad_Scenarios.txt")
   !open(UNIT=61, FILE=trim(adjustl(recipePath))//"CDL_"//trim(str(random_int))//"Bad_Scenarios.txt")
   open(UNIT=86, FILE=trim(adjustl(Flowpath))//trim(adjustl(inputFileFlow)),IOSTAT=ierror, STATUS = 'OLD')
   
   !UNIT 13 - Old input file (files.txt) contains chemical properties, applications, and the scenarios that are associated with the watershed
   !open (UNIT=13, FILE=trim(adjustl(recipePath))//trim(adjustl(inputFile)),IOSTAT=ierror, STATUS = 'OLD') !NOT SURE IF NEEDED!!
    
   if (eco_or_dw == "eco") then
     write (*,*) "ECO"
     recipePath = EcoRecipePath 
     Hydropath = EcoHydropath
     Flowpath = EcoFlowpath
     outpath    = EcoOutPath
     inputFileFlow = "huc12_outlets_metric.csv"  !"EcoMon_flowdata_TabDelim.txt"  !For Eco Flow txt file
   else if (eco_or_dw == "dwr") then
     write (*,*) "DWR"
     recipePath = DwRecipePath 
     Hydropath = DwHydropath
     Flowpath = DwFlowpath
     outpath    = DwROutPath
     inputFileFlow = "DWI_Monthly_Flows_Reservoir_Only_metric_1838.csv"   !For DW Reservoirs txt file
   else if (eco_or_dw == "dwf") then
     write (*,*) "DWF"
     recipePath = DwRecipePath 
     Hydropath = DwHydropath
     Flowpath = DwFlowpath
     outpath    = DwFOutPath
     inputFileFlow = "DWI_Monthly_Flows_Flowing_Only_metric.csv"     !For DW Flowing txt file
   
   end if

   appmass = appmass/10000.                   !convert applied Mass to kg/m2
   degradation_aqueous = 0.693/Soil_HalfLife  !per day
   degradation_sorbed = degradation_aqueous   !per day (Same Rate in Soil & Surface water (See Handbook of Env. Degradation Rates by Philip Howard, 1991)
   koc = koc/1000.                            !Now in m3/kg
    
   Loop_B : do    !This loop reads in each recipe_name
         Total_Runoff_Mass = 0.0
         Total_Leach_Mass = 0.0  !Added to track leached mass for tile drainage - mmf 4/2014
         totalApplied = 0.0
         
   !Read recipe_name - from inputFileFlow for Eco and DW
   if (eco_or_dw == "eco") then
       !read (86,*)
       read (86,*,IOSTAT=io_status) recipe_name,dummy,flow1,flow2,flow3,flow4,flow5,flow6,flow7,flow8,flow9,flow10,flow11,&
              flow12,v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,xa1,xa2,xa3,xa4,xa5,xa6,xa7,xa8,xa9,xa10,xa11,xa12
       if (is_iostat_end(io_status))  exit Loop_B  !End of File
       inputFileHydro = trim(adjustl(recipe_name)) // "_hydro.txt" !For EcoOutput txt files
   else if (eco_or_dw == "dwr") then
       !read (86,*)
       read (86,*,IOSTAT=io_status) recipe_name,vol,dummy,dummy,flow1,flow2,flow3,flow4,flow5,flow6,flow7,flow8,flow9,flow10,&
              flow11,flow12,v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,xa1,xa2,xa3,xa4,xa5,xa6,xa7,xa8,xa9,xa10,xa11,xa12    !vol here only for DW reservoirs
       if (is_iostat_end(io_status))  exit Loop_B  !End of File
       inputFileHydro = trim(adjustl(recipe_name)) // "_hydro.txt"   !For dwOutput txt files
   else if (eco_or_dw == "dwf") then
       read (86,*,IOSTAT=io_status) recipe_name,dummy,dummy,dummy,flow1,flow2,flow3,flow4,flow5,flow6,flow7,flow8,flow9,flow10,&
                flow11,flow12,v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,xa1,xa2,xa3,xa4,xa5,xa6,xa7,xa8,xa9,xa10,xa11,xa12  
       write (*,*) recipe_name
       if (is_iostat_end(io_status))  exit Loop_B  !End of File
       inputFileHydro = trim(adjustl(recipe_name)) // "_hydro.txt"   !For dwOutput txt files
   end if
 
!REVISE - ONLY READ IN DATES BETWEEN START & END DATES, NOT ALL NUM_RECORDS - but hydro pre-processed files have all num_records, so just adjust date range when writing output                          
       !Read UNIT 74, which is Watershed Hydrology input file
         open(UNIT=74, FILE=trim(adjustl(Hydropath))//trim(adjustl(inputFileHydro)),IOSTAT=ierror, STATUS = 'OLD')
         read (74,*,IOSTAT=io_status) num_records, totalarea   !num_records = # days in 65 yrs (23742 d)
         !do j = 1,num_records
         do j=1, start_count-1
             read(74,*,IOSTAT=io_status)
         end do
         do j = start_count,start_count+ndates-1
           read (74,*,IOSTAT=io_status) Total_Runoff(j)        !m3, Daily Runoff Volume
           !write(*,*) Total_Runoff(j)
           !pause
         end do
         
         !call randomf(1,5,random)
         !random_int = random   
         !write(*,*) trim(adjustl(recipepath))//trim(adjustl(recipe_name))
         if (eco_or_dw == "eco") then   !For Eco Basins
             open (UNIT=21, FILE=trim(adjustl(recipepath))//"HUC_"//trim(adjustl(recipe_name))//"_recipe.txt",IOSTAT=ierror, &
                    STATUS = 'OLD')
             !open (UNIT=21, FILE=trim(adjustl(recipepath))//"CDL_"//trim(str(random_int))//"HUC_"//trim(adjustl(recipe_name))//"_recipe.txt",IOSTAT=ierror, STATUS = 'OLD')
         else     !For DW Basins
             open (UNIT=21, FILE=trim(adjustl(recipepath))//"R5_DWI_"//trim(adjustl(recipe_name))//"_recipe.txt",IOSTAT=ierror, &
                    STATUS = 'OLD')
             !open (UNIT=21, FILE=trim(adjustl(recipepath))//"CDL_"//trim(str(random_int))//"DWI_"//trim(adjustl(recipe_name))//"_recipe.txt",IOSTAT=ierror, STATUS = 'OLD')
         end if 
         
             if (ierror /= 0)  then
                   cycle Loop_B
               end if 
   
         fullcount = 0
         count=0
         Loop_A : do 
                   read (21,*, IOSTAT = ierror) filename, area  !area is in m2
                        !write(*,*) recipe_name, filename, area
                   if (is_iostat_end(ierror))  exit Loop_A   !End of File
                                     
                   !This gets the crop code and assigns it to the variable named CROP
                   !**********************************************
                   start = index(filename,"_")+1
                   last = len_trim(filename)
                   read(filename(start: last),*) crop
                   
                   !lastm = start-2
                   !read(filename(1:lastm),*) mukey                    
                   !***********************************************
                   
                   
                   scenariofilename = trim(adjustl(Scenario_Path)) // trim(filename)
         
                   fullcount = fullcount +1  !count all the scenarios in a recipe file
                   if (any(cropdesired(1:Number_crop_ids) == crop )) then
                         count= count+1  !count only the relevant scenarios
                         call Readscenarios (scenariofilename)
               
                         totalApplied = totalApplied + sum(appMass)*area
                         dailyApplied =  sum(appMass)*area
                         !write(*,*) "P1", pesticide_mass_soil(:,1)
        
                         call process_pesticide_applications
                         
                         !write(*,*) "P2", pesticide_mass_soil(:,1)
                         
                         call pesticide_transport
                         
                   else
                       dailyApplied = 0.
                   end if 
                   
                       
                   
         end do Loop_A
         close(21)   !Close the Recipe 
                         
         call waterbody_concentration    !Calculate Pesticide Concentration in Water body
                          
         !write(*,*) "Relevant Scenarios = ", count   , fullcount 
         
         !if (count > 0) call OutputWrite
         !if (count > 0) call OutputConc  !CHANGE to thirtydayconc  mthtoxexceed anntoxexceed
         
         if (outputtype .eq. 1) then
           if (count > 0) call ExceedTox
         end if
         if (outputtype .eq. 2) then
            if (count > 0) call ThirtyDayAvg_Output
         end if
         if (outputtype .eq. 3) then
            if (count > 0) call OutputConc !Daily_Output
         end if
         
   end do Loop_B 
      
   !write(*,*) "C", Total_Runoff_Mass(1)
   
      call cpu_time (t2)  
      CALL SYSTEM_CLOCK(count2,count_rate)
      write(*,*) 'cpu time= ', t2-t1
      write(*,*) 'clock time= ', (count2-count1)/count_rate

     
    end program PesticideCalculator