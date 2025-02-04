#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <windows.h>

int main() {
  srand(time(NULL));
  
  int num, input_num;
  int score, lives;
  int max_range = 100;
  int end_score = -1;
  int record_time;
  clock_t start_time, end_time;
  int score_v2 = 0;
  int combo = 0;
  score = 0;

  int menu_state = 1;
  while (menu_state == 1) {
    system("cls");
    
    char menu_choice;
    scanf("%c", &menu_choice);

    switch (menu_choice) {
    case 'm':
      printf("new max range (current: %d) ", max_range);
      scanf("%d", &max_range);
      continue;
    case 'e':
      printf("new end score (current: %d) ", end_score);
      scanf("%d", &end_score);
      continue;
    case 'l':
      printf("new max lives (current: %d) ", lives);
      scanf("%d", &lives);
      continue;
    case 'r':
      printf("time spent (current: %d) ", record_time);
      scanf("%d", &record_time);
      continue;
    case '2':
      printf("score v2 (current: %d) ", score_v2);
      scanf("%d", &score_v2);
      continue;
    case 'x':
      menu_state = 0;
      break;
    }
  }

  if (record_time != 0) {
    start_time = clock();
  }
  system("cls");
  
  while (lives > 0) {
    system("cls");
    clock_t begin = clock();
    
    num = rand() % max_range;
    printf("%d", num);
    Sleep(1000);
    
    system("cls");
    scanf("%d", &input_num);
    clock_t end = clock();
    
    if (num != input_num) {
      if (lives - 1 <= 0) {
	break;
      }
      lives = lives - 1;
      combo = 0;
      printf(" -1");
      Sleep(750);
      continue;
    }
    else {
      if (score > end_score && end_score != -1) {
	score = end_score;
	lives = 0;
      }
      if (score_v2 != 0) {
	if (1650 - (end - begin) > 0) {
	  score += 1650 - (int)(end - begin);
	  combo++;
	  printf(" +1");
	}
      }
      else {
	 score++;
      }
    }
    Sleep(750);
  }

  if (record_time != 0) {
    end_time = clock();
  }

  printf("\a");
  printf("score: %d  time: %.2fs  combo: %d\n", score, (float)(end_time - start_time) / CLOCKS_PER_SEC, combo);
  system("pause");
  
  return 0;
}
