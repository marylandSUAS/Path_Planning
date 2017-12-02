/* Paper for reference on calculations:
 * http://www.tandfonline.com/doi/pdf/10.1080/01691864.2013.755246
 * Possible typo on page 248: B_0 = W_1 + d * u_1
 * Correction: B_0 = W_2 + d * u_1
 */

#include <math.h>
#include <stdio.h>

/* Define constants */
#define K_MAX (1/1) /* K = 1/(radius) */
#define BETA (PI/4) /* makes an isosceles triangle for curve, make it into (180 - angle) /2*/
#define C_1 (2/5 * sqrt(6-1))
#define C_2 (7.2364)
#define C_3 ((C_1 + 4)/(C_2 + 6));
/* unsure of d */
#define D (pow(C_1+4,2)/(54*C_3) *  sin(BETA)/(K_MAX * pow(cos(BETA),2)))
#define H (C_3 * D)
#define G (C_1 * C_3 * D)
#define K ((6 * C_3 * cos(BETA))/(C_1 + 4) * D)

/* Structure for a 3D point/vector */
typedef struct {
    float x;
    float y;
    float z;
} Point;

/* Function prototypes*/
Point add_vectors(Point* a, Point* b);
Point sub_vectors(Point* a, Point* b);
void scale_vector(float scale, Point* a);
float norm(Point* vector);
float angle_between(Point* a, Point* b);
float dot_product(Point* a, Point* b);
void bezier_curve(Point* a, Point* b, Point* c);
void print_point(Point* a);



/* Add two vectors */
Point add_vectors(Point* a, Point* b) {
  Point ans;
  ans.x = (a->x) + (b->x);
  ans.y = (a->y) + (b->y);
  ans.z = (a->z) + (b->z);
  return ans;
}

/* Subtract two vectors */
Point sub_vectors(Point* a, Point* b) {
  Point ans;
  ans.x = (a->x) - (b->x);
  ans.y = (a->y) - (b->y);
  ans.z = (a->z) - (b->z);
  return ans;
}

/* Multiple vector by scaling factor */
Point scale_vector(float scale, Point* a) {
  Point ans;
  ans.x = a->x * scale;
  ans.y = a->y * scale;
  ans.z = a->z * scale;
  return ans;
}

/* Calculate the norm of a vector */
float norm(Point* vector) {
  float norm = sqrt(pow(vector->x,2) + pow(vector->y,2) + pow(vector->z,2));
  return norm;
}

/* Find the angle between two vector */
float angle_between(Point* a, Point* b) {
  float ans = acos((dot_product(a,b))/(norm(a) * norm(b)));
  return ans;
}

/* Calculate the dot product between two vectors */
float dot_product(Point* a, Point* b) {
  float ans = (a->x)*(b->x) + (a->y)*(b->y) + (a->z)*(b->z);
}

/* calucate the curve and print the five points to the output file */
void bezier_curve(Point* a, Point* b, Point* c) {

  /* B and E will be points on the bezier curve and u will be unit vectors
   * that will be used in the calculaiton of the bezier curve
   */
  Point b_0, b_1, b_2, b_3, e_0, e_1, e_2, e_3, u_1, u_2, u_d;
  /* Calulate the unit vectors for future calculations */
  u_1 = sub_vectors(a,b) / norm(sub_vectors(a,b));
  u_2 = sub_vectors(c,b) / norm(sub_vectors(c,b));

  /* Calculate b_0, b_1, b_2, e_0, e_1, e_2 with equations in paper */
  b_0 = add_vectors(b,scale_vector(D,u_1));
  b_1 = sub_vectors(b_0,scale_vector(G,u_1));
  b_2 = sub_vectors(b_1,scale_vector(H,u_1));

  e_0 = add_vectors(b,scale_vector(D,u_2));
  e_1 = sub_vectors(e_0,scale_vector(G,u_2));
  e_2 = sub_vectors(e_1,scale_vector(H,u_2));

  /* Calculate u_d as unit vector from b_2 to e_2 */
  u_d = sub_vectors(e_2,b_2) / norm(sub_vectors(e_2,b_2));

  /* Calulate e_3 and b_3 with equations in paper */
  b_3 = add_vectors(b_2,scale_vector(K,u_d));
  e_3 = sub_vectors(e_2,scale_vector(K,u_d));

  /* Print the points that are used which are
   * b_0, b_1, b_3 [or e_3], e_0, e_1
   */
   print_point(&b_0);
   print_point(&b_1);
   print_point(&b_2);
   print_point(&b_3);
   print_point(&e_0);
   print_point(&e_1);

}

/* Print a point to the output file of the smoothed path (smooth_path.txt) */
void print_point(Point* a) {
  /* Create and open file to write to */
  FILE* data_writes = fopen("smooth_path.txt","a");
  fprintf(data_write, "%f %f %f\n", a->x, a->y, a->z);
  fclose(data_write);
}

int main(void) {
  /* Open file to read waypoints from */
  FILE* data_read = fopen("shortest_path.txt","r");

  /* Array for the three points currently being worked on */
  Point waypoints_in[3];
  Point waypoints_out[3];

  /* Remove file if it exists */
  remove("smooth_path.txt");

  /* Read in first 3 waypoints */
  for (int i = 0; i < 3; i ++) {
      fscanf(data_read, "%f %f %f\n", &(waypoints_in[i].x),
                                      &(waypoints_in[i].y),
                                      &(waypoints_in[i].z));
  }
  /* Print first point (starting position), no calculations necessary */
  print_point(waypoints_in[0]);

  /* Calculations for first three waypoints (middle point)
   * the function will print to output file
   */




  /* Read in one line and shift the array so that it is three points */
  while (feof(data_read) == 0) {
    /* Shift array */
    waypoints_in[0] = waypoints_in[1];
    waypoints_in[1] = waypoints_in[2];
    /* Read in one line */
    fscanf(data_read, "%f %f %f\n", &(waypoints_in[2].x),
                                    &(waypoints_in[2].y),
                                    &(waypoints_in[2].z));

    /* Calculations for first three waypoints (middle point)
     * the function will print to output file
     */


  }

  /* Print ending point (finish point), no calulations necessary */
  print_point(waypoints_in[2]);

}
