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

#define RESOLUTION_PLANE 100
#define RESOLUTION_VERTICAL 1

FILE *information;
FILE *information_temp;
FILE *sp;
FILE *sp_temp;
int updated_obstacles;

double goal_location[3];
double start_location[3];
double current_location[3];
double x_loc_increment;
double y_loc_increment;
double z_loc_increment;

double key_modifier;

//Data structures
Heap minheap;
Node grid[RESOLUTION_PLANE][RESOLUTION_PLANE][RESOLUTION_VERTICAL];
//Important nodes
Node *goal_node;
Node *start_node;
Node *current_node;
//Keep track of expanded nodes
int num_expanded;
Node **expanded_nodes;
//Successors and Predecessors wrt current node (calculated and used when needed)
int succ[27][3];
int pred[27][3];

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
	double x_val = 0.0;
	double y_val = 0.0;
	double z_val = 0.0;
	double hueristic = 0.0;

	x_val = fabs((goal[0] - curr[0]) * x_loc_increment);
	y_val = fabs((goal[1] - curr[1]) * y_loc_increment);
	z_val = fabs((goal[2] - curr[2]) * z_loc_increment);
	
	// if(z_val > 0) 
	// 	z_val*=1.25;
	// else 
	// 	z_val*=-0.75;

	hueristic = sqrt(pow(x_val,2)+pow(y_val,2)+pow(z_val,2));
	return hueristic;
}

void calc_key(double *update, int *cell){
	update[1] = min(get_g(cell),get_rhs(cell));
	update[0] = update[1]+compute_heuristic(current_node->cell,cell)+key_modifier;
	return;
}

void update_vertex(Node *node){
	double g = node->g;
	double rhs = node->rhs;
	double new_key[2];

	calc_key(new_key,node->cell);
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
}

int is_expanded(Node *node){
	int i;
	for(i = 0; i < num_expanded; i++){
		if (nodes_equal(node,expanded_nodes[i])){
			return 1;
		}
	}
	return 0;
}

void add_expanded(Node *node){
	printf("Expanding node: {%d,%d,%d} at location {%lf,%lf,%lf} with key_value: {%lf, %lf}\n",node->cell[0],node->cell[1],node->cell[2],
		node->cell[0]*x_loc_increment+start_location[0],node->cell[1]*y_loc_increment+start_location[1],
		node->cell[2]*z_loc_increment+start_location[2],node->k[0],node->k[1]);
	if(num_expanded == 0){
		expanded_nodes = (Node **) malloc(sizeof(Node *));
		expanded_nodes[0] = node;
		num_expanded++;
	}else{
		Node ***pointer = &expanded_nodes;
		num_expanded++;
		*pointer = (Node **) realloc(*pointer,sizeof(Node *)*(num_expanded));
		expanded_nodes[num_expanded-1] = node;
	}
}

int in_bounds(int *cell){
	if(cell[0] >= 0 && cell[1] >= 0 && cell[2] >= 0
		&& cell[0] < RESOLUTION_PLANE && cell[1] < RESOLUTION_PLANE
		&& cell[2] < RESOLUTION_VERTICAL){
		return 1;
	}
	return 0;
}

double cost(Node *node1, Node *node2){
	if (node1->infinite || node2->infinite){
		return max_val;
	}
	return compute_heuristic(node1->cell,node2->cell);
}

void calc_pred(Node *node){
	int *cell = node->cell;
	int check_pred[3];
	int index = 0;
	int i,j,k;

	for(i = 0; i < 3; i++){
		for(j = 0; j < 3; j++){
			for(k = 0; k < 3; k++){
				check_pred[0] = cell[0]+i-1;
				check_pred[1] = cell[1]+j-1;
				check_pred[2] = cell[2]+k-1;
				if(in_bounds(check_pred)){
					if(!(is_expanded(&(grid[check_pred[0]][check_pred[1]][check_pred[2]])))){
						pred[index][0] = check_pred[0];
						pred[index][1] = check_pred[1];
						pred[index][2] = check_pred[2];
					}else{
						pred[index][0] = -1;
						pred[index][1] = -1;
						pred[index][2] = -1;
					}
				}else{
					pred[index][0] = -1;
					pred[index][1] = -1;
					pred[index][2] = -1;
				}
				index++;
			}
		}
	}
	return;
}

void calc_succ(Node *node){
	int *cell = node->cell;
	int check_succ[3];
	int index = 0;
	int i,j,k;

	for(i = 0; i < 3; i++){
		for(j = 0; j < 3; j++){
			for(k = 0; k < 3; k++){
				check_succ[0] = cell[0]+i-1;
				check_succ[1] = cell[1]+j-1;
				check_succ[2] = cell[2]+k-1;
				if(in_bounds(check_succ) &&
					!(check_succ[0] == node->cell[0] &&
					  check_succ[1] == node->cell[1] &&
					  check_succ[2] == node->cell[2])){
	
					succ[index][0] = check_succ[0];
					succ[index][1] = check_succ[1];
					succ[index][2] = check_succ[2];
				}else{
					succ[index][0] = -1;
					succ[index][1] = -1;
					succ[index][2] = -1;
				}
				index++;
			}
		}
	}
	return;
}

void init_graph_node(Node *graph_node, int *cell){
	if(graph_node->seen){
		return;
	}
	graph_node->seen = 1;
	copy_cell(graph_node->cell,cell);
	graph_node->g = max_val;
	graph_node->rhs = max_val;
}

void initialize(){
	init_heap(&minheap);
	key_modifier = 0.0;
	num_expanded = 0;
	int goal_cell[3] = {RESOLUTION_PLANE-1,RESOLUTION_PLANE-1,RESOLUTION_VERTICAL-1};
	int start_cell[3] = {0,0,0};
	int current_cell[3] = {0,0,0};

	goal_node = &(grid[RESOLUTION_PLANE-1][RESOLUTION_PLANE-1][RESOLUTION_VERTICAL-1]);
	start_node = &(grid[0][0][0]);
	current_node = start_node;

	init_graph_node(goal_node, goal_cell);
	init_graph_node(start_node, start_cell);
	init_graph_node(current_node, current_cell);

	goal_node->rhs = 0;
	goal_node->k[0] = compute_heuristic(start_cell,goal_node->cell);
	goal_node->k[1] = 0;

	push_node(&minheap,goal_node);
}

void compute_shortest_path(){
	printf("Computing Shortest\n");
	double k_old[2];
	double k_new[2];
	double g_old = 0;
	double current_key[2];
	int i,j;
	double min_succ_rhs;
	double c,c2;
	double new_rhs;
	Node *u;

	calc_key(current_key,current_node->cell);

	while(compare_keys(top_key(&minheap),current_key) <= 0 || current_node->rhs > current_node->g){
		printf("Num Expanded: %d\n", num_expanded);
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
			for(i = 0; i < 27; i++){ // for all s in Pred(u)
				if(!(pred[i][0] == -1)){
					Node *s = &(grid[pred[i][0]][pred[i][1]][pred[i][2]]);
					if(!(s->seen)){
						int pred_cell[3] = {pred[i][0],pred[i][1],pred[i][2]};
						init_graph_node(s,pred_cell);
					}
					c = cost(s,u);
					new_rhs = min(s->rhs,c+u->g);	//rhs(s) = min(rhs(s),c(s,u) + g(u))
					s->rhs = new_rhs;					
					update_vertex(s); //updateVertex(s)
				}
			}
		}else{
			g_old = u->g;
			u->g = max_val;
			calc_pred(u);
			for(i = 0; i < 27; i++){ //for all s in Pred(u) U {u}
				if(!(pred[i][0] == -1)){ // if s is a valid pred (not out of bounds, or already expanded)
					Node *s = &(grid[pred[i][0]][pred[i][1]][pred[i][2]]);
					c = cost(s,u);
					if(s->rhs == (c + g_old)){ //if rhs(s) == c(s,u) + g_old
						if(!nodes_equal(s,goal_node)){ // if (s != s_goal)
							calc_succ(s);
							min_succ_rhs = max_val; //s->rhs = min (s' E Succ(s)) (c(s,s')+g(s'))
							for(j = 0; j < 27; j++){
								if(!(succ[j][0] == -1)){
									Node *succs = &(grid[succ[j][0]][succ[j][1]][succ[j][2]]);
									c2 = cost(s,succs);
									new_rhs = c2+succs->g;
									min_succ_rhs = (new_rhs < min_succ_rhs) ? new_rhs : min_succ_rhs;
								}
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
					for(i = 0; i < 27; i++){
						if(!(succ[i][0] == -1)){
							Node *succs = &(grid[succ[i][0]][succ[i][1]][succ[i][2]]);
							c2 = cost(s,succs);
							new_rhs = c2+succs->g;
							min_succ_rhs = (new_rhs < min_succ_rhs) ? new_rhs : min_succ_rhs;
						}
					}
					s->rhs = min_succ_rhs;
				}						
			}
			update_vertex(s);
		}
		calc_key(current_key,current_node->cell);
	}
}

void clear(char *buff, int size){
	int i;
	for(i = 0; i < size; i++){
		buff[i] = '\0';
	}
}

void extract_path(){
	printf("Extracting\n");
	int i;
	int changed_init;
	int changed = 0;
	int size = 256;
	double c,min_succ_rhs,new_rhs;
	int *step_cell;
	double step_coord[3];
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
		if(step_node->rhs == max_val){
			printf("No shortest path\n");
			fclose(sp);
			fclose(sp_temp);
			return;
		}
		calc_succ(step_node);
		min_succ_rhs = max_val; //s->rhs = min (s' E Succ(s)) (c(s,s')+g(s'))
		for(i = 0; i < 27; i++){
			if(!(succ[i][0] == -1)){
				Node *succs = &(grid[succ[i][0]][succ[i][1]][succ[i][2]]);
				c = cost(step_node,succs);
				new_rhs = c+succs->g;
				if(new_rhs < min_succ_rhs){
					min_succ_rhs = new_rhs;
					step_node = succs;
				}
			}
		}
		step_cell = step_node->cell;
		step_coord[0] = step_cell[0];//*x_loc_increment+start_location[0];
		step_coord[1] = step_cell[1];//*y_loc_increment+start_location[1];
		step_coord[2] = step_cell[2];//*z_loc_increment+start_location[2];
		if(fgets(line,256,sp) && !changed){
			sscanf(line,"%lf %lf %lf",&sp_cell[0],&sp_cell[1],&sp_cell[2]);
			clear(line, size);
			clear(buff, size);
			if(!((step_coord[0] == sp_cell[0]) &&
				 (step_coord[1] == sp_cell[1]) &&
				 (step_coord[2] == sp_cell[2]))){
				changed = 1;
			}
		}else{
			changed = 1;
		}
		sprintf(buff,"%lf %lf %lf\n",step_coord[0],step_coord[1],step_coord[2]);
		fputs(buff,sp_temp);
		clear(buff,size);
	}

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
	return;
}

void update_current_node(){
	current_node->cell[0] = floor((current_location[0]-start_location[0])/x_loc_increment);
	current_node->cell[1] = floor((current_location[1]-start_location[1])/y_loc_increment);
	current_node->cell[2] = floor((current_location[2]-start_location[2])/z_loc_increment);
}

void block_nodes(double *object,int update_nodes){
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
	double c;
	double min_succ_rhs, new_rhs;
	Node *step_node;

	int i,j,k,z;
	int i_min,j_min,k_min;
	int i_max,j_max,k_max;

	x_trans = x_loc - start_x;
	y_trans = y_loc - start_y;
	z_trans = z_loc - start_z;

	i_min = floor((x_trans - rad)/x_loc_increment);
	j_min = floor((y_trans - rad)/y_loc_increment);
	k_min = floor((z_trans - rad)/z_loc_increment);

	i_max = floor((x_trans + rad)/x_loc_increment);
	j_max = floor((y_trans + rad)/y_loc_increment);
	k_max = floor((z_trans + rad)/z_loc_increment);

	i_min = (i_min > 0) ? i_min : 0;
	j_min = (j_min > 0) ? j_min : 0;
	k_min = (k_min > 0) ? k_min : 0;

	i_max = (i_max > 0) ? i_max : 0;
	j_max = (j_max > 0) ? j_max : 0;
	k_max = (k_max > 0) ? k_max : 0;

	i_min = (i_min < RESOLUTION_PLANE-1) ? i_min : RESOLUTION_PLANE-1;
	j_min = (j_min < RESOLUTION_PLANE-1) ? j_min : RESOLUTION_PLANE-1;
	k_min = (k_min < RESOLUTION_VERTICAL-1) ? k_min : RESOLUTION_VERTICAL-1;

	i_max = (i_max < RESOLUTION_PLANE-1) ? i_max : RESOLUTION_PLANE-1;
	j_max = (j_max < RESOLUTION_PLANE-1) ? j_max : RESOLUTION_PLANE-1;
	k_max = (k_max < RESOLUTION_VERTICAL-1) ? k_max : RESOLUTION_VERTICAL-1;
	
	diag = sqrt(pow(x_loc_increment,2)+pow(y_loc_increment,2)+pow(z_loc_increment,2));
	printf("x_trans = %lf\n",x_trans);
	printf("y_trans = %lf\n",y_trans);
	printf("z_trans = %lf\n",z_trans);
	printf("i_min: %d i_max: %d\n",i_min,i_max);
	printf("j_min: %d j_max: %d\n",j_min,j_max);
	printf("k_min: %d k_max: %d\n",k_min,k_max);

	int total = (i_max-i_min+1)*(j_max-j_min+1)*(k_max-k_min+1);
	printf("Total: %d\n", total);

	for(i = i_min; i <= i_max; i++){
		for(j = j_min; j <= j_max; j++){
			for(k = k_min; k <= k_max; k++){
				total--;
				current_radius = sqrt(pow((x_trans - (i+0.5)*x_loc_increment),2) + 
									  pow((y_trans - (j+0.5)*y_loc_increment),2) +
									  pow((z_trans - (k+0.5)*z_loc_increment),2));
				miss = current_radius - rad;
				if(miss - diag/2 < 0){
					printf("Blocking: [%d,%d,%d]\n",i,j,k);
					grid[i][j][k].infinite = 1;
				}
			}
		}
	}
	
	for(i = i_min; i < i_max; i++){
		for(j = j_min; j < j_max; j++){
			for(k = k_min; k < k_max; k++){
				total--;
				if(grid[i][j][k].infinite == 0){
					//Assuming rhs
					step_node = &(grid[i][j][k]);
					if(!nodes_equal(step_node,goal_node)){ // if (s != s_goal)
						calc_succ(step_node);
						min_succ_rhs = max_val; //s->rhs = min (s' E Succ(s)) (c(s,s')+g(s'))
						for(z = 0; z < 27; z++){
							if(!(succ[z][0] == -1)){
								Node *succs = &(grid[succ[z][0]][succ[z][1]][succ[z][2]]);
								c = cost(step_node,succs);
								new_rhs = c+succs->g;
								min_succ_rhs = (new_rhs < min_succ_rhs) ? new_rhs : min_succ_rhs;
							}
						}
						step_node->rhs = min_succ_rhs;
					}
					update_vertex(step_node);
				}
			}
		}
	}
}

void confirm_updated_obstacles(){
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
}

int main(){
	printf("Start\n");

	double cost;
	double object[4];
	char junk[256];
	char line[256];
	Node last_node;

	information = fopen("flight_information.txt","r");

	fscanf(information,"%s %d", junk, &updated_obstacles);
	fscanf(information,"%s %lf %lf %lf", junk, &goal_location[0], &goal_location[1], &goal_location[2]);
	fscanf(information,"%s %lf %lf %lf", junk, &start_location[0], &start_location[1], &start_location[2]);
	fscanf(information,"%s %lf %lf %lf", junk, &current_location[0], &current_location[1], &current_location[2]);
	fgets(junk,256,information); // need this to swich inbetween using fscanf to fgets in order to move to next line

	// Need to initialize before inserting objects
	x_loc_increment = (goal_location[0]-start_location[0])/RESOLUTION_PLANE;
	y_loc_increment = (goal_location[1]-start_location[1])/RESOLUTION_PLANE;
	z_loc_increment = (goal_location[2]-start_location[2])/RESOLUTION_VERTICAL;
	initialize();

	while(fgets(line,256,information)){
		sscanf(line,"%s %lf %lf %lf %lf", junk, &object[0], &object[1], &object[2], &object[3]);
		block_nodes(object,0);
	}

	fclose(information);

	//Make sure to re-write flight information file as soon as done
	//reading to prevent overwriting new data that hasn't been iterated on.
	if(updated_obstacles){
		updated_obstacles = 0;
		confirm_updated_obstacles();
	}
	//Do the damn thing.
	compute_shortest_path();
	extract_path();

	//Start moving towards goal and recomputing if there are new obstacles!
	copy_node(&last_node, current_node);

	int print_loop = 1;
	while(!nodes_equal(current_node, goal_node)){
		if(print_loop){ 
			printf("Loop\n"); 
			print_loop = 0; 
		}
		if (current_node->rhs == max_val) return -1;
		information = fopen("flight_information.txt","r");

		fscanf(information,"%s %d", junk, &updated_obstacles);
		fscanf(information,"%s %lf %lf %lf", junk, &goal_location[0], &goal_location[1], &goal_location[2]);
		fscanf(information,"%s %lf %lf %lf", junk, &start_location[0], &start_location[1], &start_location[2]);
		fscanf(information,"%s %lf %lf %lf", junk, &current_location[0], &current_location[1], &current_location[2]);
		fgets(junk,256,information); // need this to swich inbetween using fscanf to fgets in order to move to next line

		while(fgets(line,256,information) && updated_obstacles){
			sscanf(line,"%s %lf %lf %lf %lf", junk, &object[0], &object[1], &object[2], &object[3]);
			block_nodes(object,1);
		}

		fclose(information);
		update_current_node();

		if(updated_obstacles){
			printf("Replaning\n");
			updated_obstacles = 0;
			key_modifier = key_modifier + compute_heuristic(last_node.cell,current_node->cell);
			confirm_updated_obstacles();
			compute_shortest_path();
			extract_path();
			print_loop = 1;
		}
	}
}