/* Paper that was used for reference on bezier curve calculations:
 * An analytical continuous-curvature path-smoothing algorithm
 * Kwangjin Yang
 * IEEE Transactions on Robotics 26(3):561
 * IEEE 2010
 * 1552-3098
 */

#include <math.h>
#include <stdio.h>
#include <stdlib.h>

// Define constants as in the paper
#define K_MAX (1/1) // K = 1/(radius), this will be defined for the specific UAV
#define C_1 (7.2364)
#define C_2 (.579796) // Exact: (2/5) * (sqrt(6) - 1)
#define C_3 (.346) // Exact: (C_2 + 4)/(C_1 + 6));
#define C_4 (1.12259)

/* Structure for a 2D point and 3-D vector, the calcations will be done for 3-D waypoints
 * by projecting the three 3-D waypoints (a Vector) onto a plane (to become a Point) and doing the
 * calculations in two dimensions and then reconverting to 3-D using the plane
 * shared by all three waypoints
 */

typedef struct {
    float x;
    float y;
} Point;

typedef struct {
    float x;
    float y;
    float z;
} Vector;


/* Function prototypes for 2-D points and operations for 3-D vectors
 * The waypoints are three dimensions; however, the calculations will be done in
 * two dimensions by createing a plane that the three adjacent waypoints share
 */
// 2-D Point funtions used to create the 2-D curve in function bezier_curve_smooth
// 3-D Vector functions used on the 3-D waypoints and unit vectors
Vector add_vectors(Vector* a, Vector* b);
Vector sub_vectors(Vector* a, Vector* b);
Vector scale_vector(float scale, Vector* a);
float norm_vector(Vector* a);
Vector unit_vector(Vector* a, Vector* b);

Point add_points(Point* a, Point* b);
Point sub_points(Point* a, Point* b);
Point* scale_point(float scale, Point* a);
float norm_pointm(Point* a);
float angle_point(Point* a, Point* b);
float dot_product_point(Point* a, Point* b);
Point unit_point(Point* a, Point* b);

void bezier_curve_smooth(Point* a, Point* b, Point* c);
void smooth(Vector* a, Vector* b, Vector* c);
void print_waypoint(Vector* a);

// Matrix operations needed to convert from 3-D waypoints to 2-D points and vice-versa
float** inverse(float mat[4][4]);
float determinant(float mat[3][3]);

float** mult_mat(int row1, int share_dim ,int col2, float mat1[row1][share_dim],
                                                    float mat2[share_dim][col2]);


//////////////////////////////////////////////////////////////////////////////////////
/// BASIC OPERATIONS NECESSARY TO COMPLETE MATH AS IN PAPER //////////////////////////
//////////////////////////////////////////////////////////////////////////////////////

// Add two 3-D Vectors
Vector add_vectors(Vector* a, Vector* b) {
    Vector ans;
    ans.x = a->x + b->x;
    ans.y = a->y + b->y;
    ans.z = a->z + b->z;
    return ans;
}

// Subtract two 3-D Vectors
Vector sub_vectors(Vector* a, Vector* b) {
    Vector ans;
    ans.x = a->x - b->x;
    ans.y = a->y - b->y;
    ans.z = a->z - b->z;
    return ans;
}

// Scale a 3-D vector
Vector scale_vector(float scale, Vector* a) {
    Vector ans;
    ans.x = a->x * scale;
    ans.y = a->y * scale;
    ans.z = a->z * scale;
    return ans;
}

// Find the norm of a 3-D vector
float norm_vector(Vector* a) {
    return (float)sqrt(pow(a->x,2) + pow(a->y,2) + pow(a->z,2));
}

// Create a unit vector from a to b
Vector unit_vector(Vector* a, Vector* b) {
    Vector ans;
    ans.x = (b->x - a->x);
    ans.y = (b->y - a->y);
    ans.y = (b->y - a->z);
    float mag = norm_vector(&ans);
    ans.x /= mag;
    ans.y /= mag;
    ans.z /= mag;
}

// Add two 2-D points, note the second argument is assumed to be dynamically allocated
Point add_points(Point* a, Point* b) {
  Point ans;
  ans.x = a->x + b->x;
  ans.y = a->y + b->y;
  free(b);
  return ans;
}

// Subtract two 2-D points, note the second argument is assumed to be dynamically allocated
Point sub_points(Point* a, Point* b) {
  Point ans;
  ans.x = a->x - b->x;
  ans.y = a->y - b->y;
  free(b);
  return ans;
}

/* Multiply point by scaling factor and free first argument since it will be
 * a dynamically allocated point passed directly to another function (add/sub)
 */
Point* scale_point(float scale, Point* a) {
  Point* ans = malloc(sizeof(Point *));
  ans->x = a->x * scale;
  ans->y = a->y * scale;
  return ans;
}

// Calculate the norm of a Point
float norm_point(Point* a) {
  return sqrt(pow(a->x,2) + pow(a->y,2));
}

// Find the angle between two Points
float angle_point(Point* a, Point* b) {
  return acos((dot_product_point(a,b))/(norm_point(a) * norm_point(b)));
}

// Calculate the dot product between two Points
float dot_product_point(Point* a, Point* b) {
  return (a->x) * (b->x) + (a->y) * (b->y);
}

// Calcuate a unit vector from a to b
Point unit_point(Point* a, Point* b) {
    Point ans;
    ans.x = (b->x - a->x);
    ans.y = (b->y - a->y);
    float mag = norm_point(&ans);
    ans.x /= mag;
    ans.y /= mag;
}

/* Find inverse of 4x4 matrix
 * methodology explained here (for 3x3):
 *          http://www.ccodechamp.com/c-program-to-find-inverse-of-matrix/
 */
float** inverse(float mat[4][4]) {
    // Allocate the return matrix
    float** ans = (float **)malloc(4 * 4 * sizeof(float *));
    for (int i = 0; i < 4; i++) {
        ans[i] = (float *)malloc(4 * sizeof(float *));
    }

    // Find the cofactor and also find the determinant
    float det = 0;
    float temp_mat[3][3];
    float temp;
    for (int row = 0; row < 4; row++) {
        for (int col = 0; col < 4; col++) {
            // create the minor matric
            for (int row2 = 0; row2 < 4; row2++) {
                for (int col2 = 0; col2 < 4; col2++) {
                    // skip the row and col of the element
                    if (col2 != col && row2 != row) {
                        temp_mat[row2 - (row2 > row)][col2 - (col2 > col)] = mat[row2][col2];
                    }

                }
            }

            float val = determinant(temp_mat);

            // Relevant to determinant if row = 0
            if (row == 0) {
                det +=  mat[row][col] * val;
            }
            // This is the cofactor  matrix

            ans[row][col] = val * pow(-1,col + row);


        }
    }
    // find the adjoint matrix, by transpose and multiple by 1/det
    for (int row = 0; row < 4; row++) {
        for (int col = row; col < 4; col++) {
            // transpose
            temp =  1.0 / det * ans[row][col];
            ans[row][col] = 1.0 / det * ans[col][row];
            ans[col][row] = temp;

        }
    }
        return ans;

}

// Find the determinant of a 3x3 matrix
float determinant(float mat[3][3]){
    return (mat[0][0] * (mat[1][1] * mat[2][2] - mat[2][1] * mat[1][2])
            - mat[0][1] * (mat[1][0] * mat[2][2] - mat[2][0] * mat[1][2])
            + mat[0][2] * (mat[1][0] * mat[2][1] - mat[2][0] * mat[1][1]));
}

// Multiply two matrix of any dimensions
float** mult_mat(int row1, int share_dim ,int col2, float mat1[row1][share_dim],
                                                    float mat2[share_dim][col2]) {

  float** ans;
  // dynamically allocate the answer (THIS MUST BE FREED)
  ans = malloc(sizeof(float *) * row1);
  for (int i = 0; i < row1; i++) {
    ans[i] = malloc(sizeof(float) * col2);
  }

   // Loop through all dimensions of output matrix
  for(int i = 0; i < row1; i++){
    for(int j = 0; j < col2; j++){
      // Calcuate the element for the output matrix
	    for(int z = 0; z < share_dim; z++){
	      ans[i][j] += (mat1[i][z] * mat2[z][j]);
	    }
    }
  }

  return ans;
}

////////////////////////////////////////////////////////////////////////////////
/// BEZIER CURVE MATH AS DESCRIBED IN ACADEMIC PAPER ///////////////////////////
////////////////////////////////////////////////////////////////////////////////

/* This will take in three vectors and convert to 2-D, do the bezier curve
 * calculations, convert back to 3-D and then print to output file
 */
void smooth(Vector* a, Vector* b, Vector* c) {
    // Calculate variables necessary to convert between 2-D and 3-D


}

/* Calucate the curve and print the five points to the output file that parameterize
 * the curve
 */
void bezier_curve_smooth(Point* w_1, Point* w_2, Point* w_3) {

  /* B and E will be points on the two bezier curves and u_? will be unit vectors
   * that will be used in the calculaiton of the bezier curve, which is stored
   * as a point in 3 dimensions to prevent more structs
   */
  Point b_0, b_1, b_2, b_3, e_0, e_1, e_2, e_3, u_1, u_2, u_d;

  // Calculate variables necessary to formulate the bezier curves
  u_1 = unit_point(w_2,w_1);
  u_2 = unit_point(w_2,w_3);
  float gamma = M_PI - angle_point(&u_1, &u_2);
  float beta = gamma / 2;
  float d = C_4 * sin(beta) / (K_MAX * pow(cos(beta),2));
  float h = C_3 * d;
  float g = C_2 * C_3 * d;
  float k = ((6 * C_3 * cos(beta))/(C_2 + 4)) * d;

  // Calculate b_0, b_1, b_2, e_0, e_1, e_2 with equations from paper

  b_0 = add_points(w_2,scale_point(d,&u_1));
  b_1 = sub_points(&b_0,scale_point(g,&u_1));
  b_2 = sub_points(&b_1,scale_point(h,&u_1));

  e_0 = add_points(w_2,scale_point(d,&u_2));
  e_1 = sub_points(&e_0,scale_point(g,&u_2));
  e_2 = sub_points(&e_1,scale_point(h,&u_2));

  // Calculate u_d as unit point from b_2 to e_2
  u_d = unit_point(&b_2,&e_2);

  // Calulate e_3 and b_3 with equations in paper
  b_3 = add_points(&b_2,scale_point(k,&u_d));
  e_3 = sub_points(&e_2,scale_point(k,&u_d));

}

// Print a point to the output file of the smoothed path (smooth_path.txt)
void print_waypoint(Vector* a) {
  // Create and open file to write to
  FILE* data_writes = fopen("smooth_path.txt","a");
  fprintf(data_writes, "%f %f %f\n", a->x, a->y, a->z);
  fclose(data_writes);
}

int main(void) {
  // Open file to read waypoints from
  FILE* data_read = fopen("shortest_path.txt","r");

  // Array for the three points currently being worked on as 3-D Vectors
  Vector waypoints_in[3];
  Vector waypoints_out[3];

  // Remove existing file if it exists
  remove("smooth_path.txt");

  // NOTE: SKIP FIRST LINE if it contains no waypoints???????????????????????????????????????????????????????????? ask in meeting

  // Read in first 3 waypoints (special case because must print waypoint 1)
  for (int i = 0; i < 3; i ++) {
      fscanf(data_read, "%f %f %f\n", &(waypoints_in[i].x),
                                      &(waypoints_in[i].y),
                                      &(waypoints_in[i].z));
  }
  // Print first point (starting position), no calculations necessary
  print_waypoint(&waypoints_in[0]);

  // Calculations for smoothing three waypoints
  smooth(&(waypoints_in[0]), &(waypoints_in[1]), &(waypoints_in[2]));


  // Read in one line and shift the array so that it is three points
  while (feof(data_read) == 0) {
    // Shift array
    waypoints_in[0] = waypoints_in[1];
    waypoints_in[1] = waypoints_in[2];
    // Read in one line
    fscanf(data_read, "%f %f %f\n", &(waypoints_in[2].x),
                                    &(waypoints_in[2].y),
                                    &(waypoints_in[2].z));

    // Calculations for smoothing three waypoints
    smooth(&(waypoints_in[0]), &(waypoints_in[1]), &(waypoints_in[2]));


  }

  // Print ending point (finish point), no calulations necessary
  print_waypoint(&waypoints_in[2]);

}
