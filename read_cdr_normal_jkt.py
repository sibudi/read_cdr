import csv 
import sys #stdout
import glob #directory crawl
import os
import codecs #covert char encoding
import datetime
from cStringIO import StringIO

my_dict = {}
fieldnames = ["1","2","3","4","7","14","16","17","18","20","21","22","23","28","31","32","33","34","35","36","40","41","42","43","44","45","46","47","48","49","66","67","68","69","74","82","83","96","98","99","109","110","113","120","122","128","136","137","194","196","201","203","206","208","209","211","217","223","224","225","227","228","229","230","232","233","235","236","242","251","257","259","260","261","262","263","264","273","274","275","276","281","282","284","285","290","291","292","293","297","300","301","307","308","309","310","311","314","315","317","319","320","322","324","325","326","327","329","331","332","333","335","336","338","340","341","345","349","351","353","354","355","356","357","358","360","361","364","366","368","369","373","374","375","376","377","378","379","380","382","383","384","385","393","395","398","400","419","420","421","422","423","424","425","426","427","451","452","453","454","471","499","503","504","505","506","507","511","512","513","514","515","516","517","552","553","554","555","590","591","600","605","611","612","613","614","615","616","617","618","619","620","629","686","687","801","804","805","806","807","808","809","810","811","813","819","833","834","835","836","837","838","839","841","842","843","844","845","846","848","849","850","851","860","879","884","885","886","887","888","896","897","902","904","905","906","907","908","909","910","911","915","932","944","949","950","951","952","953","982","991","992","993","994","995","996","997","998","1015","1019","1021","1022","1048","1049","1058","1087","1088","1118","1140","1141","1142","1144","1148","1149","1150","1166","1167","1168","1169","1173","1183","1184","1185","1186","1187","1188","1189","1190","1191","1192","1193","1194","1197","1198","1206","1207","1208","1209","1249","1250","1251","1252","1253","1254","1255","1256","1257","1258","1259","1260","1261","1262","1263","1264","1265","1266","1267","1268","1269","1270","1271","1272","1273","1274","1275","1276","1277","1278","1279","1280","1281","1282","1283","1284","1285","1286","1287","1288","1289","1290","1301","1305","1311","1312","1313","1314","1315","1316","1322","1323","1324","1326","1352","1372","1426","1429","1430","1431","1432","1433","1434","filename","partition_date"
]


## store stdout to variable ##
old_stdout = sys.stdout ##store old stdout 
result = StringIO() ##store everything that sent to stdout on result
sys.stdout = result
##

directory = "/backup/backup/cdr/cc/jkt/" #change directory here
extension = "*.s"
delimiter_char = "|"
BLOCKSIZE = 1048576 # or some other, desired size in bytes

#this for loop never execute if no file in this directory, so you need move for inside file checking
file = glob.glob(os.path.join(directory, extension))

if file:
    for file_name in file:
        #file_name = os.path.basename(file_name) #glob return full path, so you need to parse filename only

	###convert encoding###
        with codecs.open(file_name, "r", "ISO-8859-1") as sourceFile:
            with codecs.open(file_name + ".tmp", "w", "utf-8") as targetFile:
                while True:
                    contents = sourceFile.read(BLOCKSIZE)
                    if not contents:
                        break
                    targetFile.write(contents)
        ######################

    #for file_name in glob.glob(directory + extension): 
        with open(file_name + ".tmp", "rb") as fp: #read tmp file as it is a converted file
            for l in fp:
                line = l.strip()
	        if line: #get non empty line
                    if '{' in line and len(line) == 1: #
                        my_dict.clear()

                    elif '}' in line and len(line) == 1:
	                writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, extrasaction='ignore',
				quoting=csv.QUOTE_MINIMAL, delimiter=delimiter_char, #QUOTE_MINIMAL means only field that contains delimiter will be quote otherwise no quote
				doublequote=False, quotechar='\'', 
				escapechar='\'') #output to stdout
		
			my_dict['filename'] = os.path.basename(file_name) #tambahan field filename
			my_dict['partition_date'] = datetime.datetime.strptime(my_dict['3'], '%Y%m%d%H%M%S').strftime('%Y-%m-%d')
		        writer.writerow(my_dict)
		    
                    else:
                        var = line.split('=', 1) ##split string on first occurence delimiter
			try:
                            my_dict[var[0].strip()]=var[1].strip()
                        except IndexError:
                            my_dict[var[0].strip()]=None

	### delete tmp file
        os.remove(file_name + ".tmp")

    sys.stdout = old_stdout ##return again stdout, you can skip this
    result_string = result.getvalue() ##get stdout like string
    result_string = result_string[:-1] ##perlu ditinjau lagi
    print result_string


else:
    ##
    sys.stdout = old_stdout ##return again stdout, you can skip this
    result_string = result.getvalue() ##get stdout like string
    #print result_string
    ##

    sys.exit("Directory is kosong")
