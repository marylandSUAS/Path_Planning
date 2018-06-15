/*	UMD SUAS Team - Flight Path Algorithm
	Directed by Dr. Huan Xu
	Spring 2017
*/

#include <stdlib.h>
#include <math.h>
#include <float.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include "structures.h"
#include "minheap.h"
#include <time.h>

#define RESOLUTION_X 40 //keep square for 2d interpolation
#define RESOLUTION_Y 40 // keep square for 2d interpolation
#define RESOLUTION_Z 25 //keep unit for 2d interpolation
#define MIN_DIM_SIZE 30
#define CSP 0
#define UPDATE 1
#define DISP 2
#define ADJSUCC 3
#define FILEWRITE 4
#define BLOCK 5
#define HEAP 6
#define OTHER 7

void file_print_current_state();

FILE *information;
FILE *information_temp;
FILE *sp;
FILE *sp_temp;
FILE *wp,*wp2;
int updated_obstacles;

double goal_location[3];
double goal_location_temp[3];
int goal_cell[3];
double start_location[3];
double start_location_temp[3];
int start_cell[3];
double current_location[3];
int current_cell[3];
double origin_location[3];
double x_loc_increment;
double y_loc_increment;
double z_loc_increment;
double altitude_delta;
double current_altitude;
double key_modifier;


//Data structures
Heap minheap;
Heap expanded;
Node grid[RESOLUTION_X][RESOLUTION_Y][RESOLUTION_Z];
struct obstacle *root_obstacle;
int path[RESOLUTION_X][RESOLUTION_Y][RESOLUTION_Z];
//Important nodes
Node *goal_node;
Node *start_node;
Node *current_node;
//Keep track of expanded nodes
int num_expanded;
//Successors and Predecessors wrt current node (calculated and used when needed)
int num_succ, num_adj;
int succ[27][3];
int adj[27][3];
//Compute Update Display
clock_t current_time;
int times[8];

double min(double a, double b){
	return (a > b) ? b:a;
}

double max(double a, double b){
	return (a > b) ? a:b;
}

double get_rhs(int *cell){
	return grid[cell[0]][cell[1]][cell[2]].rhs;
}

double get_g(int *cell){
	return grid[cell[0]][cell[1]][cell[2]].g;
}

double interpolate_height(int *current_coord){
	double height = 0;
	height += altitude_delta*current_coord[0]/(2*RESOLUTION_X);
	height += altitude_delta*current_coord[1]/(2*RESOLUTION_Y);
	return height;
}

double compute_heuristic(int *curr, int *goal){
	clock_t other = clock(),diff;

	double x_val = 0.0;
	double y_val = 0.0;
	double z_val = 0.0;
	double heuristic = 0.0;

	x_val = fabs((goal[0] - curr[0]) * x_loc_increment);
	y_val = fabs((goal[1] - curr[1]) * y_loc_increment);
	z_val = (goal[2] - curr[2]) * z_loc_increment;

	z_val = z_val > 0 ? z_val * 1.25 : z_val * -0.8;
	
	heuristic = sqrt(pow(x_val,2)+pow(y_val,2)+pow(z_val,2));

	diff = clock() - other;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[OTHER] += msec;

	return heuristic;
}

void calc_key(double *update, int *cell){
	clock_t other = clock(),diff;

	update[1] = min(get_g(cell),get_rhs(cell));
	update[0] = update[1]+compute_heuristic(current_node->cell,cell)+key_modifier;

	diff = clock() - other;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[OTHER] += msec;
}

void update_vertex(Node *node){
	double g = node->g;
	double rhs = node->rhs;
	double new_key[2];

	calc_key(new_key,node->cell);

	clock_t other = clock(),diff;

	int index = node_index(&minheap,node);

	if(g!=rhs && index >= 0){
		//g != rhs AND u E U
		update_heap(&minheap,node,new_key);
	}else if(g!=rhs && index == -1){
		//g != rhs AND u !E U
		copy_key(node->k,new_key);
		push_node(&minheap,node);
	}else if(g==rhs && index >= 0){
		//g == rhs AND u E U
		remove_node(&minheap,node);
	}

	diff = clock() - other;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[OTHER] += msec;
}

int is_expanded(Node *node){
	// int i;
	// for(i = 0; i < num_expanded; i++){
	// 	if (nodes_equal(node,expanded_nodes[i])){
	// 		return 1;
	// 	}
	// }
	// return 0;

	// if(node_index(&expanded,node) > -1)
	// 	return 1;
	// else
	// 	return 0;
	return node->expanded;

}

void add_expanded(Node *node){
	clock_t other = clock(),diff;

	// printf("Expanding node: {%d,%d,%d} at location {%lf,%lf,%lf} with key_value: {%lf, %lf}\n",node->cell[0],node->cell[1],node->cell[2],
		// node->cell[0]*x_loc_increment+origin_location[0],node->cell[1]*y_loc_increment+origin_location[1],
		// node->cell[2]*z_loc_increment+origin_location[2],node->k[0],node->k[1]);

	// push_node(&expanded,node);
	// num_expanded++;
	node->expanded = 1;

	diff = clock() - other;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[OTHER] += msec;
}

void empty_expanded(){
	clock_t other = clock(), diff;

	while(expanded.heap_arr)
		pop_min(&expanded);
	// if(num_expanded){
	// 	expanded_nodes = NULL;
	// 	num_expanded = 0;
	// 	free(expanded_nodes);
	// }
	num_expanded = 0;

	diff = clock() - other;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[OTHER] += msec;
}

void remove_expanded(Node *node){
	clock_t other = clock(), diff;

	// remove_node(&expanded,node);
	node->expanded = 0;
	num_expanded--;

	diff = clock() - other;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[OTHER] += msec;
}
int in_bounds(int *cell){
	clock_t other = clock(), diff;

	if(cell[0] >= 0 && cell[1] >= 0 && cell[2] >= 0
		&& cell[0] < RESOLUTION_X && cell[1] < RESOLUTION_Y
		&& cell[2] < RESOLUTION_Z
		// && (cell[2]*z_loc_increment+origin_location[2]) >= flight_floor
		// && (cell[2]*z_loc_increment+origin_location[2]) <= flight_ceiling){
		){

		diff = clock() - other;
		int msec = diff * 1000 / CLOCKS_PER_SEC;
		times[OTHER] += msec;

		return 1;
	}
	diff = clock() - other;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[OTHER] += msec;

	return 0;
}

double cost(Node *node1, Node *node2){
	if (node1->infinite || node2->infinite){
		return max_val;
	}
	return compute_heuristic(node1->cell,node2->cell);
}

void init_graph_node(Node *graph_node, int *cell){
	clock_t other = clock(),diff;

	if(graph_node->seen){
		return;
	}
	copy_cell(graph_node->cell,cell);
	graph_node->g = max_val;
	graph_node->rhs = max_val;

	diff = clock() - other;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[OTHER] += msec;
}

void clear_adj(){
	int i = 0;
	for(i; i < 27; i++){
		adj[i][0] = 0;
		adj[i][1] = 0;
		adj[i][2] = 0;
	}
}

void calc_adj(Node *node){
	clock_t adjsucc = clock(), diff;

	int *cell = node->cell;
	int check_adj[3];
	int i,j,k;
	clear_adj();
	num_adj = 0;

	for(i = 0; i < 3; i++){
		for(j = 0; j < 3; j++){
			for(k = 0; k < 3; k++){
				check_adj[0] = cell[0]+i-1;
				check_adj[1] = cell[1]+j-1;
				check_adj[2] = cell[2]+k-1;
				if(in_bounds(check_adj) &&
					!(check_adj[0] == cell[0] &&
					  check_adj[1] == cell[1] &&
					  check_adj[2] == cell[2]) &&
					!(is_expanded(&(grid[check_adj[0]][check_adj[1]][check_adj[2]])))){
					adj[num_adj][0] = check_adj[0];
					adj[num_adj][1] = check_adj[1];
					adj[num_adj][2] = check_adj[2];
					num_adj++;
				}
			}
		}
	}

	diff = clock() - adjsucc;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[ADJSUCC] += msec;

	return;
}

void copy_adj(int **backup){
	int i;
	for(i = 0; i < num_adj; i++){
		backup[i][0] = adj[i][0];
		backup[i][1] = adj[i][1];
		backup[i][2] = adj[i][2];
	}
	return;
}

void clear_succ(){
	int i = 0;
	for(i; i < 27; i++){
		succ[i][0] = 0;
		succ[i][1] = 0;
		succ[i][2] = 0;
	}
}

void calc_succ(Node *node){
	clock_t adjsucc = clock(), diff;

	int *cell = node->cell;
	int check_succ[3];
	int index = 0;
	int i,j,k;
	clear_succ();
	num_succ = 0;

	for(i = 0; i < 3; i++){
		for(j = 0; j < 3; j++){
			for(k = 0; k < 3; k++){
				check_succ[0] = cell[0]+i-1;
				check_succ[1] = cell[1]+j-1;
				check_succ[2] = cell[2]+k-1;
				i = i + 0;
				if(in_bounds(check_succ) &&
					!(check_succ[0] == cell[0] &&
					  check_succ[1] == cell[1] &&
					  check_succ[2] == cell[2]) &&
					!(grid[check_succ[0]][check_succ[1]][check_succ[2]].infinite >= 1)
					// && is_expanded(&(grid[check_succ[0]][check_succ[1]][check_succ[2]]))
					){

					succ[index][0] = check_succ[0];
					succ[index][1] = check_succ[1];
					succ[index][2] = check_succ[2];
					num_succ++;
					index++;
				}
			}
		}
	}
	diff = clock() - adjsucc;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[ADJSUCC] += msec;
	return;
}

void update_current_node(){
	clock_t other = clock(), diff;

	current_cell[0] = 0;
	current_cell[1] = 0;
	current_cell[2] = 0;
	int x_diff = (current_location[0]-start_location[0])/x_loc_increment;
	int y_diff = (current_location[1]-start_location[1])/y_loc_increment;
	int z_diff = (current_location[2]-start_location[2])/z_loc_increment;
	current_cell[0] = start_cell[0] + x_diff;
	current_cell[1] = start_cell[1] + y_diff;
	current_cell[2] = start_cell[2] + z_diff;
	current_cell[0] = (current_cell[0] >= 0) ? current_cell[0] : 0;
	current_cell[1] = (current_cell[1] >= 0) ? current_cell[1] : 0;
	current_cell[2] = (current_cell[2] >= 0) ? current_cell[2] : 0;
	current_node = &(grid[current_cell[0]][current_cell[1]][current_cell[2]]);
	init_graph_node(current_node,current_cell);

	diff = clock() - other;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[OTHER] += msec;
}

void initialize(double *start, double *goal){
	// clock_t other = clock(), diff;
	// int i,j,k;
	// int cell[3];

	// // for(i = 0; i < RESOLUTION_X; i++){
	// // 	for(j = 0; j < RESOLUTION_Y; j++){
	// // 		for(k = 0; k < RESOLUTION_Z; k++){
	// // 			cell[0] = i; cell[1] = j; cell[2] = k;
	// // 			init_graph_node(&(grid[i][j][k]),cell);
	// // 		}
	// // 	}
	// // }

	// init_heap(&minheap);
	// init_heap(&expanded);
	// key_modifier = 0.0;
	// num_expanded = 0;
	// double temp;

	// double x_dist = goal_location[0] - start_location[0];
	// double y_dist = goal_location[1] - start_location[1];
	// double z_dist = goal_location[2] - start_location[2];
	// min_x_dist = (abs(x_dist) > 120) ? (abs(x_dist)+30) : 120;
	// min_y_dist = (abs(y_dist) > 120) ? (abs(y_dist)+30) : 120;
	// min_z_dist = (abs(z_dist) > 120) ? (abs(z_dist)+30) : 120;
	// x_loc_increment = min_x_dist/RESOLUTION_X;
	// y_loc_increment = min_y_dist/RESOLUTION_Y;
	// z_loc_increment = min_z_dist/RESOLUTION_Z;

	// double x_offset = (min_x_dist-abs(x_dist))/2;
	// double y_offset = (min_y_dist-abs(y_dist))/2;
	// double z_offset = (min_z_dist-abs(z_dist))/2;
	// int x_cell_offset = (x_offset/x_loc_increment);
	// int y_cell_offset = (y_offset/y_loc_increment);
	// int z_cell_offset = (z_offset/z_loc_increment);
	// int x_cell_dist = abs(x_dist/x_loc_increment);
	// int y_cell_dist = abs(y_dist/y_loc_increment);
	// int z_cell_dist = abs(z_dist/z_loc_increment);

	// if(x_dist > 0){
	// 	goal_cell[0] = x_cell_offset + x_cell_dist-1;
	// 	start_cell[0] = x_cell_offset;
	// }else{
	// 	goal_cell[0] = x_cell_offset;
	// 	start_cell[0] = x_cell_offset + x_cell_dist-1;
	// }
	// if(y_dist > 0){
	// 	goal_cell[1] = y_cell_offset + y_cell_dist-1;
	// 	start_cell[1] = y_cell_offset;
	// }else{
	// 	goal_cell[1] = y_cell_offset;
	// 	start_cell[1] = y_cell_offset + y_cell_dist-1;
	// }if(z_dist > 0){
	// 	goal_cell[2] = z_cell_offset + z_cell_dist-1;
	// 	start_cell[2] = z_cell_offset;
	// }else{		
	// 	goal_cell[2] = z_cell_offset;
	// 	start_cell[2] = z_cell_offset + z_cell_dist-1;
	// }
	// goal_node = &(grid[goal_cell[0]][goal_cell[1]][goal_cell[2]]);
	// start_node = &(grid[start_cell[0]][start_cell[1]][start_cell[2]]);

	// origin_location[0] = start_location[0]-start_cell[0]*x_loc_increment;
	// origin_location[1] = start_location[1]-start_cell[1]*y_loc_increment;
	// origin_location[2] = start_location[2]-start_cell[2]*z_loc_increment;

	// init_graph_node(goal_node, goal_cell);
	// init_graph_node(start_node, start_cell);
	// update_current_node();

	// goal_node->rhs = 0;
	// diff = clock() - other;
	// goal_node->k[0] = compute_heuristic(current_node->cell,goal_node->cell);
	// other = clock();
	// goal_node->k[1] = 0;
	// goal_node->seen = 1;

	// push_node(&minheap,goal_node);
	// diff += clock() - other;
	// int msec = diff * 1000 / CLOCKS_PER_SEC;
	// times[OTHER] += msec;
// 1 - decide buffer space
//		Each dimension should be at least 100m, or buffer space should be at least 20% in each dimension
// 2 - set in goal and start nodes
// 3 - calculate location increment
	clock_t other = clock(), diff;

	init_heap(&minheap);
	init_heap(&expanded);
	key_modifier = 0.0;
	num_expanded = 0;

	double buffer_percent = 10; // [%] for each side of the dimension --- |buffer_percent|____________________|buffer_percent|
	buffer_percent = buffer_percent/100; // decimal percent
	double dx = goal[0] - start[0];
	double dy = goal[1] - start[1];
	double dz = goal[2] - start[2];
	int x_n_nominal = abs(dx) > 0 ? 1 : 0;
	int y_n_nominal = abs(dy) > 0 ? 1 : 0;
	int z_n_nominal = abs(dz) > 0 ? 1 : 0;
	double x_dim_size = MIN_DIM_SIZE;
	double y_dim_size = MIN_DIM_SIZE;
	double z_dim_size = MIN_DIM_SIZE;
	if(abs(dx) >= x_dim_size){
		x_dim_size = abs(dx + buffer_percent*dx);
	}
	if(abs(dy) >= y_dim_size){
		y_dim_size = abs(dy + buffer_percent*dy);
	}
	if(abs(dz) >= z_dim_size){
		z_dim_size = abs(dz + buffer_percent*dz);
	}

	if(abs(dx) >= x_dim_size/RESOLUTION_X){
		x_n_nominal = RESOLUTION_X*abs(dx)/x_dim_size;
		if((RESOLUTION_X-x_n_nominal)%2!=0){
			x_n_nominal --;
		}
	}
	x_loc_increment = abs(dx) > 0 ? abs(dx)/x_n_nominal : x_dim_size/RESOLUTION_X;

	if(abs(dy) >= y_dim_size/RESOLUTION_Y){
		y_n_nominal = RESOLUTION_Y*abs(dy)/y_dim_size;
		if((RESOLUTION_Y-y_n_nominal)%2!=0){
			y_n_nominal --;
		}
	}
	y_loc_increment = abs(dy) > 0 ? abs(dy)/y_n_nominal : y_dim_size/RESOLUTION_Y;

	if(abs(dz) >= z_dim_size/RESOLUTION_Z){
		z_n_nominal = RESOLUTION_Z*abs(dz)/z_dim_size;
		if((RESOLUTION_Z-z_n_nominal)%2!=0){
			z_n_nominal --;
		}
	}
	z_loc_increment = abs(dz) > 0 ? abs(dz)/z_n_nominal : z_dim_size/RESOLUTION_Z;


	// Grid should be at least <MIN_DIM_SIZE> in each dimension
	// If a dimension is at least that, inset to allow <Buffer %> ammount of buffer
	// Otherwise, set size to <MIN_DIM_SIZE>
	int x_inset = (RESOLUTION_X-x_n_nominal)/2;
	int y_inset = (RESOLUTION_Y-y_n_nominal)/2;
	int z_inset	= (RESOLUTION_Z-z_n_nominal)/2;
	if(dx > 0){
		goal_cell[0] = x_inset+x_n_nominal;
		start_cell[0] = x_inset;
	}else{
		goal_cell[0] = x_inset;
		start_cell[0] = x_inset+x_n_nominal;
	}
	if(dy > 0){
		goal_cell[1] = y_inset+y_n_nominal;
		start_cell[1] = y_inset;
	}else{
		goal_cell[1] = y_inset;
		start_cell[1] = y_inset+y_n_nominal;
	}
	if(dz > 0){
		goal_cell[2] = z_inset+z_n_nominal;
		start_cell[2] = z_inset;
	}else{
		goal_cell[2] = z_inset;
		start_cell[2] = z_inset+z_n_nominal;
	}
	goal_node = &(grid[goal_cell[0]][goal_cell[1]][goal_cell[2]]);

	start_node = &(grid[start_cell[0]][start_cell[1]][start_cell[2]]);

	origin_location[0] = start_location[0]-start_cell[0]*x_loc_increment;
	origin_location[1] = start_location[1]-start_cell[1]*y_loc_increment;
	origin_location[2] = start_location[2]-start_cell[2]*z_loc_increment;

	init_graph_node(goal_node, goal_cell);
	init_graph_node(start_node, start_cell);
	update_current_node();

	goal_node->rhs = 0;
	diff = clock() - other;
	goal_node->k[0] = compute_heuristic(current_node->cell,goal_node->cell);
	other = clock();
	goal_node->k[1] = 0;
	goal_node->seen = 1;

	push_node(&minheap,goal_node);
	diff += clock() - other;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[OTHER] += msec;
}

void compute_shortest_path(){
	clock_t csp, diff = 0;
	printf("Computing Shortest\n");
	double k_old[2];
	double k_new[2];
	double g_old = 0.0;
	double current_key[2];
	int i,j;
	double min_succ_rhs;
	double c,c2;
	double new_rhs;
	Node *u;

	calc_key(current_key,current_node->cell);

	csp = clock();
	while(compare_keys(top_key(&minheap),current_key) <= 0 || current_node->rhs != current_node->g){
		// printf("Num Expanded: %d\n", num_expanded);
		// diff += clock() - csp;
		// file_print_current_state(start_cell[2]);
		// csp = clock();
		u = top_node(&minheap);
		copy_key(k_old,top_key(&minheap));
		calc_key(k_new,u->cell);
		if(compare_keys(k_old,k_new) == -1){
			update_heap(&minheap,u,k_new);
		}else if(u->g > u->rhs){
			u->g = u->rhs;
			remove_node(&minheap,u);
			add_expanded(u);
			calc_adj(u);
			for(i = 0; i < num_adj; i++){ // for all s in Pred(u)
				Node *s = &(grid[adj[i][0]][adj[i][1]][adj[i][2]]);
				if(!(s->seen)){
					int adj_cell[3] = {adj[i][0],adj[i][1],adj[i][2]};
					init_graph_node(s,adj_cell);
					s->seen = 1;
				}
				c = cost(s,u);
				new_rhs = min(s->rhs,c+u->g);	//rhs(s) = min(rhs(s),c(s,u) + g(u))
				s->rhs = new_rhs;
				update_vertex(s); //updateVertex(s)
			}
		}else{
			g_old = u->g;
			u->g = max_val;
			calc_adj(u);
			for(i = 0; i < num_adj; i++){ //for all s in Pred(u) U {u}
				if(!(adj[i][0] == -1)){ // if s is a valid adj (not out of bounds, or already expanded)
					Node *s = &(grid[adj[i][0]][adj[i][1]][adj[i][2]]);
					if(!(s->seen)){
						int adj_cell[3] = {adj[i][0],adj[i][1],adj[i][2]};
						init_graph_node(s,adj_cell);
						s->seen = 1;
					}
					c = cost(s,u);
					if(s->rhs == (c + g_old)){ //if rhs(s) == c(s,u) + g_old
						if(!nodes_equal(s,goal_node)){ // if (s != s_goal)
							calc_succ(s);
							min_succ_rhs = max_val; //s->rhs = min (s' E Succ(s)) (c(s,s')+g(s'))
							for(j = 0; j < num_succ; j++){
								Node *succs = &(grid[succ[j][0]][succ[j][1]][succ[j][2]]);
								if(!(succs->seen)){
									int succ_cell[3] = {succ[j][0],succ[j][1],succ[j][2]};
									init_graph_node(succs,succ_cell);
									succs->seen = 1;
								}
								c2 = cost(s,succs);
								new_rhs = c2+succs->g;
								min_succ_rhs = (new_rhs < min_succ_rhs) ? new_rhs : min_succ_rhs;
							}
							s->rhs = min_succ_rhs;
						}						
					}
					update_vertex(s);
				}
			}
			// Do the same to u as was done for all s in Pred(u)
			Node *s = u;
			c = cost(s,u);
			if(s->rhs == c + g_old){ //if rhs(s) == c(s,u) + g_old
				if(!nodes_equal(s,goal_node)){ // if (s != s_goal)
					calc_succ(s);
					min_succ_rhs = max_val; //s->rhs = min (s' E Succ(s)) (c(s,s')+g(s'))
					for(i = 0; i < num_succ; i++){
						Node *succs = &(grid[succ[i][0]][succ[i][1]][succ[i][2]]);
						if(!(succs->seen)){
							int succ_cell[3] = {succ[i][0],succ[i][1],succ[i][2]};
							init_graph_node(succs,succ_cell);
							succs->seen = 1;
						}
						c2 = cost(s,succs);
						new_rhs = c2+succs->g;
						min_succ_rhs = (new_rhs < min_succ_rhs) ? new_rhs : min_succ_rhs;
					}
					s->rhs = min_succ_rhs;
				}						
			}
			update_vertex(s);
		}
		calc_key(current_key,current_node->cell);
	}
	diff = clock() - csp;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[CSP] += msec;
}

void clear(char *buff, int size){
	clock_t other = clock(), diff;

	int i;
	for(i = 0; i < size; i++){
		buff[i] = '\0';
	}

	diff = clock() - other;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[OTHER] += msec;
}

void clear_path(){
	clock_t other = clock(), diff;

	int i,j,k;
	for(i = 0; i < RESOLUTION_X; i++){
		for(j = 0; j < RESOLUTION_Y; j++){
			for(k = 0; k < RESOLUTION_Z; k++){
				path[i][j][k] = (path[i][j][k] == 2) ? 2 : 0;
			}
		}
	}

	diff = clock() - other;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[OTHER] += msec;
}

void closestPoint(double *gl, double *st, double *ob, double *close){
	double lin[3] = {gl[0]-st[0],gl[1]-st[1],gl[2]-st[2]};
	double length = sqrt(pow(lin[0],2)+pow(lin[1],2)+pow(lin[2],2));
	double ln[3] = {lin[0]/length,lin[1]/length,lin[2]/length};
	double t = (((ob[0]-st[0])*ln[0])+((ob[1]-st[1])*ln[1])+(ln[2]*(ob[2]-st[2])))/(pow(ln[0],2)+pow(ln[1],2)+pow(ln[2],2));
	if (t < 0)
		t = 0;
	else if(t > length)
		t = length;
	double cp[3] = {st[0]+ln[0]*t,st[1]+ln[1]*t,st[2]+ln[2]*t};
	close[0] = cp[0];
	close[1] = cp[1];
	close[2] = cp[2];
	return;
}

double distFromPath(double *st, double *gl, double *ob){
	double close[3];
	closestPoint(gl, st, ob, close);
	double d = sqrt(pow((ob[0]-close[0]),2)+pow((ob[1]-close[1]),2)+pow((ob[2]-close[2]),2));
	return d;
}

// double dist3D_Segment_to_Segment(double *node1,double *node2, double *static_loc){
//     double u[3] = {node2[0]-node1[0],node2[1]-node1[1],node2[2]-node1[2]};
//     double v[3] = {0.0,0.0,300};
//     double w[3] = {node1[0]-static_loc[0],node1[1]-static_loc[1],node1[2]-0.0};
//     // Vector   u = S1.P1 - S1.P0;
//     // Vector   v = S2.P1 - S2.P0;
//     // Vector   w = S1.P0 - S2.P0;
//     double    a = u[0]*u[0]+u[1]*u[1]+u[2]*u[2];         // always >= 0
//     double    b = u[0]*v[0]+u[1]*v[1]+u[2]*v[2];
//     double    c = v[0]*v[0]+v[1]*v[1]+v[2]*v[2];         // always >= 0
//     double    d = u[0]*w[0]+u[1]*w[1]+u[2]*w[2];
//     double    e = u[0]*w[0]+v[1]*w[1]+v[2]*w[2];
//     double    D = a*c - b*b;        // always >= 0
//     double    sc, sN, sD = D;       // sc = sN / sD, default sD = D >= 0
//     double    tc, tN, tD = D;       // tc = tN / tD, default tD = D >= 0
//     double SMALL_NUM = 0.1;

//     // compute the line parameters of the two closest points
//     if (D < SMALL_NUM) { // the lines are almost parallel
//         sN = 0.0;         // force using point P0 on segment S1
//         sD = 1.0;         // to prevent possible division by 0.0 later
//         tN = e;
//         tD = c;
//     }
//     else {                 // get the closest points on the infinite lines
//         sN = (b*e - c*d);
//         tN = (a*e - b*d);
//         if (sN < 0.0) {        // sc < 0 => the s=0 edge is visible
//             sN = 0.0;
//             tN = e;
//             tD = c;
//         }
//         else if (sN > sD) {  // sc > 1  => the s=1 edge is visible
//             sN = sD;
//             tN = e + b;
//             tD = c;
//         }
//     }

//     if (tN < 0.0) {            // tc < 0 => the t=0 edge is visible
//         tN = 0.0;
//         // recompute sc for this edge
//         if (-d < 0.0)
//             sN = 0.0;
//         else if (-d > a)
//             sN = sD;
//         else {
//             sN = -d;
//             sD = a;
//         }
//     }
//     else if (tN > tD) {      // tc > 1  => the t=1 edge is visible
//         tN = tD;
//         // recompute sc for this edge
//         if ((-d + b) < 0.0)
//             sN = 0;
//         else if ((-d + b) > a)
//             sN = sD;
//         else {
//             sN = (-d +  b);
//             sD = a;
//         }
//     }
//     // finally do the division to get sc and tc
//     sc = (abs(sN) < SMALL_NUM ? 0.0 : sN / sD);
//     tc = (abs(tN) < SMALL_NUM ? 0.0 : tN / tD);

//     // get the difference of the two closest points
//     // double dP[3] = w + (sc * u) - (tc * v);  // =  S1(sc) - S2(tc)
//     double dp[3] = {w[0]+(sc*u[0])-(tc*v[0]),w[1]+(sc*u[1])-(tc*v[1]),w[2]+(sc*u[2])-(tc*v[2])};
//     return sqrt(pow(dp[0],2)+pow(dp[1],2)+pow(dp[2],2));   // return the closest distance
// }

double line_of_sight_cylinder(double *N1, double *N2, double *O){
	double dist = sqrt(pow((N1[2] - ((N1[2] - N2[2])*(pow(O[2],2)*(N1[0] - O[0])*(N1[0] - N2[0]) + pow(O[2],2)*(N1[1] - O[1])*(N1[1] - N2[1])))/(pow(O[2],2)*(N1[0] - N2[0])*(N1[0] - N2[0]) + pow(O[2],2)*(N1[1] - N2[1])*(N1[1] - N2[1])) + (O[2]*(O[2]*(N1[0] - O[0])*(N1[0] - N2[0])*(N1[2] - N2[2]) - N1[2]*(O[2]*pow((N1[0] - N2[0]),2) + O[2]*pow((N1[1] - N2[1]),2)) + O[2]*(N1[1] - O[1])*(N1[1] - N2[1])*(N1[2] - N2[2])))/(O[2]*(O[2]*pow((N1[0] - N2[0]),2) + O[2]*pow((N1[1] - N2[1]),2)))),2) + pow((O[0] - N1[0] + ((N1[0] - N2[0])*(pow(O[2],2)*(N1[0] - O[0])*(N1[0] - N2[0]) + pow(O[2],2)*(N1[1] - O[1])*(N1[1] - N2[1])))/(pow(O[2],2)*(N1[0] - N2[0])*(N1[0] - N2[0]) + pow(O[2],2)*(N1[1] - N2[1])*(N1[1] - N2[1]))),2) + pow((O[1] - N1[1] + ((N1[1] - N2[1])*(pow(O[2],2)*(N1[0] - O[0])*(N1[0] - N2[0]) + pow(O[2],2)*(N1[1] - O[1])*(N1[1] - N2[1])))/(pow(O[2],2)*(N1[0] - N2[0])*(N1[0] - N2[0]) + pow(O[2],2)*(N1[1] - N2[1])*(N1[1] - N2[1]))),2));
	return dist;
}

int line_of_sight(Node *node1, Node *node2, struct obstacle *curr){
	double obst_loc[3];  
	double obst_rad;
	double node1_loc[3];
	double node2_loc[3];
	double vertex1[3] = {0.0,0.0,0.0};
	double vertex2[3] = {0.0,0.0,0.0};
	double x;
	char buff[256];

	node1_loc[0] = node1->cell[0]*x_loc_increment + origin_location[0];
	node1_loc[1] = node1->cell[1]*y_loc_increment + origin_location[1];
	node1_loc[2] = node1->cell[2]*z_loc_increment + origin_location[2];
	node2_loc[0] = node2->cell[0]*x_loc_increment + origin_location[0];
	node2_loc[1] = node2->cell[1]*y_loc_increment + origin_location[1];
	node2_loc[2] = node2->cell[2]*z_loc_increment + origin_location[2];

	if(curr){
		obst_loc[0] = curr->location[0];
		obst_loc[1] = curr->location[1];
		obst_loc[2] = curr->location[2];
		obst_rad = curr->radius;
		if(curr->type == 1){
			// if(node2_loc[2] < obst_loc[2] || node1_loc[2] < obst_loc[2]){
			node2_loc[2] = 0;
			node1_loc[2] = 0;
			obst_loc[2] = 0;
			x = distFromPath(node2_loc,node1_loc,obst_loc);
			// printf("Node1: [%lf %lf %lf] Node2: [%lf %lf %lf]\n\tObst: [%lf %lf %lf] %lf Dist: %lf\n",
			// 	node1_loc[0],node1_loc[1],node1_loc[2],node2_loc[0],node2_loc[1],node2_loc[2],
			// 	obst_loc[0],obst_loc[1],obst_loc[2],obst_rad,x);
			if(x <= obst_rad)
				return 0;
			// }
		}else{
			x = distFromPath(node2_loc,node1_loc,obst_loc);
			if(x <= obst_rad)
				return 0;
		}
		if(curr->next){
			return line_of_sight(node1,node2,curr->next);
		}
	}
	double dx,dy,boundary_slope,virtual_slope = 0.0;
	clear(buff,256);
	FILE *boundary_handle = fopen("boundary.txt","r");
	if(boundary_handle){
		fgets(buff,256,boundary_handle);
		sscanf(buff,"%lf %lf",&vertex2[0],&vertex2[1]);
		
		while(fgets(buff,256,boundary_handle)){
			vertex1[0] = vertex2[0]; vertex1[1] = vertex2[1];
			sscanf(buff,"%lf %lf",&vertex2[0],&vertex2[1]);

			double st[2] = {node1_loc[0],node1_loc[1]};
			double gl[2] = {node2_loc[0],node2_loc[1]};
			double b1[2] = {vertex2[0],vertex2[1]};
			double b2[2] = {vertex1[0],vertex1[1]};
			double dbx = b2[0]-b1[0];
			double dby = b2[1]-b1[1];
			double dpx = gl[0]-st[0];
			double dpy = gl[1]-st[1];

			double t1 = (st[1]-b1[1]-(dby/dbx)*(st[0]-b1[0]))/(dby*dpx/dbx-dpy);
			double t2 = (st[0] - b1[0] + dpx*t1)/dbx;
			if(!(t1 < 0 || t1 > 1 || t2 < 0 || t2 > 1))
				return 0;
		}
	}
	fclose(boundary_handle);
	return 1;
}

void file_extract_path(){
	clock_t filewrite = clock(), diff;
	printf("Extracting\n");
	int i;
	int changed_init;
	int changed = 0;
	int size = 256;
	double c,min_succ_rhs,new_rhs;
	int *step_cell;
	int smallest_rhs[3];
	double sp_cell[3];
	char line[256];
	char buff[256];
	char *file_changed = "Changed 1\n";
	char *file_not_changed = "Changed 0\n";

	clear(line, size);
	clear(buff, size);

	sp = fopen("shortest_path.txt","r");
	while(!sp){
		sp = fopen("shortest_path.txt","r");
	}
	sp_temp = fopen("shortest_path_temp.txt","w+");
	while(!sp_temp){
		sp_temp = fopen("shortest_path_temp.txt","w+");		
	}
	wp = fopen("intermediate_waypoints.txt","w+");
	while(!wp){
		wp = fopen("intermediate_waypoints.txt","w+");		
	}
	wp2 = fopen("intermediate_waypoints2.txt","w+");
	while(!wp2){
		wp2 = fopen("intermediate_waypoints2.txt","w+");
	}

	Node *step_node = current_node;
	Node *last_node = current_node;
	Node *last_waypoint = current_node;

	fgets(line,256,sp);
	sscanf(line,"%s %d",buff,&changed_init);

	clear(line, size);
	clear(buff, size);

	sprintf(buff,"%lf %lf %lf\n",current_location[0],current_location[1],current_location[2]);
	fputs(buff,sp_temp);
	clear(buff,size);
	sprintf(buff,"Changed 1\n");
	fputs(buff,wp);
	fputs(buff,wp2);
	clear(buff,size);

	while(!nodes_equal(step_node,goal_node)){
		last_node = step_node;
		printf("step: [%d,%d,%d]\n",step_node->cell[0],step_node->cell[1],step_node->cell[2]);
		path[step_node->cell[0]][step_node->cell[1]][step_node->cell[2]] = 1;
		if(step_node->rhs == max_val){
			printf("No shortest path\n");
			fclose(sp);
			fclose(sp_temp);
			remove("shortest_path_temp.txt");
			return;
		}
		calc_succ(step_node);
		min_succ_rhs = max_val; //s->rhs = min (s' E Succ(s)) (c(s,s')+g(s'))
		for(i = 0; i < num_succ; i++){
			Node *succs = &(grid[succ[i][0]][succ[i][1]][succ[i][2]]);
			c = cost(step_node,succs);
			new_rhs = c+succs->g;
			if(new_rhs < min_succ_rhs){
				min_succ_rhs = new_rhs;
				smallest_rhs[0] = succ[i][0];
				smallest_rhs[1] = succ[i][1];
				smallest_rhs[2] = succ[i][2];
			}
		}
		if(fgets(line,256,sp) && !changed){
			sscanf(line,"%lf %lf %lf",&sp_cell[0],&sp_cell[1],&sp_cell[2]);
			clear(line, size);
			clear(buff, size);
			if(!((smallest_rhs[0] == sp_cell[0]) &&
				 (smallest_rhs[1] == sp_cell[1]) &&
				 (smallest_rhs[2] == sp_cell[2]))){
				changed = 1;
			}
		}else{
			changed = 1;
		}
		// remove_expanded(step_node);
		step_node = &(grid[smallest_rhs[0]][smallest_rhs[1]][smallest_rhs[2]]);
		// sprintf(buff,"%lf %lf %lf\n",smallest_rhs[0]*x_loc_increment+current_location[0],smallest_rhs[1]*y_loc_increment+current_location[1],interpolate_height(step_node->cell));
		sprintf(buff,"%lf %lf %lf\n",(smallest_rhs[0]-current_cell[0])*x_loc_increment+current_location[0],(smallest_rhs[1]-current_cell[1])*y_loc_increment+current_location[1],(smallest_rhs[2]-current_cell[2])*z_loc_increment+current_location[2]);
		fputs(buff,sp_temp);
		clear(buff,size);
		if(!line_of_sight(step_node,last_waypoint,root_obstacle)){
			sprintf(buff,"%lf %lf %lf\n",(last_node->cell[0]-current_cell[0])*x_loc_increment+current_location[0],(last_node->cell[1]-current_cell[1])*y_loc_increment+current_location[1],(last_node->cell[2]-current_cell[2])*z_loc_increment+current_location[2]);
			fputs(buff,wp);
			fputs(buff,wp2);
			clear(buff,size);
			last_waypoint = last_node;
		}
		last_node = step_node;
	}
	printf("step: [%d,%d,%d]\n",step_node->cell[0],step_node->cell[1],step_node->cell[2]);
	path[step_node->cell[0]][step_node->cell[1]][step_node->cell[2]] = 1;

	fclose(sp);
	fclose(sp_temp);
	fclose(wp);
	fclose(wp2);

	sp = fopen("shortest_path.txt","w+");
	while(!sp){
		sp = fopen("shortest_path.txt","w+");
	}
	sp_temp = fopen("shortest_path_temp.txt","r");
	while(!sp_temp){
		sp_temp = fopen("shortest_path_temp.txt","r");		
	}


	if(changed || changed_init){
		fputs(file_changed,sp);
	}else{
		fputs(file_not_changed,sp);
	}

	while(fgets(line,256,sp_temp)){
		fputs(line,sp);
 	}

	fclose(sp);
	fclose(sp_temp);
	remove("shortest_path_temp.txt");

	diff = clock() - filewrite;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[FILEWRITE] += msec;
	return;
}

void block_or_unblock(int *cell,int state){
	clock_t block = clock(), diff;

	// printf("Block or unblock\n");
	int cost;
	int check_adj[3];
	int index = 0;
	int src,i,j,k;
	double min_rhs;
	int *u,*v;
	grid[cell[0]][cell[1]][cell[2]].infinite += state;

	calc_adj(&(grid[cell[0]][cell[1]][cell[2]]));
	// if (state == 1){
	for(src = 0; src < num_adj; src++){
		u = adj[src];
		v = cell;
		if((get_rhs(u) == compute_heuristic(u,v) + get_g(v)) &&
			(u[0] != goal_cell[0]) && (u[1] != goal_cell[1]) && (u[2] != goal_cell[2])){

			calc_succ(&(grid[u[0]][u[1]][u[2]]));
			min_rhs = max_val;
			for(i = 0; i < num_succ; i++){
				min_rhs = min(min_rhs,compute_heuristic(u,succ[i])+get_g(succ[i]));
			}
			grid[u[0]][u[1]][u[2]].rhs = min_rhs;
			update_vertex(&(grid[u[0]][u[1]][u[2]]));
		}else{
			u = cell;
			v = adj[src];
			if((get_rhs(u) == compute_heuristic(u,v) + get_g(v)) &&
				(u[0] != goal_cell[0]) && (u[1] != goal_cell[1]) && (u[2] != goal_cell[2])){

				calc_succ(&(grid[u[0]][u[1]][u[2]]));
				min_rhs = max_val;
				for(i = 0; i < num_succ; i++){
					min_rhs = min(min_rhs,compute_heuristic(u,succ[i])+get_g(succ[i]));
				}
				grid[u[0]][u[1]][u[2]].rhs = min_rhs;
				update_vertex(&(grid[u[0]][u[1]][u[2]]));
			}
		}
	}
	// }else{
	// 	u = adj[src];
	// 	v = cell;
	// 	for(src = 0; src < num_adj; src++){
	// 		grid[adj[src][0]][adj[src][1]][adj[src][2]].rhs = min(get_rhs(adj[src]),compute_heuristic(adj[src],cell)+get_g(cell));
	// 		update_vertex(&(grid[adj[src][0]][adj[src][1]][adj[src][2]]));
	// 	}
	// }

	diff = clock() - block;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[BLOCK] += msec;
	return;
}

void block_boundary(){
	clock_t block = clock(), diff;
	
	int change_x,change_y,h;
	int vertex_cell[3] = {0,0,0};
	int block_cell[3];
	double dx,dy,boundary_slope,virtual_slope = 0.0;
	double vertex1[3] = {0.0,0.0,0.0};
	double vertex2[3] = {0.0,0.0,0.0};
	char buff[256];
	Node vertex_node;
	Node step_node;
	clear(buff,256);

	FILE *boundary_handle = fopen("boundary.txt","r");
	while(!boundary_handle){
		boundary_handle = fopen("boundary.txt","r");
	}	fgets(buff,256,boundary_handle);
	sscanf(buff,"%lf %lf",&vertex2[0],&vertex2[1]);
	
	while(fgets(buff,256,boundary_handle)){
		vertex1[0] = vertex2[0]; vertex1[1] = vertex2[1];
		sscanf(buff,"%lf %lf",&vertex2[0],&vertex2[1]);
		if(((vertex2[0] >= start_location[0] && vertex2[0] <= goal_location[0]) || (vertex2[0] <= start_location[0] && vertex2[0] >= goal_location[0]))
			&& ((vertex2[1] >= start_location[1] && vertex2[1] <= goal_location[1]) || (vertex2[1] <= start_location[1] && vertex2[1] >= goal_location[1]))){
			// vertex is inside grid -> block line behind and to next node
			vertex_cell[0] = floor((vertex2[0]-origin_location[0])/x_loc_increment);
			vertex_cell[1] = floor((vertex2[1]-origin_location[1])/y_loc_increment);
			vertex_cell[2] = 0;
			// vertex_cell[0] = (vertex_cell[0] >= 0) ? vertex_cell[0] : 0;
			// vertex_cell[1] = (vertex_cell[1] >= 0) ? vertex_cell[1] : 0;
			// vertex_cell[2] = (vertex_cell[2] >= 0) ? vertex_cell[2] : 0;
			dx = vertex1[0] - vertex2[0];
			dy = vertex1[1] - vertex2[1];
			change_x = (dx > 0) ? 1 : -1;
			change_y = (dy > 0) ? 1 : -1;
			boundary_slope = dy/dx;
			for(h = 0; h < RESOLUTION_Z; h++){
				copy_cell(current_cell,vertex_cell);
				while(in_bounds(current_cell) && (sqrt(pow((current_cell[0]-vertex_cell[0])*x_loc_increment,2)+ pow((current_cell[1]-vertex_cell[1])*y_loc_increment,2)) <= sqrt(pow(fabs(dx),2)+pow(fabs(dy),2)))){
					block_cell[0] = current_cell[0];
					block_cell[1] = current_cell[1];
					block_cell[2] = h;
					printf("Blocking Boundary Cell [%d %d %d]\n", block_cell[0], block_cell[1], block_cell[2]);
					block_or_unblock(block_cell,1);
					if(fabs(virtual_slope) > fabs(boundary_slope) || (current_cell[0] - vertex_cell[0] == 0)){
						current_cell[0] += change_x;
					}else{
						current_cell[1] += change_y;
					}
					virtual_slope = (double) (current_cell[1]-vertex_cell[1])*y_loc_increment/((current_cell[0]-vertex_cell[0])*x_loc_increment);
				}
			}
		}
	}

	diff = clock() - block;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[BLOCK] += msec;
	return;
}

void block_cylinder(double *object,double radius,int infinite){
	clock_t block = clock(), diff;

	printf("Blocking\n");
	double x_loc = object[0];
	double y_loc = object[1];
	double z_loc = object[2];
	double rad = radius;
	double start_x = origin_location[0];
	double start_y = origin_location[1];
	double start_z = origin_location[2];
	double x_trans,y_trans,z_trans;
	double diag,current_radius,miss;
	double c,c_old;
	double min_succ_rhs, new_rhs;
	Node *step_node;

	int i,j,k,z,temp;
	int i_min,j_min,k_min;
	int i_max,j_max,k_max;
	int block_cell[3];

	x_trans = x_loc - start_x;
	y_trans = y_loc - start_y;
	z_trans = z_loc - start_z;

	i_min = ((x_trans - rad)/x_loc_increment)-1;
	j_min = ((y_trans - rad)/y_loc_increment)-1;
	k_min = 0;

	i_max = ((x_trans + rad)/x_loc_increment)+1;
	j_max = ((y_trans + rad)/y_loc_increment)+1;
	k_max = ((z_trans)/z_loc_increment)+1;

	if(i_min > i_max){
		temp = i_min; i_min = i_max; i_max = temp;
	}
	if(j_min > j_max){
		temp = j_min; j_min = j_max; j_max = temp;
	}
	if(k_min > k_max){
		temp = k_min; k_min = k_max; k_max = temp;
	}

	i_min = (i_min > 0) ? i_min : 0;
	j_min = (j_min > 0) ? j_min : 0;
	k_min = (k_min > 0) ? k_min : 0;

	i_max = (i_max > 0) ? i_max : 0;
	j_max = (j_max > 0) ? j_max : 0;
	k_max = (k_max > 0) ? k_max : 0;

	i_min = (i_min < RESOLUTION_X-1) ? i_min : RESOLUTION_X-1;
	j_min = (j_min < RESOLUTION_Y-1) ? j_min : RESOLUTION_Y-1;
	k_min = (k_min < RESOLUTION_Z-1) ? k_min : RESOLUTION_Z-1;

	i_max = (i_max < RESOLUTION_X-1) ? i_max : RESOLUTION_X-1;
	j_max = (j_max < RESOLUTION_Y-1) ? j_max : RESOLUTION_Y-1;
	k_max = (k_max < RESOLUTION_Z-1) ? k_max : RESOLUTION_Z-1;
	
	diag = sqrt(pow(x_loc_increment,2)+pow(y_loc_increment,2)+pow(z_loc_increment,2));
	printf("x_trans = %lf\n",x_trans);
	printf("y_trans = %lf\n",y_trans);
	printf("z_trans = %lf\n",z_trans);
	printf("i_min: %d i_max: %d\n",i_min,i_max);
	printf("j_min: %d j_max: %d\n",j_min,j_max);
	printf("k_min: %d k_max: %d\n",k_min,k_max);

	int total = (i_max-i_min+1)*(j_max-j_min+1)*(k_max-k_min+1);
	printf("Total to check: %d\n", total);

	for(i = i_min; i <= i_max; i++){
		for(j = j_min; j <= j_max; j++){
			for(k = 0; k <= k_max; k++){
				total--;
				current_radius = sqrt(pow((x_trans - i*x_loc_increment),2) + 
									  pow((y_trans - j*y_loc_increment),2));
				miss = current_radius - rad;
				if(miss <= 0){
					// printf("Blocking: [%d,%d,%d] at loc [%lf,%lf,%lf]\n",i,j,k,
					// 	(i*x_loc_increment+start_x),(j*y_loc_increment+start_y),(k*z_loc_increment+start_z));
					block_cell[0] = i;
					block_cell[1] = j;
					block_cell[2] = k;
					block_or_unblock(block_cell,infinite);
					path[i][j][k] = (grid[i][j][k].infinite >= 1) ? 2 : path[i][j][k];
				}
			}
		}
	}
	diff = clock() - block;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[BLOCK] += msec;
}

void block_sphere(double *object,double radius,int infinite){
	clock_t block = clock(), diff;

	printf("Blocking\n");
	double x_loc = object[0];
	double y_loc = object[1];
	double z_loc = object[2];
	double rad = radius;
	double start_x = origin_location[0];
	double start_y = origin_location[1];
	double start_z = origin_location[2];
	double x_trans,y_trans,z_trans;
	double diag,current_radius,miss;
	double c,c_old;
	double min_succ_rhs, new_rhs;
	Node *step_node;

	int i,j,k,z,temp;
	int i_min,j_min,k_min;
	int i_max,j_max,k_max;
	int block_cell[3];

	x_trans = x_loc - start_x;
	y_trans = y_loc - start_y;
	z_trans = z_loc - start_z;

	i_min = ((x_trans - rad)/x_loc_increment)-1;
	j_min = ((y_trans - rad)/y_loc_increment)-1;
	k_min = ((z_trans - rad)/z_loc_increment)-1;

	i_max = ((x_trans + rad)/x_loc_increment)+1;
	j_max = ((y_trans + rad)/y_loc_increment)+1;
	k_max = ((z_trans + rad)/z_loc_increment)+1;

	if(i_min > i_max){
		temp = i_min; i_min = i_max; i_max = temp;
	}
	if(j_min > j_max){
		temp = j_min; j_min = j_max; j_max = temp;
	}
	if(k_min > k_max){
		temp = k_min; k_min = k_max; k_max = temp;
	}

	i_min = (i_min > 0) ? i_min : 0;
	j_min = (j_min > 0) ? j_min : 0;
	k_min = (k_min > 0) ? k_min : 0;

	i_max = (i_max > 0) ? i_max : 0;
	j_max = (j_max > 0) ? j_max : 0;
	k_max = (k_max > 0) ? k_max : 0;

	i_min = (i_min < RESOLUTION_X-1) ? i_min : RESOLUTION_X-1;
	j_min = (j_min < RESOLUTION_Y-1) ? j_min : RESOLUTION_Y-1;
	k_min = (k_min < RESOLUTION_Z-1) ? k_min : RESOLUTION_Z-1;

	i_max = (i_max < RESOLUTION_X-1) ? i_max : RESOLUTION_X-1;
	j_max = (j_max < RESOLUTION_Y-1) ? j_max : RESOLUTION_Y-1;
	k_max = (k_max < RESOLUTION_Z-1) ? k_max : RESOLUTION_Z-1;
	
	diag = sqrt(pow(x_loc_increment,2)+pow(y_loc_increment,2)+pow(z_loc_increment,2));
	printf("x_trans = %lf\n",x_trans);
	printf("y_trans = %lf\n",y_trans);
	printf("z_trans = %lf\n",z_trans);
	printf("i_min: %d i_max: %d\n",i_min,i_max);
	printf("j_min: %d j_max: %d\n",j_min,j_max);
	printf("k_min: %d k_max: %d\n",k_min,k_max);

	int total = (i_max-i_min+1)*(j_max-j_min+1)*(k_max-k_min+1);
	printf("Total to check: %d\n", total);

	for(i = i_min; i <= i_max; i++){
		for(j = j_min; j <= j_max; j++){
			for(k = k_min; k <= k_max; k++){
				total--;
				current_radius = sqrt(pow((x_trans - i*x_loc_increment),2) + 
									  pow((y_trans - j*y_loc_increment),2) +
									  pow((z_trans - k*z_loc_increment),2));
				miss = current_radius - rad;
				if(miss <= 0){
					// printf("Blocking: [%d,%d,%d] at loc [%lf,%lf,%lf]\n",i,j,k,
					// 	(i*x_loc_increment+start_x),(j*y_loc_increment+start_y),(k*z_loc_increment+start_z));
					block_cell[0] = i;
					block_cell[1] = j;
					block_cell[2] = k;
					block_or_unblock(block_cell,infinite);
					path[i][j][k] = (grid[i][j][k].infinite >= 1) ? 2 : path[i][j][k];
				}
			}
		}
	}
	diff = clock() - block;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[BLOCK] += msec;
}

void block_moving(double *position, double *velocity, double rad, int infinite){
	clock_t block = clock(), diff;

	printf("Blocking\n");
	double x_loc = position[0];
	double y_loc = position[1];
	double z_loc = position[2];
	double x_vel = velocity[0];
	double y_vel = velocity[1];
	double z_vel = velocity[2];

	double start_x = origin_location[0];
	double start_y = origin_location[1];
	double start_z = origin_location[2];
	double xerr_f,yerr_f,zerr_f; // x error forward etc ...
	double xerr_b,yerr_b,zerr_b; // x error backwards etc ...
	double err_b_dist,err_f_dist;
	double currentx,currenty,currentz;
	double a,b,c,area;

	double x_trans,y_trans,z_trans;
	double diag,current_radius,miss;
	double min_succ_rhs, new_rhs;
	Node *step_node;

	int i,j,k,z,temp;
	int i_min,j_min,k_min;
	int i_max,j_max,k_max;
	int block_cell[3];

	x_trans = x_loc - start_x;
	y_trans = y_loc - start_y;
	z_trans = z_loc - start_z;

	xerr_f = x_trans + x_vel;
	yerr_f = y_trans + y_vel;
	zerr_f = z_trans + z_vel;
	xerr_b = x_trans - x_vel;
	yerr_b = y_trans - y_vel;
	zerr_b = z_trans - z_vel;

	double backwards_err[] = {xerr_b,yerr_b,zerr_b};
	double forwards_err[] = {xerr_f,yerr_f,zerr_f};
	double err_dist = sqrt(pow((xerr_f-xerr_b),2) +
						   pow((yerr_f-yerr_b),2) +
						   pow((zerr_f-zerr_b),2));

	if(xerr_b < xerr_f){
		i_min = ((xerr_b - rad)/x_loc_increment)-1;
		i_max = ((xerr_f + rad)/x_loc_increment)+1;
	}else{
		i_min = ((xerr_f - rad)/x_loc_increment)-1;
		i_max = ((xerr_b + rad)/x_loc_increment)+1;
	}
	if(yerr_b < yerr_f){
		j_min = ((yerr_b - rad)/y_loc_increment)-1;
		j_max = ((yerr_f + rad)/y_loc_increment)+1;
	}else{
		j_min = ((yerr_f - rad)/y_loc_increment)-1;
		j_max = ((yerr_b + rad)/y_loc_increment)+1;
	}
	if(zerr_b < zerr_f){
		k_min = ((zerr_b - rad)/z_loc_increment)-1;
		k_max = ((zerr_f + rad)/z_loc_increment)+1;
	}else{
		k_min = ((zerr_f - rad)/z_loc_increment)-1;
		k_max = ((zerr_b + rad)/z_loc_increment)+1;
	}

	// if(i_min > i_max){
	// 	temp = i_min; i_min = i_max; i_max = temp;
	// }
	// if(j_min > j_max){
	// 	temp = j_min; j_min = j_max; j_max = temp;
	// }
	// if(k_min > k_max){
	// 	temp = k_min; k_min = k_max; k_max = temp;
	// }

	i_min = (i_min > 0) ? i_min : 0;
	j_min = (j_min > 0) ? j_min : 0;
	k_min = (k_min > 0) ? k_min : 0;

	i_max = (i_max > 0) ? i_max : 0;
	j_max = (j_max > 0) ? j_max : 0;
	k_max = (k_max > 0) ? k_max : 0;

	i_min = (i_min < RESOLUTION_X-1) ? i_min : RESOLUTION_X-1;
	j_min = (j_min < RESOLUTION_Y-1) ? j_min : RESOLUTION_Y-1;
	k_min = (k_min < RESOLUTION_Z-1) ? k_min : RESOLUTION_Z-1;

	i_max = (i_max < RESOLUTION_X-1) ? i_max : RESOLUTION_X-1;
	j_max = (j_max < RESOLUTION_Y-1) ? j_max : RESOLUTION_Y-1;
	k_max = (k_max < RESOLUTION_Z-1) ? k_max : RESOLUTION_Z-1;
	
	diag = sqrt(pow(x_loc_increment,2)+pow(y_loc_increment,2)+pow(z_loc_increment,2));
	printf("x_trans = %lf\n",x_trans);
	printf("y_trans = %lf\n",y_trans);
	printf("z_trans = %lf\n",z_trans);
	printf("i_min: %d i_max: %d\n",i_min,i_max);
	printf("j_min: %d j_max: %d\n",j_min,j_max);
	printf("k_min: %d k_max: %d\n",k_min,k_max);

	int total = (i_max-i_min+1)*(j_max-j_min+1)*(k_max-k_min+1);	
	printf("Total to check: %d\n", total);

	for(i = i_min; i <= i_max; i++){
		for(j = j_min; j <= j_max; j++){
			for(k = k_min; k <= k_max; k++){
				total--;
				currentx = i*x_loc_increment;
				currenty = j*y_loc_increment;
				currentz = k*z_loc_increment;
				err_f_dist = sqrt(pow((xerr_f - currentx),2) + 
								  pow((yerr_f - currenty),2) +
								  pow((zerr_f - currentz),2));
				err_b_dist = sqrt(pow((xerr_b - currentx),2) + 
								  pow((yerr_b - currenty),2) +
								  pow((zerr_b - currentz),2));
				if(pow(err_f_dist,2)+pow(err_dist,2) < pow(err_b_dist,2)){
					// Inside err_f cap, solve distance to err line < radius
					current_radius = err_f_dist;
					miss = current_radius - rad;
					// miss = 0;
				}else if(pow(err_b_dist,2)+pow(err_dist,2) < pow(err_f_dist,2)){
					// Inside err_b cap, solve distance to err line < radius
					current_radius = err_b_dist;
					miss = current_radius - rad;
					// miss = 0;
				}else{
					// Between err points, solve distance to err point < radius
					a = err_b_dist;
					b = err_f_dist;
					c = err_dist;
					area = 0.25*sqrt((a+b+c)*(b+c-a)*(c+a-b)*(a+b-c));
					current_radius = 2*area/err_dist;
					miss = current_radius - rad;
					// miss = 0;
				}
				if(miss <= 0){
					// printf("Blocking: [%d,%d,%d] at loc [%lf,%lf,%lf]\n",i,j,k,
					// 	(i*x_loc_increment+start_x),(j*y_loc_increment+start_y),(k*z_loc_increment+start_z));
					block_cell[0] = i;
					block_cell[1] = j;
					block_cell[2] = k;
					block_or_unblock(block_cell,infinite);
					path[i][j][k] = (grid[i][j][k].infinite >= 1) ? 2 : path[i][j][k];
				}
			}
		}
	}
	diff = clock() - block;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[BLOCK] += msec;
}

void set_mark_0(Obstacle *curr){
	clock_t other = clock(), diff;

	if(curr){
		curr->mark = 0;
		set_mark_0(curr->next);
	}

	diff = clock() - other;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[OTHER] += msec;
}

// void mark_if_alive(Obstacle **curr, int type, double x, double y, double z, double rad, double velx, double vely, double velz){
// 	if(curr && *curr){
// 		if((*curr)->location[0] == x && (*curr)->location[1] == y && (*curr)->location[2] == z && (*curr)->radius == rad && (*curr)->mark != 2){
// 			(*curr)->mark = 1; // Mark 1) Obstacle is already in grid
// 		}else if((*curr)->next){
// 			mark_if_alive(&((*curr)->next),type,x,y,z,rad,velx,vely,velz);
// 		}else{
// 			struct obstacle *temp = (*curr)->next;
// 			(*curr)->next = malloc(sizeof(struct obstacle));
// 			(*curr)->next->location[0] = x;
// 			(*curr)->next->location[1] = y;
// 			(*curr)->next->location[2] = z;
// 			(*curr)->next->velocity[0] = velx;
// 			(*curr)->next->velocity[1] = vely;
// 			(*curr)->next->velocity[2] = velz;
// 			(*curr)->next->radius = rad;
// 			(*curr)->next->type = type;
// 			(*curr)->next->mark = 2; // Mark 2) New Obstacle
// 			(*curr)->next->next = temp;
// 		}
// 	}else if(curr){
// 		(*curr) = malloc(sizeof(struct obstacle));
// 		(*curr)->location[0] = x;
// 		(*curr)->location[1] = y;
// 		(*curr)->location[2] = z;
// 		(*curr)->velocity[0] = velx;
// 		(*curr)->velocity[1] = vely;
// 		(*curr)->velocity[2] = velz;
// 		(*curr)->radius = rad;
// 		(*curr)->type = type;
// 		(*curr)->mark = 2;
// 		(*curr)->next = NULL;
// 	}else{
// 		printf("mark_if_alive root deleted\n"); // Root was deleted
// 	}
// }

Obstacle *mark_if_alive(Obstacle *curr, int type, double x, double y, double z, double rad, double velx, double vely, double velz){
	if(curr){
		if(curr->location[0] == x && curr->location[1] == y && curr->location[2] == z && curr->radius == rad && curr->mark != 2){
			curr->mark = 1; // Mark 1) Obstacle is already in grid
		}else if(curr->next){
			curr->next = mark_if_alive(curr->next,type,x,y,z,rad,velx,vely,velz);
		}else{
			struct obstacle *temp = curr->next;
			curr->next = malloc(sizeof(struct obstacle));
			curr->next->location[0] = x;
			curr->next->location[1] = y;
			curr->next->location[2] = z;
			curr->next->velocity[0] = velx;
			curr->next->velocity[1] = vely;
			curr->next->velocity[2] = velz;
			curr->next->radius = rad;
			curr->next->type = type;
			curr->next->mark = 2; // Mark 2) New Obstacle
			curr->next->next = temp;
			return curr;
		}
	}else{
		curr = malloc(sizeof(struct obstacle));
		curr->location[0] = x;
		curr->location[1] = y;
		curr->location[2] = z;
		curr->velocity[0] = velx;
		curr->velocity[1] = vely;
		curr->velocity[2] = velz;
		curr->radius = rad;
		curr->type = type;
		curr->mark = 2;
		curr->next = NULL;
		return curr;
	}
}

// void update_grid_with_obstacles(struct obstacle **curr){
// 	printf("1\n");
// 	if(curr && *curr){
// 		printf("2\n");
// 		if((*curr)->mark){
// 			printf("3\n");
// 			if((*curr)->mark == 2){ // Obstacle is new
// 				printf("4\n");
// 				if((*curr)->type == 1){
// 					printf("5\n");
// 					block_cylinder((*curr)->location,(*curr)->radius,1);
// 				}else if((*curr)->type == 2){
// 					block_sphere((*curr)->location,(*curr)->radius,1);
// 				}else{
// 					block_moving((*curr)->location,(*curr)->velocity,(*curr)->radius,1);
// 				}
// 				update_grid_with_obstacles(&((*curr)->next));
// 			}else if((*curr) && (*curr)->next){ // Obstacle allready in grid
// 				update_grid_with_obstacles(&((*curr)->next));
// 			}
// 		}else{ // Obstacle was deleted in the flight information file
// 			printf("11\n");
// 			struct obstacle *temp;
// 			temp = (*curr);
// 			if((*curr)->type == 1){
// 				block_cylinder((*curr)->location,(*curr)->radius,-1);
// 			}else if((*curr)->type == 2){
// 				block_sphere((*curr)->location,(*curr)->radius,-1);
// 			}else{
// 				block_moving((*curr)->location,(*curr)->velocity,(*curr)->radius,-1);				
// 			}
// 			*curr = (*curr)->next;
// 			temp->next = NULL;
// 			free(temp);
// 			printf("15\n");
// 			if((*curr) && (*curr)->next){
// 				printf("16\n");
// 				update_grid_with_obstacles(&((*curr)->next));
// 			}
// 		}
// 		printf("17\n");
// 	}else if(!curr){
// 		printf("18\n");
// 		printf("update_grid_with_obstacles root deleted\n"); // Root was deleted
// 	}
// 	printf("19\n");
// }

Obstacle *update_grid_with_obstacles(struct obstacle *curr){
	// printf("1\n");
	if(curr){
		// printf("2\n");
		if(curr->mark){
			// printf("3\n");
			if(curr->mark == 2){ // Obstacle is new
				// printf("4\n");
				if(curr->type == 1){
					// printf("5\n");
					block_cylinder(curr->location,curr->radius,1);
				}else if(curr->type == 2){
					block_sphere(curr->location,curr->radius,1);
				}else{
					block_moving(curr->location,curr->velocity,curr->radius,1);
				}
				curr->next = update_grid_with_obstacles(curr->next);
			}else if(curr && curr->next){ // Obstacle allready in grid
				curr->next = update_grid_with_obstacles(curr->next);
			}
		}else{ // Obstacle was deleted in the flight information file
			// printf("11\n");
			struct obstacle *temp;
			temp = curr->next;
			if(curr->type == 1){
				block_cylinder(curr->location,curr->radius,-1);
			}else if(curr->type == 2){
				block_sphere(curr->location,curr->radius,-1);
			}else{
				block_moving(curr->location,curr->velocity,curr->radius,-1);				
			}
			curr = NULL;
			free(curr);
			// printf("15\n");
			return temp;
		}
		// printf("17\n");
	}else{
		return curr;
	}
	// printf("18\n");
	return curr;
}

void file_set_updated_obstacles_0(){
	clock_t filewrite = clock(), diff;

	char line[256];

	information = fopen("flight_information.txt","r");
	while(!information){
		information = fopen("flight_information.txt","r");
	}
	information_temp = fopen("information_temp.txt","w+");
	while(!information_temp){
		information_temp = fopen("information_temp.txt","w+");
	}

	// Throw away first line in information, and write instead.
	clear(line,256);
	fgets(line,256,information);
	fputs("Update 0\n",information_temp);

	// Copy all other lines exactly.
	while(fgets(line,256,information)){
		fputs(line,information_temp);
		clear(line,256);
	}

	fclose(information);
	fclose(information_temp);

	// Rewrite original file with new information
	information = fopen("flight_information.txt","w+");
	while(!information){
		information = fopen("flight_information.txt","w+");
	}
	information_temp = fopen("information_temp.txt","r");
	while(!information_temp){
		information_temp = fopen("information_temp.txt","r");
	}

	while(fgets(line,256,information_temp)){
		fputs(line,information);
		clear(line,256);
	}

	fclose(information);
	fclose(information_temp);
	remove("information_temp.txt");

	diff = clock() - filewrite;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[FILEWRITE] += msec;
}

void file_show_path(int vert_cell){
	clock_t disp = clock(), diff;

	int i,j,k,x,y,z;
	int buff_length;
	int cell_length = 3;
	char buff[8];
	FILE *file_show_path;

	file_show_path = fopen("path.txt","w+");
	while(!file_show_path){
		file_show_path = fopen("path.txt","w+");
	}
	for(j = RESOLUTION_Y-1; j >= 0; j--){
		for(x = 0; x < 2; x++){
			fputs("|",file_show_path);
			for(i = 0; i < RESOLUTION_X; i++){
				if(x == 0){ // Cell Border
					for(y = 0; y < cell_length; y++){
						fputs("_",file_show_path);
					}
				}else if(x == 1){ // Cell Location
					if(path[i][j][vert_cell] == 1){
						sprintf(buff," X\0");
					}else if(path[i][j][vert_cell] == 2){
						sprintf(buff," O\0");
					}else{
						sprintf(buff," \0");
					}
					buff_length = strlen(buff);
					for(y = buff_length; y < cell_length; y++){
						strcat(buff," ");
					}
					fputs(buff,file_show_path);
				}
				fputs("|",file_show_path);
			}
			fprintf(file_show_path,"\n");
		}
	}
	fclose(file_show_path);

	diff = clock() - disp;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[DISP] += msec;
}

void file_show_rhs(int vert_cell){
	int i,j,k,x,y,z;
	int buff_length;
	int cell_length = 9;
	int index_length = ((int) log(RESOLUTION_X > RESOLUTION_Y ? RESOLUTION_X : RESOLUTION_Y)) +1;
	char buff[40];
	FILE *file_show_rhs;

	file_show_rhs = fopen("rhs.txt","w+");
	while(!file_show_rhs){
		file_show_rhs = fopen("rhs.txt","w+");
	}
	for(j = RESOLUTION_Y-1; j >= 0; j--){
		for(x = 0; x < 3; x++){
			if(x == 1){
				sprintf(buff,"%d\0",j);
				buff_length = strlen(buff);
				for(y = buff_length; y < index_length-1; y++){
					strcat(buff," ");
				}
				strcat(buff,"|");
				fputs(buff,file_show_rhs);
			}else if(x == 2){
				sprintf(buff," \0");
				for(y = 1; y < index_length-1; y++){
					strcat(buff," ");
				}
				strcat(buff,"|");
				fputs(buff,file_show_rhs);
			}else{
				sprintf(buff,"_\0");
				for(y = 1; y < index_length-1; y++){
					strcat(buff,"_");
				}
				strcat(buff,"|");
				fputs(buff,file_show_rhs);
			}
			for(i = 0; i < RESOLUTION_X; i++){
				if(x == 0){ // Cell Border
					for(y = 0; y < cell_length; y++){
						fputs("_",file_show_rhs);
					}
				}else if(x == 1){ // Cell Border
					for(y = 0; y < cell_length; y++){
						fputs(" ",file_show_rhs);
					}
				}else if(x == 2){ // Cell Location
					if(grid[i][j][vert_cell].infinite >= 1){
						sprintf(buff," /OBST\\\0");
					}else if(grid[i][j][vert_cell].rhs == max_val){
						sprintf(buff,"RHS_inf\0");
					}else if(grid[i][j][vert_cell].seen == 1){
						sprintf(buff,"%.4lf\0",(grid[i][j][vert_cell].rhs));
						if(is_expanded(&(grid[i][j][vert_cell])))
							strcat(buff,"*");
					}else{
						sprintf(buff," \0");
					}
					buff_length = strlen(buff);
					for(y = buff_length; y < cell_length; y++){
						strcat(buff," ");
					}
					fputs(buff,file_show_rhs);
				}
				fputs("|",file_show_rhs);
			}
			fprintf(file_show_rhs,"\n");
		}
	}
	for(x = 0; x < 2; x++){
		if(x == 0){
			sprintf(buff,"_\0");
			for(y = 1; y < index_length-1; y++){
				strcat(buff,"_");
			}
			strcat(buff,"|");
			fputs(buff,file_show_rhs);
		}else{
			sprintf(buff," \0");
			for(y = 1; y < index_length-1; y++){
				strcat(buff," ");
			}
			strcat(buff,"|");
			fputs(buff,file_show_rhs);
		}
		for(i = 0; i < RESOLUTION_X; i++){
			if(x == 0){
				for(y = 0; y < cell_length; y++){
					fputs("_",file_show_rhs);
				}
			}else{
				sprintf(buff,"%d\0",i);
				buff_length = strlen(buff);
				for(y = buff_length; y < cell_length; y++){
					strcat(buff," ");
				}
				fputs(buff,file_show_rhs);
			}
			fputs("|",file_show_rhs);
		}
		fprintf(file_show_rhs,"\n");
	}
	fclose(file_show_rhs);
}

void file_show_rhs_csv(int vert_cell){
	int i,j,k,x,y,z;
	int buff_length;
	int cell_length = 8;
	char buff[40];
	FILE *file_show_rhs;

	file_show_rhs = fopen("rhs.csv","w+");
	while(!file_show_rhs){
		file_show_rhs = fopen("rhs.csv","w+");		
	}
	for(j = RESOLUTION_Y-1; j >= 0; j--){
		for(x = 0; x < 1; x++){
			for(i = 0; i < RESOLUTION_X; i++){
				if(grid[i][j][vert_cell].infinite == 1){
					fprintf(file_show_rhs,"inf,");
				}else if(grid[i][j][vert_cell].rhs == max_val){
					fprintf(file_show_rhs,"RHS_inf,");
				}else if(grid[i][j][vert_cell].rhs == 0){
					fprintf(file_show_rhs," ,");
				}else{
					fprintf(file_show_rhs,"%.4lf,",(grid[i][j][vert_cell].rhs));
				}
			}
			fprintf(file_show_rhs,"\n");
		}
	}
	fclose(file_show_rhs);
}

void file_print_current_state(int vert_cell){
	clock_t disp = clock(), diff;

	int i,j,k,x,y,z;
	int buff_length;
	int cell_length = 15;
	char buff[30];
	FILE *curr_state;
	k = vert_cell;

	curr_state = fopen("current_state.txt","w+");
	while(!curr_state){
		curr_state = fopen("current_state.txt","w+");		
	}
	for(j = RESOLUTION_Y-1; j >= 0; j--){
		for(x = 0; x < 7; x++){
			fputs("|",curr_state);
			for(i = 0; i < RESOLUTION_X; i++){
				if(x == 0){ // Cell Border
					for(y = 0; y < cell_length; y++){
						fputs("_",curr_state);
					}
				}else if(x == 1){ // Cell Location
					sprintf(buff,"[%d,%d,%d]\0",i,j,k);
					buff_length = strlen(buff);
					for(y = buff_length; y < cell_length; y++){
						strcat(buff," ");
					}
					fputs(buff,curr_state);
				}else if(x == 2){ // Cell Seen
					sprintf(buff,"Seen %d\0",(grid[i][j][vert_cell].seen));
					buff_length = strlen(buff);
					for(y = buff_length; y < cell_length; y++){
						strcat(buff," ");
					}
					fputs(buff,curr_state);
				}else if(x == 3){ // Cell Infinite
					sprintf(buff,"Infinite %d\0",(grid[i][j][vert_cell].infinite));
					buff_length = strlen(buff);
					for(y = buff_length; y < cell_length; y++){
						strcat(buff," ");
					}
					fputs(buff,curr_state);
				}else if(x == 4){ // Cell G
					if(grid[i][j][0].g == max_val){
						sprintf(buff,"G inf\0");
					}else{
						sprintf(buff,"G %.4lf\0",(grid[i][j][vert_cell].g));						
					}
					buff_length = strlen(buff);
					for(y = buff_length; y < cell_length; y++){
						strcat(buff," ");
					}
					fputs(buff,curr_state);
				}else if(x == 5){ // Cell RHS
					if(grid[i][j][0].rhs == max_val){
						sprintf(buff,"RHS inf\0");
					}else{
						sprintf(buff,"RHS %.4lf\0",(grid[i][j][vert_cell].rhs));
					}
					buff_length = strlen(buff);
					for(y = buff_length; y < cell_length; y++){
						strcat(buff," ");
					}
					fputs(buff,curr_state);
				}else if(x == 6){ // Cell RHS
					sprintf(buff,"[%0.1lf,%0.1lf]\0",(grid[i][j][vert_cell].k[0]),(grid[i][j][vert_cell].k[1]));
					buff_length = strlen(buff);
					for(y = buff_length; y < cell_length; y++){
						strcat(buff," ");
					}
					fputs(buff,curr_state);
				}

				fputs("|",curr_state);
			}
			fputs("\n",curr_state);
		}
	}
	fclose(curr_state);
	file_show_rhs(vert_cell);
	file_show_rhs_csv(vert_cell);
	file_show_path(vert_cell);	

	diff = clock() - disp;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[DISP] += msec;
}

void file_print_blocks(){
	FILE *blocks = fopen("3D_blocks.txt","w+");
	while(!blocks){
		blocks = fopen("3D_blocks.txt","w+");	
	}
	int i,j,k;
	char buff[256];

	for(i = 0; i < RESOLUTION_X; i++){
		for(j = 0; j < RESOLUTION_Y; j++){
			for(k = 0; k < RESOLUTION_Z; k++){
				if((grid[i][j][k]).infinite > 0){
					sprintf(buff,"[%lf %lf %lf] [%lf %lf %lf]\n",i*x_loc_increment+origin_location[0],
						j*y_loc_increment+origin_location[1],k*z_loc_increment+origin_location[2],
						x_loc_increment,y_loc_increment,z_loc_increment);
					fputs(buff,blocks);
				}
			}
		}
	}
	sprintf(buff,"[%lf %lf %lf] [%lf %lf %lf]\n",origin_location[0],origin_location[1],origin_location[2],
		x_loc_increment,y_loc_increment,z_loc_increment);
	fputs(buff,blocks);
	sprintf(buff,"[%lf %lf %lf] [%lf %lf %lf]\n",origin_location[0],
		RESOLUTION_Y*y_loc_increment+origin_location[1],origin_location[2],
		x_loc_increment,y_loc_increment,z_loc_increment);
	fputs(buff,blocks);
	sprintf(buff,"[%lf %lf %lf] [%lf %lf %lf]\n",RESOLUTION_X*x_loc_increment+origin_location[0],
		origin_location[1],origin_location[2],
		x_loc_increment,y_loc_increment,z_loc_increment);
	fputs(buff,blocks);
	sprintf(buff,"[%lf %lf %lf] [%lf %lf %lf]\n",RESOLUTION_X*x_loc_increment+origin_location[0],
		RESOLUTION_Y*y_loc_increment+origin_location[1],origin_location[2],
		x_loc_increment,y_loc_increment,z_loc_increment);
	fputs(buff,blocks);
	sprintf(buff,"[%lf %lf %lf] [%lf %lf %lf]\n",origin_location[0],origin_location[1],RESOLUTION_Z*z_loc_increment + origin_location[2],
		x_loc_increment,y_loc_increment,z_loc_increment);
	fputs(buff,blocks);
	sprintf(buff,"[%lf %lf %lf] [%lf %lf %lf]\n",origin_location[0],
		RESOLUTION_Y*y_loc_increment+origin_location[1],RESOLUTION_Z*z_loc_increment + origin_location[2],
		x_loc_increment,y_loc_increment,z_loc_increment);
	fputs(buff,blocks);
	sprintf(buff,"[%lf %lf %lf] [%lf %lf %lf]\n",RESOLUTION_X*x_loc_increment+origin_location[0],
		origin_location[1],RESOLUTION_Z*z_loc_increment + origin_location[2],
		x_loc_increment,y_loc_increment,z_loc_increment);
	fputs(buff,blocks);
	sprintf(buff,"[%lf %lf %lf] [%lf %lf %lf]\n",RESOLUTION_X*x_loc_increment+origin_location[0],
		RESOLUTION_Y*y_loc_increment+origin_location[1],RESOLUTION_Z*z_loc_increment + origin_location[2],
		x_loc_increment,y_loc_increment,z_loc_increment);
	fputs(buff,blocks);
	fclose(blocks);
}

int prepare_2D_loc(double *coord_3D){
	coord_3D[2] = 0.0;
}

int prepare_2D_cell(int *coord_3D){
	coord_3D[2] = 0;
}
// max obst rad: static - 91m | dynamic - 61m
int main(){
	printf("Start\n");

	clock_t start_time = clock(), current_time = clock(), end_time;
	int t;
	int cet;
	double cost;
	double object[7];
	char junk[256];
	char line[256];
	Node last_node;
	int rewind_file = 1;

	times[0] = 0; times[1] = 0; times[2] = 0; times[3] = 0; times[4] = 0; times[5] = 0; times[6] = 0; times[7] = 0;
	information = fopen("flight_information.txt","r");
	while(!information){
		information = fopen("flight_information.txt","r");
	}

	fscanf(information,"%s %d", junk, &updated_obstacles);
	fscanf(information,"%s %lf %lf %lf", junk, &goal_location[0], &goal_location[1], &goal_location[2]);
	fscanf(information,"%s %lf %lf %lf", junk, &start_location[0], &start_location[1], &start_location[2]);
	fscanf(information,"%s %lf %lf %lf", junk, &current_location[0], &current_location[1], &current_location[2]);
	fgets(junk,256,information); // need this to swich inbetween using fscanf to fgets in order to move to next line
	printf("Start: [%lf %lf %lf]\n",start_location[0],start_location[1],start_location[2]);
	printf("Goal: [%lf %lf %lf]\n",goal_location[0],goal_location[1],goal_location[2]);
	// altitude_delta = goal_location[2] - start_location[2];
	// current_altitude = current_location[2] - start_location[2];
	// prepare_2D_loc(goal_location); prepare_2D_loc(start_location); prepare_2D_loc(current_location);

	// Need to initialize before inserting objects
	initialize(start_location,goal_location);
	// block_boundary();

	set_mark_0(root_obstacle);
	while(fgets(line,256,information)){
		clear(junk,256);
		sscanf(line,"%s %lf %lf %lf %lf", junk, &object[0], &object[1], &object[2], &object[3]);
		// prepare_2D_loc(object);
		if(strcmp(junk,"static") == 0){
			root_obstacle = mark_if_alive(root_obstacle,1,object[0],object[1],object[2],object[3],0.0,0.0,0.0);
		}else if(strcmp(junk,"dynamic") == 0){
			root_obstacle = mark_if_alive(root_obstacle,2,object[0],object[1],object[2],object[3],0.0,0.0,0.0);
		}else{
			sscanf(line,"%s %lf %lf %lf %lf %lf %lf %lf", junk, &object[0], &object[1], &object[2], &object[3],
				&object[4], &object[5], &object[6]);
			root_obstacle = mark_if_alive(root_obstacle,3,object[0],object[1],object[2],object[6],object[3],object[4],object[5]);
		}
	}
	cet = (clock()-current_time)* 1000 / CLOCKS_PER_SEC; current_time = clock();
	printf("UOL Time: %d seconds %d milliseconds\n", cet/1000, cet%1000);
	fclose(information);

	//Make sure to re-write flight information file as soon as done
	//reading to prevent overwriting new data that hasn't been iterated on.
	if(updated_obstacles){
		updated_obstacles = 0;
		root_obstacle = update_grid_with_obstacles(root_obstacle);
		file_print_blocks();
		file_set_updated_obstacles_0();
	}
	cet = (clock()-current_time)* 1000 / CLOCKS_PER_SEC; current_time = clock();
	printf("UGWO Time: %d seconds %d milliseconds\n", cet/1000, cet%1000);
	//Do the damn thing.
	// file_print_current_state(start_cell[2]);
	compute_shortest_path();
	cet = (clock()-current_time)* 1000 / CLOCKS_PER_SEC; current_time = clock();
	printf("CSP Time: %d seconds %d milliseconds\n", cet/1000, cet%1000);
	// file_print_current_state(start_cell[2]);
	file_show_path(start_cell[2]);
	file_show_rhs(start_cell[2]);
	cet = (clock()-current_time)* 1000 / CLOCKS_PER_SEC; current_time = clock();
	printf("PCS Time: %d seconds %d milliseconds\n", cet/1000, cet%1000);
	file_extract_path();
	cet = (clock()-current_time)* 1000 / CLOCKS_PER_SEC; current_time = clock();
	printf("EP Time: %d seconds %d milliseconds\n", cet/1000, cet%1000);
	file_show_path(start_cell[2]);
	cet = (clock()-current_time)* 1000 / CLOCKS_PER_SEC; current_time = clock();
	printf("SP Time: %d seconds %d milliseconds\n", cet/1000, cet%1000);

	//Start moving towards goal and recomputing if there are new obstacles!
	copy_node(&last_node, current_node);

	int print_loop = 1;
	while(!nodes_equal(current_node, goal_node)){
		if(print_loop){ 
			cet = (clock()-current_time)* 1000 / CLOCKS_PER_SEC; current_time = clock();
			printf("GAP Time: %d seconds %d milliseconds\n", cet/1000, cet%1000);
			end_time = clock() - start_time;
			int total_time = end_time * 1000 / CLOCKS_PER_SEC;

			printf("Loop\n");
			// printf("thing %lf\n\n",sqrt(0.01+0.01));	 
			print_loop = 0;
			printf("Times: \n");
			printf("Total Time taken %d seconds %d milliseconds\n", total_time/1000, total_time%1000);
			printf("CSP Time taken %d seconds %d milliseconds\n", times[CSP]/1000, times[CSP]%1000);
			printf("Update Time taken %d seconds %d milliseconds\n", times[UPDATE]/1000, times[UPDATE]%1000);
			printf("Display Time taken %d seconds %d milliseconds\n", times[DISP]/1000, times[DISP]%1000);
			printf("Pred/Succ Time taken %d seconds %d milliseconds\n", times[ADJSUCC]/1000, times[ADJSUCC]%1000);
			printf("Filewrite Time taken %d seconds %d milliseconds\n", times[FILEWRITE]/1000, times[FILEWRITE]%1000);
			printf("Block Time taken %d seconds %d milliseconds\n", times[BLOCK]/1000, times[BLOCK]%1000);
			printf("Other Time taken %d seconds %d milliseconds\n", times[OTHER]/1000, times[OTHER]%1000);
			times[0] = 0; times[1] = 0; times[2] = 0; times[3] = 0; times[4] = 0; times[5] = 0; times[6] = 0; times[7] = 0;
		}
		return 0;
		start_time = clock();

		if (current_node->g == max_val){
			printf("No Path Found\n");
			return 0;
		}


		while(rewind_file == 1){
			information = fopen("flight_information.txt","r");
			while(!information){
				information = fopen("flight_information.txt","r");
			}
			fscanf(information,"%s %d", junk, &updated_obstacles);
			if(updated_obstacles == 1)
				rewind_file = 0;
			else if(updated_obstacles == 2)
				return 0;
			fclose(information);
		}
		rewind_file = 1;
		information = fopen("flight_information.txt","r");
		while(!information){
			information = fopen("flight_information.txt","r");
		}
		fscanf(information,"%s %d", junk, &updated_obstacles);
		fscanf(information,"%s %lf %lf %lf", junk, &goal_location_temp[0], &goal_location_temp[1], &goal_location_temp[2]);
		fscanf(information,"%s %lf %lf %lf", junk, &start_location_temp[0], &start_location_temp[1], &start_location_temp[2]);
		fscanf(information,"%s %lf %lf %lf", junk, &current_location[0], &current_location[1], &current_location[2]);
		fgets(junk,256,information); // need this to swich inbetween using fscanf to fgets in order to move to next line
		// altitude_delta = goal_location[2] - start_location[2];
		// current_altitude = current_location[2] - start_location[2];
		// prepare_2D_loc(goal_location); prepare_2D_loc(start_location); prepare_2D_loc(current_location);

		if(updated_obstacles == 2){
			return 0;
		}

		if(!((start_location_temp[0] == start_location[0]) && (start_location_temp[1] == start_location[1]) && (start_location_temp[2] == start_location[2]) && 
			(goal_location_temp[0] == goal_location[0]) && (goal_location_temp[1] == goal_location[1]) && (goal_location_temp[2] == goal_location[2]))){
			printf("Start or goal was changed. Algorithm is incapable of changing start or goal after initializing grid.");
			printf("Goal: %lf %lf %lf\n",start_location_temp[0],start_location_temp[1],start_location_temp[2]);
			printf("Start: %lf %lf %lf\n",goal_location_temp[0],goal_location_temp[1],goal_location_temp[2]);
			return 0;
		}

		set_mark_0(root_obstacle);
		while(fgets(line,256,information)){
			clear(junk,256);
			sscanf(line,"%s %lf %lf %lf %lf", junk, &object[0], &object[1], &object[2], &object[3]);
			// prepare_2D_loc(object);
			if(strcmp(junk,"static")==0){
				root_obstacle = mark_if_alive(root_obstacle,1,object[0],object[1],object[2],object[3],0.0,0.0,0.0);
			}else if(strcmp(junk,"moving")==0){
				sscanf(line,"%s %lf %lf %lf %lf %lf %lf %lf", junk, &object[0], &object[1], &object[2], &object[3],
					&object[4], &object[5], &object[6]);
				root_obstacle = mark_if_alive(root_obstacle,3,object[0],object[1],object[2],object[6],object[3],object[4],object[5]);
			}else{
				root_obstacle = mark_if_alive(root_obstacle,2,object[0],object[1],object[2],object[3],0.0,0.0,0.0);			
			}
		}

		fclose(information);
		update_current_node();

 		if(updated_obstacles){
			printf("Replaning\n");
			root_obstacle = update_grid_with_obstacles(root_obstacle);
			file_print_blocks();
			updated_obstacles = 0;
			key_modifier = key_modifier + compute_heuristic(last_node.cell,current_node->cell);
			file_set_updated_obstacles_0();
			compute_shortest_path();
			// file_print_current_state(start_cell[2]);
			file_show_path(start_cell[2]);
			clear_path();
			file_extract_path();
			file_show_path(start_cell[2]);
			print_loop = 1;
		}
		//OR if vehicle isn't following the calculated path, replan
	}
}