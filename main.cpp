#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>

#include <random>
#include <fstream>



int main() {
    const size_t N = 50000;
    std::vector<double> numbers(N);
    
    // Генерация случайных чисел
    auto start_gen = std::chrono::high_resolution_clock::now();
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(1.0, 1000.0);
    for (size_t i = 0; i < N; ++i) {
        numbers[i] = dis(gen);
    }
    auto end_gen = std::chrono::high_resolution_clock::now();
    double gen_time = std::chrono::duration<double, std::milli>(end_gen - start_gen).count();
    
    // Сортировка
    auto start_sort = std::chrono::high_resolution_clock::now();
    std::sort(numbers.begin(), numbers.end());
    auto end_sort = std::chrono::high_resolution_clock::now();
    double sort_time = std::chrono::duration<double, std::milli>(end_sort - start_sort).count();
    
    // Проверка отсортированности
    bool sorted = true;
    for (size_t i = 0; i < N - 1; ++i) {
        if (numbers[i] > numbers[i + 1]) {
            sorted = false;
            break;
        }
    }
    
    // Сохранение результатов в JSON
    std::ofstream out("result.json");
    out << "{";
    out << "\"generation_time\":" << gen_time << ",";
    out << "\"sorting_time\":" << sort_time << ",";
    out << "\"total_time\":" << (gen_time + sort_time) << ",";
    out << "\"correctly_sorted\":" << (sorted ? "true" : "false");
    out << "}";
    out.close();
    
    return 0;
}
