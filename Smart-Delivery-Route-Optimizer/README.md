# Smart Delivery Route Optimizer

An academic route-planning dashboard built with Python and Streamlit. It uses the project's Dijkstra implementation to calculate a shortest route through selected delivery locations, shows the route on an interactive map, and provides step-by-step directions.

> **Data disclaimer:** Included road distances and map coordinates are illustrative sample data. The application does not use GPS, real map data, live traffic, or AI-based routing.

## Requirements and setup (Windows PowerShell)

Python 3.10 or later is recommended.

```powershell
cd "C:\Users\Hema\OneDrive\Desktop\Smart-Delivery-Route-Optimizer"
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks virtual-environment activation, run the application with the environment's executable directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## Run

```powershell
python -m streamlit run app.py
```

Streamlit prints a local URL (normally `http://localhost:8501`) to open in a browser.

## Features

- **Dashboard:** delivery locations, optimized distance, estimated travel time, and a quick route summary.
- **Route planner:** select a start, destination, and multiple delivery locations.
- **Route optimization:** calculate the route through each selected stop using the project's heap-based Dijkstra implementation.
- **Route map:** explore delivery locations and the optimized path on an interactive map.
- **Results:** inspect the final route, estimated travel time, and step-by-step directions.

The app is focused on these five route-planning pages. Map coordinates are illustrative and are not used to calculate road distances.
The sample network uses Shindevasti, RK PG, NexaUltra Stay PG, Alard Univercity, Cafe De Flora, Jigri Katta, Dmart Hinjewadi, and Pheonix Millenium Mall Wakad. The names, map coordinates, and road distances are illustrative.

## Project structure

```text
Smart-Delivery-Route-Optimizer/
├── app.py
├── delivery_routes.py
├── requirements.txt
├── README.md
├── .streamlit/
│   └── config.toml
├── app_pages/
│   ├── dashboard.py
│   ├── optimization.py
│   ├── planner.py
│   ├── route_map.py
│   └── results.py
├── algorithms/
│   ├── __init__.py
│   ├── _validation.py
│   ├── dijkstra.py
│   ├── bellman_ford.py
│   ├── prim.py
│   ├── kruskal.py
│   ├── merge_sort.py
│   ├── binary_search.py
│   └── coin_change.py
├── visualization/
│   ├── __init__.py
│   ├── delivery_map.py
│   ├── graph_visualizer.py
│   └── performance_charts.py
├── data/
│   └── sample_network.json
└── tests/
    ├── test_delivery_routes.py
    ├── test_dijkstra.py
    ├── test_mst.py
    └── test_sorting_searching.py
```

## Tests

Run the standard-library test suite from the project root:

```powershell
python -m unittest discover -s tests -v
```

The tests cover Dijkstra route calculation, selected delivery stops, direction details, and the existing algorithm modules.

## Notes and limitations

The delivery planner assumes undirected roads with non-negative finite distances. Delivery locations are visited in the order selected. Estimated travel time uses a configurable average speed and excludes stops, traffic, and road conditions. Sample coordinates and distances are illustrative; the app does not use GPS, live maps, or traffic data.
