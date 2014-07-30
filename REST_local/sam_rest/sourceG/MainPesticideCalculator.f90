program PesticideCalculator
   
   use Variables
   use transport
   use pesticide_application_module
   use output
   use ReadScenarioFiles
   use WaterBodyConc
   
   implicit none
   character(len=100) :: inputFile         !Watershed Recipe input file
   character(len=100) :: inputFileHydro    !Watershed Hydrology input file
   character(len=100) :: inputFileFlow     !Flow Volumes input file
   
   real               :: t1,t2
   integer            :: count1, count2
   integer            :: start, last, lastm    !index used to locate crop number in file name 
   integer            :: io_status, ieof, ierror, status
   character(len=100) :: filename, scenariofilename

   integer :: i,count,fullcount,j,k,kk,t,tk

   character(len=256) :: message   
   logical :: hydro_only
   integer :: count_rate    !real
   
   call cpu_time (t1)  
   call SYSTEM_CLOCK(count1)

   !Read Chemical Inputs and get Scenario Files
     !Read inputFile and eco_or_dw from SAM.inp (created by SAMBeta.vb)
       open (UNIT=39, FILE=trim(adjustl("SAM.inp")),IOSTAT=ierror, STATUS = 'OLD')    !"C:\SAM_repository\SAM.inp"
       read(39,*,IOSTAT=io_status) eco_or_dw
    
   if (eco_or_dw == "eco") then
     recipePath = EcoRecipePath 
     Hydropath = EcoHydropath
     Flowpath = EcoFlowpath
     outpath    = EcoOutPath
     inputFileFlow = "huc12_outlets.txt"                           !For Eco txt file - THIS FILE WILL BE UPDATED ONCE MONTHLY NHDPLUS FLOWS ARE FULLY COMPILED - mmf 6/12/14
   else if (eco_or_dw == "dwr") then
     recipePath = DwRecipePath 
     Hydropath = DwHydropath
     Flowpath = DwFlowpath
     outpath    = DwFOutPath
     inputFileFlow = "DWI_Monthly_Flows_Reservoir_Only_metric.csv"  !For DW Reservoirs txt file
   else if (eco_or_dw == "dwf") then
     recipePath = DwRecipePath 
     Hydropath = DwHydropath
     Flowpath = DwFlowpath
     outpath    = DwFOutPath
     inputFileFlow = "DWI_Monthly_Flows_Flowing_Only_metric.csv"    !For DW Flowing txt file
   end if

   open(UNIT=61, FILE=trim(adjustl(recipepath))//'Bad_Scenarios.txt')
   open(UNIT=86, FILE=trim(adjustl(Flowpath))//trim(adjustl(inputFileFlow)),IOSTAT=ierror, STATUS = 'OLD')
   
   !THESE CHEMICAL/RECIPE PROPERTIES ARE ENTERED IN GUI & READ IN FROM "SAM.inp"
   read (39,*) start_count                    !num_record of simulation start date, since 1/1/1948
   read (39,*) startjul                       !Simulation Start Julian date
   read (39,*) endjul                         !Simulation End Julian date
   read (39,*) ndates                         !Total # days in simulation
   read (39,*) (juliandates(i), i=1,ndates)   !Julian dates of simulation days
   read (39,*) (sdates(i), i=1,ndates)        !Actual date strings
   read (39,*)                                !Chemical name
   read (39,*) Number_crop_ids                !Total # crops
   read (39,*) cropdesired(1:Number_crop_ids) !Crop IDs
   read (39,*) Koc                            !Koc, read as mL/g
   read (39,*) Soil_HalfLife                  !Soil half life
   read (39,*) napps                          !Total # applications
   read (39,*) (appnumrec(i),i=1,napps)       !Application num_record
   read (39,*) (appdate(i), i=1,napps)        !Application dates (Julian format)
   read (39,*) (appmass(i), i=1,napps)        !Mass of each application (read as kg/ha, coverted to kg/m2 below)
   read (39,*) (appMethod(i), i=1,napps)      !Application method (1=ground,...)
   read (39,*) outputtype                     !Output type (1=ToxExd,2=30dMax,3=Daily)
   read (39,*) toxthreshold                   !Output tox threshold level (30d or ann)
   read (39,*) toxthrestype                   !Output tox thres type (1=30d,2=ann)
   read (39,*) outputformat                   !Output format (1=table,2=map)
    
   appmass = appmass/10000.                   !convert applied Mass to kg/m2
   degradation_aqueous = 0.693/Soil_HalfLife  !per day
   degradation_sorbed = degradation_aqueous   !per day (Same Rate in Soil & Surface water (See Handbook of Env. Degradation Rates by Philip Howard, 1991)
   koc = koc/1000.                            !Now in m3/kg
    
   Loop_B : do    !This loop reads in each recipe_name
         Total_Runoff_Mass = 0.0
         Total_Leach_Mass = 0.0  !Added to track leached mass for tile drainage - mmf 4/2014
         totalApplied = 0.0
         
   !Read recipe_name from inputFileFlow for Eco and DW
         
    if (eco_or_dw == "eco") then
       !NOTE: Eco flow file is still under development & is not available to read at this point; Trip is finishing compilation of NHDPlus data for Eco HUCs (mmf 6/12/14)
       read (86,*,IOSTAT=io_status) dummy,dummy,recipe_name,dummy,dummy,dummy,dummy,flow1,flow2,flow3,flow4,flow5,flow6,&
            flow7,flow8,flow9,flow10,flow11,flow12,v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,xa1,xa2,xa3,xa4,xa5,xa6,xa7,xa8,&
            xa9,xa10,xa11,xa12
       if (is_iostat_end(io_status))  exit Loop_B  !End of File
       inputFileHydro = trim(adjustl(recipe_name)) // "_hydro.txt" !For EcoOutput txt files
       
   else if (eco_or_dw == "dwr") then
       read (86,*,IOSTAT=io_status) recipe_name,vol,dummy,dummy,flow1,flow2,flow3,flow4,flow5,flow6,flow7,flow8,flow9,flow10,&
            flow11,flow12,v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,xa1,xa2,xa3,xa4,xa5,xa6,xa7,xa8,xa9,xa10,xa11,xa12    !vol here only for DW reservoirs
        write (*,*) recipe_name
       if (is_iostat_end(io_status))  exit Loop_B  !End of File
       inputFileHydro = trim(adjustl(recipe_name)) // "_hydro.txt"   !For dwOutput txt files
        
   else if (eco_or_dw == "dwf") then
       read (86,*,IOSTAT=io_status) recipe_name,dummy,dummy,dummy,flow1,flow2,flow3,flow4,flow5,flow6,flow7,flow8,flow9,flow10,&
            flow11,flow12,v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,xa1,xa2,xa3,xa4,xa5,xa6,xa7,xa8,xa9,xa10,xa11,xa12 
       if (is_iostat_end(io_status))  exit Loop_B  !End of File
       inputFileHydro = trim(adjustl(recipe_name)) // "_hydro.txt"   !For dwOutput txt files
   end if
                             
       !Read UNIT 74, Watershed Hydrology input file
         open(UNIT=74, FILE=trim(adjustl(Hydropath))//trim(adjustl(inputFileHydro)),IOSTAT=ierror, STATUS = 'OLD')
         read (74,*,IOSTAT=io_status) num_records, totalarea   !num_records = # days in 65 yrs (23742 d)
         
         do j=1, start_count-1
             read(74,*,IOSTAT=io_status)
         end do
         do j = start_count,start_count+ndates-1
           read (74,*,IOSTAT=io_status) Total_Runoff(j)        !m3, Daily Runoff Volume
         end do
   
         if (eco_or_dw == "eco") then   !For Eco Basins
            open (UNIT=21, FILE=trim(adjustl(recipepath))//"HUC12_"//trim(adjustl(recipe_name))//"_recipe.txt",IOSTAT=ierror, &
                  STATUS = 'OLD')
         else     !For DW Basins
            open (UNIT=21, FILE=trim(adjustl(recipepath))//"DWI_"//trim(adjustl(recipe_name))//".txt",IOSTAT=ierror, &
                  STATUS = 'OLD')
         end if 
         
             if (ierror /= 0)  then
                   cycle Loop_B
               end if 
 
         fullcount = 0
         count=0
         Loop_A : do 
                   read (21,*, IOSTAT = ierror) filename, area  !area is in m2
                   if (is_iostat_end(ierror))  exit Loop_A   !End of File
                                     
                   !This gets the crop code and assigns it to the variable named CROP
                   !**********************************************
                   start = index(filename,"_")+1
                   last = len_trim(filename)
                   read(filename(start: last),*) crop
                   
                   lastm = start-2
                   read(filename(1:lastm),*) mukey                    
                   !***********************************************
                  
                   scenariofilename = trim(adjustl(Scenario_Path)) // trim(filename)
         
                   fullcount = fullcount +1  !count all the scenarios in a recipe file
                   if (any(cropdesired(1:Number_crop_ids) == crop )) then
                         count= count+1  !count only the relevant scenarios
                         call Readscenarios(scenariofilename)
               
                         totalApplied = totalApplied + sum(appMass)*area
                         dailyApplied =  sum(appMass)*area
        
                         call process_pesticide_applications
                         
                         call pesticide_transport
                         
                   else
                       dailyApplied = 0.
                   end if                        
                   
         end do Loop_A
         close(21)   !Close the Recipe 
                         
         call waterbody_concentration    !Calculate Pesticide Concentration in Water body
         
         if (outputtype .eq. 1) then
           if (count > 0) call ExceedTox
         end if
         if (outputtype .eq. 2) then
            if (count > 0) call ThirtyDayAvg_Output
         end if
         if (outputtype .eq. 3) then
            if (count > 0) call OutputConc            !Daily_Output
         end if
         
               
   end do Loop_B 
   
      call cpu_time (t2)  
      CALL SYSTEM_CLOCK(count2,count_rate)
      write(*,*) 'cpu time= ', t2-t1
      write(*,*) 'clock time= ', (count2-count1)/count_rate

     
    end program PesticideCalculator