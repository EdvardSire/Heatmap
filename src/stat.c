#include "defs.h"
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <stdio.h>

int main() {
  // Open logfile
  time_t current_time;
  struct tm *time_info;
  char formatted_date[20]; // Make sure the buffer is large enough

  time(&current_time);
  time_info = localtime(&current_time);

  strftime(formatted_date, sizeof(formatted_date), "%Y%m%d", time_info);
  strcat(logfile, formatted_date);

  FILE *file = fopen(logfile, "r+");
  if (file == nullptr) {
    fprintf(stderr, "cannot open this.txt\n");
    return 1;
  }

  fseek(file, 0, SEEK_END);
  long fsize = ftell(file);
  fseek(file, 0, SEEK_SET); /* same as rewind(f); */

  char *data = (char *)malloc(fsize + 1);
  fread(data, fsize, 1, file);
  fclose(file);
  data[fsize] = 0;
  printf("home free!\n");

  char tmp[3];
  tmp[2] = '\0';
  int charCount[256] = {0};

  for (int i = 0; i < fsize;) { // NO INCREMENT
    tmp[0] = data[i++];
    tmp[1] = data[i++];
    unsigned char number = (int)strtol(tmp, NULL, 16);
    charCount[number]++;
  }

  for (int i = 0; i < 256; i++)
    printf("%d ", charCount[i]);

  return 0;
}
