#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "structures.h"
#include "minheap.h"
// Create, Insert, Extract Min, Empty, Adjust Priority

double empty_heap_key[2] = {max_val,max_val};
int left(int i){ return (2 * i); }
int right(int i){ return (2 * i + 1); }
int parent(int i){ return (i/2); }
int isLeaf(int i, int m){ return (left(i) > m); }
int isRoot(int i){ return (i == 1); }

void init_heap(Heap *root){
	if(root->size){
		root->size = 0;
		root->heap_arr = NULL;
		free(root->heap_arr);
	}
	root -> size = 0;
	root -> heap_arr = NULL;
}

int is_heap_empty(Heap *root){
	return !root->size;
}

// Returns index in array (from 0), otherwise returns -1 if not in heap 
int node_index(Heap *root, Node *graph_node){
	int i, found = 0;
	int size = root->size;
	for(i = 0; i < size; i++){
		if (nodes_equal(root->heap_arr[i],graph_node)){
			found = 1;
			break;
		}
	}
	if (found) 
		return i;
	else
		return -1;
}

void sift_down(Node **A, int i, int m) { // sift down A[i] in A[1..m]
	int l = left(i); // left child
	int r = right(i); // right child
	int curr = i;
	if (l <= m && (compare_keys(A[curr-1]->k,A[l-1]->k) == 1)) curr = l; // left child exists and smaller
	if (r <= m && (compare_keys(A[curr-1]->k,A[r-1]->k) == 1) && (compare_keys(A[r-1]->k,A[l-1]->k) == -1)) curr = r; // right child exists and smaller
	if (curr != i) { // if either child smaller
		Node *temp = A[i-1];
		A[i-1] = A[curr-1];
		A[curr-1] = temp; // swap with larger child
		sift_down(A, curr, m); // and recurse
	}
}

void bubble_up(Node **A, int i){
	int p = parent(i); // parent
	int curr = i;
	if (p > 0 && (compare_keys(A[curr-1]->k,A[p-1]->k) == -1)){ // parent exists and is larger
		curr = p;
		Node *temp = A[i-1];
		A[i-1] = A[curr-1];
		A[curr-1] = temp; // swap with larger parent
		bubble_up(A, curr); // and recurse
	}
}

//If removed, returns true (non-zero)
int remove_node(Heap *root, Node *graph_node){
	int i = node_index(root, graph_node);
	if (i >= 0){
		if(root->size == 1){
			free(root->heap_arr);
			root->size--;
		}else{
			int nodep_size = sizeof(Node *);
			int curr_size = root->size;
			root->heap_arr[i] = root->heap_arr[root->size-1];
			root->heap_arr = (Node **) realloc(root->heap_arr,nodep_size*(curr_size-1));
			root->size--;
			sift_down(root->heap_arr,i+1,root->size);
		}
	}
	return i+1;
}

void push_node(Heap *root, Node *graph_node){
	if(root->size == 0){
		root->heap_arr = (Node **) malloc(sizeof(Node *));
		root->heap_arr[0] = graph_node;
	}else{
		int curr_size = root->size;
		int nodep_size = sizeof(Node *);
		root->heap_arr = (Node **) realloc(root->heap_arr,nodep_size*(curr_size+1));
		root->heap_arr[curr_size] = graph_node;
	}
	root->size++;
	bubble_up(root->heap_arr,root->size);
}

void update_heap(Heap *root, Node *graph_node, double *new_key){
	if (remove_node(root,graph_node)){
		copy_key(graph_node->k,new_key);
		push_node(root,graph_node);
	}
}

Node *pop_min(Heap *root){
	Node *temp = root->heap_arr[0];
	if(root->size == 1){
		free(root->heap_arr);
		root->size--;
	}else{
		int nodep_size = sizeof(Node *);
		int curr_size = root->size;
		root->heap_arr[0] = root->heap_arr[root->size-1];
		root->heap_arr = (Node **) realloc(root->heap_arr,nodep_size*(curr_size-1));
		root->size--;
		sift_down(root->heap_arr,1,root->size);
	}
	return temp;
}

double *top_key(Heap *root){
	if(root->size){
		return root->heap_arr[0]->k;
	}
	return empty_heap_key;
}

Node *top_node(Heap *root){
	if(root->size){
		return root->heap_arr[0];
	}
}