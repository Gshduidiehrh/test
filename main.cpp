#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>

#include <sstream>
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
    
    std::ofstream out("result.json");
    out << generate_json(gen_time, sort_time, sorted);
    out.close();
    
    return 0;
}
