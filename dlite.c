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

#define RESOLUTION_X 40
#define RESOLUTION_Y 40
#define RESOLUTION_VERTICAL 10
#define CSP 0
#define UPDATE 1
#define DISP 2
#define PREDSUCC 3
#define FILEWRITE 4
#define BLOCK 5
#define HEAP 6
#define OTHER 7

void print_current_state();

FILE *information;
FILE *information_temp;
FILE *sp;
FILE *sp_temp;
int updated_obstacles;

double goal_location[3];
double goal_location_temp[3];
double start_location[3];
double start_location_temp[3];
double current_location[3];
double x_loc_increment;
double y_loc_increment;
double z_loc_increment;

double key_modifier;

//Data structures
Heap minheap;
Heap expanded;
Node grid[RESOLUTION_X][RESOLUTION_Y][RESOLUTION_VERTICAL];
Obstacle *root_obstacle;
int path[RESOLUTION_X][RESOLUTION_Y][RESOLUTION_VERTICAL];
//Important nodes
Node *goal_node;
Node *start_node;
Node *current_node;
//Keep track of expanded nodes
int num_expanded;
//Successors and Predecessors wrt current node (calculated and used when needed)
int num_pred, num_succ;
int succ[27][3];
int pred[27][3];
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

double compute_heuristic(int *curr, int *goal){
	clock_t other = clock(),diff;

	double x_val = 0.0;
	double y_val = 0.0;
	double z_val = 0.0;
	double heuristic = 0.0;

	x_val = fabs((goal[0] - curr[0]) * x_loc_increment);
	y_val = fabs((goal[1] - curr[1]) * y_loc_increment);
	z_val = fabs((goal[2] - curr[2]) * z_loc_increment);
	
	heuristic = sqrt(pow(x_val,2)+pow(y_val,2)+pow(z_val,2));
	// heuristic += ((double)(rand()%10))/((double)RAND_MAX);

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
	if(node_index(&expanded,node) > -1)
		return 1;
	else
		return 0;
}

void add_expanded(Node *node){
	clock_t other = clock(),diff;

	printf("Expanding node: {%d,%d,%d} at location {%lf,%lf,%lf} with key_value: {%lf, %lf}\n",node->cell[0],node->cell[1],node->cell[2],
		node->cell[0]*x_loc_increment+start_location[0],node->cell[1]*y_loc_increment+start_location[1],
		node->cell[2]*z_loc_increment+start_location[2],node->k[0],node->k[1]);
	push_node(&expanded,node);
	num_expanded++;
	// if(num_expanded == 0){
	// 	expanded_nodes = (Node **) malloc(sizeof(Node *));
	// 	expanded_nodes[0] = node;
	// 	num_expanded++;
	// }else{
	// 	Node ***pointer = &expanded_nodes;
	// 	num_expanded++;
	// 	*pointer = (Node **) realloc(*pointer,sizeof(Node *)*(num_expanded));
	// 	expanded_nodes[num_expanded-1] = node;
	// }

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

	remove_node(&expanded,node);
	// if(num_expanded){
	// 	expanded_nodes = NULL;
	// 	num_expanded = 0;
	// 	free(expanded_nodes);
	// }
	num_expanded--;

	diff = clock() - other;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[OTHER] += msec;
}
int in_bounds(int *cell){
	clock_t other = clock(), diff;

	if(cell[0] >= 0 && cell[1] >= 0 && cell[2] >= 0
		&& cell[0] < RESOLUTION_X && cell[1] < RESOLUTION_Y
		&& cell[2] < RESOLUTION_VERTICAL){

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

void calc_pred(Node *node){
	clock_t predsucc = clock(), diff;

	int *cell = node->cell;
	int check_pred[3];
	int index = 0;
	int i,j,k;
	num_pred = 0;

	for(i = 0; i < 3; i++){
		for(j = 0; j < 3; j++){
			for(k = 0; k < 3; k++){
				check_pred[0] = cell[0]+i-1;
				check_pred[1] = cell[1]+j-1;
				check_pred[2] = cell[2]+k-1;
				if(in_bounds(check_pred) && !(grid[check_pred[0]][check_pred[1]][check_pred[2]].infinite == 1)){
					if(!(is_expanded(&(grid[check_pred[0]][check_pred[1]][check_pred[2]])))){
						pred[index][0] = check_pred[0];
						pred[index][1] = check_pred[1];
						pred[index][2] = check_pred[2];
						num_pred++;
						index++;
					}
				}
			}
		}
	}

	diff = clock() - predsucc;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[PREDSUCC] += msec;

	return;
}

void calc_succ(Node *node){
	clock_t predsucc = clock(), diff;

	int *cell = node->cell;
	int check_succ[3];
	int index = 0;
	int i,j,k;
	num_succ = 0;

	for(i = 0; i < 3; i++){
		for(j = 0; j < 3; j++){
			for(k = 0; k < 3; k++){
				check_succ[0] = cell[0]+i-1;
				check_succ[1] = cell[1]+j-1;
				check_succ[2] = cell[2]+k-1;
				if(in_bounds(check_succ) &&
					!(check_succ[0] == cell[0] &&
					  check_succ[1] == cell[1] &&
					  check_succ[2] == cell[2]) &&
					!(grid[check_succ[0]][check_succ[1]][check_succ[2]].infinite == 1) &&
					is_expanded(&(grid[check_succ[0]][check_succ[1]][check_succ[2]]))){

					succ[index][0] = check_succ[0];
					succ[index][1] = check_succ[1];
					succ[index][2] = check_succ[2];
					num_succ++;
					index++;
				}
			}
		}
	}
	diff = clock() - predsucc;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[PREDSUCC] += msec;
	return;
}

void update_current_node(){
	clock_t other = clock(), diff;

	int current_cell[3] = {0,0,0};
	current_cell[0] = floor((current_location[0]-start_location[0])/x_loc_increment);
	current_cell[1] = floor((current_location[1]-start_location[1])/y_loc_increment);
	current_cell[2] = floor((current_location[2]-start_location[2])/z_loc_increment);
	current_cell[0] = (current_cell[0] >= 0) ? current_cell[0] : 0;
	current_cell[1] = (current_cell[1] >= 0) ? current_cell[1] : 0;
	current_cell[2] = (current_cell[2] >= 0) ? current_cell[2] : 0;
	current_node = &(grid[current_cell[0]][current_cell[1]][current_cell[2]]);
	init_graph_node(current_node,current_cell);

	diff = clock() - other;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[OTHER] += msec;
}

void initialize(){
	clock_t other = clock(), diff;

	init_heap(&minheap);
	init_heap(&expanded);
	key_modifier = 0.0;
	num_expanded = 0;

	int goal_cell[3] = {RESOLUTION_X-1,RESOLUTION_Y-1,RESOLUTION_VERTICAL-1};
	goal_node = &(grid[goal_cell[0]][goal_cell[1]][goal_cell[2]]);

	int start_cell[3] = {0,0,0};
	start_node = &(grid[0][0][0]);

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
	while(compare_keys(top_key(&minheap),current_key) <= 0 || current_node->rhs > current_node->g){
		printf("Num Expanded: %d\n", num_expanded);
		// diff += clock() - csp;
		// print_current_state();
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
			calc_pred(u);
			for(i = 0; i < num_pred; i++){ // for all s in Pred(u)
				Node *s = &(grid[pred[i][0]][pred[i][1]][pred[i][2]]);
				if(!(s->seen)){
					int pred_cell[3] = {pred[i][0],pred[i][1],pred[i][2]};
					init_graph_node(s,pred_cell);
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
			calc_pred(u);
			for(i = 0; i < num_pred; i++){ //for all s in Pred(u) U {u}
				if(!(pred[i][0] == -1)){ // if s is a valid pred (not out of bounds, or already expanded)
					Node *s = &(grid[pred[i][0]][pred[i][1]][pred[i][2]]);
					if(!(s->seen)){
						int pred_cell[3] = {pred[i][0],pred[i][1],pred[i][2]};
						init_graph_node(s,pred_cell);
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
			for(k = 0; k < RESOLUTION_VERTICAL; k++){
				path[i][j][k] = (path[i][j][k] == 2) ? 2 : 0;
			}
		}
	}

	diff = clock() - other;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[OTHER] += msec;
}

void extract_path(){
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
	sp_temp = fopen("shortest_path_temp.txt","w");

	Node *step_node = current_node;

	fgets(line,256,sp);
	sscanf(line,"%s %d",buff,&changed_init);

	clear(line, size);
	clear(buff, size);

	while(!nodes_equal(step_node,goal_node)){
		printf("step: [%d,%d,%d]\n",step_node->cell[0],step_node->cell[1],step_node->cell[2]);
		path[step_node->cell[0]][step_node->cell[1]][step_node->cell[2]] = 1;
		if(step_node->rhs == max_val){
			printf("No shortest path\n");
			fclose(sp);
			fclose(sp_temp);
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
		remove_expanded(step_node);
		step_node = &(grid[smallest_rhs[0]][smallest_rhs[1]][smallest_rhs[2]]);
		sprintf(buff,"%lf %lf %lf\n",smallest_rhs[0]*x_loc_increment+current_location[0],smallest_rhs[1]*y_loc_increment+current_location[1],smallest_rhs[2]*z_loc_increment+current_location[2]);
		fputs(buff,sp_temp);
		clear(buff,size);
	}
	printf("step: [%d,%d,%d]\n",step_node->cell[0],step_node->cell[1],step_node->cell[2]);
	path[step_node->cell[0]][step_node->cell[1]][step_node->cell[2]] = 1;

	fclose(sp);
	fclose(sp_temp);

	sp = fopen("shortest_path.txt","w");
	sp_temp = fopen("shortest_path_temp.txt","r");


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

void update_edge_costs(int i_min,int j_min,int k_min,int i_max,int j_max,int k_max){
	// print_current_state();
	clock_t update = clock(), diff, relevant = 0;
	int i,j,k,z;
	double min_succ_rhs,new_rhs;
	double c;
	Node *step_node;
	for(i = i_min; i <= i_max; i++){
		for(j = j_min; j <= j_max; j++){
			for(k = k_min; k <= k_max; k++){
				if((grid[i][j][k].infinite == 0) && (!nodes_equal(&(grid[i][j][k]),goal_node)) && (grid[i][j][k].seen == 1)){
					relevant += clock() - update;
					// print_current_state();
					step_node = &(grid[i][j][k]);
					calc_succ(step_node);
					update = clock();
					min_succ_rhs = max_val; //s->rhs = min (s' E Succ(s)) (c(s,s')+g(s'))
					printf("Updating node: [%d %d %d], at loc [%lf,%lf,%lf]. rhs was: %0.4lf ",i,j,k,i+start_location[0],j+start_location[1],k+start_location[2],(float)(step_node->rhs));
					for(z = 0; z < num_succ; z++){
						if(!(succ[z][0] == -1)){
							Node *succs = &(grid[succ[z][0]][succ[z][1]][succ[z][2]]);
							if(!(succs->seen)){
								int succ_cell[3] = {succ[z][0],succ[z][1],succ[z][2]};
								init_graph_node(succs,succ_cell);
								succs->seen = 1;
							}
							c = cost(step_node,succs);
							new_rhs = c+succs->g;
							if(new_rhs < min_succ_rhs){
								min_succ_rhs = new_rhs;
							}
						}
					}
					printf("now: %0.4lf.\n",(float)min_succ_rhs);
					step_node->rhs = min_succ_rhs;
					update_vertex(step_node);
				}
			}
		}
	}
	relevant += clock() - update;
	diff = relevant;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[UPDATE] += msec;
}

void block_or_unblock(double *object,int infinite){
	clock_t block = clock(), diff;

	printf("Blocking\n");
	double x_loc = object[0];
	double y_loc = object[1];
	double z_loc = object[2];
	double rad = object[3];
	double start_x = start_location[0];
	double start_y = start_location[1];
	double start_z = start_location[2];
	double x_trans,y_trans,z_trans;
	double diag,current_radius,miss;
	double c,c_old;
	double min_succ_rhs, new_rhs;
	Node *step_node;

	int i,j,k,z,temp;
	int i_min,j_min,k_min;
	int i_max,j_max,k_max;

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
	k_min = (k_min < RESOLUTION_VERTICAL-1) ? k_min : RESOLUTION_VERTICAL-1;

	i_max = (i_max < RESOLUTION_X-1) ? i_max : RESOLUTION_X-1;
	j_max = (j_max < RESOLUTION_Y-1) ? j_max : RESOLUTION_Y-1;
	k_max = (k_max < RESOLUTION_VERTICAL-1) ? k_max : RESOLUTION_VERTICAL-1;
	
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
				if(miss <= diag/4){
					printf("Blocking: [%d,%d,%d] at loc [%lf,%lf,%lf]\n",i,j,k,(i+start_x),(j+start_y),(k+start_z));
					grid[i][j][k].infinite += infinite;
					path[i][j][k] = (grid[i][j][k].infinite >= 1) ? 2 : 0;
				}
			}
		}
	}
	diff = clock() - block;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[BLOCK] += msec;

	update_edge_costs(i_min,j_min,k_min,i_max,j_max,k_max);
	print_current_state();
}

void mark_obstacles(Obstacle *curr){
	clock_t other = clock(), diff;

	if(curr){
		curr->mark = 0;
		mark_obstacles(curr->next);
	}

	diff = clock() - other;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[OTHER] += msec;
}

void update_obstacle_list(Obstacle **curr, double x, double y, double z, double rad){
	if(curr && *curr){
		if((*curr)->location[0] == x && (*curr)->location[1] == y && (*curr)->location[2] == z && (*curr)->radius == rad){
			(*curr)->mark = 1;
		}else if((*curr)->next){
			update_obstacle_list(&((*curr)->next),x,y,z,rad);
		}else{
			Obstacle *temp = (*curr)->next;
			(*curr)->next = malloc(sizeof(Obstacle));
			(*curr)->next->location[0] = x;
			(*curr)->next->location[1] = y;
			(*curr)->next->location[2] = z;
			(*curr)->next->radius = rad;
			(*curr)->next->mark = 2;
			(*curr)->next->next = temp;
		}
	}else if(curr){
		(*curr) = malloc(sizeof(Obstacle));
		(*curr)->location[0] = x;
		(*curr)->location[1] = y;
		(*curr)->location[2] = z;
		(*curr)->radius = rad;
		(*curr)->mark = 2;
		(*curr)->next = NULL;
	}else{
		printf("Update_Obstacle_List broken");
		//broken
	}
}

void update_grid_with_obstacles(Obstacle **curr){
	if(curr && *curr){
		if((*curr)->mark){
			if((*curr)->mark == 2){
				block_or_unblock((*curr)->location,1);
				update_grid_with_obstacles(&((*curr)->next));
			}else{
				update_grid_with_obstacles(&((*curr)->next));
			}
		}else{
			Obstacle *temp;
			temp = (*curr);
			block_or_unblock((*curr)->location,-1);
			(*curr) = (*curr)->next;
			temp = NULL;
			free(temp);
			update_grid_with_obstacles(&((*curr)->next));
		}
	}
}

void confirm_updated_obstacles(){
	clock_t filewrite = clock(), diff;

	char line[256];

	information = fopen("flight_information.txt","r");
	information_temp = fopen("information_temp.txt","w");

	//Critical step here. Throw away first line in information, and write instead.
	fgets(line,256,information);
	fputs("Updated_Obstacles 0\n",information_temp);

	//Copy all other lines exactly.
	while(fgets(line,256,information)){
		fputs(line,information_temp);
	}

	fclose(information);
	fclose(information_temp);

	//Now rewrite original file with new information
	information = fopen("flight_information.txt","w");
	information_temp = fopen("information_temp.txt","r");

	while(fgets(line,256,information_temp)){
		fputs(line,information);
	}

	fclose(information);
	fclose(information_temp);

	diff = clock() - filewrite;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[FILEWRITE] += msec;
}

void show_path(){
	clock_t disp = clock(), diff;

	int i,j,k,x,y,z;
	int buff_length;
	int cell_length = 3;
	char buff[8];
	FILE *show_path;

	show_path = fopen("path.txt","w");
	for(j = RESOLUTION_Y-1; j >= 0; j--){
		for(x = 0; x < 2; x++){
			fputs("|",show_path);
			for(i = 0; i < RESOLUTION_X; i++){
				if(x == 0){ // Cell Border
					for(y = 0; y < cell_length; y++){
						fputs("_",show_path);
					}
				}else if(x == 1){ // Cell Location
					if(path[i][j][0] == 1){
						sprintf(buff," X\0");
					}else if(path[i][j][0] == 2){
						sprintf(buff," O\0");
					}else{
						sprintf(buff," \0");
					}
					buff_length = strlen(buff);
					for(y = buff_length; y < cell_length; y++){
						strcat(buff," ");
					}
					fputs(buff,show_path);
				}
				fputs("|",show_path);
			}
			fprintf(show_path,"\n");
		}
	}
	fclose(show_path);

	diff = clock() - disp;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[DISP] += msec;
}

void show_rhs(){
	int i,j,k,x,y,z;
	int buff_length;
	int cell_length = 9;
	int index_length = ((int) log(RESOLUTION_X > RESOLUTION_Y ? RESOLUTION_X : RESOLUTION_Y)) +1;
	char buff[40];
	FILE *show_rhs;

	show_rhs = fopen("rhs.txt","w");
	for(j = RESOLUTION_Y-1; j >= 0; j--){
		for(x = 0; x < 3; x++){
			if(x == 1){
				sprintf(buff,"%d\0",j);
				buff_length = strlen(buff);
				for(y = buff_length; y < index_length-1; y++){
					strcat(buff," ");
				}
				strcat(buff,"|");
				fputs(buff,show_rhs);
			}else if(x == 2){
				sprintf(buff," \0");
				for(y = 1; y < index_length-1; y++){
					strcat(buff," ");
				}
				strcat(buff,"|");
				fputs(buff,show_rhs);
			}else{
				sprintf(buff,"_\0");
				for(y = 1; y < index_length-1; y++){
					strcat(buff,"_");
				}
				strcat(buff,"|");
				fputs(buff,show_rhs);
			}
			for(i = 0; i < RESOLUTION_X; i++){
				if(x == 0){ // Cell Border
					for(y = 0; y < cell_length; y++){
						fputs("_",show_rhs);
					}
				}else if(x == 1){ // Cell Border
					for(y = 0; y < cell_length; y++){
						fputs(" ",show_rhs);
					}
				}else if(x == 2){ // Cell Location
					if(grid[i][j][0].infinite >= 1){
						sprintf(buff," /OBST\\\0");
					}else if(grid[i][j][0].rhs == max_val){
						sprintf(buff,"RHS_inf\0");
					}else if(grid[i][j][0].seen == 1){
						sprintf(buff,"%.4lf\0",(grid[i][j][0].rhs));
						if(is_expanded(&(grid[i][j][0])))
							strcat(buff,"*");
					}else{
						sprintf(buff," \0");
					}
					buff_length = strlen(buff);
					for(y = buff_length; y < cell_length; y++){
						strcat(buff," ");
					}
					fputs(buff,show_rhs);
				}
				fputs("|",show_rhs);
			}
			fprintf(show_rhs,"\n");
		}
	}
	for(x = 0; x < 2; x++){
		if(x == 0){
			sprintf(buff,"_\0");
			for(y = 1; y < index_length-1; y++){
				strcat(buff,"_");
			}
			strcat(buff,"|");
			fputs(buff,show_rhs);
		}else{
			sprintf(buff," \0");
			for(y = 1; y < index_length-1; y++){
				strcat(buff," ");
			}
			strcat(buff,"|");
			fputs(buff,show_rhs);
		}
		for(i = 0; i < RESOLUTION_X; i++){
			if(x == 0){
				for(y = 0; y < cell_length; y++){
					fputs("_",show_rhs);
				}
			}else{
				sprintf(buff,"%d\0",i);
				buff_length = strlen(buff);
				for(y = buff_length; y < cell_length; y++){
					strcat(buff," ");
				}
				fputs(buff,show_rhs);
			}
			fputs("|",show_rhs);
		}
		fprintf(show_rhs,"\n");
	}
	fclose(show_rhs);
}

void show_rhs_csv(){
	int i,j,k,x,y,z;
	int buff_length;
	int cell_length = 8;
	char buff[40];
	FILE *show_rhs;

	show_rhs = fopen("rhs.csv","w+");
	for(j = RESOLUTION_Y-1; j >= 0; j--){
		for(x = 0; x < 1; x++){
			for(i = 0; i < RESOLUTION_X; i++){
				if(grid[i][j][0].infinite == 1){
					fprintf(show_rhs,"inf,");
				}else if(grid[i][j][0].rhs == max_val){
					fprintf(show_rhs,"RHS_inf,");
				}else if(grid[i][j][0].rhs == 0){
					fprintf(show_rhs," ,");
				}else{
					fprintf(show_rhs,"%.4lf,",(grid[i][j][0].rhs));
				}
			}
			fprintf(show_rhs,"\n");
		}
	}
	fclose(show_rhs);
}

void print_current_state(){
	clock_t disp = clock(), diff;

	int i,j,k,x,y,z;
	int buff_length;
	int cell_length = 15;
	char buff[30];
	FILE *curr_state;
	k = 0;

	curr_state = fopen("current_state.txt","w");
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
					sprintf(buff,"Seen %d\0",(grid[i][j][0].seen));
					buff_length = strlen(buff);
					for(y = buff_length; y < cell_length; y++){
						strcat(buff," ");
					}
					fputs(buff,curr_state);
				}else if(x == 3){ // Cell Infinite
					sprintf(buff,"Infinite %d\0",(grid[i][j][0].infinite));
					buff_length = strlen(buff);
					for(y = buff_length; y < cell_length; y++){
						strcat(buff," ");
					}
					fputs(buff,curr_state);
				}else if(x == 4){ // Cell G
					if(grid[i][j][0].g == max_val){
						sprintf(buff,"G inf\0");
					}else{
						sprintf(buff,"G %.4lf\0",(grid[i][j][0].g));						
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
						sprintf(buff,"RHS %.4lf\0",(grid[i][j][0].rhs));
					}
					buff_length = strlen(buff);
					for(y = buff_length; y < cell_length; y++){
						strcat(buff," ");
					}
					fputs(buff,curr_state);
				}else if(x == 6){ // Cell RHS
					sprintf(buff,"[%0.1lf,%0.1lf]\0",(grid[i][j][0].k[0]),(grid[i][j][0].k[1]));
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
	show_rhs();
	show_rhs_csv();

	diff = clock() - disp;
	int msec = diff * 1000 / CLOCKS_PER_SEC;
	times[DISP] += msec;
}

int main(){
	printf("Start\n");

	clock_t start_time = clock(), current_time = clock(), end_time;
	int t;
	int cet;
	double cost;
	double object[4];
	char junk[256];
	char line[256];
	Node last_node;

	times[0] = 0; times[1] = 0; times[2] = 0; times[3] = 0; times[4] = 0; times[5] = 0; times[6] = 0; times[7] = 0;
	information = fopen("flight_information.txt","r");

	fscanf(information,"%s %d", junk, &updated_obstacles);
	fscanf(information,"%s %lf %lf %lf", junk, &goal_location[0], &goal_location[1], &goal_location[2]);
	fscanf(information,"%s %lf %lf %lf", junk, &start_location[0], &start_location[1], &start_location[2]);
	fscanf(information,"%s %lf %lf %lf", junk, &current_location[0], &current_location[1], &current_location[2]);
	fgets(junk,256,information); // need this to swich inbetween using fscanf to fgets in order to move to next line

	// Need to initialize before inserting objects
	x_loc_increment = (RESOLUTION_X > 1) ? (goal_location[0]-start_location[0])/(RESOLUTION_X-1) : (goal_location[0]-start_location[0]);
	y_loc_increment = (RESOLUTION_Y > 1) ? (goal_location[1]-start_location[1])/(RESOLUTION_Y-1) : (goal_location[1]-start_location[1]);
	z_loc_increment = (RESOLUTION_VERTICAL > 1) ? (goal_location[2]-start_location[2])/(RESOLUTION_VERTICAL-1) : (goal_location[2]-start_location[2]);
	initialize();

	mark_obstacles(root_obstacle);
	while(fgets(line,256,information)){
		sscanf(line,"%s %lf %lf %lf %lf", junk, &object[0], &object[1], &object[2], &object[3]);
		update_obstacle_list(&root_obstacle,object[0],object[1],object[2],object[3]);
	}
	cet = (clock()-current_time)* 1000 / CLOCKS_PER_SEC; current_time = clock();
	printf("UOL Time: %d seconds %d milliseconds\n", cet/1000, cet%1000);
	fclose(information);

	//Make sure to re-write flight information file as soon as done
	//reading to prevent overwriting new data that hasn't been iterated on.
	if(updated_obstacles){
		updated_obstacles = 0;
		update_grid_with_obstacles(&root_obstacle);
		confirm_updated_obstacles();
	}
	cet = (clock()-current_time)* 1000 / CLOCKS_PER_SEC; current_time = clock();
	printf("UGWO Time: %d seconds %d milliseconds\n", cet/1000, cet%1000);
	//Do the damn thing.
	compute_shortest_path();
	cet = (clock()-current_time)* 1000 / CLOCKS_PER_SEC; current_time = clock();
	printf("CSP Time: %d seconds %d milliseconds\n", cet/1000, cet%1000);
	print_current_state();
	cet = (clock()-current_time)* 1000 / CLOCKS_PER_SEC; current_time = clock();
	printf("PCS Time: %d seconds %d milliseconds\n", cet/1000, cet%1000);
	extract_path();
	cet = (clock()-current_time)* 1000 / CLOCKS_PER_SEC; current_time = clock();
	printf("EP Time: %d seconds %d milliseconds\n", cet/1000, cet%1000);
	show_path();
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
			printf("Pred/Succ Time taken %d seconds %d milliseconds\n", times[PREDSUCC]/1000, times[PREDSUCC]%1000);
			printf("Filewrite Time taken %d seconds %d milliseconds\n", times[FILEWRITE]/1000, times[FILEWRITE]%1000);
			printf("Block Time taken %d seconds %d milliseconds\n", times[BLOCK]/1000, times[BLOCK]%1000);
			printf("Other Time taken %d seconds %d milliseconds\n", times[OTHER]/1000, times[OTHER]%1000);
			times[0] = 0; times[1] = 0; times[2] = 0; times[3] = 0; times[4] = 0; times[5] = 0; times[6] = 0; times[7] = 0;
		}
		start_time = clock();
		if (current_node->rhs == max_val) return -1;
		information = fopen("flight_information.txt","r");

		fscanf(information,"%s %d", junk, &updated_obstacles);
		fscanf(information,"%s %lf %lf %lf", junk, &goal_location_temp[0], &goal_location_temp[1], &goal_location_temp[2]);
		fscanf(information,"%s %lf %lf %lf", junk, &start_location_temp[0], &start_location_temp[1], &start_location_temp[2]);
		fscanf(information,"%s %lf %lf %lf", junk, &current_location[0], &current_location[1], &current_location[2]);
		fgets(junk,256,information); // need this to swich inbetween using fscanf to fgets in order to move to next line

		if(!((start_location_temp[0] == start_location[0]) && (start_location_temp[1] == start_location[1]) && (start_location_temp[2] == start_location[2]) && 
			(goal_location_temp[0] == goal_location[0]) && (goal_location_temp[1] == goal_location[1]) && (goal_location_temp[2] == goal_location[2]))){
			return 0;
		}

		mark_obstacles(root_obstacle);
		while(fgets(line,256,information) && updated_obstacles){
			sscanf(line,"%s %lf %lf %lf %lf", junk, &object[0], &object[1], &object[2], &object[3]);
			update_obstacle_list(&root_obstacle,object[0],object[1],object[2],object[3]);
		}

		fclose(information);
		update_current_node();

 		if(updated_obstacles){
			printf("Replaning\n");
			update_grid_with_obstacles(&root_obstacle);
			updated_obstacles = 0;
			key_modifier = key_modifier + compute_heuristic(last_node.cell,current_node->cell);
			confirm_updated_obstacles();
			compute_shortest_path();
			print_current_state();
			clear_path();
			extract_path();
			show_path();
			print_loop = 1;
		}
		//OR if vehicle isn't following the calculated path, replan
	}
}