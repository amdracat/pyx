#include "test_framework/test_framework.h"

// Each module's test runner functions
extern void run_all_tests_queue();
extern void run_all_tests_list();

int main() {
    // Run all module tests
    run_all_tests_queue();
    run_all_tests_list();

    // Print overall test results
    print_results();

    return 0;
}
