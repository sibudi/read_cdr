cd /DATA/CDR/CC/NORMAL

ls -lh > list_file.out

tanggal=`date -d '1 hour ago' "+%-d"`
#bulan=`date -d '1 hour ago' "+%m"`
jam=`date -d '1 hour ago' "+%H"`

start_time=`date +'%Y-%m-%d %H:%M:%S'`

echo "Start Time :" $start_time

	echo "List File in Normal Directory into list_jkt_${tanggal}_$jam.out"
        more list_file.out | awk '{if ($7 == "'"$tanggal"'") print $8"|"$9}' | grep $jam: | grep jkt_in | awk -F'|' '{print $2}' > list_jkt_${tanggal}_$jam.out

	echo list_jkt_${tanggal}_$jam.out

	if [ ! -d  /DATA/backup/cdr/cc/jkt/ ]
	then
		mkdir /DATA/backup/cdr/cc/jkt/
		
		for a in `cat list_jkt_${tanggal}_$jam.out`
                do
                        cd /DATA/CDR/CC/NORMAL
                        echo "MOVE DATA $a into /DATA/backup/cdr/cc/jkt/"
                        mv $a /DATA/backup/cdr/cc/jkt/
                done

                echo "Start Load JKT${jam} :" `date +'%Y-%m-%d %H:%M:%S'`
                psql -a -h 10.1.37.67 -U gpadmin  -d mtrass -c "insert into cdr.cdr_normal_jkt select * from cdr.ext_cdr_normal_jkt"
                echo "END Load JKT${jam} :" `date +'%Y-%m-%d %H:%M:%S'`
	else

		for a in `cat list_jkt_${tanggal}_$jam.out`	
		do 
			cd /DATA/CDR/CC/NORMAL
			echo "MOVE DATA $a into /DATA/backup/cdr/cc/jkt/"
			mv $a /DATA/backup/cdr/cc/jkt/
		done
		
	        echo "Start Load JKT${jam} :" `date +'%Y-%m-%d %H:%M:%S'`
		psql -a -h 10.1.37.67 -U gpadmin  -d mtrass -c "insert into cdr.cdr_normal_jkt select * from cdr.ext_cdr_normal_jkt"
		echo "END Load JKT${jam} :" `date +'%Y-%m-%d %H:%M:%S'`	
	
	fi

	rm -f list_jkt_${tanggal}_$jam.out
	tanggal=$(printf "%02d" $tanggal)
	
	if [ ! -d  /DATA/backup/archive/jkt_${tanggal}_$jam ] 
 	then
		echo "Creating jkt_${tanggal}_$jam Directory"
		mkdir  /DATA/backup/archive/jkt_${tanggal}_$jam
		echo "Moving Data Into jkt_${tanggal}_$jam"
		mv /DATA/backup/cdr/cc/jkt/* /DATA/backup/archive/jkt_${tanggal}_$jam
	else
		echo "Moving Data Into jkt_${tanggal}_$jam" 
		mv /DATA/backup/cdr/cc/jkt/* /DATA/backup/archive/jkt_${tanggal}_$jam
	fi


echo "End Time :" `date +'%Y-%m-%d %H:%M:%S'`
