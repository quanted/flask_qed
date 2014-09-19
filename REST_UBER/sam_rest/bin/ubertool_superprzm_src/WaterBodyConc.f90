  Module WaterBodyConc
    implicit none
    contains
  
  !pure subroutine get_date (date1900, YEAR,MONTH,DAY)  !computes GREGORIAN CALENDAR DATE (YEAR,MONTH,DAY) given days since 1900
    !implicit none
    !integer,intent(out) :: YEAR,MONTH,DAY
    !integer,intent(in)  :: date1900  !days since 1900 (julian date)
    !integer :: L,n,i,j

   !L= 2483590 + date1900

   !n= 4*L/146097

   !L= L-(146097*n+3)/4
   !I= 4000*(L+1)/1461001
   !L= L-1461*I/4+31
   !J= 80*L/2447

   !day= L-2447*J/80
   !L= J/11
   !month = J+2-12*L
   !year = 100*(N-49)+I+L

  !end subroutine get_date
  
  
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
        !read (86,*) objID, dummy, dummy, dummy, flow, dummy, xarea  !NHD flow (cfs)
                !vol = xarea*40.                                     !xarea(m2) * length (40m) = vol of water body (CONSTANT)
                waterbody_conc_adj(1) = 0.0
                !flow = flow*((1/3.28084)**3)*86400.                 !convert NHD flow cfs to m3/d
                !Base flow is difference btw total flow and avg daily runoff
                avgrunoff = sum(Total_Runoff)/ndates !num_records   !m3/d
                !!baseflow = flow - avgrunoff                       !OLD - now calculated baseflow is below for each mth
                
                !Array of monthly avg flows - 12 monthly values, repeated over all years - mmf 12/3/13
                !flow_scaled = flow * mflow_factors  !Monthly avg flows
                
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
                       baseflow(t) = 1.e-6                !m3/d
                     else
                       baseflow(t) = mflow(t) - avgrunoff !m3/d
                     end if
                  else if (mthindex(t) .eq. 2) then     !February
                     mflow(t) = flow2
                     mxarea(t) = xa2
                     mvol(t) = xa2*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 3) then     !March
                     mflow(t) = flow3
                     mxarea(t) = xa3
                     mvol(t) = xa3*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 4) then     !April
                     mflow(t) = flow4
                     mxarea(t) = xa4
                     mvol(t) = xa4*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 5) then     !May
                     mflow(t) = flow5
                     mxarea(t) = xa5
                     mvol(t) = xa5*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 6) then     !June
                     mflow(t) = flow6
                     mxarea(t) = xa6
                     mvol(t) = xa6*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 7) then     !July
                     mflow(t) = flow7
                     mxarea(t) = xa7
                     mvol(t) = xa7*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 8) then     !August
                     mflow(t) = flow8
                     mxarea(t) = xa8
                     mvol(t) = xa8*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 9) then     !September
                     mflow(t) = flow9
                     mxarea(t) = xa9
                     mvol(t) = xa9*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 10) then     !October
                     mflow(t) = flow10
                     mxarea(t) = xa10
                     mvol(t) = xa10*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 11) then     !November
                     mflow(t) = flow11
                     mxarea(t) = xa11
                     mvol(t) = xa11*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 12) then     !December
                     mflow(t) = flow12
                     mxarea(t) = xa12
                     mvol(t) = xa12*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  end if                            
                  
                end do
                                    
                !***********************************************
                q_adj_tot(1) = baseflow(1)+Total_Runoff(start_count)
                
                do d=2,ndates !2, num_records                                 !for each day
                                    
                  !Add avg daily direct surface runoff (calculated by SuperPRZMHydro) to base flow (derived from NHDPlus total flow)
                  q_adj_tot(d) = baseflow(d) + Total_Runoff(start_count-1+d)                   !total flow, adding back in daily runoff peaks
                  k_adj(d) = q_adj_tot(d)/mvol(d)                                    !effective rate constant for advection, units [1/d]
                  initconc_adj(d) = (Total_Runoff_Mass(start_count-1+d)/mvol(d))+waterbody_conc_adj(d-1) !kg/m3
                  waterbody_conc_adj(d) = initconc_adj(d)*exp(-k_adj(d))           !assumed t = 1 in Ci*e^(-kt)
                  avgconc_adj(d) = (initconc_adj(d)/k_adj(d))*(1-exp(-k_adj(d)))   !avgconc = area under curve/t = Ci/k*(1-e^-k)
                  
                  !Simple concentration calc - for comparsion
                  conc_simple(d) = Total_Runoff_Mass(start_count-1+d)/q_adj_tot(d)
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
        !read (86,*) objID, dummy, dummy, dummy, flow, dummy, xarea, vol  !NHD flow (cfs), vol (m3)  ***READ IN ALREADY IN MainPesticideCalculator
                waterbody_conc_adj(1) = 0.0
                !flow = flow*((1/3.28084)**3)*86400.                      !convert NHD flow cfs to m3/d
                !Base flow is difference btw total flow and avg daily runoff
                avgrunoff = sum(Total_Runoff)/ndates !num_records  !m3/d
        
                !Array of monthly avg flows - 12 monthly values, repeated over all years - mmf 12/3/13
                !flow_scaled = flow * mflow_factors  !Array of monthly avg flows
                
                !**********************************************
                !This gets the month for juliandate and assigns monthly avg flow to mflow(t)
                !**********************************************
                do t=1,ndates !1,num_records   
                    call get_date(juliandates(t), YEAR,MONTH,DAY)
                    mthindex(t) = month                    
                  
                  if (mthindex(t) .eq. 1) then          !January
                     mflow(t) = flow1
                     mxarea(t) = xa1
                     mvol(t) = vol   !Read in from input flow file, constant across all months for reservoirs - mmf 4/2014
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6                   !m3/d
                     else
                       baseflow(t) = mflow(t) - avgrunoff  !m3/d
                     end if
                  else if (mthindex(t) .eq. 2) then     !February
                     mflow(t) = flow2
                     mxarea(t) = xa2
                     mvol(t) = vol
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 3) then     !March
                     mflow(t) = flow3
                     mxarea(t) = xa3
                     mvol(t) = vol
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 4) then     !April
                     mflow(t) = flow4
                     mxarea(t) = xa4
                     mvol(t) = vol
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 5) then     !May
                     mflow(t) = flow5
                     mxarea(t) = xa5
                     mvol(t) = vol
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 6) then     !June
                     mflow(t) = flow6
                     mxarea(t) = xa6
                     mvol(t) = vol
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 7) then     !July
                     mflow(t) = flow7
                     mxarea(t) = xa7
                     mvol(t) = vol
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 8) then     !August
                     mflow(t) = flow8
                     mxarea(t) = xa8
                     mvol(t) = vol
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 9) then     !September
                     mflow(t) = flow9
                     mxarea(t) = xa9
                     mvol(t) = vol
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 10) then     !October
                     mflow(t) = flow10
                     mxarea(t) = xa10
                     mvol(t) = vol
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 11) then     !November
                     mflow(t) = flow11
                     mxarea(t) = xa11
                     mvol(t) = vol
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 12) then     !December
                     mflow(t) = flow12
                     mxarea(t) = xa12
                     mvol(t) = vol
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  end if                            
                  
                end do
                
                q_adj_tot(1) = baseflow(1)+Total_Runoff(start_count)
                
                do d=2,ndates  !2, num_records                                   !for each day                
                !Add avg daily direct surface runoff (calculated by SuperPRZMHydro) to base flow (derived from NHDPlus total flow)
                  q_adj_tot(d) = baseflow(d) + Total_Runoff(start_count-1+d)            !total flow, assuming runoff was included in flow read in from .txt
                  k_adj(d) = degradation_aqueous + (q_adj_tot(d)/mvol(d))                         !effective rate constant for advection, units [1/d]
                  initconc_adj(d) = (Total_Runoff_Mass(start_count-1+d)/mvol(d))+waterbody_conc_adj(d-1) !kg/m3
                  waterbody_conc_adj(d) = initconc_adj(d)*exp(-k_adj(d))        !assumed t = 1 in Ci*e^(-kt)
                  avgconc_adj(d) = (initconc_adj(d)/k_adj(d))*(1-exp(-k_adj(d)))  !avgconc = area under curve/t = Ci/k*(1-e^-k)
                  
                !Simple conc calc - for comparison
                  conc_simple(d) = Total_Runoff_Mass(start_count-1+d)/q_adj_tot(d)
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
       !For DW Flowing Basins 
        !read (86,*) dummy, dummy, dummy, flow, dummy, xarea    !NHD flow (cfs) ***READ IN ALREADY IN MainPesticideCalculator
                !vol = xarea*40.                                 !xarea(m2) * length (40m) = vol of water body (CONSTANT)
                waterbody_conc_adj(1) = 0.0
               !flow = flow*((1/3.28084)**3)*86400.             !convert baseflow ft3/s to m3/d
               !Base flow is difference btw total flow and avg daily runoff
                avgrunoff = sum(Total_Runoff)/ndates !num_records  !m3/d
                
               !Array of monthly avg flows - 12 monthly values, repeated over all years - mmf 12/3/13
               !flow_scaled = flow * mflow_factors  !Array of monthly avg flows
                
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
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 2) then     !February
                     mflow(t) = flow2
                     mxarea(t) = xa2
                     mvol(t) = xa2*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 3) then     !March
                     mflow(t) = flow3
                     mxarea(t) = xa3
                     mvol(t) = xa3*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 4) then     !April
                     mflow(t) = flow4
                     mxarea(t) = xa4
                     mvol(t) = xa4*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 5) then     !May
                     mflow(t) = flow5
                     mxarea(t) = xa5
                     mvol(t) = xa5*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 6) then     !June
                     mflow(t) = flow6
                     mxarea(t) = xa6
                     mvol(t) = xa6*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 7) then     !July
                     mflow(t) = flow7
                     mxarea(t) = xa7
                     mvol(t) = xa7*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 8) then     !August
                     mflow(t) = flow8
                     mxarea(t) = xa8
                     mvol(t) = xa8*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 9) then     !September
                     mflow(t) = flow9
                     mxarea(t) = xa9
                     mvol(t) = xa9*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 10) then     !October
                     mflow(t) = flow10
                     mxarea(t) = xa10
                     mvol(t) = xa10*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 11) then     !November
                     mflow(t) = flow11
                     mxarea(t) = xa11
                     mvol(t) = xa11*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  else if (mthindex(t) .eq. 12) then     !December
                     mflow(t) = flow12
                     mxarea(t) = xa12
                     mvol(t) = xa12*40.
                     if (mflow(t) < avgrunoff) then
                       baseflow(t) = 1.e-6
                     else
                       baseflow(t) = mflow(t) - avgrunoff
                     end if
                  end if                           
                  
                end do
                
                q_adj_tot(1) = baseflow(1)+Total_Runoff(start_count)
                
                do d=2,ndates  !2, num_records           !for each day                 
                  !Add avg daily direct surface runoff (calculated by SuperPRZMHydro) to base flow (derived from NHDPlus total flow)
                  q_adj_tot(d) = baseflow(d) + Total_Runoff(start_count-1+d)        !total flow, assuming runoff was included in flow read in from .txt
                  k_adj(d) = q_adj_tot(d)/mvol(d)                         !effective rate constant for advection, units [1/d]
                  initconc_adj(d) = (Total_Runoff_Mass(start_count-1+d)/mvol(d))+waterbody_conc_adj(d-1) !kg/m3
                  waterbody_conc_adj(d) = initconc_adj(d)*exp(-k_adj(d))        !assumed t = 1 in Ci*e^(-kt)
                  avgconc_adj(d) = (initconc_adj(d)/k_adj(d))*(1-exp(-k_adj(d)))  !avgconc = area under curve/t = Ci/k*(1-e^-k)
                  
                  !Simple conc calc - for comparison
                  conc_simple(d) = Total_Runoff_Mass(start_count-1+d)/q_adj_tot(d)
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