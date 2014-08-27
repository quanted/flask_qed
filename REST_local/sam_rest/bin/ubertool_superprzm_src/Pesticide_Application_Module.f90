module pesticide_application_module
    implicit none
    integer,private :: status
contains
!**********************************************************
subroutine process_pesticide_applications
!use variables_inputs, ONLY:ncpds

!the output of this module is pesticide_Mass(increments_1,num_records) which is the daily additions of pesticide mass to 
!the extraction zone

use variables, ONLY: plant_factor, &
                     covmax,       &
                     appdate,      &
                     appmass,      &
                     napps,        &
                     appMethod,              &
                     soil_distribution_2cm,  &
                     !increments_1,       &
                     foliar_degradation,     &
                     rain,                   &
                     pesticide_mass_soil,    &
                     washoff_coeff,num_records, &
                     startjul, &
                     endjul, &
                     start_count, &
                     ndates, &
                     appnumrec
 
implicit none

       integer :: i, j, k, n
       integer :: node_max_depo

       real,dimension(napps)   :: canopy_pesticide_additions  !0 value is no addition

       real    :: canopy_mass
       real    :: exponent
       integer :: day
       integer :: previous_day
       real    :: pesticide_remaining

!      !%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
!      !%%%%%%%%%%%%%%%%%%%%% Chemical Appication Method Specifics  %%%%%%%%%%%%%%%%%%%%%%%%
!      !%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
       canopy_pesticide_additions = 0.
       pesticide_mass_soil = 0.0
       previous_day = 0 
                    
    j=1  !application tracker
    Day_LOOP: do day = start_count, start_count+ndates-1  !1, num_records
        
            !CHECK IF THERE IS A PESTICIDE APPLICATION
            if (day == appnumrec(j)) then  !Application Day
                                    
            select case (appMethod(j))
                case (2)  !CANOPY APPLICATION
                    canopy_pesticide_additions(j) = appmass(j)*plant_factor(appnumrec(j))*covmax   
                    pesticide_mass_soil(day) = (appmass(j) - canopy_pesticide_additions(j))* soil_distribution_2cm
                    !pesticide_mass_soil(:,day) = (appmass(j) - canopy_pesticide_additions(j))* soil_distribution_2cm 
                    canopy_mass =  canopy_pesticide_additions(j) + canopy_mass*exp(-real(day-previous_day)*foliar_degradation) !degradation between apps            
                    previous_day = day 
                    j=1+j
                    
                case (1)  !SOIL APPLICATION
                    pesticide_mass_soil(day) = pesticide_mass_soil(day)+ appmass(j)* soil_distribution_2cm
                    !pesticide_mass_soil(:,day) = pesticide_mass_soil(:,day)+ appmass(j)* soil_distribution_2cm  !ORIGINAL               
                   
                    !OLD, prior to GUI - Apply Pesticide over 50 day period, first 50% from day 0-6, second 50% from day 7-49 
                    !pesticide_mass_soil(:,day) = pesticide_mass_soil(:,day) + ((appmass(j)/2.)/7. * soil_distribution_2cm)                 
                    !do k=1,6
                      !pesticide_mass_soil(:,day+k) =  pesticide_mass_soil(:,day+k) + ((appmass(j)/2.)/7. * soil_distribution_2cm)
                    !end do
                    !do n=7,49
                      !pesticide_mass_soil(:,day+n) = pesticide_mass_soil(:,day+n) + ((appmass(j)/2.)/43. * soil_distribution_2cm) 
                    !end do      
                     
                    j=1+j   
                end select               
           
            end if
            
            !CHECK IF IT IS A RAIN/WASHOFF DAY
            !calculate reductions on canopy due to degradation and washoff
            if (rain(day) > 0.) then   
                canopy_mass = canopy_mass*exp(-real(day-previous_day)*foliar_degradation) !amount on canopy on rain day
                exponent = -rain(day)*washoff_coeff            
                pesticide_remaining = canopy_mass*exp(exponent)
                
                !pesticide_mass_soil(:,day) = pesticide_mass_soil(:,day)+(canopy_mass-pesticide_remaining)/increments_1  !uniformly distributed to 2 cm                    
                pesticide_mass_soil(day) = pesticide_mass_soil(day)+(canopy_mass-pesticide_remaining)  !REVISED for 1 compartment
                canopy_mass= pesticide_remaining 
                previous_day = day
            end if
         !*******************************************************************
             
           !still need to add in harvest        
           
    end do  Day_LOOP
    
   end subroutine process_pesticide_applications 
    
    
    !
!      integer :: harvest_switch
!      real    :: canopy_to_soil
!      !##########################################################
!
!      !determine the depth node corresponding to each application deposition in soil
!      !now performed in input processing: forall(i=1:naps) depi_node(i) = find_node(number_soil_incr,depth,depi(i))
! 
!      !this is the actual depth of incorporation the program will use for each pesticide application,
!      !which is somehat different than the input depth due to discretization
 !      depth_at_node = depth(depi_node)  !array with depths corresponding to depi_node
 
 !      node_max_depo =maxval(depi_node) !the node of max incorporation depth that`is specified in input


!      !this is the node corresponding to the foliar washoff deposition in the soil
!  !    washoff_node = find_node(number_soil_incr,depth,washoff_depth)
!    
!!number_washoff_days =0
!
!!!check to see if there are any foliar applications, then prepare allocation
!if (any(canopy_pesticide_additions>0.)) then  !there may be cam 2 but on a day with no plants, thus condition is not simply cam 2
!      canopy_mass = 0.
!!      canopy_apply_date = 0
!!      foliar_yes = .TRUE.  !used in pesticide transport module to add in foliar washoff
!      
!      !***** create smaller relevant canopy application arrays ********
!      !****************************************************************
!      number_canopy_apps = count(canopy_pesticide_additions > 0.)
!
!      allocate (canopy_application(number_canopy_apps), STAT= status)
!      allocate (canopy_apply_date (number_canopy_apps), STAT= status)
!
!      !**************************************************************
!      !           get the dates for the canopy applications
!      !              fill the date and application arrays
!      !***************************************************************
!      j=1
!      do i=1, napps
!         if (canopy_pesticide_additions(i) >0) then
!            canopy_apply_date(j) = app_date(i)
!            canopy_application(j)= canopy_pesticide_additions(i)
!            j= j+1
!         end if
!      end do
!      !******************************************************
!      !count the rain days after the first app, these are the relevant washoff days
!
!      number_washoff_days = count(rain(canopy_apply_date(1):num_records) > 0..AND.  plant_factor(canopy_apply_date(1):num_records) > 0. )
!
!      allocate (pesticide_washoff(number_washoff_days), STAT= status)  !this is populated in loop below
!      allocate (washoff_date(number_washoff_days), STAT= status)
!
!      j=1  !application tracker
!      prev_canopymass = 0.
!      previous_day=0
!      k = 0
!      m= 0
!      harvest_switch =0
!
!      !this loop only calculates canopy pest mass on rain days or application days
!      !the output from this loop is "washoff_into_soil" and :"washoff_date"
 !    Day_LOOP: do day = 1, num_records
        
         
 !        !harvest eliminates the canopy
 !        if(plant_factor(day) > 0.) then
 !          harvest_switch = 0
 !
 !          !******this section checks for canopy applications*****************
 ! !         if (day<=canopy_apply_date(number_canopy_apps))then  !prevents checks after last app, otherwise array issues
 !             if (day == canopy_apply_date(j) ) then	
 !                !degradation between apps
 !                canopy_mass = canopy_application(j) +prev_canopymass*exp(-real(day-previous_day)*foliar_degradation)
 !                !update previous value storage
 !                prev_canopymass =canopy_mass
 !                previous_day = day 
 !                j=1+j
 !             end if
 !!          end if
 !
 !          !********** this section checks for rainfall events ***************
 !          !calculate reductions on canopy due to degradation and washoff
 !          if (rain(day) > 0.) then
 !             k=k+1
 !             washoff_date(k) = day  ! <-----OUTPUT-------<<
 !             prev_canopymass = prev_canopymass*exp(-real(day-previous_day)*foliar_degradation)
 !             exponent = -rain(day)*washoff_coeff
 !             pesticide_washoff(k) = prev_canopymass*(1.-exp(exponent)) !  <-----OUTPUT------<<
 !             prev_canopymass= prev_canopymass*exp(exponent)
 !             previous_day = day
 !          end if
 !        !*******************************************************************
 !        else  ! after harvest
 !          if (harvest_switch == 0) then
 !             m= m+1
 !             harvest_date(m)  = day
 !             harvest_to_soil(m) =  prev_canopymass*exp(-real(day-previous_day)*foliar_degradation)
 !             harvest_switch = 1
 !             prev_canopymass = 0.
 !          end if
 !        end if
 !!     end do  Day_LOOP
!!
!!      !populate the array that holds the depositions of washoff into soil
!!       allocate (washoff_into_soil(washoff_node,number_washoff_days),STAT= status)
!!!           allocate (harvest_into_soil(washoff_node,ncpds),STAT= status)
!!
!!       washoff_into_soil=0.
!!       forall (i=1:washoff_node, j=1:number_washoff_days)
!!          !  washoff_into_soil(i,j) = decreasing_distribution(pesticide_washoff(j),depth(washoff_node),depth(i),delta_x(i))
!!          washoff_into_soil(i,j) = uniform_distribution(pesticide_washoff(j),depth(washoff_node),delta_x)
!!       end forall
!!
!!       forall (i=1:washoff_node, j=1:ncpds)
!!           harvest_into_soil(i,j) = decreasing_distribution(harvest_to_soil(j),depth(washoff_node),depth(i),delta_x)
!!       end forall
!!
!!!		     deallocate (pesticide_washoff)
!!             deallocate (canopy_apply_date)
!!             deallocate (canopy_application)  
!end if
!!!%%%%%%%%%%%%%%%%%%  end FOLIAR APPLICATION CAM 2 Calculations     %%%%%%%%%%%%%%%%%
!!!%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
!






!****************************************************************************
pure elemental real function decreasing_distribution(mass,length,position,dx)
    !given a "mass" that is distributed linearly decreasing to "length"
    !for any increment "dx" along the "length", this subroutine will give
    !the amount of mass in that increments "dx"
        implicit none
        real,intent(in) :: mass		!base of triangle
        real,intent(in) :: length	!height of triangle
        real,intent(in) :: position !the cumulative depth at dx
        real,intent(in) :: dx		!the increment size

        decreasing_distribution = mass*dx /length * (2.+ (dx-2.*position)/length)

end function decreasing_distribution



!****************************************************************************
pure elemental real function uniform_distribution(mass,length,dx)
    !given a "mass" that is distributed uniformly to "length"
    !for any increment "dx" along the "length", this subroutine will give
    !the amount of mass in that increments "dx"
        implicit none
        real,intent(in) :: mass		 !width 
        real,intent(in) :: length	 !height 
        real,intent(in) :: dx		 !the increment size

        uniform_distribution = mass*dx /length 

end function uniform_distribution
!*****************************************************************************


end module pesticide_application_module