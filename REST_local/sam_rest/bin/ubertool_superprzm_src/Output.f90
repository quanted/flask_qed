module Output
implicit none
    contains
    
!****************************************************************
!****OUTPUT EXCEEDANCES OF TOX THRESHOLDS************************
!****************************************************************
   subroutine ExceedTox
   use Variables
  
   integer :: i, numcols, numcols2
   character(len= 100) :: filename
   character(len=100)  :: siteID
   
   siteID = trim(adjustl(recipe_name))
   
    if (toxthrestype .eq. 1) then  !30 day tox exceedances
        if (eco_or_dw == "eco") then
            filename =  "Eco_"//trim(adjustl(recipe_name)) // "_30d_exceedtox.out"  !eco
        else
            filename =  "DWI_"//trim(adjustl(recipe_name)) // "_30d_exceedtox.out"  !dw
        end if
        numcols = 14
        open(UNIT= 59, FILE = trim(Outpath) // filename, RECL = (7*numcols+10))
        write(59,*) "HUC, Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec, Ann"
        write(59,15) trim(adjustl(recipe_name)), mth_chronic_exceed(1),mth_chronic_exceed(2),mth_chronic_exceed(3),&
            mth_chronic_exceed(4),mth_chronic_exceed(5),mth_chronic_exceed(6),mth_chronic_exceed(7),mth_chronic_exceed(8),&
            mth_chronic_exceed(9),mth_chronic_exceed(10),mth_chronic_exceed(11),mth_chronic_exceed(12),sum(mth_chronic_exceed)
15      format(A12,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5)     
    end if
   
    if (toxthrestype .eq. 2) then  !Annual tox exceedances
        if (eco_or_dw == "eco") then
            filename = "Eco_"//trim(adjustl(recipe_name)) // "_ann_exceedtox.out"  !eco
        else
            filename = "DWI_"//trim(adjustl(recipe_name)) // "_ann_exceedtox.out"  !dw
        end if
        numcols2 = 44
        open(UNIT= 59, FILE = trim(Outpath) // filename, RECL = (7*numcols2+10))
        write(59,*) "HUC, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986,&
           1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005,&
            2006, 2007, 2008, 2009, 2010, 2011, 2012"
        write(59,17) trim(adjustl(recipe_name)), ann_chronic_exceed(1),ann_chronic_exceed(2),ann_chronic_exceed(3),&
          ann_chronic_exceed(4),ann_chronic_exceed(5),ann_chronic_exceed(6),ann_chronic_exceed(7),ann_chronic_exceed(8),&
          ann_chronic_exceed(9),ann_chronic_exceed(10),ann_chronic_exceed(11),ann_chronic_exceed(12),ann_chronic_exceed(13),&
          ann_chronic_exceed(14),ann_chronic_exceed(15),ann_chronic_exceed(16),ann_chronic_exceed(17),ann_chronic_exceed(18),&
          ann_chronic_exceed(19),ann_chronic_exceed(20),ann_chronic_exceed(21),ann_chronic_exceed(22),ann_chronic_exceed(23),&
          ann_chronic_exceed(24),ann_chronic_exceed(25),ann_chronic_exceed(26),ann_chronic_exceed(27),ann_chronic_exceed(28),&
          ann_chronic_exceed(29),ann_chronic_exceed(30),ann_chronic_exceed(31),ann_chronic_exceed(32),ann_chronic_exceed(33),&
          ann_chronic_exceed(34),ann_chronic_exceed(35),ann_chronic_exceed(36),ann_chronic_exceed(37),ann_chronic_exceed(38),&
          ann_chronic_exceed(39),ann_chronic_exceed(40),ann_chronic_exceed(41),ann_chronic_exceed(42),ann_chronic_exceed(43)
17      format(A12,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,&
              1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,&
              1x,I5,1x,I5,1x,I5,1x,I5,1x,I5,1x,I5)         
    end if
    
    close(59)
   end subroutine ExceedTox
   
!****************************************************************
!****OUTPUT 30d AVG CONCENTRATIONS DAILY*************************
!****************************************************************
   subroutine ThirtyDayAvg_Output
   use Variables
   integer :: i, numcols, numcols2
   character(len= 100) :: filename
   if (eco_or_dw == "eco") then
       filename =  "Eco_"//trim(adjustl(recipe_name)) // "_30davg.out"  !eco
   else
       filename =  "DWI_"//trim(adjustl(recipe_name)) // "_30davg.out"  !dw
   end if
      
   open(UNIT= 59, FILE = trim(Outpath) // filename) !, RECL = (7*numcols+10))   
   write(59,*) "JulD, 30dAvgConc(ug/L)"
   do i = 1, ndates       
       write(59,15) juliandates(i), thirtydayavg(i)*1000000.
15 format(I6,1x,E11.4)  
   end do
   close(59)
   end subroutine ThirtyDayAvg_Output  
   
!****************************************************************
!****OUTPUT DAILY CONCENTRATIONS ONLY*************************
!****************************************************************
   subroutine Daily_Output
   use Variables
   integer :: i, numcols, numcols2
   character(len= 100) :: filename
   if (eco_or_dw == "eco") then
       filename =  "Eco_"//trim(adjustl(recipe_name)) // "_daily.out"  !eco
   else
       filename =  "DWI_"//trim(adjustl(recipe_name)) // "_daily.out"  !dw
   end if
      
   open(UNIT= 59, FILE = trim(Outpath) // filename) !, RECL = (7*numcols+10))   
   write(59,*) "JulD, Conc(ug/L)"
!14 format(A8,1x,A10)
   do i = 1, ndates       
       write(59,*) juliandates(i), avgconc_adj(i)*1000000.
!15 format(I6,1x,E11.4)  
   end do
   close(59)
   end subroutine Daily_Output 
   
   
!********************************************************************
!Diagnostics outputs for testing purposes - mmf
!********************************************************************
   
   subroutine OutputWrite
   use Variables, ONLY: recipe_name,Total_Runoff_Mass,Total_Runoff, totalarea, area, &
   num_records,OutPath,totalApplied,eco_or_dw,juliandates,rain
   
   !character(len=4) ,intent(in)  :: eco_or_dw 
   integer :: i
   character(len= 100) :: filename

   if (eco_or_dw == "eco") then
     filename =  recipe_name(14:len_trim(recipe_name)-11) // "_pestConc.out"  !eco
   else
     filename =  recipe_name(24:len_trim(recipe_name)-11) // "_pestConc.out"  !dw
   end if
   

   open(UNIT= 55, FILE = trim(Outpath) // filename)
                                   
   write(55,*) "totalApplied (kg): ",totalApplied, "Total_Runoff_Mass/totalApplied: ",sum(Total_Runoff_Mass)/totalApplied
   write(55,*) "Pesticide Mass (kg), Concentration (ug/L)"
   
   do i = 1, num_records
       write(55,*) Total_Runoff_Mass(i), (Total_Runoff_Mass(i)*1000000.)/Total_Runoff(i)  !kg/m3 -> ug/L
   end do
   
   close(55)

   end subroutine OutputWrite   
   
  
   subroutine OutputConc
   use Variables
   
   !character(len=4) ,intent(in)  :: eco_or_dw 
   integer :: i
   character(len= 100) :: filename
   character(len=100)  :: siteID
   
   if (eco_or_dw == "eco") then
     filename =   trim(adjustl(recipe_name)) // "_pestAvgConc_distrib.out"  !recipe_name(14:len_trim(recipe_name)-11) // "_pestAvgConc_distrib.out"  !eco
     siteID = trim(adjustl(recipe_name))
   else
     filename =  trim(adjustl(recipe_name)) // "_pestAvgConc_distrib.out"  !dw
     siteID = trim(adjustl(recipe_name))
   end if
   
   open(UNIT= 59, FILE = trim(Outpath) // filename)
                                   
   write(59,*) "Total_Runoff_Mass/totalApplied: ",sum(Total_Runoff_Mass)/totalApplied
   write(59,*) "NHD Flow(m3/d), AvgSurfRunoff/NHD Flow, Total Area (m2), AvgRunoff (m3/d)"
   write(59,*)  flow, avgrunoff/flow, totalarea, avgrunoff
   !write(59,*) "Mthly avg flows"
   !write(59,*)  flow_scaled
   write(59,*) "JulianDate, TotalFlow(m3/d), Baseflow(m3/d), Runoff(m3/d), AvgConc(ug/L)" !, Mass(kg), AvgConc(ug/L), Runoff(m3/d)"   !SimpleConc (ug/L)
   
   do i = 1, ndates       
       write(59,*) juliandates(i), q_adj_tot(i), baseflow(i), Total_Runoff(start_count-1+i), avgconc_adj(i)*1000000. !, rain(start_count+i), Total_Runoff(start_count+i), Total_Runoff_Mass(start_count+i), avgconc_adj(start_count+i)*1000000. !, conc_simple(start_count+i)*1000000.  !kg/m3->ug/L
   end do
   
   close(59)

   end subroutine OutputConc

  subroutine OutputDiag
     use Variables
   
   integer :: i
   character(len= 100) :: filename
   character(len=100)  :: siteID
   
   if (eco_or_dw == "eco") then
     filename =  recipe_name(14:len_trim(recipe_name)-11) // "_pestDiag.out"  !eco
     siteID = recipe_name(14:len_trim(recipe_name)-11)
   else
     filename =  trim(adjustl(recipe_name)) // "_pestDiag.out"  !dw
     siteID = trim(adjustl(recipe_name))
   end if
   
   open(UNIT= 59, FILE = trim(Outpath) // filename)
   
   write(59,*) "[Daily Runoff Mass/Total Applied] , [Daily Applied/Total Applied]"
   do i = 1, num_records 
       write(59,*) Total_Runoff_Mass(i)/totalApplied, pesticide_mass_soil(i)/totalApplied
       !write(59,*) Total_Runoff_Mass(i)/totalApplied, sum(pesticide_mass_soil(:,i))/totalApplied
   end do
   
   close(59)

  end subroutine OutputDiag

subroutine OutputDiag2
     use Variables
   
   integer :: i
   character(len= 100) :: filename
   character(len=100)  :: siteID
   
   if (eco_or_dw == "eco") then
     filename =  recipe_name(14:len_trim(recipe_name)-11) // "_pestDiag2.out"  !eco
     siteID = recipe_name(14:len_trim(recipe_name)-11)
   else
     filename =  trim(adjustl(recipe_name)) // "_pestDiag2.out"  !dw
     siteID = trim(adjustl(recipe_name))
   end if
   
   open(UNIT= 59, FILE = trim(Outpath) // filename)
   
   write(59,*) "AvgRunoff, TotalArea"

   write(59,*) sum(Total_Runoff)/num_records, totalarea
   
   close(59)

  end subroutine OutputDiag2  
  
end module output