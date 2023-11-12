import os
import requests
import networkx as nx
from util import *

max_depth = 0


def custom_key(x):
    citing_paper = x.get("citingPaper")
    if isinstance(citing_paper, dict):
        citation_count = citing_paper.get("citationCount")
        return 0 if citation_count is None else citation_count
    else:
        return 0


def get_citations(pid):
    params = {'fields': 'citationCount'}
    url = f"https://api.semanticscholar.org/graph/v1/paper/{pid}/citations"
    response = requests.get(url, params=params)

    if response:
        results = response.json()

        tmp_citations = results.get("data", [])
        tmp_citations = sorted(tmp_citations, key=custom_key, reverse=True)
        citations = []
        for citing_paper in tmp_citations:
            curr_pid = citing_paper["citingPaper"]["paperId"]
            citations.append(curr_pid)
        return citations
    else:
        return []


def traverse_references(citations, papers, curr_depth=0):
    if (curr_depth == max_depth):
        return
    for citation_pid in citations:
        curr_citations = get_citations(citation_pid)
        papers[citation_pid] = curr_citations
        traverse_references(curr_citations, papers, curr_depth + 1)


def generate_graph(papers):
    graph = nx.Graph()
    for pid, citations in papers.items():
        for citation in citations:
            graph.add_edge(pid, citation)
    return graph

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

def get_papers(pid):
    papers = {}
    citations = get_citations(pid)
    papers[pid] = citations
    traverse_references(citations, papers)
    return papers



if __name__ == "__main__":

    topics = [
        {"topic": "ia", "pids": ["204e3073870fae3d05bcbc2f6a8e263d9b72e776",
                                 "2c03df8b48bf3fa39054345bafabfeff15bfd11d",
                                 "abd1c342495432171beb7ca8fd9551ef13cbd0ff"]},
        {"topic": "bd", "pids": ["627be67feb084f1266cfc36e5aed3c3e7e6ce5f0",
                                 "92936ad88a5412bc48b86900da94b08fb7a3eefb",
                                 "e5616898a40b7c7356f7ea6bf49d16227b07abfe"]}
    ]

    for topic in topics:
        for pid in topic["pids"]:
            filename = topic["topic"] + "_" + pid
            
            print("*** " + filename + " ***")
            
            papers = get_papers(pid)
            print("- Papers from SS")
            
            graph = generate_graph(papers)
            print("- Graph")
            
            draw_graph(graph, "png/"+ filename)
            print("- png")

            graph_to_json(graph, "json/"+filename)
            print("- json")
    
    generate_final_graph()