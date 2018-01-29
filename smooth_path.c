/* Paper for reference on calculations:
 * http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=5428840&tag=1
 */

#include <math.h>
#include <stdio.h>
#include <stdlib.h>

// Define constants as in the paper
#define K_MAX (1/1) // K = 1/(radius), this will be defined for plane
#define C_1 (7.2364)
#define C_2 (.579796) // (2/5) * sqrt(6) - 1)
#define C_3 (.346) // (C_1 + 4)/(C_2 + 6));
#define C_4 (1.12259)

// Structure for a 3D point/vector
typedef struct {
    float x;
    float y;
    float z;
} Point;

// Function prototypes
Point add_vectors(Point* a, Point* b);
Point sub_vectors(Point* a, Point* b);
void scale_vector(float scale, Point* a);
float norm(Point* vector);
float angle(Point* a, Point* b);
float dot_product(Point* a, Point* b);
void bezier_curve(Point* a, Point* b, Point* c);
void print_point(Point* a);
float[4][4] inverse(float mat[4][4]);

/* find inverse of 4x4 matrix
 * explained here: http://www.ccodechamp.com/c-program-to-find-inverse-of-matrix/
 * free output to prevesnt memory leaks
 * this can defintely be optimized...*/
float** inverse(float mat[4][4]) {
    // find determinant of matrix

    // allocate the return matrix
    float** ans = (int **)malloc(4 * 4 * sizeof(int *));
    for (int i = 0; i < 4; i++) {
        ans[i] = (int *)malloc(4 * sizeof(int *);
    }

    // find the cofactor and also find the determinant
    float det = 0;
    float temp[4][4];
    for (int col = 0; col < 3; i++) {
        for (int row = 0; row < 3; row++) {
            // create the minor matric
            for (int col2 = 0; col2 < 3; col2++) {
                for (int row2 = 0; row2 < 3; row2++) {
                    // skip the row and col of the element
                    if (col2 != col && row2 != row) {
                        ans[col2 - (col1 > col)][row2 - (row2 > row)] = mat[row][col];
                    }
                }
            }
            float val = determinant(temp);

            // relevant to determinant if row = 0
            if (row == 0){
                det +=  mat[row][col] * val;
            }
            // This is the cofactor  matrix

            ans[row][col] = val * pow(-1,col + row);
        }
        // find the adjoint matrix, by transpose and multiple by 1/det
        for (int col = 0; col < 3; col++) {
            for (int row = 0l row < 3; row++) {
                if (row != col) {
                    // transpose
                    temp = ans[row][col];
                    ans[row][col] = ans[col][row];
                    ans[col][row] = temp;
                }

            }
        }
        return ans;
    }
}

// Find the determinant of a 3x3 matrix
float determinant(float mat[3][3]){
    return (mat[0][0] * (mat[1][1] * mat[2][2] - mat[2][1] * mat[1][2])
            - mat[0][1] * (mat[1][0] * mat[2][2] - mat[2][0] * mat[1][2])
            + mat[0][2] * (mat[1][0] * mat[2][1] - mat[2][0] * mat[1][1]));
}


}
// Add two vectors
Point add_vectors(Point* a, Point* b) {
  Point ans;
  ans.x = (a->x) + (b->x);
  ans.y = (a->y) + (b->y);
  ans.z = (a->z) + (b->z);
  return ans;
}

// Subtract two vectors
Point sub_vectors(Point* a, Point* b) {
  Point ans;
  ans.x = (a->x) - (b->x);
  ans.y = (a->y) - (b->y);
  ans.z = (a->z) - (b->z);
  return ans;
}

// Multiple vector by scaling factor
Point scale_vector(float scale, Point* a) {
  Point ans;
  ans.x = a->x * scale;
  ans.y = a->y * scale;
  ans.z = a->z * scale;
  return ans;
}

// Calculate the norm of a vector
float norm(Point* vector) {
  return sqrt(pow(vector->x,2) + pow(vector->y,2) + pow(vector->z,2));
}

// Find the angle between two vector
float angle(Point* a, Point* b) {
  return acos((dot_product(a,b))/(norm(a) * norm(b)));
}

// Calculate the dot product between two vectors
float dot_product(Point* a, Point* b) {
  return (a->x)*(b->x) + (a->y)*(b->y) + (a->z)*(b->z);
}

// calucate the curve and print the five points to the output file
void bezier_curve(Point* a, Point* b, Point* c) {

  /* B and E will be points on the two bezier curves and u_? will be unit vectors
   * that will be used in the calculaiton of the bezier curve, which is stored
   * as a point in 3 dimensions to prevent more structs
   */

  Point b_0, b_1, b_2, b_3, e_0, e_1, e_2, e_3, u_1, u_2, u_d;

  // Calculate variables necessary to formulate bezier curves
  float gamma = PI - angle(sub_vectors(a,b), sub_vectors(c,b));
  float beta = gamma / 2;
  float d = C_4 * sin(beta) / (K_MAX * pow(cos(beta),2));
  float h = C_3 * d;
  float g = C_2 * C_3 * d;
  float k = ((6 * C_3 * cos(beta))/(C_2 + 4)) * d;

  // Calulate the unit vectors for future calculations
  u_1 = sub_vectors(a,b) / norm(sub_vectors(a,b));
  u_2 = sub_vectors(c,b) / norm(sub_vectors(c,b));

  // Calculate b_0, b_1, b_2, e_0, e_1, e_2 with equations in paper
  b_0 = add_vectors(b,scale_vector(d,u_1));
  b_1 = sub_vectors(b_0,scale_vector(g,u_1));
  b_2 = sub_vectors(b_1,scale_vector(h,u_1));

  e_0 = add_vectors(b,scale_vector(d,u_2));
  e_1 = sub_vectors(e_0,scale_vector(g,u_2));
  e_2 = sub_vectors(e_1,scale_vector(h,u_2));

  // Calculate u_d as unit vector from b_2 to e_2
  u_d = sub_vectors(e_2,b_2) / norm(sub_vectors(e_2,b_2));

  // Calulate e_3 and b_3 with equations in paper
  b_3 = add_vectors(b_2,scale_vector(k,u_d));
  e_3 = sub_vectors(e_2,scale_vector(k,u_d));

  /* Print the points that are used which are
   * b_0, b_1, b_3 [or e_3], e_0, e_1
   * note: b_3 should equal e_3
   */
   print_point(&b_0);
   print_point(&b_1);
   print_point(&b_3);
   print_point(&e_0);
   print_point(&e_1);

}

// Print a point to the output file of the smoothed path (smooth_path.txt)
void print_point(Point* a) {
  // Create and open file to write to
  FILE* data_writes = fopen("smooth_path.txt","a");
  fprintf(data_write, "%f %f %f\n", a->x, a->y, a->z);
  fclose(data_write);
}

int main(void) {
  // Open file to read waypoints from
  FILE* data_read = fopen("shortest_path.txt","r");

  // Array for the three points currently being worked on
  Point waypoints_in[3];
  Point waypoints_out[3];

  // Remove file if it exists
  remove("smooth_path.txt");

  // Read in first 3 waypoints
  for (int i = 0; i < 3; i ++) {
      fscanf(data_read, "%f %f %f\n", &(waypoints_in[i].x),
                                      &(waypoints_in[i].y),
                                      &(waypoints_in[i].z));
  }
  // Print first point (starting position), no calculations necessary
  print_point(waypoints_in[0]);

  /* Calculations for first three waypoints (middle point)
   * the function will print to output file
   */




  // Read in one line and shift the array so that it is three points
  while (feof(data_read) == 0) {
    // Shift array
    waypoints_in[0] = waypoints_in[1];
    waypoints_in[1] = waypoints_in[2];
    // Read in one line
    fscanf(data_read, "%f %f %f\n", &(waypoints_in[2].x),
                                    &(waypoints_in[2].y),
                                    &(waypoints_in[2].z));

    /* Calculations for first three waypoints (middle point)
     * the function will print to output file
     */


  }

  // Print ending point (finish point), no calulations necessary
  print_point(waypoints_in[2]);

}
