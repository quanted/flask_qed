Module ThirtyDayAvgConc
    implicit none
    contains  
        
        subroutine thirtydayconc
            use Variables
            use Utilities
            integer :: i
            integer :: day,month,year
    
    !******************************************************************** 
        !Compute 30-day average concentrations
    !********************************************************************            
                do i = 30, ndates   !over all dates, starting at day 30 because doing backward 30d avg
                    call get_date(juliandates(i), YEAR,MONTH,DAY)
                    mthindex(i) = month
                    yrindex(i) = year
                    thirtydayavg(i) = sum(avgconc_adj(i-29:i)*1000000.)/30.  !ug/L
                end do
        end subroutine thirtydayconc
    end Module ThirtyDayAvgConc