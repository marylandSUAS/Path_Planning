#include <stdio.h>
#include <string.h>
#include "minheap.h"
#include "structures.h"

int main(){
	Heap minheap;
	Node node1, node2, node3, node4;
	Node *test1, *test2, *test3, *test4;

	printf("size of node: %d\n", sizeof(Node));

	int cell1[3] = {1,2,3};
	int cell2[3] = {4,5,6};
	int cell3[3] = {7,8,9};
	int cell4[3] = {10,11,12};

	double key1[2] = {1.0,2.0};
	double key2[2] = {2.0,3.0};
	double key3[2] = {1.0,3.0};
	double key4[2] = {4.0,5.0};
	double key5[2] = {1.0,1.0};

	copy_cell(node1.cell,cell1);
	node1.g = 62.235;
	node1.rhs = 353.12;
	copy_key(node1.k,key1);

	copy_cell(node2.cell,cell2);
	node2.g = 6236.1235;
	node2.rhs = 35423.12;
	copy_key(node2.k,key2);

	copy_cell(node3.cell,cell3);
	node3.g = 623.1035;
	node3.rhs = 3543.2;
	copy_key(node3.k,key3);

	copy_cell(node4.cell,cell4);
	node4.g = 6236.10235;
	node4.rhs = 35423.12;
	copy_key(node4.k,key4);

	init_heap(&minheap);

	push_node(&minheap,&node1);
	push_node(&minheap,&node2);
	push_node(&minheap,&node3);
	push_node(&minheap,&node4);

	update_heap(&minheap,&node4,key5);

	test1 = pop_min(&minheap);
	test2 = pop_min(&minheap);
	test3 = pop_min(&minheap);
	test4 = pop_min(&minheap);


	printf("1st g: %f\n", test1->g);
	printf("2nd g: %f\n", test2->g);
	printf("3rd g: %f\n", test3->g);
	printf("4th g: %f\n", test4->g);
}