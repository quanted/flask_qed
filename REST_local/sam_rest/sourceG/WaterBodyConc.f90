  Module WaterBodyConc
    implicit none
    contains
  
  
   subroutine waterbody_concentration
  
    use Variables
    use AnnExceed
    use MthExceed
    use ThirtyDayAvgConc
    use Utilities
    
    integer :: t,d,i,c
    integer :: day,month,year
       
    !Calculate Daily Pesticide Conc
    if (eco_or_dw == "eco") then   !For Eco Basins  
                !vol = xarea*40.                                     !xarea(m2) * length (40m) = vol of water body (CONSTANT)
                waterbody_conc_adj(1) = 0.0
                avgrunoff = sum(Total_Runoff)/ndates !num_records    !m3/d
                
                !**********************************************
                !This gets the month of the juliandate and assigns monthly avg flow to mflow(t)
                !**********************************************
                do t=1,ndates  
                    call get_date(juliandates(t), YEAR,MONTH,DAY)
                    mthindex(t) = month                    
                  if (mthindex(t) .eq. 1) then          !January
                     mflow(t) = flow1
                     mxarea(t) = xa1
                     mvol(t) = xa1*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0                  !m3/d     
                     else
                       baseflow(t) = mflow(t) - avgrunoff !m3/d   
                     end if
                  else if (mthindex(t) .eq. 2) then     !February
                     mflow(t) = flow2
                     mxarea(t) = xa2
                     mvol(t) = xa2*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 3) then     !March
                     mflow(t) = flow3
                     mxarea(t) = xa3
                     mvol(t) = xa3*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 4) then     !April
                     mflow(t) = flow4
                     mxarea(t) = xa4
                     mvol(t) = xa4*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 5) then     !May
                     mflow(t) = flow5
                     mxarea(t) = xa5
                     mvol(t) = xa5*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 6) then     !June
                     mflow(t) = flow6
                     mxarea(t) = xa6
                     mvol(t) = xa6*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 7) then     !July
                     mflow(t) = flow7
                     mxarea(t) = xa7
                     mvol(t) = xa7*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 8) then     !August
                     mflow(t) = flow8
                     mxarea(t) = xa8
                     mvol(t) = xa8*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 9) then     !September
                     mflow(t) = flow9
                     mxarea(t) = xa9
                     mvol(t) = xa9*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 10) then     !October
                     mflow(t) = flow10
                     mxarea(t) = xa10
                     mvol(t) = xa10*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 11) then     !November
                     mflow(t) = flow11
                     mxarea(t) = xa11
                     mvol(t) = xa11*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 12) then     !December
                     mflow(t) = flow12
                     mxarea(t) = xa12
                     mvol(t) = xa12*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  end if                            
                end do
                                    
                !***********************************************
                q_adj_tot(1) = baseflow(1)+Total_Runoff(start_count)
                do d=2,ndates  !for each day  
                  !Add avg daily direct surface runoff (calculated by SuperPRZMHydro) to base flow (derived from NHDPlus total flow)
                  q_adj_tot(d) = baseflow(d) + Total_Runoff(start_count-1+d)                   !total flow, adding back in daily runoff peaks
                  k_adj(d) = q_adj_tot(d)/mvol(d)                                              !effective rate constant for advection, units [1/d]
                  initconc_adj(d) = (Total_Runoff_Mass(start_count-1+d)/mvol(d))+waterbody_conc_adj(d-1) !kg/m3
                  waterbody_conc_adj(d) = initconc_adj(d)*exp(-k_adj(d))           !assumed t = 1 in Ci*e^(-kt)
                  avgconc_adj(d) = (initconc_adj(d)/k_adj(d))*(1-exp(-k_adj(d)))   !avgconc = area under curve/t = Ci/k*(1-e^-k)
                  conc_simple(d) = Total_Runoff_Mass(start_count-1+d)/q_adj_tot(d) !Simple concentration calc - for comparsion
                end do 
          
        !************************************************************************************** 
        !Compute monthly and annual exceedances of chronic toxicty threshold and 30d avg concs
        !**************************************************************************************
                if (outputtype .eq. 1)  then
                    if (toxthrestype .eq. 1) then
                        call mthtoxexceed
                    else if (toxthrestype .eq. 2) then
                        call anntoxexceed
                    end if  
                end if
                if(outputtype .eq. 2) then  
                    call thirtydayconc  !computes 30d avg concs
                end if
       
    else if (eco_or_dw == "dwr") then    !for DW Reservoirs - Total_Runoff_Mass/volume
                waterbody_conc_adj(1) = 0.0
                avgrunoff = sum(Total_Runoff)/ndates   !m3/d
                
                !**********************************************
                !This gets the month for juliandate and assigns monthly avg flow to mflow(t)
                !**********************************************
                do t=1,ndates 
                    call get_date(juliandates(t), YEAR,MONTH,DAY)
                    mthindex(t) = month                    
                  if (mthindex(t) .eq. 1) then          !January
                     mflow(t) = flow1
                     mxarea(t) = xa1
                     mvol(t) = vol   !Read in from input flow file, constant across all months for reservoirs - mmf 4/2014
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0                  !m3/d     
                     else
                       baseflow(t) = mflow(t) - avgrunoff !m3/d   
                     end if
                  else if (mthindex(t) .eq. 2) then     !February
                     mflow(t) = flow2
                     mxarea(t) = xa2
                     mvol(t) = vol
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 3) then     !March
                     mflow(t) = flow3
                     mxarea(t) = xa3
                     mvol(t) = vol
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 4) then     !April
                     mflow(t) = flow4
                     mxarea(t) = xa4
                     mvol(t) = vol
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 5) then     !May
                     mflow(t) = flow5
                     mxarea(t) = xa5
                     mvol(t) = vol
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 6) then     !June
                     mflow(t) = flow6
                     mxarea(t) = xa6
                     mvol(t) = vol
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 7) then     !July
                     mflow(t) = flow7
                     mxarea(t) = xa7
                     mvol(t) = vol
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 8) then     !August
                     mflow(t) = flow8
                     mxarea(t) = xa8
                     mvol(t) = vol
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 9) then     !September
                     mflow(t) = flow9
                     mxarea(t) = xa9
                     mvol(t) = vol
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 10) then     !October
                     mflow(t) = flow10
                     mxarea(t) = xa10
                     mvol(t) = vol
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 11) then     !November
                     mflow(t) = flow11
                     mxarea(t) = xa11
                     mvol(t) = vol
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 12) then     !December
                     mflow(t) = flow12
                     mxarea(t) = xa12
                     mvol(t) = vol
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  end if                            
                end do
                
                q_adj_tot(1) = baseflow(1)+Total_Runoff(start_count)
                do d=2,ndates  !for each day                
                !Add avg daily direct surface runoff (calculated by SuperPRZMHydro) to base flow (derived from NHDPlus total flow)
                  q_adj_tot(d) = baseflow(d) + Total_Runoff(start_count-1+d)     !total flow, assuming runoff was included in flow read in from .txt
                  k_adj(d) = degradation_aqueous + (q_adj_tot(d)/mvol(d))        !deg aqueous + effective rate constant for advection, units [1/d]
                  initconc_adj(d) = (Total_Runoff_Mass(start_count-1+d)/mvol(d))+waterbody_conc_adj(d-1) !kg/m3
                  waterbody_conc_adj(d) = initconc_adj(d)*exp(-k_adj(d))            !assumed t = 1 in Ci*e^(-kt)
                  avgconc_adj(d) = (initconc_adj(d)/k_adj(d))*(1-exp(-k_adj(d)))    !avgconc = area under curve/t = Ci/k*(1-e^-k)
                  conc_simple(d) = Total_Runoff_Mass(start_count-1+d)/q_adj_tot(d)  !Simple conc calc - for comparison
                end do
                        
        !************************************************************************************** 
        !Compute monthly and annual exceedances of chronic toxicty threshold and 30d avg concs
        !**************************************************************************************
                if (outputtype .eq. 1)  then
                    if (toxthrestype .eq. 1) then
                        call mthtoxexceed
                    else if (toxthrestype .eq. 2) then
                        call anntoxexceed
                    end if  
                end if
                if(outputtype .eq. 2) then  
                    call thirtydayconc  !computes 30d avg concs
                end if
                    
    else if (eco_or_dw == "dwf") then !for DW Flowing
                !vol = xarea*40.                                !xarea(m2) * length (40m) = vol of water body (if assume CONSTANT)
                waterbody_conc_adj(1) = 0.0
                avgrunoff = sum(Total_Runoff)/ndates !num_records  !m3/d
                
                !**********************************************
                !This gets the month for juliandate and assigns monthly avg flow to mflow(t)
                !**********************************************
                do t=1,ndates  !1,num_records   
                    call get_date(juliandates(t), YEAR,MONTH,DAY)
                    mthindex(t) = month                 
                  if (mthindex(t) .eq. 1) then          !January
                     mflow(t) = flow1
                     mxarea(t) = xa1
                     mvol(t) = xa1*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0                  !m3/d     
                     else
                       baseflow(t) = mflow(t) - avgrunoff !m3/d   
                     end if
                  else if (mthindex(t) .eq. 2) then     !February
                     mflow(t) = flow2
                     mxarea(t) = xa2
                     mvol(t) = xa2*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 3) then     !March
                     mflow(t) = flow3
                     mxarea(t) = xa3
                     mvol(t) = xa3*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 4) then     !April
                     mflow(t) = flow4
                     mxarea(t) = xa4
                     mvol(t) = xa4*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 5) then     !May
                     mflow(t) = flow5
                     mxarea(t) = xa5
                     mvol(t) = xa5*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 6) then     !June
                     mflow(t) = flow6
                     mxarea(t) = xa6
                     mvol(t) = xa6*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 7) then     !July
                     mflow(t) = flow7
                     mxarea(t) = xa7
                     mvol(t) = xa7*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 8) then     !August
                     mflow(t) = flow8
                     mxarea(t) = xa8
                     mvol(t) = xa8*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 9) then     !September
                     mflow(t) = flow9
                     mxarea(t) = xa9
                     mvol(t) = xa9*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 10) then     !October
                     mflow(t) = flow10
                     mxarea(t) = xa10
                     mvol(t) = xa10*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 11) then     !November
                     mflow(t) = flow11
                     mxarea(t) = xa11
                     mvol(t) = xa11*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 12) then     !December
                     mflow(t) = flow12
                     mxarea(t) = xa12
                     mvol(t) = xa12*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 0.0
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  end if                           
                end do
                
                q_adj_tot(1) = baseflow(1)+Total_Runoff(start_count)
                do d=2,ndates   !for each day                 
                  !Add avg daily direct surface runoff (calculated by SuperPRZMHydro) to base flow (derived from NHDPlus total flow)
                  q_adj_tot(d) = baseflow(d) + Total_Runoff(start_count-1+d)        !total flow, assuming runoff was included in flow read in from .txt
                  k_adj(d) = q_adj_tot(d)/mvol(d)                                   !effective rate constant for advection, units [1/d]
                  initconc_adj(d) = (Total_Runoff_Mass(start_count-1+d)/mvol(d))+waterbody_conc_adj(d-1) !kg/m3
                  waterbody_conc_adj(d) = initconc_adj(d)*exp(-k_adj(d))            !assumed t = 1 in Ci*e^(-kt)
                  avgconc_adj(d) = (initconc_adj(d)/k_adj(d))*(1-exp(-k_adj(d)))    !avgconc = area under curve/t = Ci/k*(1-e^-k)
                  conc_simple(d) = Total_Runoff_Mass(start_count-1+d)/q_adj_tot(d)  !Simple conc calc - for comparison
                end do  
        
        !************************************************************************************** 
        !Compute monthly and annual exceedances of chronic toxicty threshold and 30d avg concs
        !**************************************************************************************
                if (outputtype .eq. 1)  then
                    if (toxthrestype .eq. 1) then
                        call mthtoxexceed
                    else if (toxthrestype .eq. 2) then
                        call anntoxexceed
                    end if  
                end if
                if(outputtype .eq. 2) then  
                    call thirtydayconc  !computes 30d avg concs
                end if
              
    end if
        
    end subroutine waterbody_concentration
    
    end Module WaterBodyConc