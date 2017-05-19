FLAGS = -g
PROGS = main test reset
CLEANUP = rmobj rmhd rmother
RMALL = rmexec rmobj rmhd rmother

all: $(PROGS)

test: test.o minheap.o structures.o
	gcc -o test test.o minheap.o structures.o

main: dlite.o minheap.o structures.o
	gcc -o main dlite.o minheap.o structures.o

test.o: test.c minheap.h structures.h
	gcc $(FLAGS) -c test.c

dlite.o: dlite.c minheap.h structures.h
	gcc $(FLAGS) -c dlite.c

minheap.o: minheap.c minheap.h structures.h
	gcc $(FLAGS) -c minheap.c

structures.o: structures.c structures.h
	gcc $(FLAGS) -c structures.c

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