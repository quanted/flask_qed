Module Utilities
    implicit none
    contains
    
    subroutine get_date (date1900, YEAR,MONTH,DAY)  !computes GREGORIAN CALENDAR DATE (YEAR,MONTH,DAY) given days since 1900
    implicit none
    integer,intent(out) :: YEAR,MONTH,DAY
    integer,intent(in)  :: date1900  !days since 1900 (julian date)
    integer :: L,n,i,j
  
   L= 2483590 + date1900
   n= 4*L/146097
   L= L-(146097*n+3)/4
   I= 4000*(L+1)/1461001
   L= L-1461*I/4+31
   J= 80*L/2447
   day= L-2447*J/80
   L= J/11
   month = J+2-12*L
   year = 100*(N-49)+I+L
    end subroutine get_date
    
    subroutine randomf(n1,n2,RANDOM)
        implicit none
        integer,intent(out) :: RANDOM
        integer,intent(in)  :: n1,n2
        
        real  :: r
        call random_number(r)
        random = n1 + int(n2*r)
    end subroutine randomf
    
    !Convert integer to a string - mmf 7/2014
    character(len=20) function str(k)
        integer, intent(in) :: k
        write(str,*) k
        str = adjustl(str)
    end function str
    
end Module Utilities