#!/usr/bin/env bash

locust -f ./"individual scenario"/sign_in_test.py --no-web --csv=sign_in_1 --run-time 3m -c 1  -r 1
locust -f ./"individual scenario"/sign_in_test.py --no-web --csv=sign_in_2 --run-time 10m -c 10 -r 0.2
locust -f ./"individual scenario"/sign_in_test.py --no-web --csv=sign_in_3 --run-time 10m -c 20 -r 0.2

locust -f ./"individual scenario"/view_project_list_test.py --no-web --csv=view_project_list_1 --run-time 3m -c 1 -r 1
locust -f ./"individual scenario"/view_project_list_test.py --no-web --csv=view_project_list_2 --run-time 10m -c 10 -r 0.2
locust -f ./"individual scenario"/view_project_list_test.py --no-web --csv=view_project_list_3 --run-time 10m -c 20 -r 0.2

locust -f ./"individual scenario"/search_project_keyword_test.py --no-web --csv=search_project_keyword_1 --run-time 3m -c 1  -r 1
locust -f ./"individual scenario"/search_project_keyword_test.py --no-web --csv=search_project_keyword_2 --run-time 10m -c 10 -r 0.2
locust -f ./"individual scenario"/search_project_keyword_test.py --no-web --csv=search_project_keyword_3 --run-time 10m -c 20 -r 0.2

locust -f ./"individual scenario"/manage_project_role_permission_test.py --no-web --csv=manage_project_role_permission_1 --run-time 3m -c 1  -r 1
locust -f ./"individual scenario"/manage_project_role_permission_test.py --no-web --csv=manage_project_role_permission_2 --run-time 10m -c 10 -r 0.2
locust -f ./"individual scenario"/manage_project_role_permission_test.py --no-web --csv=manage_project_role_permission_3 --run-time 10m -c 20 -r 0.2

locust -f ./"individual scenario"/manage_working_hour_test.py --no-web --csv=manage_working_hour_1 --run-time 3m -c 1 -r 1
locust -f ./"individual scenario"/manage_working_hour_test.py --no-web --csv=manage_working_hour_2 --run-time 10m -c 10 -r 0.2
locust -f ./"individual scenario"/manage_working_hour_test.py --no-web --csv=manage_working_hour_3 --run-time 10m -c 20 -r 0.2

locust -f ./"individual scenario"/manage_risk_test.py --no-web --csv=manage_risk_1 --run-time 3m -c 1 -r 1
locust -f ./"individual scenario"/manage_risk_test.py --no-web --csv=manage_risk_2 --run-time 10m -c 10 -r 0.2
locust -f ./"individual scenario"/manage_risk_test.py --no-web --csv=manage_risk_3 --run-time 10m -c 20 -r 0.2

locust -f ./"mixed scenario"/mixed_scenario_test.py --no-web --csv=mixed_scenario_1 --run-time 10m -c 20 -r 0.2
locust -f ./"mixed scenario"/mixed_scenario_test.py --no-web --csv=mixed_scenario_2 --run-time 20m -c 40 -r 0.2

locust -f ./"mixed scenario"/mixed_scenario_test.py --no-web --csv=spike_1 --run-time 1h -c 14 -r 0.2
locust -f ./"mixed scenario"/mixed_scenario_test.py --no-web --csv=spike_2 --run-time 2h -c 20 -r 0.2
locust -f ./"mixed scenario"/mixed_scenario_test.py --no-web --csv=spike_3 --run-time 1h -c 40 -r 0.2
locust -f ./"mixed scenario"/mixed_scenario_test.py --no-web --csv=spike_4 --run-time 30m -c 80 -r 0.2
locust -f ./"mixed scenario"/mixed_scenario_test.py --no-web --csv=spike_5 --run-time 30m -c 200 -r 0.2

locust -f ./"mixed scenario"/mixed_scenario_test.py --no-web --csv=volume_1 --run-time 20m -c 200 -r 0.1
locust -f ./"mixed scenario"/mixed_scenario_test.py --no-web --csv=volume_2 --run-time 1h30m -c 500 -r 0.1 --step-load --step-clients 100 --step-time 15m
locust -f ./"mixed scenario"/mixed_scenario_test.py --no-web --csv=volume_3 --run-time 3h30m -c 2000 -r 0.1 --step-load --step-clients 100 --step-time 10m

locust -f ./"mixed scenario"/mixed_scenario_test.py --no-web --csv= --run-time 1h -c 14 -r 0.1
locust -f ./"mixed scenario"/mixed_scenario_test.py --no-web --csv= --run-time 9h -c 20 -r 0.1
locust -f ./"mixed scenario"/mixed_scenario_test.py --no-web --csv= --run-time 1h -c 14 -r 0.1

