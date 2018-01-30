// Create, Insert, Extract Min, Empty, Adjust Priority
#if !defined(MINHEAP_H)
#define MINHEAP_H

#include "structures.h"

int left(int i);
int right(int i);
int parent(int i);
int isLeaf(int i, int m);
int isRoot(int i);

void init_heap(Heap *root);

int is_heap_empty(Heap *root);

void nullify(Node *node);

int node_index(Heap *root, Node *graph_node);

void sift_down(Node **A, int i, int m);

void bubble_up(Node **A, int i);

int remove_node(Heap *root, Node *graph_node);

void push_node(Heap *root, Node *graph_node);

void update_heap(Heap *root, Node *graph_node, double *new_key);

Node *pop_min(Heap *root);

double *top_key(Heap *root);

Node *top_node(Heap *root);
#endif