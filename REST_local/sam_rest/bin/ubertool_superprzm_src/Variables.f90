module variables
implicit none
save
    
    !***** Recipe Path ***************************
    character(len=200)  :: RecipePath 
    !Randomize Recipe CDL, out of 5 CDL subfolders, see Utilities - mmf 7/2014
    character(len=200)  :: DwRecipePath =   '\dwRecipes\DWI_recipes_082014\' !'J:\dwRecipes_huc12\'
    character(len=200)  :: EcoRecipepath =  '\EcoRecipes_huc12\huc12_Xwalk_recipes\' !'C:\SAM_repository\EcoRecipes_huc12\' !'J:\EcoRecipes_huc12\'
    character(len=40)   :: recipe_name      !the current recipe file being processed
    
    !***** binScenario Path ***************************
    character(len=200)  :: Scenario_Path =  '\binScenarios_all\binScenarios_SoilGrps\' !'1extr_test\' !'J:\binScenarios_1extr\'
    character(len=4)    :: eco_or_dw       !specifies eco or dw paths
    
    !*******Watershed Hydrology Path*******************
    character(len=200)  :: Hydropath
    character(len=200)  :: DwHydropath = '\dwOutput_all\dwOutput_SoilGrps\' !'J:\dwOutput_1extr_huc12\'   !****_hydro.txt, contains: totalarea, num_records, Total_Runoff
    character(len=200)  :: EcoHydropath = '\EcoOutput_all\EcoOutput_SoilGrps\' !'1extr_huc12_test\' !'J:\EcoOutput_1extr_huc12\' !****_hydro.txt
    
    !*******Flow Volumes Path***************************
    character(len=200)  :: Flowpath
    character(len=200)  :: DwFlowpath = '\dwRecipes\DWI_recipes_082014\'  !'J:\dwRecipes_huc12\'
    character(len=200)  :: EcoFlowpath = '\EcoRecipes_huc12\huc12_Xwalk_recipes\'  !'J:\EcoRecipes_huc12\' 
    
    !**** OUTPUT PATH **************************************
    character(len=200)  :: Outpath
    character(len=200)  :: EcoOutpath =  '\EcoPestOut_all\EcoPestOut_SoilGrps\' !'EcoPestOut_1extr_73.4by_30yr_huc12_test\' !'J:\EcoPestOut_1extr_73.4by_30yr_huc12\' !'G:\Teams and Panels\Special Teams\SAM\EcoPestOut\TriApp_20days\'
    character(len=200)  :: DwFOutpath =  '\dwPestOut_all\dwPestOut_SoilGrps\Flowing\'  !'J:\dwPestOut_1extr_73.4by_30yr_huc12\Flowing\' !'G:\Teams and Panels\Special Teams\SAM\dwPestOut\Flowing\'
    character(len=200)  :: DwROutpath =  '\dwPestOut_all\dwPestOut_SoilGrps\Reservoirs\' !'J:\dwPestOut_1extr_73.4by_30yr_huc12\Reservoirs\' !'G:\Teams and Panels\Special Teams\SAM\dwPestOut\Reservoirs\'
    
    !Parameters
    integer, parameter :: maxdays = 45000 !24000 !this is the number of days used for allocations
    integer, parameter :: appmax = 1000    !maximum number of applications
    integer            :: Number_crop_ids
    integer            :: crop
    !integer            :: mukey     !before SoilGrps
    character          :: mukey
    
    !From Watershed Hydro Input*********************
    real                     :: totalarea      !m2 area
    real, dimension(maxdays) :: Total_Runoff   !m3 of runoff from watershed
    
    !From Flow Volumes Input************************
    character(len=100) :: objID
    real :: factor                      !unit conversion factor
    
    real :: v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12               !monthly mean velocity m/s
    real :: xa1,xa2,xa3,xa4,xa5,xa6,xa7,xa8,xa9,xa10,xa11,xa12   !monthly mean xarea (m2)
    real :: flow1,flow2,flow3,flow4,flow5,flow6,flow7,flow8,flow9,flow10,flow11,flow12  !monthly mean flow in m3/d
    
    !for Eco simulations until get monthly NHDPlus- mmf 7/2014
    real :: xarea                       !m2, annual mean x-sectional area
    real :: flow                        !cfs, need to convert to m3/d!
    real :: vol                         !m3, annual  mean volume of water body
    real,dimension(maxdays) :: waterbody_conc     !kg/m3, calculated conc in water body
    real,dimension(maxdays) :: initconc !kg/m3, calculated total conc in water body
    real,dimension(maxdays) :: kconst   !effective rate constant for advection, completely mixed flow reactor (CMFR) assumed
    real,dimension(maxdays) :: q_tot    !m3/d, total flow of water body = baseflow + runoff flow
    real,dimension(maxdays) :: avgconc
    !real :: timestep !s, where Vol/Flow = timestep
    character(len=100) :: dummy         !placeholder dummy
    real               :: masstot
    real               :: avgrunoff
    !real :: baseflow
    real,dimension(maxdays) :: baseflow
    real,dimension(maxdays) :: waterbody_conc_adj !kg/m3, calculated conc in water body, adjusted b/c now subtracts out avgrunoff from NHDflow to get baseflow, then adds in daily runoff
    real,dimension(maxdays) :: initconc_adj !kg/m3, calculated total conc in water body
    real,dimension(maxdays) :: k_adj        !effective rate constant for advection, completely mixed flow reactor (CMFR) assumed
    real,dimension(maxdays) :: q_adj_tot    !m3/d, total flow of water body = baseflow + runoff flow
    real,dimension(maxdays) :: avgconc_adj
    real,dimension(maxdays) :: conc_simple
    
    ! Pesticide Inputs******************************         
    integer,dimension(5)               :: cropdesired
    real                               :: Koc            !ml/g
    real                               :: Soil_HalfLife  !days
    integer                            :: napps      !number of total applications in the simulation
    integer                            :: ndates
    integer                            :: start_count
    integer,dimension(maxdays)         :: juliandates
    character(len=100), dimension(maxdays) :: sdates
    character(len=100)                 :: sdate
    integer,dimension(maxdays)         :: appdate    !number of simulation timestep for each app (or days after sim start) 
    integer,dimension(maxdays)         :: appnumrec
    real,dimension(maxdays)            :: appmass
    integer,dimension(maxdays)         :: appmethod
    integer                            :: startjul
    integer                            :: endjul
    
   character(len=100)                  :: monthindex
   integer, dimension(maxdays)         :: mthindex
   integer, dimension(maxdays)         :: yrindex
   
   integer,dimension(maxdays)      :: mth_chronic_exceed
   integer,dimension(maxdays)      :: ann_chronic_exceed
   !real                            :: chronic_threshold = 4.     !ug/L
   real,dimension(maxdays)         :: thirtydayavg
   
    !*************************************************
        
    ! OUTPUT******************************************
    integer :: outputtype   != 1  !Output type (1=ToxExd,2=30dMax,3=DailyConc)
    real    :: toxthreshold != 4  !Output toxicity threshold (for 30-d or ann)
    integer :: outputformat       !Output format (1=table,2=map)
    integer :: toxthrestype != 2  !Output tox thres type (1=30d, 2=annual)

    real, dimension(maxdays)  :: Total_Runoff_Mass !kg
    
    real, dimension(maxdays)  ::  Total_Leach_Mass !kg   !Added to track leached mass, for potential for tile drainage - mmf 4/2014 
   
    real,   dimension(appmax) :: appdepth


    !Not used -> integer, parameter :: number_soil_incr = 21
    !integer, parameter :: increments_1 = 1  !the node that defines the bottom of the runoff extraction depth

    real, parameter :: soil_distribution_2cm = 0.75  !REVISED for 1 COMPARTMENT - UNIFORM EXTRACTION
    !real, dimension(increments_1), parameter :: soil_distribution_2cm = (/ 0.75, & 
                                                                      !0.0975, &
                                                                      !0.0925, &
                                                                      !0.0875, &
                                                                      !0.0825, &
                                                                      !0.0775, &
                                                                      !0.0725, &
                                                                      !0.0675, &
                                                                      !0.0625, &
                                                                      !0.0575, &
                                                                      !0.0525  /)

   !real, dimension(increments_1), parameter :: extraction_coeff= (/ &    !NO LONGER USED for 1 COMPARTMENT - UNIFORM EXTRACTION
                                                           !0.739514493, &
                                                           !0.542394654, &
                                                           !0.397817708, &
                                                           !0.291778187, &
                                                           !0.214003823, &
                                                           !0.156960453, &
                                                           !0.115122166, &
                                                           !0.084436003, &
                                                           !0.061929329, &
                                                           !0.045421878 /)   
   
   !Implement runoff calculation similar to SWCC:
   real :: runoff_effic = 0.266  !Bypass 73.4%; was 0.266 in PRZM5/SWCC; amount of runoff bypassing surface soil
   !real :: runoff_extr_depth = 2 !depth of runoff interaction
   !real :: runoff_decline = 1.55 !exponential factor for interaction decline with depth
   !real, dimension(increments_1), parameter:: delx_avg_depth = (/0.1,0.3,0.5,0.7,0.9,1.1,1.3,1.5,1.7,1.9/)
   
   !Old 6/2014- once used for NHDPlus annual mean scaling to get monthly mean flows
   !real, dimension(12), parameter :: mflow_factors=(/0.84, 1.26, 3.04, 2.18, 1.70, 1.14, 0.06, 0.14, 0.02, 0.18, 0.58, 0.88 /) !0.09, 0.18, 0.20, 0.20, 0.11, 0.04, 0.01, 0.01, 0.01, 0.01, 0.03, 0.11/)
   !real, dimension(12) :: flow_scaled, mflow_sc
   !real, dimension(maxdays)  :: mflow  !vector of monthly mean total flows
   
   real, dimension(maxdays)  :: mflow  !vector of monthly mean total flows
   real, dimension(maxdays)  :: mxarea !vector of monthly mean xareas
   real, dimension(maxdays)  :: mvol   !vector of monthly mean volumes
   
   !real, dimension(increments_1), parameter :: depth = (/0.02/) !(/ 0.002,0.004,0.006,0.008,.01,0.012,0.014,0.016,0.018,0.02 /)  
   real, parameter           :: delta_x = 0.02   !0.002           !meters
   
   integer      :: num_records  
   integer      :: NumberOfYears
   real         :: covmax
   
!   real,dimension(increments_1,maxdays) :: extraction_array

   real, dimension(1,maxdays)                  :: soil_water_m_all  !REVISED for 1 compartment
   !real,dimension(increments_1,maxdays)       :: soil_water_m_all  !(number_soil,incr,num_records)
  
   real                                       :: bulk_density      !stored as kg/m3
   
   real                                       :: org_carbon        !fraction
   real,dimension(maxdays)                    :: rain              !only precip above zero C
   real,dimension(maxdays)                    :: plant_factor

   

   integer                                        :: count_runoff     !number of days of actual runoff
   real,dimension(maxdays)                        :: runoff
   integer,dimension(maxdays)                     :: date_runoff
   
   integer                                        :: count_velocity   !number of days of water moving vertically (leaching)     
   real, dimension(maxdays)                       :: leaching         !REVISED for 1 compartment
   !real,dimension(0:increments_1,maxdays)        :: leaching         !(0:number_soil,incr,num_records)
   integer,dimension(maxdays)                     :: date_velocity
    
    real   :: degradation_aqueous      !per day
    real   :: degradation_sorbed       !per day
    real   :: foliar_degradation = 0.0 !per day
    real   :: washoff_coeff = 0.1

    real,dimension(maxdays)         :: pesticide_mass_soil        !REVISED for 1 compartment
    !real,dimension(increments_1,maxdays) :: pesticide_mass_soil  !this is the applied mass of pesticide into the soil
            
    real,dimension(maxdays) :: leached_mass, stored_mass, runoff_mass, degraded_mass, dailyApplied !, sorb_mass !NEW - sorb_mass ADDED TO ACCOUNT FOR SORBED MASS
    real :: totalMassRunoff, totalApplied
    real :: total_mass     !REVISED for 1 compartment
    !real,dimension(increments_1)  :: total_mass  !daily mass in profile
    
    real        :: area   !area of each scenario m2
    
    real        :: pesticide_applied
       
end module variables