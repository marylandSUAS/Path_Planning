/* Paper for reference on calculations:
 * http://www.tandfonline.com/doi/pdf/10.1080/01691864.2013.755246
 */

#include <math.h>
#include <stdio.h>

/* Define constants */
#define K_MAX 1
#define BETA PI/4
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
  Point B_0, B_1, B_2, B_3, E_0, E_1, E_2, E_3, u_1, u_2, u_d;

  /*calulate the unit vectors */

  /*


}


int main(void) {
  /* Open file to read waypoints from */
  FILE* data_read = fopen("shortest_path.txt","r");

  /* Array for the three points currently being worked on */
  Point waypoints_in[3];
  Point waypoints_out[3];

  /* remove file if it exists */
  remove("smooth_path.txt");

  /* Create and open file to write to */
  FILE* data_write = fopen("smooth_path.txt","a");

  /* Read in first 3 waypoints */
  for (int i = 0; i < 3; i ++) {
      fscanf(data_read, "%f %f %f\n", &(waypoints_in[i].x),
                                      &(waypoints_in[i].y),
                                      &(waypoints_in[i].z));
  }
  /* print first point (starting position)*/
  fprintf(data_write, "%f %f %f\n", waypoints_in[0].x,
                                    waypoints_in[0].y,
                                    waypoints_in[0].z);

  /* Calculations for first three waypoints (middle point) */



  /* print stuff for the special first case */

  fprintf(data_write, "%f %f %f\n", waypoints_in[0].x,
                                    waypoints_in[0].y,
                                    waypoints_in[0].z);
  /* Read in one line and shift the array so that it is three points */
  while (feof(data_read) == 0) {
    /* shift array */
    waypoints_in[0] = waypoints_in[1];
    waypoints_in[1] = waypoints_in[2];
    /* read in one line */
    fscanf(data_read, "%f %f %f\n", &(waypoints_in[2].x),
                                    &(waypoints_in[2].y),
                                    &(waypoints_in[2].z));
    /* calculations here */
    fprintf(data_write, "%f %f %f\n", waypoints_in[0].x,
                                      waypoints_in[0].y,
                                      waypoints_in[0].z);
  }

  /* print ending point */

}
