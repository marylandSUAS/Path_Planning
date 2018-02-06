flight_info = File.open("flight_information.txt","r")
flight_info_temp = File.open("flight_info_reset.txt","w")
flight_info_temp.puts("Updated_Obstacles 1\n")
flight_info.gets
while line = flight_info.gets
	flight_info_temp.puts(line)
end
flight_info.close
flight_info_temp.close
flight_info = File.open("flight_information.txt","w")
flight_info_temp = File.open("flight_info_reset.txt","r")
while line = flight_info_temp.gets
	flight_info.puts(line)
end
flight_info.close
flight_info_temp.close