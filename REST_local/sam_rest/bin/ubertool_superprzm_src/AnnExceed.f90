 Module AnnExceed
    implicit none
    contains
        
        subroutine anntoxexceed
            use Variables
            use Utilities
            
            integer :: i
            integer :: day,month,year
            
    
    !******************************************************************** 
        !Compute annual exceedances of chronic toxicty threshold
    !********************************************************************
                ann_chronic_exceed = 0.
                
                do i = 30, ndates   !over all dates, starting at day 30 because doing backward 30d avg
                    call get_date(juliandates(i), YEAR,MONTH,DAY)
                    mthindex(i) = month
                    yrindex(i) = year
                    thirtydayavg(i) = sum(avgconc_adj(i-29:i)*1000000.)/30.  !ug/L
                   
                    if (thirtydayavg(i) .gt. toxthreshold)  then                   
                        selectcase(yrindex(i))
                            case(1970)
                                ann_chronic_exceed(1) = ann_chronic_exceed(1)+1
                            case(1971)
                                ann_chronic_exceed(2) = ann_chronic_exceed(2)+1
                            case(1972)
                                ann_chronic_exceed(3) = ann_chronic_exceed(3)+1
                            case(1973)
                                ann_chronic_exceed(4) = ann_chronic_exceed(4)+1
                            case(1974)
                                ann_chronic_exceed(5) = ann_chronic_exceed(5)+1
                            case(1975)
                                ann_chronic_exceed(6) = ann_chronic_exceed(6)+1
                            case(1976)
                                ann_chronic_exceed(7) = ann_chronic_exceed(7)+1
                            case(1977)
                                ann_chronic_exceed(8) = ann_chronic_exceed(8)+1
                            case(1978)
                                ann_chronic_exceed(9) = ann_chronic_exceed(9)+1
                            case(1979)
                                ann_chronic_exceed(10) = ann_chronic_exceed(10)+1
                            case(1980)
                                ann_chronic_exceed(11) = ann_chronic_exceed(11)+1
                            case(1981)
                                ann_chronic_exceed(12) = ann_chronic_exceed(12)+1
                            case(1982)
                                ann_chronic_exceed(13) = ann_chronic_exceed(13)+1
                            case(1983)
                                ann_chronic_exceed(14) = ann_chronic_exceed(14)+1
                            case(1984)
                                ann_chronic_exceed(15) = ann_chronic_exceed(15)+1
                            case(1985)
                                ann_chronic_exceed(16) = ann_chronic_exceed(16)+1
                            case(1986)
                                ann_chronic_exceed(17) = ann_chronic_exceed(17)+1
                            case(1987)
                                ann_chronic_exceed(18) = ann_chronic_exceed(18)+1
                            case(1988)
                                ann_chronic_exceed(19) = ann_chronic_exceed(19)+1
                            case(1989)
                                ann_chronic_exceed(20) = ann_chronic_exceed(20)+1
                            case(1990)
                                ann_chronic_exceed(21) = ann_chronic_exceed(21)+1
                            case(1991)
                                ann_chronic_exceed(22) = ann_chronic_exceed(22)+1
                            case(1992)
                                ann_chronic_exceed(23) = ann_chronic_exceed(23)+1
                            case(1993)
                                ann_chronic_exceed(24) = ann_chronic_exceed(24)+1
                            case(1994)
                                ann_chronic_exceed(25) = ann_chronic_exceed(25)+1
                            case(1995)
                                ann_chronic_exceed(26) = ann_chronic_exceed(26)+1
                            case(1996)
                                ann_chronic_exceed(27) = ann_chronic_exceed(27)+1
                            case(1997)
                                ann_chronic_exceed(28) = ann_chronic_exceed(28)+1
                            case(1998)
                                ann_chronic_exceed(29) = ann_chronic_exceed(29)+1
                            case(1999)
                                ann_chronic_exceed(30) = ann_chronic_exceed(30)+1
                            case(2000)
                                ann_chronic_exceed(31) = ann_chronic_exceed(31)+1
                            case(2001)
                                ann_chronic_exceed(32) = ann_chronic_exceed(32)+1
                            case(2002)
                                ann_chronic_exceed(33) = ann_chronic_exceed(33)+1
                            case(2003)
                                ann_chronic_exceed(34) = ann_chronic_exceed(34)+1
                            case(2004)
                                ann_chronic_exceed(35) = ann_chronic_exceed(35)+1
                            case(2005)
                                ann_chronic_exceed(36) = ann_chronic_exceed(36)+1
                            case(2006)
                                ann_chronic_exceed(37) = ann_chronic_exceed(37)+1
                            case(2007)
                                ann_chronic_exceed(38) = ann_chronic_exceed(38)+1
                            case(2008)
                                ann_chronic_exceed(39) = ann_chronic_exceed(39)+1
                            case(2009)
                                ann_chronic_exceed(40) = ann_chronic_exceed(40)+1
                            case(2010)
                                ann_chronic_exceed(41) = ann_chronic_exceed(41)+1
                            case(2011)
                                ann_chronic_exceed(42) = ann_chronic_exceed(42)+1
                            case(2012)
                                ann_chronic_exceed(43) = ann_chronic_exceed(43)+1
                        end select
                            
                    end if
                end do
        end subroutine anntoxexceed
    end Module AnnExceed
    