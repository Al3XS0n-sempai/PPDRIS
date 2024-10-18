#!/bin/bash

# Файл в который будет записываться PID процесса мониторинга.
monitoring_pid_file="/tmp/monitoring_pid"

# Функция мониторинга. Будет запускаться в подпроцессе (fork).
function monitoring() {
  file_date=''
  start_timestamp=$(date '+%s')
  while true; do
    current_date=$(date '+%F')

    timestamp=$(date '+%s')
    free_inodes=$(df -i / | tail -n 1 | awk '{ print $4 }')
    filesystem=$(df / | tail -n 1 | awk '{ print $1 }')
    disk_usage=$(df / | tail -n 1 | awk '{ print $5 }')

    if [[ $file_date != $current_date ]]; then
      file_date=$current_date
      touch ./${start_timestamp}-${file_date}.csv
      printf "filesystem,timestamp,disk_usage,free_inodes\n" >./${start_timestamp}-${file_date}.csv
    fi

    printf "%s,%s,%s,%s\n" $filesystem $timestamp $disk_usage $free_inodes >>./${start_timestamp}-${file_date}.csv

    sleep 60
  done
}

# Запуск функции мониторинга. + проверка
function start() {
  if [[ -e $monitoring_pid_file ]]; then
    printf "ERROR: Already started with pid $(cat $monitoring_pid_file).\n"
    exit 1
  else
    monitoring &
    echo $! >$monitoring_pid_file
    echo $!
  fi
}

# Завершения мониторинга по PID его процесса. + проверка
function stop() {
  if [[ -e $monitoring_pid_file ]]; then
    local monitoring_pid=$(cat $monitoring_pid_file)
    kill $monitoring_pid
    rm $monitoring_pid_file
  else
    printf "ERROR: Monitoring are not started or lost.\n"
    exit 1
  fi
}

# Проверка статуса мониторинга
function status() {
  if [[ -e $monitoring_pid_file ]]; then
    printf "Monitoring is started with pid=$(cat $monitoring_pid_file).\n"
  else
    printf "Monitoring are not started.\n"
  fi
}

case "$1" in
START)
  printf "STARTING MONITORING\n"
  start
  ;;
STOP)
  printf "STOPPING MONITORING\n"
  stop
  ;;
STATUS)
  status
  ;;
*)
  printf "Invalid argument. Please use as $0 {START|STOP|STATUS}.\n"
  printf "\n\tSTART - to start monitoring.\n\tSTOP - to stop the monitoring.\n\tSTATUS - to check current status.\n"
  ;;
esac
