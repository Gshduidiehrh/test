#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <fstream>
#include <random>
#include <sstream>
#include <filesystem>
#include <cctype>

namespace fs = std::filesystem;

std::string generate_json(const std::string& username, double gen_time, double sort_time, bool sorted) {
    std::stringstream json;
    json << "{";
    json << "\"username\":\"" << username << "\",";
    json << "\"generation_time\":" << gen_time << ",";
    json << "\"sorting_time\":" << sort_time << ",";
    json << "\"total_time\":" << (gen_time + sort_time) << ",";
    json << "\"correctly_sorted\":" << (sorted ? "true" : "false");
    json << "}";
    return json.str();
}

bool is_valid_username(const std::string& username) {
    if (username.empty()) return false;
    for (char c : username) {
        if (!std::isalnum(c) && c != '_' && c != '-') {
            return false;
        }
    }
    return true;
}

int main(int argc, char* argv[]) {
    // Получаем никнейм из аргументов командной строки
    std::string username = "unknown";
    if (argc > 1) {
        username = argv[1];
    }
    
    // Проверяем валидность никнейма
    if (!is_valid_username(username)) {
        std::cerr << "Error: Invalid username. Use only alphanumeric characters, underscores and hyphens.\n";
        return 1;
    }

    const size_t N = 100000;
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
    
    // Проверка корректности сортировки
    bool sorted = true;
    for (size_t i = 0; i < N - 1; ++i) {
        if (numbers[i] > numbers[i + 1]) {
            sorted = false;
            break;
        }
    }
    
    // Создаем папку для результатов
    fs::create_directory("results");
    
    // Сохраняем результат с именем пользователя
    std::string filename = "results/" + username + ".json";
    std::ofstream out(filename);
    out << generate_json(username, gen_time, sort_time, sorted);
    out.close();
    
    std::cout << "Results saved to: " << filename << "\n";
    std::cout << "Generation time: " << gen_time << " ms\n";
    std::cout << "Sorting time: " << sort_time << " ms\n";
    std::cout << "Total time: " << (gen_time + sort_time) << " ms\n";
    std::cout << "Correctly sorted: " << (sorted ? "yes" : "no") << "\n";
    
    return 0;
}
