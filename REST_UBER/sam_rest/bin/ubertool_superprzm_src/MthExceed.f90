Module MthExceed
    implicit none
    contains  
        
        subroutine mthtoxexceed
            use Variables
            use Utilities
            integer :: i
            integer :: day,month,year
    
    !******************************************************************** 
        !Compute monthly exceedances of chronic toxicty threshold
    !********************************************************************            
                mth_chronic_exceed = 0.
             
                do i = 30, ndates   !over all dates, starting at day 30 because doing backward 30d avg
                    call get_date(juliandates(i), YEAR,MONTH,DAY)
                    mthindex(i) = month
                    yrindex(i) = year
                    thirtydayavg(i) = sum(avgconc_adj(i-29:i)*1000000.)/30.  !ug/L
                   
                    if (thirtydayavg(i) .gt. toxthreshold)  then                   
                        selectcase(mthindex(i))
                            case(1)
                                mth_chronic_exceed(1) = mth_chronic_exceed(1) + 1
                            case(2)
                                mth_chronic_exceed(2) = mth_chronic_exceed(2) + 1
                            case(3)
                                mth_chronic_exceed(3) = mth_chronic_exceed(3) + 1
                            case(4)
                                mth_chronic_exceed(4) = mth_chronic_exceed(4) + 1
                            case(5)
                                mth_chronic_exceed(5) = mth_chronic_exceed(5) + 1
                            case(6)
                                mth_chronic_exceed(6) = mth_chronic_exceed(6) + 1
                            case(7)
                                mth_chronic_exceed(7) = mth_chronic_exceed(7) + 1
                            case(8)
                                mth_chronic_exceed(8) = mth_chronic_exceed(8) + 1
                            case(9)
                                mth_chronic_exceed(9) = mth_chronic_exceed(9) + 1
                            case(10)
                                mth_chronic_exceed(10) = mth_chronic_exceed(10) + 1
                            case(11)
                                mth_chronic_exceed(11) = mth_chronic_exceed(11) + 1
                            case(12)
                                mth_chronic_exceed(12) = mth_chronic_exceed(12) + 1
                            end select
                    end if
                end do
        end subroutine mthtoxexceed
    end Module MthExceed
    