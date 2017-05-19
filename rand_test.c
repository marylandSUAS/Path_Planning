#include <stdlib.h>
#include <math.h>
#include <float.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include "structures.h"
#include "minheap.h"
#include <time.h>

int main(){
	clock_t test1 = clock(), diff1;
	int i,msec1,msec2;
	for(i = 0; i < 100000000; i++){}
	clock_t test2 = clock(), diff2;
	diff2 = clock() - test2;
	msec2 = diff2*1000/CLOCKS_PER_SEC;
	diff1 = clock() - test1;
	msec1 = diff1*1000/CLOCKS_PER_SEC;
	printf("Clock1: %d _ %d",msec1/1000,msec1%1000);
	printf("Clock2: %d _ %d",msec2/1000,msec2%1000);
}