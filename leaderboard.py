name: Update Leaderboard

on:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:

permissions:
  contents: write
  actions: read  # Добавлено новое разрешение

jobs:
  update-leaderboard:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      
    - name: Wait for artifacts
      run: sleep 30  # Задержка для доступности артефактов
      
    - name: Get workflow ID
      id: get_workflow_id
      run: |
        workflow_id=$(gh api repos/${{ github.repository }}/actions/workflows/benchmark.yml --jq '.id')
        echo "workflow_id=$workflow_id" >> $GITHUB_OUTPUT
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        
    - name: Download benchmark artifacts
      uses: actions/download-artifact@v4
      with:
        path: benchmark-artifacts
        name: benchmark_outputs
        workflow: ${{ steps.get_workflow_id.outputs.workflow_id }}
        
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
              fi
            fi
          done
        fi
        
    # Остальные шаги без изменений...
