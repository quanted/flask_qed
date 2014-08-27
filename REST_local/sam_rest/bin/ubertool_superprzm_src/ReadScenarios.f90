Module ReadScenarioFiles
implicit none

contains
    
subroutine ReadScenarios(filename)
    use Variables, ONLY:  leaching,covmax,num_records,numberOfYears,soil_water_m_all,bulk_density, & !increments_1, & !number_soil_incr,& 
                      delta_x, rain, plant_factor, runoff, Scenario_Path,cropdesired, Number_crop_ids,  area,recipe_name,   &
                      count_runoff ,count_velocity , date_runoff, date_velocity,org_carbon  !,depth
    
    implicit none
    character(len=100),intent(in) :: filename
    integer :: ierror   , i

    
    open (UNIT=88, FILE=filename,IOSTAT=ierror, STATUS = 'OLD', FORM ='UNFORMATTED')   
    if (ierror /= 0) then 
                 write(61,*) "problem with ",filename  !Bad_scenario.txt
      return
    end if
   
    read(88) covmax
    !May need to add following:
    !read(88,IOSTAT=reason) covmax
    !if (reason /= 0) then
        !badscenario = 1
        !return
    !end if
    
    
    read(88) num_records
    !May need to add following:
    !read(88,IOSTAT=reason) num_records
    !if (reason /= 0) then
        !badscenario = 1
        !return
    !end if
    read(88) numberOfYears 
    !May need to add following:
    !read(88,IOSTAT=reason) numberOfYears
    !if (reason /= 0) then
        !badscenario = 1
        !return
    !end if
    
    read(88) count_runoff
    !May need to add following:
    !read(88,IOSTAT=reason) count_runoff
    !if (reason /= 0) then
        !badscenario = 1
        !return
    !end if
    
    do i = 1, count_runoff
         read(88) date_runoff(i), runoff(i)
 
    end do
    
    read(88) soil_water_m_all(:,1:num_records)  !REVISED for 1 compartment
    !read(88) soil_water_m_all  (1:increments_1,1:num_records)
    !May need to add following:
    !read(88,IOSTAT=reason) soil_water_m_all(:,1:num_records)
    !if (reason /= 0) then
        !badscenario = 1
        !return
    !end if
    
    read(88) count_velocity
    !May need to add following:
    !read(88,IOSTAT=reason) count_velocity
    !if (reason /= 0) then
        !badscenario = 1
        !return
    !end if
                 
    do i = 1, count_velocity
         read(88)  date_velocity(i), leaching(i)  !leaching(0:increments_1,i)  !water exiting cell 
    end do 
    

    read(88) org_carbon
    read(88) bulk_density  !scalar     
    
    read(88) !depth vector
   
    read(88) rain(1:num_records)           
    read(88) plant_factor(1:num_records)

    close(88)

end subroutine ReadScenarios
  
    

    
end Module ReadScenarioFiles


