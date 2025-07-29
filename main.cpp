#include <iostream>
#include <sstream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <fstream>
#include <random>

std::string generate_json(double gen_time, double sort_time, bool sorted) {
    std::stringstream json;
    json << "{";
    json << "\"generation_time\":" << gen_time << ",";
    json << "\"sorting_time\":" << sort_time << ",";
    json << "\"total_time\":" << (gen_time + sort_time) << ",";
    json << "\"correctly_sorted\":" << (sorted ? "true" : "false");
    json << "}";
    return json.str();
}

int main() {
    const size_t N = 100000;
    std::vector<double> numbers(N);
    
    std::cout << "Starting program: sorting benchmark" << std::endl;
    std::cerr << "DEBUG: Allocating memory for " << N << " elements" << std::endl;

    auto start_gen = std::chrono::high_resolution_clock::now();
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(1.0, 1000.0);
    for (size_t i = 0; i < N; ++i) {
        numbers[i] = dis(gen);
    }
    auto end_gen = std::chrono::high_resolution_clock::now();
    double gen_time = std::chrono::duration<double, std::milli>(end_gen - start_gen).count();
    
    auto start_sort = std::chrono::high_resolution_clock::now();
    std::sort(numbers.begin(), numbers.end());
    auto end_sort = std::chrono::high_resolution_clock::now();
    double sort_time = std::chrono::duration<double, std::milli>(end_sort - start_sort).count();
    
    bool sorted = true;
    for (size_t i = 0; i < N - 1; ++i) {
        if (numbers[i] > numbers[i + 1]) {
            sorted = false;
            break;
        }
    }
    
    std::cout << "Generation time: " << gen_time << " ms" << std::endl;
    std::cout << "Sorting time: " << sort_time << " ms" << std::endl;
    std::cout << "Total time: " << (gen_time + sort_time) << " ms" << std::endl;
    std::cout << "Correctly sorted: " << (sorted ? "yes" : "no") << std::endl;
    
    if (!sorted) {
        std::cerr << "ERROR: Array is not sorted correctly!" << std::endl;
    }
    
    std::ofstream out("result.json");
    out << generate_json(gen_time, sort_time, sorted);
    out.close();
    
    return 0;
}
