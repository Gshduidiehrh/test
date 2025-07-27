#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <fstream>
#include <random>
#include <sstream>

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
    const size_t N = 100000;  // Увеличили размер данных для теста
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
    
    // "Оптимизированная" сортировка
    auto start_sort = std::chrono::high_resolution_clock::now();
    
    // Простая оптимизация: используем параллельную сортировку
    #if __has_include(<execution>)
        std::sort(std::execution::par, numbers.begin(), numbers.end());
    #else
        std::sort(numbers.begin(), numbers.end());
    #endif
    
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
    
    // Сохранение результатов
    std::ofstream out("result.json");
    out << generate_json(gen_time, sort_time, sorted);
    out.close();
    
    std::cout << "Тестовое решение выполнено успешно!\n";
    return 0;
}
