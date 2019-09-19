// do a good lot of nothing
#include <FreeRTOS.h>
#include <task.h>
#include <stdio.h>

void task1(void *) {
	while (1) {
		puts("task1");

		vTaskDelay(1000 / portTICK_PERIOD_MS);
	}
}

void task2(void *) {
	vTaskDelay(500);
	while (1) {
		puts("task2");

		vTaskDelay(1000 / portTICK_PERIOD_MS);
	}
}

int main() {
	xTaskCreate(task1, "tsk1", 128, NULL, 2, NULL);
	xTaskCreate(task2, "tsk2", 128, NULL, 2, NULL);
	
	vTaskStartScheduler();

	for (;;);
}
