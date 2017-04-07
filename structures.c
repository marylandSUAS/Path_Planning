#include "structures.h"

void copy_node(Node *dst, Node *src){
	int i;

	copy_cell(dst->cell,src->cell);
	copy_key(dst->k,src->k);

	dst->infinite = src->infinite;
	dst->g = src->g;
	dst->rhs = src->rhs;

}
//-1 if key1 < key2
//0  if key1 = key2
//1  if key1 > key2
int compare_keys(double *key1, double *key2){
	int return_Val = 1;

	if (key1[0] < key2[0]){
		return_Val = -1;
	}else if (key1[0] == key2[0] && key1[1] < key2[1]){
		return_Val = -1;
	}else if (key1[0] == key2[0] && key1[1] == key2[1]){
		return_Val = 0;
	}

	return return_Val;
}

void copy_cell(int *dst, int *src){
	int i;
	for(i = 0; i < 3; i++){
		dst[i] = src[i];
	}
	return;
}

void copy_key(double *dst, double *src){
	dst[0] = src[0];
	dst[1] = src[1];
}

int nodes_equal(Node *node1, Node *node2){
	int i;
	for(i = 0; i < 3; i++){
		if (node1->cell[i] != node2->cell[i]) return 0;
	}
	return 1;
}