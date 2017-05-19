#include <float.h>

#if !defined(STRUCTURES_H)
#define STRUCTURES_H

#if !defined(max_val)
#define max_val DBL_MAX
#endif

typedef struct{
	int seen;
	int infinite;
	int cell[3];
	double g;
	double rhs;
	double k[2];
} Node;

typedef struct{
	int size;
	Node **heap_arr;
} Heap;

typedef struct obstacle{
	double location[3];
	double radius;
	int mark;
	struct obstacle *next;
} Obstacle;

void copy_node(Node *dst, Node *src);

int compare_keys(double *key1, double *key2);

void copy_cell(int *dst, int *src);

void copy_key(double *dst, double *src);

int nodes_equal(Node *node1, Node *node2);

#endif