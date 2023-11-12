# Knowledge Graph Generator

Knowledge graph generator using Semantic Scholar API to retrieve citations. Citations depth can be configured.

## 🛠️ Installation and setup 

First, create and activate the virtual environment.

```shell
python3 -m venv env
source env/bin/activate
```

Then install requirements.

```shell
pip install -r requirements.txt
```

Finally, create dirs.
```shell
mkdir json
mkdir png
```


## ⚙️ Features 
### Generate multiple knowledge graphs from a list of seeds 
`generate-graphs.py` generates knowledge graphs from a list of seeds. 
```python
    topics = [
        {"topic": "ia", "pids": [
            "204e3073870fae3d05bcbc2f6a8e263d9b72e776",
            ...
        ]},
    ...
    ]
```

Then it serializes graphs in json files (/json dir) and draws png figures (/png dir).

In `generate_final_graph()` a final graph is done by joining the partial graphs of the `\json` folter.

```python
def generate_final_graph():

    dir = "json"

    final_graph = nx.Graph()

    for filename in os.listdir(dir):
        path = os.path.join(dir, filename)
        if os.path.isfile(path):
            partial = json_to_graph(path)
            final_graph = nx.disjoint_union(final_graph, partial)

    draw_graph(final_graph, "png/final_graph") 
    graph_to_json(final_graph, "json/final_graph") 

```

### (TO DO) Distributed final graph generator

In `/mapreduce` directory, there are a mapper and a reducer to generate a final graph, like the `generate_final_graph()` method but in a distributed way using Hadoop. It need to be tested in a cluster with a launch script like this:

```shell
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
        -file mapper.py \
        -mapper "./mapper.py" \
        -file reducer.py  \
        -reducer "./reducer.py" \
        -input input/ \
        -output /output
```
