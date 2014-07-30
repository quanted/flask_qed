module variables
implicit none
save
    
!The following paths will need to be revised, based on your directory structure - mmf 6/12/14

    !***** Recipe Path ***************************
    character(len=100)  :: RecipePath 
    character(len=100)  :: DwRecipepath =   'D:\GitHub\ubertool_src\ubertool_ecorest\REST_local\sam_rest\sourceG\SAM_Uber\&
                                              DWI_recipes\'  
    character(len=100)  :: EcoRecipepath =  'D:\GitHub\ubertool_src\ubertool_ecorest\REST_local\sam_rest\sourceG\SAM_Uber\&
                                              EcoRecipes\'  
    character(len=40)   :: recipe_name      !the current recipe file being processed
    
    !***** binScenario Path ***************************
    character(len=100)  :: Scenario_Path =  'D:\GitHub\ubertool_src\ubertool_ecorest\REST_local\sam_rest\sourceG\SAM_Uber\&
                                              binScenarios\'
    character(len=4)    :: eco_or_dw        !specifies eco or dw paths
    
    !*******Watershed Hydrology Path*******************
    character(len=100)  :: Hydropath
    character(len=100)  :: DwHydropath = 'D:\GitHub\ubertool_src\ubertool_ecorest\REST_local\sam_rest\sourceG\SAM_Uber\&
                                              dwOutput\'
    character(len=100)  :: EcoHydropath = 'D:\GitHub\ubertool_src\ubertool_ecorest\REST_local\sam_rest\sourceG\SAM_Uber\&
                                              EcoOutput\'
    
    !*******Flow Volumes Path***************************
    character(len=100)  :: Flowpath
    character(len=100)  :: DwFlowpath = 'D:\GitHub\ubertool_src\ubertool_ecorest\REST_local\sam_rest\sourceG\SAM_Uber\&
                                              DWI_recipes\'
    character(len=100)  :: EcoFlowpath = 'D:\GitHub\ubertool_src\ubertool_ecorest\REST_local\sam_rest\sourceG\SAM_Uber\&
                                              EcoRecipes\'
    
    !**** OUTPUT PATH **************************************
    character(len=100)  :: Outpath
    character(len=100)  :: EcoOutpath =  'D:\GitHub\ubertool_src\ubertool_ecorest\REST_local\sam_rest\sourceG\SAM_Uber\&
                                              EcoPestOut\'
    character(len=100)  :: DwFOutpath =  'D:\GitHub\ubertool_src\ubertool_ecorest\REST_local\sam_rest\sourceG\SAM_Uber\dwPestOut\&
                                              Flowing\'
    character(len=100)  :: DwROutpath =  'D:\GitHub\ubertool_src\ubertool_ecorest\REST_local\sam_rest\sourceG\SAM_Uber\dwPestOut\&
                                              Reservoirs\'
    
    !Parameters
    integer, parameter :: maxdays = 45000  !this is the number of days used for allocations
    integer, parameter :: appmax = 1000    !maximum number of applications
    integer            :: Number_crop_ids
    integer            :: crop
    integer            :: mukey
    
    !From Watershed Hydro Input*********************
    real                     :: totalarea      !m2 area
    real, dimension(maxdays) :: Total_Runoff   !m3 of runoff from watershed
    
    !From Flow Volumes Input************************
    character(len=100) :: objID
    real :: factor                             !unit conversion factor
    
    real :: v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12               !monthly mean velocity m/s
    real :: xa1,xa2,xa3,xa4,xa5,xa6,xa7,xa8,xa9,xa10,xa11,xa12   !monthly mean xarea (m2)
    real :: flow1,flow2,flow3,flow4,flow5,flow6,flow7,flow8,flow9,flow10,flow11,flow12  !monthly mean flow in m3/d
    real :: vol                                                  !m3, annual mean volume of water body
    real,dimension(maxdays) :: waterbody_conc     !kg/m3, calculated conc in water body
    real,dimension(maxdays) :: initconc !kg/m3, calculated total conc in water body
    real,dimension(maxdays) :: kconst   !effective rate constant for advection, completely mixed flow reactor (CMFR) assumed
    real,dimension(maxdays) :: q_tot    !m3/d, total flow of water body = baseflow + runoff flow
    real,dimension(maxdays) :: avgconc    
        
    character(len=100) :: dummy         !placeholder dummy
    real               :: masstot
    real               :: avgrunoff

    real,dimension(maxdays) :: baseflow
    real,dimension(maxdays) :: waterbody_conc_adj !kg/m3, calculated conc in water body, subtracts out avgrunoff from NHDflow to get baseflow, then adds in daily runoff
    real,dimension(maxdays) :: initconc_adj !kg/m3, calculated total conc in water body
    real,dimension(maxdays) :: k_adj        !effective rate constant for advection, completely mixed flow reactor (CMFR) assumed
    real,dimension(maxdays) :: q_adj_tot    !m3/d, total flow of water body = baseflow + runoff flow
    real,dimension(maxdays) :: avgconc_adj
    real,dimension(maxdays) :: conc_simple
    
    ! Pesticide Inputs******************************         
    integer,dimension(5)               :: cropdesired
    real                               :: Koc            !mL/g
    real                               :: Soil_HalfLife  !days
    integer                            :: napps      !number of total applications in the simulation
    integer                            :: ndates
    integer                            :: start_count
    integer,dimension(maxdays)         :: juliandates
    character(len=100), dimension(maxdays) :: sdates
    character(len=100)                 :: sdate
    integer,dimension(maxdays)         :: appdate   !number of simulation timesteps for each app (or days after sim start) 
    integer,dimension(maxdays)         :: appnumrec
    real,dimension(maxdays)            :: appmass
    integer,dimension(maxdays)         :: appmethod
    integer                            :: startjul
    integer                            :: endjul
    
   character(len=100)                  :: monthindex
   integer, dimension(maxdays)         :: mthindex
   integer, dimension(maxdays)         :: yrindex
   
   integer,dimension(maxdays)          :: mth_chronic_exceed
   integer,dimension(maxdays)          :: ann_chronic_exceed
   real,dimension(maxdays)             :: thirtydayavg
    !*************************************************
        
    ! OUTPUT******************************************
    integer :: outputtype    !Output type (1=ToxExd,2=30dMax,3=AnnPeak)
    real    :: toxthreshold  !Output toxicity threshold (for 30-d or 14-d max)
    integer :: outputformat  !Output format (1=table,2=map)
    integer :: toxthrestype  !Output tox thres type (1=30d, 2=annual)

    real, dimension(maxdays)  :: Total_Runoff_Mass !kg
    
    real, dimension(maxdays)  ::  Total_Leach_Mass !kg   !Added to track leached mass, for potential for tile drainage - mmf 4/2014
    
    real, dimension(appmax) :: appdepth

    real, parameter :: soil_distribution_2cm = 0.75  !for 1 COMPARTMENT - UNIFORM EXTRACTION

   !Implement runoff calculation similar to SWCC:
   real :: runoff_effic = 0.266  !Bypass 73.4%; efficiency was also 0.266 in PRZM5/SWCC- accounts for amount of runoff not bypassing surface soil
   
   real, dimension(maxdays)  :: mflow  !vector of monthly mean total flows
   real, dimension(maxdays)  :: mxarea !vector of monthly mean xareas
   real, dimension(maxdays)  :: mvol   !vector of monthly mean volumes
   real, parameter           :: delta_x = 0.02   !meters
   
   integer      :: num_records  
   integer      :: NumberOfYears
   real         :: covmax
   
   real, dimension(1,maxdays)                 :: soil_water_m_all  !for 1 compartment
  
   real                                       :: bulk_density      !stored as kg/m3
   
   real                                       :: org_carbon        !fraction
   real,dimension(maxdays)                    :: rain              !only precip above zero C
   real,dimension(maxdays)                    :: plant_factor

   integer                                    :: count_runoff     !number of days of actual runoff
   real,dimension(maxdays)                    :: runoff
   integer,dimension(maxdays)                 :: date_runoff
   
   integer                                        :: count_velocity   !number of days of water moving vertically (leaching)     
   real, dimension(maxdays)                       :: leaching         !for 1 compartment
   integer,dimension(maxdays)                     :: date_velocity
    
    real   :: degradation_aqueous      !per day
    real   :: degradation_sorbed       !per day
    real   :: foliar_degradation = 0.0 !per day
    real   :: washoff_coeff = 0.1

    real,dimension(maxdays)         :: pesticide_mass_soil        !for 1 compartment
            
    real,dimension(maxdays) :: leached_mass, stored_mass, runoff_mass, degraded_mass, dailyApplied      !sorb_mass may be added to account for sorbed mass in future
    real :: totalMassRunoff, totalApplied
    real :: total_mass     !for 1 compartment
    
    real        :: area   !area of each scenario m2
    
    real        :: pesticide_applied
       
end module variables