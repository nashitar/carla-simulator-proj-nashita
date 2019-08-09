#!/bin/bash

python3 SetWeather.py & (cd ..../UnrealEngine_4.22/carla/Dist/CARLA_0.9.5-428-g0ce908d-dirty/LinuxNoEditor/PythonAPI/examples;python3 spawn_npc.py -n 80) & python3 CollectDataHurried.py & python3 CollectDataJaywalking.py & python3 CollectDataLawful.py
