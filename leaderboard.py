name: Update Leaderboard

on:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:

permissions:
  contents: write
  actions: read  # Ключевое разрешение

jobs:
  update-leaderboard:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      
    - name: Find last benchmark run
      id: find_benchmark
      run: |
        # Установка необходимых инструментов
        sudo apt-get update
        sudo apt-get install -y jq
        
        # Поиск последнего успешного запуска Benchmark Runner
        response=$(curl -s -H "Authorization: token ${{ secrets.GITHUB_TOKEN }}" \
          "https://api.github.com/repos/${{ github.repository }}/actions/runs?event=workflow_run&status=completed")
        
        # Извлекаем ID последнего запуска
        run_id=$(echo "$response" | jq '.workflow_runs[] | select(.name == "Benchmark Runner") | .id' | head -1)
        
        if [ -z "$run_id" ]; then
          echo "::error::No successful benchmark runs found"
          exit 1
        fi
        
        echo "Found benchmark run ID: $run_id"
        echo "run_id=$run_id" >> $GITHUB_OUTPUT
        
    - name: Download benchmark artifacts
      uses: actions/download-artifact@v4
      with:
        path: benchmark-artifacts
        name: benchmark_outputs
        run_id: ${{ steps.find_benchmark.outputs.run_id }}
        
    - name: Prepare results
      run: |
        mkdir -p results
        if [ -d "benchmark-artifacts" ]; then
          for artifact_dir in benchmark-artifacts/*; do
            if [ -d "$artifact_dir" ]; then
              user_file="$artifact_dir/user.txt"
              result_file="$artifact_dir/result.json"
              
              if [ -f "$user_file" ] && [ -f "$result_file" ]; then
                user=$(cat "$user_file")
                mkdir -p "results/$user"
                cp "$result_file" "results/$user/result.json"
                echo "Processed user: $user"
              else
                echo "Missing files in $artifact_dir"
              fi
            fi
          done
        else
          echo "No benchmark artifacts found"
        fi
        
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.x'
        
    - name: Install dependencies
      run: pip install pillow
        
    - name: Generate leaderboard
      run: python3 leaderboard.py
        
    - name: Commit and push
      run: |
        git config user.name "github-actions"
        git config user.email "actions@users.noreply.github.com"
        git add LEADERBOARD.md
        git add leaderboard.png
        if [ -n "$(git status --porcelain)" ]; then
          git commit -m "📊 Обновление таблицы лидеров"
          git push
        fi
