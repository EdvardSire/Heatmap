#include "defs.h"
#include <fcntl.h>
#include <linux/input-event-codes.h>
#include <linux/input.h>
#include <poll.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#define MAGIC_KEYCODE_INDEX 10 + 16 + 16
// timeval + short + short => first byte in value
// see debug

#define input_dev "/dev/input/event4"
#define timeout_ms 5000

void info(char *word) {
  printf("[INFO]: ");
  printf("%s\n", word);
}

void warn(char *word) {
  printf("[WARN]: ");
  printf("%s\n", word);
}

void debug() {
  char s[] = "struct input_event{ \n"
             "\tstruct timeval time\n"
             "\tunsigned short type\n"
             "\tunsigned short code\n"
             "\tunsigned int value}\n";

  // the third byte in the last int represents press down
  // or up; 00 is the up press
  // The first byte here is the keycode
  printf("\n%s\n", s);

  // datestring
}

void SIGINT_callback(int signum) {

  printf("\nYou SIGINTed the program!\n");
  exit(signum);
}

int main() {

  // Open logfile
  time_t current_time;
  struct tm *time_info;
  char formatted_date[20]; // Make sure the buffer is large enough

  time(&current_time);
  time_info = localtime(&current_time);

  strftime(formatted_date, sizeof(formatted_date), "%Y%m%d", time_info);
  strcat(logfile, formatted_date);

  FILE *file = fopen(logfile, "a");
  if (file != NULL) {
    info((char *)"Logfile open success!");
    info(logfile);
  } else {
    warn((char *)"cant open logfile, exiting.");
    exit(0);
  }

  // Create poll
  struct pollfd fds[1];
  fds[0].fd = open(input_dev, O_RDONLY | O_NONBLOCK);
  if (fds[0].fd < 0) {
    printf("error unable open for reading '%s'\n", input_dev);
    return (0);
  }
  fds[0].events = POLLIN;

  // debug();

  // Reading Input
  const int input_size = 4096;
  unsigned char input_data[input_size];
  memset(input_data, 0, input_size);

  struct input_event EV;
  int ret;
  signal(SIGINT, SIGINT_callback);
  while (1) {
    ret = poll(fds, 1, timeout_ms);

    if (ret > 0) {
      if (fds[0].revents) {
        ssize_t return_code = read(fds[0].fd, input_data, input_size);

        if (return_code < 0) {
          printf("error %d\n", (int)return_code);
          break;
        } else {
          printf("total bytes read %d/%d\n", (int)return_code, input_size);

          memcpy(&EV, input_data, sizeof(EV));

          for (int i = 0; i < return_code; i++) {
            if (i == 10 || i == 10 + 16 || i == 10 + 16 + 16)
              printf("\n");
            printf("%02X ", (unsigned char)input_data[i]);
          }
          printf("\n");
          printf("Try to grab: %02X\n",
                 (unsigned char)input_data[MAGIC_KEYCODE_INDEX]);
          printf("Int value: %d\n",
                 (unsigned char)input_data[MAGIC_KEYCODE_INDEX]);
          fprintf(file, "%02X", (unsigned char)input_data[MAGIC_KEYCODE_INDEX]);
          fflush(file);

          memset(input_data, 0, input_size);
        }
      } else {
        printf("error\n");
      }
    } else {
      printf("no poll\n");
    }
  }

  close(fds[0].fd);
  return 0;
}
