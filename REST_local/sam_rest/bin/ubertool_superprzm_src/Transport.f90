module transport
implicit none

contains


subroutine pesticide_transport

    !This routine is a pseudo tipping bucket model. in which in flow and outflow occur
    !simultaneously and evenly throughout the time increment --i.e, there is not
    !a specific pre-outflow filling time.  This allows (I think) for faster computation time
    !but should be checked (this is how PRZM does it in any case)
    
    ! use variables_inputs, ONLY: ncpds, output_depth
    ! use variables_other, ONLY:num_records,app_date,naps_adj, number_soil_incr, &
!        bulk_density, delta_x, depth,leaching, soil_water_m_all
!                                  
!    use variables_pesticide,  ONLY:kd,degradation_aqueous,degradation_sorbed,   &
!        soil_pesticide_additions, washoff_into_soil,  &
!        depi_node,  washoff_date, foliar_yes, washoff_node, &
!        harvest_date, harvest_into_soil,output_concentration,output_node
!   
!   use utilities_module


use Variables, ONLY: num_records, ndates, start_count, bulk_density, soil_water_m_all,delta_x,leaching,   &  !increments_1
                    degradation_aqueous,degradation_sorbed,napps, appdate,  pesticide_mass_soil,  &
                   leached_mass,  stored_mass, runoff_mass,degraded_mass,runoff,   &   !extraction_coeff
                    Total_Runoff_Mass,Total_Leach_Mass,area,org_carbon,koc,date_velocity,date_runoff,objID,xarea, &
                    runoff_effic !,runoff_decline, runoff_extr_depth, delx_avg_depth

    !*****************************degraded_mass(n)***************************************************
    implicit none

    real                         :: rho_kd
    real                         :: kd             !m3/kg 
    
    !Retardation factor, R = 1 + (bulk_density*kd)/porosity = 1 + rho_kd / porosity --> So R*theta = theta + rho_kd   Assume like an 'effective volume'
    real :: retardation  !(below) retardation = theta + rho_kd = fraction of water content + [mass on solid/mass in soln]
    real :: theta  !Volumetric water content or Fraction of water content in each compartment (m/m)
    real :: R_dx

    integer :: n,j

    real :: conc           !conc at start, before degradation
    real :: nextconc       !conc after degradation, for next day
    real :: averageconc    !avg daily conc
    real :: total_mass     !daily mass in single compartment
    real :: deg_total      !bio + runoff dissipation + leaching
    real :: deg_biological !dissipation by biological (or other non hydrological means)
    real :: q_runoff
    real :: q_leaching
    
    real :: conc_diff, sum_conc_change
        
    integer :: i    
    integer :: z, zz
    
    real :: oldmass
    real :: expbiodeg
    
    integer :: wash_limit  !prevents array out of bounds in loop below
    
    real :: bottom_conc    !aqueous conc at bottom
    
     leached_mass = 0.
     stored_mass  = 0.
     runoff_mass  = 0.
     degraded_mass= 0.
     conc = 0.
     
    !From Karickhoff, S. (1984), Organic Pollutant Sorption in Aquatic Systems, J. Hydraul. Eng., 110(6), 707–735.
        !kd = ratio of solid conc to aqueous conc; kd = 0.63e-6*kow*foc = koc*foc [m3/g]; Here foc = org_carbon
        !koc = 0.63e-6*kow  [m3/g]
        !get oc value and calc kd from koc, and then convert to rho_kd
    kd = koc*org_carbon      
    
    !convert distribution coeff, kd [m3/g], to dimensionless partition coeff. or ratio of mass concentrations (rho_kd) = bulk_density*kd    
    rho_kd = bulk_density*kd    !scalar, constant with time and in the top 2 cm; bulk_density comes from binScenarios/ files
       
    total_mass = 0.
    conc = 0.
    
   !wash_limit = size(washoff_date)  !see below
   !output_node = find_node(number_soil_incr,depth,output_depth)

    expbiodeg = exp(-degradation_aqueous) !where aqueous and sorbed deg. are equal, this calculation will benefit the speed as shown below

    zz=1  !increments the velocity array when velocity > 0
    z=1   !increments the runoff array when runoff  > 0
      
    !****  Day loop ***********************************************
    !Day loop, this loop will assess whether transport occurs or just degradation (and will route
    !calculations to bypass transport). Calculation is by analytical solution. 
          !OLD METHOD for solving partial diff eqn by backward finite difference - Transport uses main diagonal and subminor diagonal
          !because of backward differencing and no explicit dispersion term (i.e., it is not tridiagonal)
    
    do while (date_runoff(z) < start_count)
        z=z+1
    end do
    
    do while (date_velocity(zz) < start_count)
        zz=zz+1
    end do       
        
    do n = start_count, start_count+ndates-1    !1,num_records
        !write(*,*) "z, zz:", z, zz
        !write(*,*) date_runoff(z),date_velocity(zz)
        !pause
        theta = soil_water_m_all(1,n)/delta_x   !theta (dimensionless), soil_water_m (array of soil water in profile),delta_x(meters)
        retardation= theta+rho_kd             !changes daily according to water content, like "effective volume"    
        R_dx = delta_x * retardation          !"not quite" retardation factor in x-direction, simplified slightly from documentation
        
        deg_biological = degradation_aqueous   !Or a more complicated expression likely to never be used, unless separate aqueous deg desired -> (theta*degradation_aqueous + rho_kd*degradation_sorbed )/retardation  != degradation_aqueous(theta+rho_kd)/(theta+rho_kd) OR essentially, deg_biological = degradation_aqueous 
           
        if (n == date_runoff(z)) then
             q_runoff = runoff(z) * runoff_effic  !Note: q_runoff has dimension of [m] because flow normalized by area
             z=z+1
             !write(*,*)"yes runoff",q_runoff
        else
            q_runoff = 0.0
            !write(*,*)"no runoff",q_runoff
        end if    
 
        !deg_total   = deg_biological + runoff_profile /R_dx  ! add in runoff to total degradation rate

        !************ Add in Pest Applications *************************************
        total_mass =  total_mass  +  pesticide_mass_soil(n)
      
        !write(*,*) "total mass", total_mass
        !pause
        !***********************************************************
        !If no leaching occurring, then the transport section is bypassed
        !And control goes to the degradation-only section

        if (date_velocity(zz) == n )then  !zz is the index to the leaching/infiltration days
            !Revised for 1 COMPARTMENT - UNIFORM EXTRACTION SOLUTION
            q_leaching = leaching(zz)  !Note: leaching has dimension of [m] because flow normalized by area
            deg_total   = deg_biological + q_runoff/R_dx + q_leaching/R_dx
            !write(*,*) deg_biological, q_runoff/R_dx, q_leaching/R_dx, deg_total
            !pause
                                  
            !********Convert Mass to concentration*******************
            conc = total_mass/retardation/delta_x
            nextconc = conc * exp(-deg_total)
            averageconc = (conc/deg_total)*(1-exp(-deg_total))  !Cavg = Co/k (1-exp(-kt))

            !*********Convert Concentration back to mass *************
            total_mass = nextconc*retardation*delta_x  
            
            !*********************************************************
            
            !~~~~~~~CHECK CONC CALC~~~~~~~~~~~~~~~~~~~
            !conc_diff = conc - nextconc
            !sum_conc_change = averageconc*deg_biological + averageconc*q_runoff/R_dx + averageconc*q_leaching/R_dx
            !write(*,*) conc_diff, sum_conc_change
            !pause
            !~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            !These are masses - convert conc to mass by multiplying by R_dx or (delta_x*retardation), which is why there is no "/R_dx" here
            leached_mass(n) = averageconc * q_leaching
            stored_mass(n) = total_mass
            runoff_mass(n) =  averageconc * q_runoff
            degraded_mass(n) = averageconc * deg_biological*retardation
    
            zz=zz+1
         else  !This is the DEGRADATION ONLY (no leaching) section	
            oldmass = total_mass
            total_mass = total_mass * expbiodeg
            stored_mass(n) = total_mass
            degraded_mass(n) = oldmass - stored_mass(zz)
            
            
        end if
          !write(*,*) 'end', conc
          !pause
    end do   !end day loop

    Total_Runoff_Mass = Total_Runoff_Mass + runoff_mass*area  !Accumulates Multi Watershed Info. hold vector of daily pest mass in runoff
    
    Total_Leach_Mass = Total_Leach_Mass + leached_mass*area  !Added to track leached mass for tile drainage - mmf 4/2014                                                                 

end subroutine pesticide_transport

 
end module transport