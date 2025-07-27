#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>

#include <sstream>
#include <fstream>



struct Result {
    double generation_time;
    double sorting_time;
    
    std::string to_json() {
        std::stringstream ss;
        ss << "{"
           << "\"generation_time\":" << generation_time << ","
           << "\"sorting_time\":" << sorting_time
           << "}";
        return ss.str();
    }
};

int main() {
    const size_t N = 50000;
    std::vector<double> numbers(N);
    Result result;
    

    auto start_gen = std::chrono::high_resolution_clock::now();
    for (size_t i = 0; i < N; ++i) {
        numbers[i] = N - i;  
    }
    auto end_gen = std::chrono::high_resolution_clock::now();
    result.generation_time = std::chrono::duration<double, std::milli>(end_gen - start_gen).count();
    auto start_sort = std::chrono::high_resolution_clock::now();
    std::sort(numbers.begin(), numbers.end());
    auto end_sort = std::chrono::high_resolution_clock::now();
    result.sorting_time = std::chrono::duration<double, std::milli>(end_sort - start_sort).count();

    std::ofstream out("result.json");
    out << result.to_json();
    out.close();
    
    return 0;
}
