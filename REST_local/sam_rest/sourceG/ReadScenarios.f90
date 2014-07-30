Module ReadScenarioFiles
implicit none

contains
    
subroutine ReadScenarios(filename)
    use Variables, ONLY:  leaching,covmax,num_records,numberOfYears,soil_water_m_all,bulk_density, & 
                      delta_x, rain, plant_factor, runoff, Scenario_Path,cropdesired, Number_crop_ids,  area,recipe_name,   &
                      count_runoff ,count_velocity , date_runoff, date_velocity,org_carbon  
    
    implicit none
    character(len=100),intent(in) :: filename
    integer :: ierror, i, reason
    integer:: badscenario

    
    open (UNIT=88, FILE=filename,IOSTAT=ierror, STATUS = 'OLD', FORM ='UNFORMATTED')   
    if (ierror /= 0) then 
                 write(61,*) "problem with ",filename  !Bad_scenario.txt
      return
    end if
   
    read(88) covmax    
    
    read(88) num_records
    
    read(88) numberOfYears 
    
    read(88) count_runoff
    
    do i = 1, count_runoff
         read(88) date_runoff(i), runoff(i)
    end do
    
    read(88) soil_water_m_all(:,1:num_records)    !for 1 compartment
    
    read(88) count_velocity
                 
    do i = 1, count_velocity
         read(88)  date_velocity(i), leaching(i)  !water exiting cell 
    end do 
    

    read(88) org_carbon
    read(88) bulk_density  !scalar     
    
    read(88)               !depth vector
   
    read(88) rain(1:num_records)           
    read(88) plant_factor(1:num_records)

    close(88)

end subroutine ReadScenarios
  
        
end Module ReadScenarioFiles


