#CC = i686-w64-mingw32-gcc
CC = gcc
FLAGS = -g
PROGS = main reset
CLEANUP = rmobj rmhd rmother
RMALL = rmexec rmobj rmhd rmother

all: $(PROGS)

main: dlite.o minheap.o structures.o
	$(CC) -o main dlite.o minheap.o structures.o

dlite.o: dlite.c minheap.h structures.h
	$(CC) $(FLAGS) -c dlite.c

minheap.o: minheap.c minheap.h structures.h
	$(CC) $(FLAGS) -c minheap.c

structures.o: structures.c structures.h
	$(CC) $(FLAGS) -c structures.c

drmem_m: main
	drmemory main.exe

drmem_t: test
	drmemory.exe test.exe

reset: flight_information.txt
	ruby reset.rb

rmall: $(RMALL)
clean: $(CLEANUP)

rmexec:
	rm -f *.exe
rmobj:
	rm -f *.o
rmhd:
	rm -f *.gch
rmother:
