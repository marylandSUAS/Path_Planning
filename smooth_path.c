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
#define MAX(x,y) (((x) > (y)) ? (x): (y))
#define MIN(x,y) (((x) < (y)) ? (x): (y))

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
Vector* cross_prod_vector(Vector* a, Vector* b);

Point add_points(Point* a, Point* b);
Point sub_points(Point* a, Point* b);
Point* scale_point(float scale, Point* a);
float norm_point(Point* a);
float dist_point(Point* a, Point* b);
float angle_point(Point* a, Point* b);
float dot_product_point(Point* a, Point* b);
Point unit_point(Point* a, Point* b);

float** bezier_curve_smooth(Point* a, Point* b, Point* c);
void smooth(Vector* a, Vector* b, Vector* c);
void print_waypoint(Vector* a);

// Matrix operations needed to convert from 3-D waypoints to 2-D points and vice-versa
float** inverse(float** mat);
float determinant(float mat[3][3]);
float** mult_mat(int row1, int share_dim ,int col2, float** mat1, float** mat2);

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

// Cross product of two vectors (a x b)
Vector* cross_prod_vector(Vector* a, Vector* b) {
  Vector* ans = malloc(sizeof(Vector));
  ans->x = (a->y * b->z) - (a->z * b->y);
  ans->y = (a->z * b->x) - (a->x * b->z);
  ans->z = (a->x * b->y) - (a->y * b->x);
  return ans;
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
  Point* ans = malloc(sizeof(Point));
  ans->x = a->x * scale;
  ans->y = a->y * scale;
  return ans;
}

// Calculate the norm of a Point
float norm_point(Point* a) {
  return sqrt(pow(a->x,2) + pow(a->y,2));
}

// Distance between two points
float dist_point(Point* a, Point* b) {
  Point ans;
  ans.x = a->x - b->x;
  ans.y = a->y - b->y;
  return norm_point(&ans);
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
float** inverse(float** mat) {
    // Allocate the return matrix
    float** ans = (float **)malloc(4 * sizeof(float *));
    for (int i = 0; i < 4; i++) {
        ans[i] = malloc(4 * sizeof(float));
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
float** mult_mat(int row1, int share_dim ,int col2, float** mat1, float** mat2) {
  float** ans;
  // dynamically allocate the answer (THIS MUST BE FREED)
  ans = (float **)malloc(row1 * sizeof(float *));
  for (int i = 0; i < row1; i++) {
    ans[i] = (float *)malloc(col2 * sizeof(float));
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
void smooth(Vector* w_1, Vector* w_2, Vector* w_3) {
  // Calculate unit vectors necessary to convert between 2-D and 3-D
  Vector u_t = unit_vector(w_1, w_2);
  Vector u_p = unit_vector(w_3, w_2);
  Vector* u_b = cross_prod_vector(&u_t,&u_p);
  Vector* u_n = cross_prod_vector(u_b, &u_t);

  // Construct transformation matrix
  float** tm = (float **)malloc(4 * sizeof(float *));
  for (int i = 0; i < 4; i++) {
    tm[i] = (float *)malloc(4 * sizeof(float));
  }
  for (int i = 0; i < 4; i++) {
    for (int j = 0; j < 4; j++) {
      if (i == 3) {
        tm[i][j] = (i == j) ? 1 : 0;
      } else if (j == 0) {
        switch(i) {
          case 0: tm[i][j] = u_t.x; break;
          case 1: tm[i][j] = u_t.y; break;
          default: tm[i][j] = u_t.z;
        }
      } else if (j == 1) {
        switch(i) {
          case 0: tm[i][j] = u_n->x; break;
          case 1: tm[i][j] = u_n->y; break;
          default: tm[i][j] = u_n->z;
        }
      } else if (j == 2) {
        switch(i) {
          case 0: tm[i][j] = u_b->x; break;
          case 1: tm[i][j] = u_b->y; break;
          default: tm[i][j] = u_b->z;
        }
      } else {
        switch(i) {
          case 0: tm[i][j] = w_1->x; break;
          case 1: tm[i][j] = w_1->y; break;
          default: tm[i][j] = w_1->z;
        }
      }
    }
  }

  // These are dunamicallt created due to calling the cross product function
  free(u_b);
  free(u_n);

  // 4 x 4 matrix
  float** inv_tm = inverse(tm);


  // Must make the waypoints have an extra 0 to allow transformation
  float** w_1_4;
  float** w_2_4;
  float** w_3_4;
  w_1_4[0][1] = w_1->x;
  w_2_4[0][1] = w_2->x;
  w_3_4[0][1] = w_3->x;
  w_1_4[1][1] = w_1->y;
  w_2_4[1][1] = w_2->y;
  w_3_4[1][1] = w_3->y;
  w_1_4[2][1] = w_1->z;
  w_2_4[2][1] = w_2->z;
  w_3_4[2][1] = w_3->z;
  w_1_4[3][1] = w_2_4[3][1] = w_3_4[3][1] = 0;

  // Convert to 2-D, all are 4 x 1 matrices
  float** p_1_mat = mult_mat(4, 4, 1, inv_tm, w_1_4);
  float** p_2_mat = mult_mat(4, 4, 1, inv_tm, w_2_4);
  float** p_3_mat = mult_mat(4, 4, 1, inv_tm, w_3_4);

  // inv_tm is dynamically allocated due to calling the inverse function
  for (int i = 0; i < 4; i++) {
    free(inv_tm[i]);
  }
  free(inv_tm);

  // Obtain the (x,y) from the previously calculated matrices (p_1,p_2.p_3)
  Point p_1 = {p_1_mat[0][0],p_1_mat[1][0]};
  Point p_2 = {p_2_mat[0][0],p_2_mat[1][0]};
  Point p_3 = {p_3_mat[0][0],p_3_mat[1][0]};
  // The return value from mult_mat is dynamically allocated
  for (int i = 0; i < 4; i ++) {
    free(p_1_mat[i]);
    free(p_2_mat[i]);
    free(p_3_mat[i]);
  }
  free(p_1_mat);
  free(p_2_mat);
  free(p_3_mat);

  // Run the 2-D bezier_curve_smooth on the converted waypoints
  float** points = bezier_curve_smooth(&p_1, &p_2, &p_3);

  // Convert the 2-D returned poinnts back to 3-D
  float** output = mult_mat(4, 4, 8, tm, points);

  // Print the points
  FILE* data_writes = fopen("smooth_path.txt","a");
  fprintf(data_writes, "%f %f %f\n", output[0][0], output[1][0], output[2][0]); //b_0
  fprintf(data_writes, "%f %f %f\n", output[0][1], output[1][1], output[2][1]); //b_1
  fprintf(data_writes, "%f %f %f\n", output[0][3], output[1][3], output[2][3]); //b_3
  fprintf(data_writes, "%f %f %f\n", output[0][6], output[1][6], output[2][6]); //e_1
  fprintf(data_writes, "%f %f %f\n", output[0][7], output[1][7], output[2][7]); //e_0
  fclose(data_writes);

  // The bezier_curve_smooth and mult_mat returns a dynamically allocated array
  for (int i = 0; i < 4; i++) {
    free(points[i]);
    free(output[i]);
  }
  free(output);
  free(points);




}

/* Calucate the curve and print the five points to the output file that parameterize
 * the curve
 */
float** bezier_curve_smooth(Point* w_1, Point* w_2, Point* w_3) {

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
  // Incase the curve in not possible
  d = MIN(d , .9 * MIN(dist_point(w_1,w_2), dist_point(w_3,w_2)));
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

  float** s_2D = (float **)malloc(4 * sizeof(float *));
  for (int i = 0; i < 4; i++) {
    s_2D[i] = (float *)malloc(8 * sizeof(float));
  }

  // Create a return matrix that has all the struc information
  for (int row = 0; row < 4; row++) {
    for (int col = 0; col < 8; col++) {
      if (row == 3) {
        s_2D[row][col] = 0;
      } else if (row == 4) {
        s_2D[row][col] = 1;
      } else {
        switch (row) {
          case (1) :
            s_2D[row][0] = b_0.x;
            s_2D[row][1] = b_1.x;
            s_2D[row][2] = b_2.x;
            s_2D[row][3] = b_3.x;
            s_2D[row][4] = e_0.x;
            s_2D[row][5] = e_1.x;
            s_2D[row][6] = e_2.x;
            s_2D[row][7] = e_3.x;
            break;
          case (2) :
            s_2D[row][0] = b_0.y;
            s_2D[row][1] = b_1.y;
            s_2D[row][2] = b_2.y;
            s_2D[row][3] = b_3.y;
            s_2D[row][4] = e_0.y;
            s_2D[row][5] = e_1.y;
            s_2D[row][6] = e_2.y;
            s_2D[row][7] = e_3.y;
            break;
        }
      }
    }
  }
  return s_2D;
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
