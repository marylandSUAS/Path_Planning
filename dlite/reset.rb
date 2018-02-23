flight_info = File.open("flight_information.txt","r")
flight_info_temp = File.open("flight_info_reset.txt","w")
flight_info_temp.puts("Update 1\n")
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
system('rm flight_info_reset.txt')
if File.exists?('shortest_path_temp.txt')
	system('rm shortest_path_temp.txt')
end
shortest_path = File.open("shortest_path.txt","w")
shortest_path.puts("Changed 0\n")
shortest_path.close
blocks = File.open("3D_blocks.txt","w")
blocks.puts("")
blocks.close
wps = File.open("intermediate_waypoints.txt","w")
wps.puts("Changed 0\n")
wps.close